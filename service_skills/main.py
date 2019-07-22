from aiohttp import web
import argparse
from service_skills import Api
from service_skills.routes import setup_routes
from service_skills.config import get_config
from service_skills.db import get_db


def get_args():
    parser = argparse.ArgumentParser(description="skills service")
    #parser.add_argument('--path')
    parser.add_argument('--port')
    return parser.parse_args()


def start():
    app = web.Application()
    args = get_args()
    config = get_config(args)
    db = get_db(config)
    api = Api(config, db)
    setup_routes(app, api)
    web.run_app(app, port=config.port)


if __name__ == '__main__':
    start()
