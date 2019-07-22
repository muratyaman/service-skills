from aiohttp import web


def setup_routes(app, api):
    routes = [
        web.get('/', api.root),
        web.get('/api', api.root),
        web.get('/api/skills', api.root),
        web.get('/api/skills/profiles', api.profiles_search),
        web.post('/api/skills/profiles', api.profiles_create),
        web.get('/api/skills/profiles/{user_id}', api.profiles_retrieve),
        web.put('/api/skills/profiles/{user_id}', api.profiles_update),
        web.patch('/api/skills/profiles/{user_id}', api.profiles_update),
        web.delete('/api/skills/profiles/{user_id}', api.profiles_delete)
    ]
    app.add_routes(routes)
