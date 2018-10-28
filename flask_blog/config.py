class Config:
    SECRET_KEY = 'f2559f1aa7235166fbc63899be2967b7'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    # Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7612@127.0.0.1:3306/myblog'