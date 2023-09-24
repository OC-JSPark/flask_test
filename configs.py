import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))   ##__file__의 절대경로의 디렉토리명을 확인해보자.

class Config:
    """ Flask Config """    
    SECRET_KEY = 'secret'
    SESSION_COOKIE_NAME = 'googlekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/googlekaap?charset=utf8' ## /googlekaap은 db명을 넣는것이다.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list' 

class DevelomentConfig(Config): ## 위에 만든 Config를 상속받는형태이기 떄문에(Config) 가 들어간다.
     
     """ Flask Config for dev """
     DEBUG = True #true일때 (debug환경일때) 
     SEND_LEMAX_AGE_DEFAULT = 1 # 1s로 바꾸니 바로 갱신될것이다.
     # TODO: Front호출시 처리
     WTF_CF_NABLED = False

class TestingConfig(DevelomentConfig):
     __test__ = False   ## test로 시작하지만, testcase를 타지말라고 False로 둔다.
     TESTING = True
     SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}' ## 동일경로에 sqlite_test.db가 생성된다.

class ProductionConfig(DevelomentConfig):
     pass