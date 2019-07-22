version = '1.0.0'


class Config:

    def __init__(self, args):
        self.version = version
        self.port = args.port
        self.db_dsn = 'mongodb://localhost:27017/'
        self.db_name = 'service_skills'
        pass


def get_config(args):
    return Config(args)
