from aiohttp import web
from service_skills.helpers import nowf
from service_skills.config import Config
from service_skills.db import Db


class Api:

    def __init__(self, config: Config, db: Db):
        self.config = config
        self.db = db
        pass

    async def root(self, request):
        data = {
            'version': self.config.version,
            'ts': nowf()
        }
        return web.json_response(data)

    async def profiles_search(self, request):
        skills_str = request.query['skills']
        skills_list = skills_str.split(',')
        params = {
            'skills': {'$all': skills_list}
        }
        profiles = self.db.profiles_search(params)
        data = {
            'data': profiles,
            'ts': nowf()
        }
        return web.json_response(data)

    async def profiles_upsert(self, request):
        # user_id, skills
        params = request.json()
        user_id = request.match_info.get('user_id', '')
        if 'user_id' in params:
            user_id = params['user_id']
        found = self.db.profiles_retrieve(user_id)
        if found:
            change = {'skills': params['skills']}
            result = self.db.profiles_update(user_id, change)
        else:
            result = self.db.profiles_create(params)
        data = {
            'data': result,
            'ts': nowf()
        }
        return web.json_response(data)

    async def profiles_create(self, request):
        return self.profiles_upsert(request)

    async def profiles_retrieve(self, request):
        user_id = request.match_info.get('user_id', '')
        profile = self.db.profiles_retrieve(user_id)
        data = {
            'data': profile,
            'ts': nowf()
        }
        return web.json_response(data)

    async def profiles_update(self, request):
        return self.profiles_upsert(request)

    async def profiles_delete(self, request):
        user_id = request.match_info.get('user_id', 'n/a')
        result = self.db.profiles_delete(user_id)
        data = {
            'data': result,
            'ts': nowf()
        }
        return web.json_response(data)

