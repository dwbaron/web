class Config:
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    # Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7612@127.0.0.1:3306/myblog'