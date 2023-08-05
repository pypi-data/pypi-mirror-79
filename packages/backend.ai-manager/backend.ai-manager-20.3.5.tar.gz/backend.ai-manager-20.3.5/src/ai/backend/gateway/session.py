'''
REST-style session management APIs.
'''

import asyncio
import base64
from decimal import Decimal
from datetime import datetime, timedelta
import functools
from io import BytesIO
import json
import logging
import re
from pathlib import Path
import secrets
from typing import (
    Any, Optional,
    Iterable,
    Tuple,
    Mapping, MutableMapping,
    Union,
)
import uuid

import aiohttp
from aiohttp import web, hdrs
import aiohttp_cors
from aiojobs.aiohttp import atomic
import aioredis
import aiotools
from async_timeout import timeout
from dateutil.parser import isoparse
from dateutil.tz import tzutc
import multidict
import sqlalchemy as sa
from sqlalchemy.sql.expression import true, null
import trafaret as t

from ai.backend.common import redis, validators as tx
from ai.backend.common.docker import ImageRef
from ai.backend.common.exception import (
    UnknownImageReference,
    AliasResolutionFailed,
)
from ai.backend.common.logging import BraceStyleAdapter
from ai.backend.common.utils import str_to_timedelta
from ai.backend.common.types import (
    AgentId, KernelId,
    SessionTypes,
)
from ai.backend.common.plugin.monitor import GAUGE
from ai.backend.common.utils import current_loop
from .defs import REDIS_STREAM_DB
from .exceptions import (
    InvalidAPIParameters,
    GenericNotFound,
    ImageNotFound,
    InsufficientPrivilege,
    SessionNotFound,
    SessionAlreadyExists,
    TooManySessionsMatched,
    BackendError,
    InternalServerError,
    TaskTemplateNotFound
)
from .auth import auth_required
from .types import CORSOptions, WebMiddleware
from .utils import (
    catch_unexpected, check_api_params, get_access_key_scopes, undefined
)
from .manager import ALL_ALLOWED, READ_ALLOWED, server_status_required
from ..manager.models import (
    domains,
    association_groups_users as agus, groups,
    keypairs, kernels, query_bootstrap_script,
    keypair_resource_policies,
    users, UserRole,
    vfolders,
    AgentStatus, KernelStatus,
    query_accessible_vfolders,
    session_templates,
    verify_vfolder_name,
    DEAD_KERNEL_STATUSES,
)

log = BraceStyleAdapter(logging.getLogger('ai.backend.gateway.session'))

_json_loads = functools.partial(json.loads, parse_float=Decimal)


class UndefChecker(t.Trafaret):
    def check_and_return(self, value: Any) -> object:
        if value == undefined:
            return value
        else:
            self._failure('Invalid Undef format', value=value)
            return None


creation_config_v1 = t.Dict({
    t.Key('mounts', default=None): t.Null | t.List(t.String),
    t.Key('environ', default=None): t.Null | t.Mapping(t.String, t.String),
    t.Key('clusterSize', default=None): t.Null | t.Int[1:],
})
creation_config_v2 = t.Dict({
    t.Key('mounts', default=None): t.Null | t.List(t.String),
    t.Key('environ', default=None): t.Null | t.Mapping(t.String, t.String),
    t.Key('clusterSize', default=None): t.Null | t.Int[1:],
    t.Key('instanceMemory', default=None): t.Null | tx.BinarySize,
    t.Key('instanceCores', default=None): t.Null | t.Int,
    t.Key('instanceGPUs', default=None): t.Null | t.Float,
    t.Key('instanceTPUs', default=None): t.Null | t.Int,
})
creation_config_v3 = t.Dict({
    t.Key('mounts', default=None): t.Null | t.List(t.String),
    t.Key('environ', default=None): t.Null | t.Mapping(t.String, t.String),
    tx.AliasedKey(['cluster_size', 'clusterSize'], default=None):
        t.Null | t.Int[1:],
    tx.AliasedKey(['scaling_group', 'scalingGroup'], default=None):
        t.Null | t.String,
    t.Key('resources', default=None): t.Null | t.Mapping(t.String, t.Any),
    tx.AliasedKey(['resource_opts', 'resourceOpts'], default=None):
        t.Null | t.Mapping(t.String, t.Any),
})
creation_config_v3_template = t.Dict({
    t.Key('mounts', default=undefined): UndefChecker | t.Null | t.List(t.String),
    t.Key('environ', default=undefined): UndefChecker | t.Null | t.Mapping(t.String, t.String),
    tx.AliasedKey(['cluster_size', 'clusterSize'], default=undefined):
        UndefChecker | t.Null | t.Int[1:],
    tx.AliasedKey(['scaling_group', 'scalingGroup'], default=undefined):
        UndefChecker | t.Null | t.String,
    t.Key('resources', default=undefined): UndefChecker | t.Null | t.Mapping(t.String, t.Any),
    tx.AliasedKey(['resource_opts', 'resourceOpts'], default=undefined):
        UndefChecker | t.Null | t.Mapping(t.String, t.Any),
})
creation_config_v4 = t.Dict({
    t.Key('mounts', default=None): t.Null | t.List(t.String),
    tx.AliasedKey(['mount_map', 'mountMap'], default=None): t.Null | t.Mapping(t.String, t.String),
    t.Key('environ', default=None): t.Null | t.Mapping(t.String, t.String),
    tx.AliasedKey(['cluster_size', 'clusterSize'], default=None): t.Null | t.Int[1:],
    tx.AliasedKey(['scaling_group', 'scalingGroup'], default=None): t.Null | t.String,
    t.Key('resources', default=None): t.Null | t.Mapping(t.String, t.Any),
    tx.AliasedKey(['resource_opts', 'resourceOpts'], default=None): t.Null | t.Mapping(t.String, t.Any),
    tx.AliasedKey(['preopen_ports', 'preopenPorts'], default=None): t.Null | t.List(t.Int[1024:65535]),
})
creation_config_v4_template = t.Dict({
    t.Key('mounts', default=undefined): UndefChecker | t.Null | t.List(t.String),
    tx.AliasedKey(['mount_map', 'mountMap'], default=undefined):
        UndefChecker | t.Null | t.Mapping(t.String, t.String),
    t.Key('environ', default=undefined): UndefChecker | t.Null | t.Mapping(t.String, t.String),
    tx.AliasedKey(['cluster_size', 'clusterSize'], default=undefined):
        UndefChecker | t.Null | t.Int[1:],
    tx.AliasedKey(['scaling_group', 'scalingGroup'], default=undefined):
        UndefChecker | t.Null | t.String,
    t.Key('resources', default=undefined): UndefChecker | t.Null | t.Mapping(t.String, t.Any),
    tx.AliasedKey(['resource_opts', 'resourceOpts'], default=undefined):
        UndefChecker | t.Null | t.Mapping(t.String, t.Any),
})


overwritten_param_check = t.Dict({
    t.Key('template_id'): tx.UUID,
    t.Key('session_name'): t.Regexp(r'^(?=.{4,64}$)\w[\w.-]*\w$', re.ASCII),
    t.Key('image', default=None): t.Null | t.String,
    tx.AliasedKey(['session_type', 'sess_type']): tx.Enum(SessionTypes),
    t.Key('group', default='default'): t.String,
    t.Key('domain', default='default'): t.String,
    t.Key('config', default=dict): t.Mapping(t.String, t.Any),
    t.Key('tag', default=None): t.Null | t.String,
    t.Key('enqueue_only', default=False): t.ToBool,
    t.Key('max_wait_seconds', default=0): t.Int[0:],
    t.Key('reuse', default=True): t.ToBool,
    t.Key('startup_command', default=None): t.Null | t.String,
    t.Key('bootstrap_script', default=None): t.Null | t.String,
    t.Key('owner_access_key', default=None): t.Null | t.String
})


def sub(d, old, new):
    for k, v in d.items():
        if isinstance(v, Mapping) or isinstance(v, dict):
            d[k] = sub(v, old, new)
        elif d[k] == old:
            d[k] = new
    return d


def drop(d, dropval):
    newd = {}
    for k, v in d.items():
        if isinstance(v, Mapping) or isinstance(v, dict):
            newd[k] = drop(v, dropval)
        elif v != dropval:
            newd[k] = v
    return newd


async def _create(request: web.Request, params: Any, dbpool) -> web.Response:
    if params['domain'] is None:
        params['domain'] = request['user']['domain_name']
    scopes_param = {
        'owner_access_key': (None if params['owner_access_key'] is undefined
                             else params['owner_access_key'])
    }
    requester_access_key, owner_access_key = await get_access_key_scopes(request, scopes_param)
    log.info('GET_OR_CREATE (ak:{0}/{1}, img:{2}, s:{3})',
             requester_access_key, owner_access_key if owner_access_key != requester_access_key else '*',
             params['image'], params['session_name'])

    registry = request.app['registry']
    resp: MutableMapping[str, Any] = {}
    requester_uuid = request['user']['uuid']

    if mount_map := params['config'].get('mount_map'):
        for p in mount_map.values():
            if p is None:
                continue
            if not p.startswith('/home/work/'):
                raise InvalidAPIParameters(f'Path {p} should start with /home/work/')
            if p is not None and not verify_vfolder_name(p.replace('/home/work/', '')):
                raise InvalidAPIParameters(f'Path {str(p)} is reserved for internal operations.')

    mount_map = params['config'].get('mount_map')
    if mount_map is not None:
        for p in mount_map.values():
            if p is None:
                continue
            if not p.startswith('/home/work/'):
                raise InvalidAPIParameters(f'Path {p} should start with /home/work/')
            if p is not None and not verify_vfolder_name(p.replace('/home/work/', '')):
                raise InvalidAPIParameters(f'Path {str(p)} is reserved for internal operations.')

    # Resolve the image reference.
    try:
        requested_image_ref = \
            await ImageRef.resolve_alias(params['image'], request.app['config_server'].etcd)
        async with dbpool.acquire() as conn, conn.begin():
            query = (sa.select([domains.c.allowed_docker_registries])
                       .select_from(domains)
                       .where(domains.c.name == params['domain']))
            allowed_registries = await conn.scalar(query)
            if requested_image_ref.registry not in allowed_registries:
                raise AliasResolutionFailed
    except AliasResolutionFailed:
        raise ImageNotFound

    # Check existing (owner_access_key, session_name) instance
    try:
        # NOTE: We can reuse the session IDs of TERMINATED sessions only.
        # NOTE: Reusing a session in the PENDING status returns an empty value in service_ports.
        kern = await registry.get_session(params['session_name'], owner_access_key)
        running_image_ref = ImageRef(kern['image'], [kern['registry']])
        if running_image_ref != requested_image_ref:
            # The image must be same if get_or_create() called multiple times
            # against an existing (non-terminated) session
            raise SessionAlreadyExists(extra_data={'existingSessionId': str(kern['id'])})
        if not params['reuse']:
            # Respond as error since the client did not request to reuse,
            # but provide the overlapping session ID for later use.
            raise SessionAlreadyExists(extra_data={'existingSessionId': str(kern['id'])})
        # Respond as success with the reused session's information.
        return web.json_response({
            'sessionId': str(kern['id']),
            'sessionName': str(kern['sess_id']),
            'status': kern['status'].name,
            'service_ports': kern['service_ports'],
            'created': False,
        }, status=200)
    except SessionNotFound:
        # It's time to create a new session.
        pass

    if params['session_type'] == SessionTypes.BATCH and not params['startup_command']:
        raise InvalidAPIParameters('Batch sessions must have a non-empty startup command.')
    if params['session_type'] != SessionTypes.BATCH and params['starts_at']:
        raise InvalidAPIParameters('Parameter starts_at should be used only for batch sessions')
    starts_at: Union[datetime, None] = None
    if params['starts_at']:
        try:
            starts_at = isoparse(params['starts_at'])
        except ValueError:
            _td = str_to_timedelta(params['starts_at'])
            starts_at = datetime.now(tzutc()) + _td

    try:
        start_event = asyncio.Event()
        kernel_id: Optional[KernelId] = None

        def interrupt_wait(ctx: Any, event_name: str, agent_id: AgentId,
                           started_kernel_id: str, *args, **kwargs) -> None:
            nonlocal start_event, kernel_id
            if kernel_id is not None and started_kernel_id == str(kernel_id):
                start_event.set()

        start_handler = request.app['event_dispatcher'].subscribe('kernel_started', None,
                                                                  interrupt_wait)
        term_handler = request.app['event_dispatcher'].subscribe('kernel_terminated', None,
                                                                 interrupt_wait)
        cancel_handler = request.app['event_dispatcher'].subscribe('kernel_cancelled', None,
                                                                   interrupt_wait)

        async with dbpool.acquire() as conn, conn.begin():
            if requester_access_key != owner_access_key:
                # Admin or superadmin is creating sessions for another user.
                # The check for admin privileges is already done in get_access_key_scope().
                query = (
                    sa.select([keypairs.c.user, keypairs.c.resource_policy,
                               users.c.role, users.c.domain_name])
                    .select_from(sa.join(keypairs, users, keypairs.c.user == users.c.uuid))
                    .where(keypairs.c.access_key == owner_access_key)
                )
                result = await conn.execute(query)
                row = await result.fetchone()
                owner_domain = row['domain_name']
                owner_uuid = row['user']
                owner_role = row['role']
                query = (
                    sa.select([keypair_resource_policies])
                    .select_from(keypair_resource_policies)
                    .where(keypair_resource_policies.c.name == row['resource_policy'])
                )
                result = await conn.execute(query)
                resource_policy = await result.fetchone()
            else:
                # Normal case when the user is creating her/his own session.
                owner_domain = request['user']['domain_name']
                owner_uuid = requester_uuid
                owner_role = UserRole.USER
                resource_policy = request['keypair']['resource_policy']

            query = (
                sa.select([domains.c.name])
                .select_from(domains)
                .where(
                    (domains.c.name == owner_domain) &
                    (domains.c.is_active)
                )
            )
            qresult = await conn.execute(query)
            domain_name = await qresult.scalar()
            if domain_name is None:
                raise InvalidAPIParameters('Invalid domain')

            if owner_role == UserRole.SUPERADMIN:
                # superadmin can spawn container in any designated domain/group.
                query = (
                    sa.select([groups.c.id])
                    .select_from(groups)
                    .where(
                        (groups.c.domain_name == params['domain']) &
                        (groups.c.name == params['group']) &
                        (groups.c.is_active)
                    ))
                qresult = await conn.execute(query)
                group_id = await qresult.scalar()
            elif owner_role == UserRole.ADMIN:
                # domain-admin can spawn container in any group in the same domain.
                if params['domain'] != owner_domain:
                    raise InvalidAPIParameters("You can only set the domain to the owner's domain.")
                query = (
                    sa.select([groups.c.id])
                    .select_from(groups)
                    .where(
                        (groups.c.domain_name == owner_domain) &
                        (groups.c.name == params['group']) &
                        (groups.c.is_active)
                    ))
                qresult = await conn.execute(query)
                group_id = await qresult.scalar()
            else:
                # normal users can spawn containers in their group and domain.
                if params['domain'] != owner_domain:
                    raise InvalidAPIParameters("You can only set the domain to your domain.")
                query = (
                    sa.select([agus.c.group_id])
                    .select_from(agus.join(groups, agus.c.group_id == groups.c.id))
                    .where(
                        (agus.c.user_id == owner_uuid) &
                        (groups.c.domain_name == owner_domain) &
                        (groups.c.name == params['group']) &
                        (groups.c.is_active)
                    ))
                qresult = await conn.execute(query)
                group_id = await qresult.scalar()
            if group_id is None:
                raise InvalidAPIParameters('Invalid group')

            # Use keypair bootstrap_script if it is not delivered as a parameter
            # (only for INTERACTIVE sessions).
            if params['session_type'] == SessionTypes.INTERACTIVE and not params['bootstrap_script']:
                script, _ = await query_bootstrap_script(conn, owner_access_key)
                params['bootstrap_script'] = script

        kernel_id = await asyncio.shield(request.app['registry'].enqueue_session(
            params['session_name'], owner_access_key,
            requested_image_ref,
            params['session_type'],
            params['config'],
            resource_policy,
            domain_name=params['domain'],
            bootstrap_script=params['bootstrap_script'],
            group_id=group_id,
            user_uuid=owner_uuid,
            user_role=request['user']['role'],
            startup_command=params['startup_command'],
            session_tag=params['tag'],
            starts_at=starts_at,
        ))
        resp['sessionId'] = str(kernel_id)  # changed since API v5
        resp['sessionName'] = str(params['session_name'])
        resp['status'] = 'PENDING'
        resp['servicePorts'] = []
        resp['created'] = True

        if not params['enqueue_only']:
            request.app['pending_waits'].add(asyncio.current_task())
            max_wait = params['max_wait_seconds']
            try:
                if max_wait > 0:
                    with timeout(max_wait):
                        await start_event.wait()
                else:
                    await start_event.wait()
            except asyncio.TimeoutError:
                resp['status'] = 'TIMEOUT'
            else:
                await asyncio.sleep(0.5)
                async with request.app['dbpool'].acquire() as conn, conn.begin():
                    query = (
                        sa.select([
                            kernels.c.status,
                            kernels.c.service_ports,
                        ])
                        .select_from(kernels)
                        .where(kernels.c.id == kernel_id)
                    )
                    result = await conn.execute(query)
                    row = await result.first()
                    if row['status'] == KernelStatus.RUNNING:
                        resp['status'] = 'RUNNING'
                        for item in row['service_ports']:
                            response_dict = {
                                'name': item['name'],
                                'protocol': item['protocol'],
                                'ports': item['container_ports'],
                            }
                            if 'url_template' in item.keys():
                                response_dict['url_template'] = item['url_template']
                            if 'allowed_arguments' in item.keys():
                                response_dict['allowed_arguments'] = item['allowed_arguments']
                            if 'allowed_envs' in item.keys():
                                response_dict['allowed_envs'] = item['allowed_envs']
                            resp['servicePorts'].append(response_dict)
                    else:
                        resp['status'] = row['status'].name

    except asyncio.CancelledError:
        raise
    except BackendError:
        log.exception('GET_OR_CREATE: exception')
        raise
    except UnknownImageReference:
        raise InvalidAPIParameters(f"Unknown image reference: {params['image']}")
    except Exception:
        await request.app['error_monitor'].capture_exception(context={'user': owner_uuid})
        log.exception('GET_OR_CREATE: unexpected error!')
        raise InternalServerError
    finally:
        request.app['pending_waits'].discard(asyncio.current_task())
        request.app['event_dispatcher'].unsubscribe('kernel_cancelled', cancel_handler)
        request.app['event_dispatcher'].unsubscribe('kernel_terminated', term_handler)
        request.app['event_dispatcher'].unsubscribe('kernel_started', start_handler)
    return web.json_response(resp, status=201)


@server_status_required(ALL_ALLOWED)
@auth_required
@check_api_params(t.Dict(
    {
        tx.AliasedKey(['template_id', 'templateId']): t.Null | tx.UUID,
        tx.AliasedKey(['name', 'clientSessionToken'], default=undefined) >> 'session_name':
            UndefChecker | t.Regexp(r'^(?=.{4,64}$)\w[\w.-]*\w$', re.ASCII),
        tx.AliasedKey(['image', 'lang'], default=undefined): UndefChecker | t.Null | t.String,
        tx.AliasedKey(['type', 'sessionType'], default='interactive') >> 'session_type':
            tx.Enum(SessionTypes),
        tx.AliasedKey(['group', 'groupName', 'group_name'], default='default'): t.String,
        tx.AliasedKey(['domain', 'domainName', 'domain_name'], default='default'): t.String,
        t.Key('config', default=dict): t.Mapping(t.String, t.Any),
        t.Key('tag', default=undefined): UndefChecker | t.Null | t.String,
        t.Key('enqueueOnly', default=False) >> 'enqueue_only': t.ToBool,
        t.Key('maxWaitSeconds', default=0) >> 'max_wait_seconds': t.Int[0:],
        tx.AliasedKey(['starts_at', 'startsAt'], default=None): t.Null | t.String,
        t.Key('reuseIfExists', default=True) >> 'reuse': t.ToBool,
        t.Key('startupCommand', default=undefined) >> 'startup_command':
            UndefChecker | t.Null | t.String,
        tx.AliasedKey(['bootstrap_script', 'bootstrapScript'], default=undefined):
            UndefChecker | t.Null | t.String,
        t.Key('owner_access_key', default=undefined): UndefChecker | t.Null | t.String,
    }
), loads=_json_loads)
async def create_from_template(request: web.Request, params: Any) -> web.Response:
    dbpool = request.app['dbpool']

    if params['image'] is None and params['template_id'] is None:
        raise InvalidAPIParameters('Both image and template_id can\'t be None!')

    api_version = request['api_version']
    try:
        if 5 <= api_version[0]:
            params['config'] = creation_config_v4_template.check(params['config'])
        elif (4, '20190315') <= api_version:
            params['config'] = creation_config_v3_template.check(params['config'])
    except t.DataError as e:
        log.debug('Validation error: {0}', e.as_dict())
        raise InvalidAPIParameters('Input validation error',
                                   extra_data=e.as_dict())
    async with dbpool.acquire() as conn, conn.begin():
        query = (
                    sa.select([session_templates.c.template])
                      .select_from(session_templates)
                      .where((session_templates.c.id == params['template_id']) &
                                session_templates.c.is_active)
                )
        template = await conn.scalar(query)
        if not template:
            raise TaskTemplateNotFound

    template = json.loads(template)
    log.debug('Template: {0}', template)

    param_from_template = {
        'image': template['spec']['kernel']['image'],
    }

    if template['spec']['session_type'] == 'interactive':
        param_from_template['session_type'] = SessionTypes.INTERACTIVE
    elif template['spec']['session_type'] == 'batch':
        param_from_template['session_type'] = SessionTypes.BATCH

    # TODO: Remove `type: ignore` when mypy supports type inference for walrus operator
    # Check https://github.com/python/mypy/issues/7316
    # TODO: remove `NOQA` when flake8 supports Python 3.8 and walrus operator
    # Check https://gitlab.com/pycqa/flake8/issues/599
    if tag := template['metadata'].get('tag'):  # noqa
        param_from_template['tag'] = tag
    if runtime_opt := template['spec']['kernel']['run']:  # noqa
        if bootstrap := runtime_opt['bootstrap']:  # noqa
            param_from_template['bootstrap_script'] = bootstrap
        if startup := runtime_opt['startup_command']:  # noqa
            param_from_template['startup_command'] = startup

    config_from_template: MutableMapping[Any, Any] = {}
    if mounts := template['spec'].get('mounts'):  # noqa
        config_from_template['mounts'] = list(mounts.keys())
        config_from_template['mount_map'] = {
            key: value
            for (key, value) in mounts.items()
            if len(value) > 0
        }
    if environ := template['spec']['kernel'].get('environ'):  # noqa
        config_from_template['environ'] = environ
    if resources := template['spec'].get('resources'):  # noqa
        config_from_template['resources'] = resources

    override_config = drop(dict(params['config']), undefined)
    override_params = drop(dict(params), undefined)

    log.debug('Default config: {0}', config_from_template)
    log.debug('Default params: {0}', param_from_template)

    log.debug('Override config: {0}', override_config)
    log.debug('Override params: {0}', override_params)
    config_from_template.update(override_config)
    param_from_template.update(override_params)

    try:
        params = overwritten_param_check.check(param_from_template)
    except RuntimeError as e1:
        log.exception(e1)
    except t.DataError as e2:
        log.debug('Error: {0}', str(e2))
        raise InvalidAPIParameters('Error while validating template')
    params['config'] = config_from_template

    log.debug('Updated param: {0}', params)

    if git := template['spec']['kernel']['git']:  # noqa
        if _dest := git.get('dest_dir'):  # noqa
            target = _dest
        else:
            target = git['repository'].split('/')[-1]

        cmd_builder = 'git clone '
        if credential := git.get('credential'):  # noqa
            proto, url = git['repository'].split('://')
            cmd_builder += f'{proto}://{credential["username"]}:{credential["password"]}@{url}'
        else:
            cmd_builder += git['repository']
        if branch := git.get('branch'):  # noqa
            cmd_builder += f' -b {branch}'
        cmd_builder += f' {target}\n'

        if commit := git.get('commit'):  # noqa
            cmd_builder = 'CWD=$(pwd)\n' + cmd_builder
            cmd_builder += f'cd {target}\n'
            cmd_builder += f'git checkout {commit}\n'
            cmd_builder += 'cd $CWD\n'

        bootstrap = base64.b64decode(params.get('bootstrap_script') or b'').decode()
        bootstrap += '\n'
        bootstrap += cmd_builder
        params['bootstrap_script'] = base64.b64encode(bootstrap.encode()).decode()
    return await _create(request, params, dbpool)


@server_status_required(ALL_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        tx.AliasedKey(['name', 'clientSessionToken']) >> 'session_name':
            t.Regexp(r'^(?=.{4,64}$)\w[\w.-]*\w$', re.ASCII),
        tx.AliasedKey(['image', 'lang']): t.String,
        tx.AliasedKey(['type', 'sessionType'], default='interactive') >> 'session_type':
            tx.Enum(SessionTypes),
        tx.AliasedKey(['group', 'groupName', 'group_name'], default='default'): t.String,
        tx.AliasedKey(['domain', 'domainName', 'domain_name'], default='default'): t.String,
        t.Key('config', default=dict): t.Mapping(t.String, t.Any),
        t.Key('tag', default=None): t.Null | t.String,
        t.Key('enqueueOnly', default=False) >> 'enqueue_only': t.ToBool,
        t.Key('maxWaitSeconds', default=0) >> 'max_wait_seconds': t.Int[0:],
        tx.AliasedKey(['starts_at', 'startsAt'], default=None): t.Null | t.String,
        t.Key('reuseIfExists', default=True) >> 'reuse': t.ToBool,
        t.Key('startupCommand', default=None) >> 'startup_command': t.Null | t.String,
        tx.AliasedKey(['bootstrap_script', 'bootstrapScript'], default=None): t.Null | t.String,
        t.Key('owner_access_key', default=None): t.Null | t.String,
    }),
    loads=_json_loads)
async def create_from_params(request: web.Request, params: Any) -> web.Response:
    if params['session_name'] in ['from-template']:
        raise InvalidAPIParameters(f'Requested session ID {params["session_name"]} is reserved word')

    api_version = request['api_version']
    if 5 <= api_version[0]:
        creation_config = creation_config_v4.check(params['config'])
    elif (4, '20190315') <= api_version:
        creation_config = creation_config_v3.check(params['config'])
    elif 2 <= api_version[0] <= 4:
        creation_config = creation_config_v2.check(params['config'])
    elif api_version[0] == 1:
        creation_config = creation_config_v1.check(params['config'])
    else:
        raise InvalidAPIParameters('API version not supported')
    params['config'] = creation_config

    return await _create(request, params, request.app['dbpool'])


async def handle_kernel_lifecycle(app: web.Application, agent_id: AgentId, event_name: str,
                                  raw_kernel_id: str,
                                  reason: str = None,
                                  exit_code: int = None) -> None:
    kernel_id = uuid.UUID(raw_kernel_id)
    registry = app['registry']
    if event_name == 'kernel_preparing':
        await registry.set_kernel_status(kernel_id, KernelStatus.PREPARING, reason)
    elif event_name == 'kernel_pulling':
        await registry.set_kernel_status(kernel_id, KernelStatus.PULLING, reason)
    elif event_name == 'kernel_creating':
        await registry.set_kernel_status(kernel_id, KernelStatus.PREPARING, reason)
    elif event_name == 'kernel_started':
        # The create_kernel() RPC caller will set the "RUNNING" status.
        pass
    elif event_name == 'kernel_terminating':
        # The destroy_kernel() API handler will set the "TERMINATING" status.
        pass
    elif event_name == 'kernel_terminated':
        await registry.mark_kernel_terminated(kernel_id, reason, exit_code)


async def handle_kernel_stat_sync(app: web.Application, agent_id: AgentId, event_name: str,
                                  raw_kernel_ids: str) -> None:
    kernel_ids = [*map(uuid.UUID, raw_kernel_ids.split(','))]
    await app['registry'].sync_kernel_stats(kernel_ids)


async def handle_batch_result(app: web.Application, agent_id: AgentId, event_name: str,
                              raw_kernel_id: str, exit_code: int) -> None:
    kernel_id = uuid.UUID(raw_kernel_id)
    registry = app['registry']
    if event_name == 'kernel_success':
        await registry.set_session_result(kernel_id, True, exit_code)
    elif event_name == 'kernel_failure':
        await registry.set_session_result(kernel_id, False, exit_code)


async def handle_instance_lifecycle(app: web.Application, agent_id: AgentId, event_name: str,
                                    reason: str = None) -> None:
    if event_name == 'instance_started':
        log.info('instance_lifecycle: ag:{0} joined ({1})', agent_id, reason)
        await app['registry'].update_instance(agent_id, {
            'status': AgentStatus.ALIVE,
        })
    elif event_name == 'instance_terminated':
        if reason == 'agent-lost':
            await app['registry'].mark_agent_terminated(agent_id, AgentStatus.LOST)
        elif reason == 'agent-restart':
            log.info('agent@{0} restarting for maintenance.', agent_id)
            await app['registry'].update_instance(agent_id, {
                'status': AgentStatus.RESTARTING,
            })
        else:
            # On normal instance termination, kernel_terminated events were already
            # triggered by the agent.
            await app['registry'].mark_agent_terminated(agent_id, AgentStatus.TERMINATED)


async def handle_instance_heartbeat(app: web.Application, agent_id: AgentId, event_name: str,
                                    agent_info: Mapping[str, Any]) -> None:
    await app['registry'].handle_heartbeat(agent_id, agent_info)


@catch_unexpected(log)
async def check_agent_lost(app, interval):
    try:
        now = datetime.now(tzutc())
        timeout = timedelta(seconds=app['config']['manager']['heartbeat-timeout'])

        async def _check_impl():
            async for agent_id, prev in app['redis_live'].ihscan('last_seen'):
                prev = datetime.fromtimestamp(float(prev), tzutc())
                if now - prev > timeout:
                    await app['event_dispatcher'].produce_event(
                        'instance_terminated', ('agent-lost', ),
                        agent_id=agent_id)

        await redis.execute_with_retries(lambda: _check_impl())
    except asyncio.CancelledError:
        pass


# NOTE: This event is ignored during the grace period.
async def handle_instance_stats(app: web.Application, agent_id: AgentId, event_name: str,
                                kern_stats) -> None:
    await app['registry'].handle_stats(agent_id, kern_stats)


async def handle_kernel_log(app: web.Application, agent_id: AgentId, event_name: str,
                            raw_kernel_id: str, container_id: str):
    dbpool = app['dbpool']
    redis_conn: aioredis.Redis = await redis.connect_with_retries(
        app['config']['redis']['addr'].as_sockaddr(),
        db=REDIS_STREAM_DB,
        password=(app['config']['redis']['password']
                  if app['config']['redis']['password'] else None),
        encoding=None,
    )
    # The log data is at most 10 MiB.
    log_buffer = BytesIO()
    log_key = f'containerlog.{container_id}'
    try:
        list_size = await redis.execute_with_retries(
            lambda: redis_conn.llen(log_key)
        )
        if list_size is None:
            # The log data is expired due to a very slow event delivery.
            # (should never happen!)
            log.warning('tried to store console logs for cid:{}, but the data is expired',
                        container_id)
            return
        for _ in range(list_size):
            # Read chunk-by-chunk to allow interleaving with other Redis operations.
            chunk = await redis.execute_with_retries(lambda: redis_conn.lpop(log_key))
            log_buffer.write(chunk)
        try:
            async with dbpool.acquire() as conn, conn.begin():
                query = (sa.update(kernels)
                           .values(container_log=log_buffer.getvalue())
                           .where(kernels.c.id == raw_kernel_id))
                await conn.execute(query)
        finally:
            # Clear the log data from Redis when done.
            await redis.execute_with_retries(
                lambda: redis_conn.delete(log_key)
            )
    finally:
        log_buffer.close()
        redis_conn.close()
        await redis_conn.wait_closed()


async def report_stats(app: web.Application) -> None:
    stats_monitor = app['stats_monitor']
    await stats_monitor.report_metric(
        GAUGE, 'ai.backend.gateway.coroutines', len(asyncio.Task.all_tasks()))

    all_inst_ids = [
        inst_id async for inst_id
        in app['registry'].enumerate_instances()]
    await stats_monitor.report_metric(
        GAUGE, 'ai.backend.gateway.agent_instances', len(all_inst_ids))

    async with app['dbpool'].acquire() as conn, conn.begin():
        query = (sa.select([sa.func.sum(keypairs.c.concurrency_used)])
                   .select_from(keypairs))
        n = await conn.scalar(query)
        await stats_monitor.report_metric(
            GAUGE, 'ai.backend.gateway.active_kernels', n)

        subquery = (sa.select([sa.func.count()])
                      .select_from(keypairs)
                      .where(keypairs.c.is_active == true())
                      .group_by(keypairs.c.user_id))
        query = sa.select([sa.func.count()]).select_from(subquery.alias())
        n = await conn.scalar(query)
        await stats_monitor.report_metric(
            GAUGE, 'ai.backend.users.has_active_key', n)

        subquery = subquery.where(keypairs.c.last_used != null())
        query = sa.select([sa.func.count()]).select_from(subquery.alias())
        n = await conn.scalar(query)
        await stats_monitor.report_metric(
            GAUGE, 'ai.backend.users.has_used_key', n)

        '''
        query = sa.select([sa.func.count()]).select_from(usage)
        n = await conn.scalar(query)
        await stats_monitor.report_metric(
            GAUGE, 'ai.backend.gateway.accum_kernels', n)
        '''


async def stats_report_timer(app):
    while True:
        try:
            await asyncio.shield(report_stats(app))
        except asyncio.CancelledError:
            break
        except Exception:
            await app['error_monitor'].capture_exception()
            log.exception('stats_report_timer: unexpected error')
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            break


@server_status_required(READ_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        t.Key('forced', default='false'): t.ToBool(),
    }))
async def destroy(request: web.Request, params: Any) -> web.Response:
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    if params['forced'] and request['user']['role'] not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        raise InsufficientPrivilege('You are not allowed to force-terminate')
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    domain_name = None
    if requester_access_key != owner_access_key and \
            not request['is_superadmin'] and request['is_admin']:
        domain_name = request['user']['domain_name']
    log.info('DESTROY (ak:{0}/{1}, s:{2}, forced:{3})',
             requester_access_key, owner_access_key, session_name, params['forced'])
    last_stat = await registry.destroy_session(
        session_name, owner_access_key,
        forced=params['forced'],
        domain_name=domain_name,
    )
    resp = {
        'stats': last_stat,
    }
    return web.json_response(resp, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        t.Key('id'): t.String(),
    }))
async def match_sessions(request: web.Request, params: Any) -> web.Response:
    """
    A quick session-ID matcher API for use with auto-completion in CLI.
    """
    registry = request.app['registry']
    id_or_name_prefix = params['id']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('MATCH_SESSIONS(ak:{0}/{1}, prefix:{2})',
             requester_access_key, owner_access_key, id_or_name_prefix)
    matches = []
    try:
        compute_session = await registry.get_session(id_or_name_prefix, owner_access_key)
        matches.append({
            'id': compute_session['id'],
            'name': compute_session['sess_id'],
            'status': compute_session['status'].name,
        })
    except TooManySessionsMatched as e:
        matches.extend(e.extra_data['matches'])
    return web.json_response({
        'matches': matches,
    }, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
async def get_info(request: web.Request) -> web.Response:
    # NOTE: This API should be replaced with GraphQL version.
    resp = {}
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('GET_INFO (ak:{0}/{1}, s:{2})',
             requester_access_key, owner_access_key, session_name)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        kern = await registry.get_session(session_name, owner_access_key, field='*')
        resp['domainName'] = kern['domain_name']
        resp['groupId'] = str(kern['group_id'])
        resp['userId'] = str(kern['user_uuid'])
        resp['lang'] = kern['image']  # legacy
        resp['image'] = kern['image']
        resp['registry'] = kern['registry']
        resp['tag'] = kern['tag']

        # Resource occupation
        resp['containerId'] = str(kern['container_id'])
        resp['occupiedSlots'] = str(kern['occupied_slots'])
        resp['occupiedShares'] = str(kern['occupied_shares'])
        resp['environ'] = str(kern['environ'])

        # Lifecycle
        resp['status'] = kern['status'].name  # "e.g. 'KernelStatus.RUNNING' -> 'RUNNING' "
        resp['statusInfo'] = str(kern['status_info'])
        age = datetime.now(tzutc()) - kern['created_at']
        resp['age'] = int(age.total_seconds() * 1000)  # age in milliseconds
        resp['creationTime'] = str(kern['created_at'])
        resp['terminationTime'] = str(kern['terminated_at']) if kern['terminated_at'] else None

        resp['numQueriesExecuted'] = kern['num_queries']
        resp['lastStat'] = kern['last_stat']

        # Resource limits collected from agent heartbeats were erased, as they were deprecated
        # TODO: factor out policy/image info as a common repository

        log.info('information retrieved: {0!r}', resp)
    except BackendError:
        log.exception('GET_INFO: exception')
        raise
    return web.json_response(resp, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
async def restart(request: web.Request) -> web.Response:
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('RESTART (ak:{0}/{1}, s:{2})',
             requester_access_key, owner_access_key, session_name)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        await registry.restart_session(session_name, owner_access_key)
    except BackendError:
        log.exception('RESTART: exception')
        raise
    except:
        await request.app['error_monitor'].capture_exception(context={'user': request['user']['uuid']})
        log.exception('RESTART: unexpected error')
        raise web.HTTPInternalServerError
    return web.Response(status=204)


@server_status_required(READ_ALLOWED)
@auth_required
async def execute(request: web.Request) -> web.Response:
    resp = {}
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    try:
        params = await request.json(loads=json.loads)
        log.info('EXECUTE(ak:{0}/{1}, s:{2})',
                 requester_access_key, owner_access_key, session_name)
    except json.decoder.JSONDecodeError:
        log.warning('EXECUTE: invalid/missing parameters')
        raise InvalidAPIParameters
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        api_version = request['api_version']
        if api_version[0] == 1:
            run_id = params.get('runId', secrets.token_hex(8))
            mode = 'query'
            code = params.get('code', None)
            opts = None
        elif api_version[0] >= 2:
            assert 'runId' in params, 'runId is missing!'
            run_id = params['runId']  # maybe None
            assert params.get('mode'), 'mode is missing or empty!'
            mode = params['mode']
            assert mode in {'query', 'batch', 'complete', 'continue', 'input'}, \
                   'mode has an invalid value.'
            if mode in {'continue', 'input'}:
                assert run_id is not None, 'continuation requires explicit run ID'
            code = params.get('code', None)
            opts = params.get('options', None)
        # handle cases when some params are deliberately set to None
        if code is None: code = ''  # noqa
        if opts is None: opts = {}  # noqa
        if mode == 'complete':
            # For legacy
            resp['result'] = await registry.get_completions(
                session_name, owner_access_key, code, opts)
        else:
            raw_result = await registry.execute(
                session_name, owner_access_key,
                api_version, run_id, mode, code, opts,
                flush_timeout=2.0)
            if raw_result is None:
                # the kernel may have terminated from its side,
                # or there was interruption of agents.
                resp['result'] = {
                    'status': 'finished',
                    'runId': run_id,
                    'exitCode': 130,
                    'options': {},
                    'files': [],
                    'console': [],
                }
                return web.json_response(resp, status=200)
            # Keep internal/public API compatilibty
            result = {
                'status': raw_result['status'],
                'runId': raw_result['runId'],
                'exitCode': raw_result.get('exitCode'),
                'options': raw_result.get('options'),
                'files': raw_result.get('files'),
            }
            if api_version[0] == 1:
                result['stdout'] = raw_result.get('stdout')
                result['stderr'] = raw_result.get('stderr')
                result['media'] = raw_result.get('media')
                result['html'] = raw_result.get('html')
            else:
                result['console'] = raw_result.get('console')
            resp['result'] = result
    except AssertionError as e:
        log.warning('EXECUTE: invalid/missing parameters: {0!r}', e)
        raise InvalidAPIParameters(extra_msg=e.args[0])
    except BackendError:
        log.exception('EXECUTE: exception')
        raise
    return web.json_response(resp, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
async def interrupt(request: web.Request) -> web.Response:
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('INTERRUPT(ak:{0}/{1}, s:{2})',
             requester_access_key, owner_access_key, session_name)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        await registry.interrupt_session(session_name, owner_access_key)
    except BackendError:
        log.exception('INTERRUPT: exception')
        raise
    return web.Response(status=204)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
async def complete(request: web.Request) -> web.Response:
    resp = {
        'result': {
            'status': 'finished',
            'completions': [],
        }
    }
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    try:
        params = await request.json(loads=json.loads)
        log.info('COMPLETE(ak:{0}/{1}, s:{2})',
                 requester_access_key, owner_access_key, session_name)
    except json.decoder.JSONDecodeError:
        raise InvalidAPIParameters
    try:
        code = params.get('code', '')
        opts = params.get('options', None) or {}
        await registry.increment_session_usage(session_name, owner_access_key)
        resp['result'] = await request.app['registry'].get_completions(
            session_name, owner_access_key, code, opts)
    except AssertionError:
        raise InvalidAPIParameters
    except BackendError:
        log.exception('COMPLETE: exception')
        raise
    return web.json_response(resp, status=200)


@server_status_required(READ_ALLOWED)
@auth_required
async def upload_files(request: web.Request) -> web.Response:
    loop = asyncio.get_event_loop()
    reader = await request.multipart()
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('UPLOAD_FILE (ak:{0}/{1}, s:{2})',
             requester_access_key, owner_access_key, session_name)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        file_count = 0
        upload_tasks = []
        async for file in aiotools.aiter(reader.next, None):
            if file_count == 20:
                raise InvalidAPIParameters('Too many files')
            file_count += 1
            # This API handles only small files, so let's read it at once.
            chunks = []
            recv_size = 0
            while True:
                chunk = await file.read_chunk(size=1048576)
                if not chunk:
                    break
                chunk_size = len(chunk)
                if recv_size + chunk_size >= 1048576:
                    raise InvalidAPIParameters('Too large file')
                chunks.append(chunk)
                recv_size += chunk_size
            data = file.decode(b''.join(chunks))
            log.debug('received file: {0} ({1:,} bytes)', file.filename, recv_size)
            t = loop.create_task(
                registry.upload_file(session_name, owner_access_key,
                                     file.filename, data))
            upload_tasks.append(t)
        await asyncio.gather(*upload_tasks)
    except BackendError:
        log.exception('UPLOAD_FILES: exception')
        raise
    return web.Response(status=204)


@server_status_required(READ_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        tx.MultiKey('files'): t.List(t.String),
    }))
async def download_files(request: web.Request, params: Any) -> web.Response:
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    files = params.get('files')
    log.info('DOWNLOAD_FILE (ak:{0}/{1}, s:{2}, path:{3!r})',
             requester_access_key, owner_access_key, session_name,
             files[0])
    try:
        assert len(files) <= 5, 'Too many files'
        await registry.increment_session_usage(session_name, owner_access_key)
        # TODO: Read all download file contents. Need to fix by using chuncking, etc.
        results = await asyncio.gather(*map(
            functools.partial(registry.download_file, session_name, owner_access_key),
            files))
        log.debug('file(s) inside container retrieved')
    except asyncio.CancelledError:
        raise
    except BackendError:
        log.exception('DOWNLOAD_FILE: exception')
        raise
    except (ValueError, FileNotFoundError):
        raise InvalidAPIParameters('The file is not found.')
    except Exception:
        await request.app['error_monitor'].capture_exception(context={'user': request['user']['uuid']})
        log.exception('DOWNLOAD_FILE: unexpected error!')
        raise InternalServerError

    with aiohttp.MultipartWriter('mixed') as mpwriter:
        headers = multidict.MultiDict({'Content-Encoding': 'identity'})
        for tarbytes in results:
            mpwriter.append(tarbytes, headers)
        return web.Response(body=mpwriter, status=200)


@auth_required
@server_status_required(READ_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('file'): t.String,
    }))
async def download_single(request: web.Request, params: Any) -> web.Response:
    ''' Download single file from scratch root. Only for small files.
    '''
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    file = params['file']
    log.info('DOWNLOAD_SINGLE (ak:{0}/{1}, s:{2}, path:{3!r})',
             requester_access_key, owner_access_key, session_name, file)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        result = await registry.download_file(session_name, owner_access_key, file)
    except asyncio.CancelledError:
        raise
    except BackendError:
        log.exception('DOWNLOAD_SINGLE: exception')
        raise
    except (ValueError, FileNotFoundError):
        raise InvalidAPIParameters('The file is not found.')
    except Exception:
        await request.app['error_monitor'].capture_exception(context={'user': request['user']['uuid']})
        log.exception('DOWNLOAD_SINGLE: unexpected error!')
        raise InternalServerError
    return web.Response(body=result, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
async def list_files(request: web.Request) -> web.Response:
    try:
        session_name = request.match_info['session_name']
        requester_access_key, owner_access_key = await get_access_key_scopes(request)
        params = await request.json(loads=json.loads)
        path = params.get('path', '.')
        log.info('LIST_FILES (ak:{0}/{1}, s:{2}, path:{3})',
                 requester_access_key, owner_access_key, session_name, path)
    except (asyncio.TimeoutError, AssertionError,
            json.decoder.JSONDecodeError) as e:
        log.warning('LIST_FILES: invalid/missing parameters, {0!r}', e)
        raise InvalidAPIParameters(extra_msg=str(e.args[0]))
    resp: MutableMapping[str, Any] = {}
    try:
        registry = request.app['registry']
        await registry.increment_session_usage(session_name, owner_access_key)
        result = await registry.list_files(session_name, owner_access_key, path)
        resp.update(result)
        log.debug('container file list for {0} retrieved', path)
    except asyncio.CancelledError:
        raise
    except BackendError:
        log.exception('LIST_FILES: exception')
        raise
    except Exception:
        await request.app['error_monitor'].capture_exception(context={'user': request['user']['uuid']})
        log.exception('LIST_FILES: unexpected error!')
        raise InternalServerError
    return web.json_response(resp, status=200)


@atomic
@server_status_required(READ_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        t.Key('owner_access_key', default=None): t.Null | t.String,
    }))
async def get_container_logs(request: web.Request, params: Any) -> web.Response:
    registry = request.app['registry']
    session_name = request.match_info['session_name']
    dbpool = request.app['dbpool']
    requester_access_key, owner_access_key = await get_access_key_scopes(request)
    log.info('GET_CONTAINER_LOG (ak:{}/{}, s:{})',
             requester_access_key, owner_access_key, session_name)
    resp = {'result': {'logs': ''}}
    async with dbpool.acquire() as conn, conn.begin():
        compute_session = await registry.get_session(
            session_name, owner_access_key,
            field=[kernels.c.container_log],
            allow_stale=True,
            db_connection=conn,
        )
        if (
            compute_session.status in DEAD_KERNEL_STATUSES and
            compute_session.container_log is not None
        ):
            log.debug('returning log from database record')
            resp['result']['logs'] = compute_session.container_log.decode('utf-8')
            return web.json_response(resp, status=200)
    try:
        await registry.increment_session_usage(session_name, owner_access_key)
        resp['result'] = await registry.get_logs_from_agent(session_name, owner_access_key)
        log.debug('returning log from agent')
    except BackendError:
        log.exception('GET_CONTAINER_LOG(ak:{}/{}, s:{}): unexpected error',
                      requester_access_key, owner_access_key, session_name)
        raise
    return web.json_response(resp, status=200)


@server_status_required(READ_ALLOWED)
@auth_required
@check_api_params(
    t.Dict({
        tx.AliasedKey(['session_name', 'sessionName', 'task_id', 'taskId']) >> 'kernel_id': tx.UUID,
    }))
async def get_task_logs(request: web.Request, params: Any) -> web.StreamResponse:
    log.info('GET_TASK_LOG (ak:{}, k:{})',
             request['keypair']['access_key'], params['kernel_id'])
    domain_name = request['user']['domain_name']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']
    raw_kernel_id = params['kernel_id'].hex
    mount_prefix = await request.app['config_server'].get('volumes/_mount')
    fs_prefix = await request.app['config_server'].get('volumes/_fsprefix')
    async with request.app['dbpool'].acquire() as conn, conn.begin():
        matched_vfolders = await query_accessible_vfolders(
            conn, user_uuid,
            user_role=user_role, domain_name=domain_name,
            allowed_vfolder_types=['user'],
            extra_vf_conds=(vfolders.c.name == '.logs'))
        if not matched_vfolders:
            raise GenericNotFound('You do not have ".logs" vfolder for persistent task logs.')
        log_vfolder = matched_vfolders[0]
        log_path = (
            Path(mount_prefix) / log_vfolder['host'] / Path(fs_prefix.lstrip('/')) /
            log_vfolder['id'].hex /
            'task' / raw_kernel_id[:2] / raw_kernel_id[2:4] / f'{raw_kernel_id[4:]}.log'
        )

    def check_file():
        if not log_path.is_file():
            raise GenericNotFound('The requested log file or the task was not found.')
        try:
            with open(log_path, 'rb'):
                pass
        except IOError:
            raise GenericNotFound('The requested log file is not readable.')

    loop = current_loop()
    await loop.run_in_executor(None, check_file)
    return web.FileResponse(log_path, headers={
        hdrs.CONTENT_TYPE: "text/plain",
    })


async def init(app: web.Application) -> None:
    event_dispatcher = app['event_dispatcher']
    event_dispatcher.consume('kernel_preparing', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_pulling', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_creating', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_started', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_terminating', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_terminated', app, handle_kernel_lifecycle)
    event_dispatcher.consume('kernel_success', app, handle_batch_result)
    event_dispatcher.consume('kernel_failure', app, handle_batch_result)
    event_dispatcher.consume('kernel_stat_sync', app, handle_kernel_stat_sync)
    event_dispatcher.consume('kernel_log', app, handle_kernel_log)
    event_dispatcher.consume('instance_started', app, handle_instance_lifecycle)
    event_dispatcher.consume('instance_terminated', app, handle_instance_lifecycle)
    event_dispatcher.consume('instance_heartbeat', app, handle_instance_heartbeat)
    event_dispatcher.consume('instance_stats', app, handle_instance_stats)

    app['pending_waits'] = set()

    # Scan ALIVE agents
    app['agent_lost_checker'] = aiotools.create_timer(
        functools.partial(check_agent_lost, app), 1.0)
    app['stats_task'] = asyncio.create_task(stats_report_timer(app))


async def shutdown(app: web.Application) -> None:
    app['agent_lost_checker'].cancel()
    await app['agent_lost_checker']
    app['stats_task'].cancel()
    await app['stats_task']

    checked_tasks = ('kernel_agent_event_collector', 'kernel_ddtimer')
    for tname in checked_tasks:
        t = app.get(tname, None)
        if t and not t.done():
            t.cancel()
            await t

    for task in app['pending_waits']:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


def create_app(default_cors_options: CORSOptions) -> Tuple[web.Application, Iterable[WebMiddleware]]:
    app = web.Application()
    app.on_startup.append(init)
    app.on_shutdown.append(shutdown)
    app['api_versions'] = (1, 2, 3, 4)
    cors = aiohttp_cors.setup(app, defaults=default_cors_options)
    cors.add(app.router.add_route('POST', '/_/create-from-template', create_from_template))
    cors.add(app.router.add_route('GET',  '/_/match', match_sessions))
    cors.add(app.router.add_route('POST', '', create_from_params))
    session_resource = cors.add(app.router.add_resource(r'/{session_name}'))
    cors.add(session_resource.add_route('GET',    get_info))
    cors.add(session_resource.add_route('PATCH',  restart))
    cors.add(session_resource.add_route('DELETE', destroy))
    cors.add(session_resource.add_route('POST',   execute))
    task_log_resource = cors.add(app.router.add_resource(r'/_/logs'))
    cors.add(task_log_resource.add_route('HEAD', get_task_logs))
    cors.add(task_log_resource.add_route('GET',  get_task_logs))
    cors.add(app.router.add_route('GET',  '/{session_name}/logs', get_container_logs))
    cors.add(app.router.add_route('POST', '/{session_name}/interrupt', interrupt))
    cors.add(app.router.add_route('POST', '/{session_name}/complete', complete))
    cors.add(app.router.add_route('POST', '/{session_name}/upload', upload_files))
    cors.add(app.router.add_route('GET',  '/{session_name}/download', download_files))
    cors.add(app.router.add_route('GET',  '/{session_name}/download_single', download_single))
    cors.add(app.router.add_route('GET',  '/{session_name}/files', list_files))
    return app, []
