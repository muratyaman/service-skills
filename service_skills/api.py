from aiohttp import web
import logging

from .helpers import nowf
from .config import Config
from .db import Db


def log_request(request, ext=''):
    m = '{} {} {}'.format(request.method, request.path, ext)
    #logging.info(m)
    print(m)


def nz(obj, prop, default=None, same_type_var=''):
    result = default
    if obj is not None:
        if isinstance(obj, object):
            if prop in obj:
                if isinstance(obj[prop], type(same_type_var)):
                    result = obj[prop]
    return result


def validate_user_id(user_id=''):
    error = 'user_id required'
    if user_id is not None:
        if isinstance(user_id, str):
            if user_id != '':
                error = None
    return error


def validate_skills(skills):
    error = 'skills required'
    if skills is not None:
        if isinstance(skills, list):
            if len(skills):
                error = None
    return error


class Api:

    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db
        pass

    async def root(self, request):
        log_request(request)
        output = {
            'version': self.config.version,
            'ts': nowf()
        }
        return web.json_response(output)

    async def profiles_search(self, request):
        log_request(request)
        params = {}
        error = None

        skills_str = nz(request.query, 'skills', '', '')
        if skills_str != '':
            skills_list = skills_str.split(',')
            error = validate_skills(skills_list)
            if error is None:
                params = {'skills': {'$all': skills_list}}

        profiles = self.db.profiles_search(params)
        output = {
            'data': profiles,
            'error': error,
            'ts': nowf()
        }
        return web.json_response(output)

    async def profiles_upsert(self, body, user_id=''):
        error = None
        result = None

        while True:
            skills = nz(body, 'skills', [], [])
            error = validate_skills(skills)
            if error is not None:
                break

            if user_id == '':  # from URL
                mode = 'create'
                user_id = nz(body, 'user_id', '', '')
            else:
                mode = 'update'

            error = validate_user_id(user_id)
            if error is not None:
                break

            # still, run upsert() to avoid duplicates for same user_id
            result = self.db.profiles_upsert(user_id, skills)
            break  # run loop once
        # end while

        output = {
            'data': result,
            'error': error,
            'ts': nowf()
        }
        return web.json_response(output)

    async def profiles_create(self, request):
        log_request(request)
        body = await request.json()
        return await self.profiles_upsert(body)

    async def profiles_update(self, request):
        user_id = request.match_info.get('user_id', '')
        log_request(request, 'user_id {}'.format(user_id))
        body = await request.json()
        return await self.profiles_upsert(body, user_id)

    async def profiles_retrieve(self, request):
        user_id = request.match_info.get('user_id', '')
        log_request(request, 'user_id {}'.format(user_id))
        profile = None
        error = validate_user_id(user_id)
        if error is not None:
            profile = self.db.profiles_retrieve(user_id)

        output = {
            'data': profile,
            'error': error,
            'ts': nowf()
        }
        return web.json_response(output)

    async def profiles_delete(self, request):
        log_request(request)
        user_id = request.match_info.get('user_id', '')
        result = False
        if user_id != '':
            result = self.db.profiles_delete(user_id)

        output = {
            'data': result,
            'ts': nowf()
        }
        return web.json_response(output)


def get_api(config: Config, db: Db):
    return Api(config, db)

