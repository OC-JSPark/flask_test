from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SESSION_COOKIE_NAME'] = 'googlekaap'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@localhost/googlekaap?charset=utf8'  ## /googlekaap은 db명을 넣는것이다.
    app.config['SQLALCHMEY_TACK_MODIFICATIONS'] = False
    if app.config['DEBUG']: #true일때
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1 # 1s로 바꾸니 바로 갱신될것이다.

    ''' DB INIT '''
    db.init_app(app)
    ## TDD할때 sqlite를 사용할건데 altertable이라는 RDBMS의 query중에 테이블의 형상을 바꾸는 쿼리가 안먹을수 있다. sqlite는.왜냐면 test용도니깐. 그런것을 대응해주기 위한 예외처리를 넣어주자.
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, redner_as_batch=True)
    else:
        migrate.init_app(app,db)
    migrate.init_app(app,db)


    ''' Blueprint Route INIT '''
    from googlekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)



    ''' CSRF INIT '''
    csrf.init_app(app)

    
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html')
    return app
