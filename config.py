import datetime
import os


# 配置类基类
class BaseConfig(object):
    JWT_SECRET_KEY = "4921"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)

    # 数据库配置
    DIALCT = "mysql"
    DRITVER = "pymysql"
    HOST = 'localhost'
    PORT = "3306"
    USERNAME = "root"
    PASSWORD = "ufo-62418676" # TODO
    DBNAME = 'shadow_url' # TODO

    SQLALCHEMY_DATABASE_URI = f"{DIALCT}+{DRITVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8"
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

# 生产环境配置类
class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

# 开发模式配置类
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
