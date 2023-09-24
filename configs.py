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

class ProductionConfig(DevelomentConfig):
     pass