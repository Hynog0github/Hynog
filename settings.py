class Config(object):
    # 默认调试设置
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dfds3d3dssdfsdfdsfe22fs"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

