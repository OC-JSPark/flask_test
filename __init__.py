from flask import Flask, render_template,g
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

# flask run -> create_app()
def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SESSION_COOKIE_NAME'] = 'googlekaap'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/googlekaap?charset=utf8' ## /googlekaap은 db명을 넣는것이다.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list' 

    if app.config['DEBUG'] == True: #true일때 (debug환경일때) 
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1 # 1s로 바꾸니 바로 갱신될것이다.
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['WTF_CSRF_ENABLED'] = False  ## api test할때 CSRF token is mission error 발생하는데 post method 보낼때 CSRF token을 같이 실어서 보내준다. 지금 문서화에서는 해당작업을 안했기에 이런 에러가 뜬다.

    """ === CSRF Init === """
    csrf.init_app(app)


    """ === Database Init === """
    db.init_app(app)
    ## TDD할때 sqlite를 사용할건데 altertable이라는 RDBMS의 query중에 테이블의 형상을 바꾸는 쿼리가 안먹을수 있다. sqlite는.왜냐면 test용도니깐. 그런것을 대응해주기 위한 예외처리를 넣어주자.
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


    ''' Blueprint Route INIT '''
    from googlekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    ''' Restx INIT '''
    from googlekaap.apis import blueprint as api
    app.register_blueprint(api)


 

    """ REQUEST HOOK """
    @app.before_request
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html')
    
    # ''' === Method & Request context Practice === '''
    # from flask import request
    # @app.route('/test/method/', defaults={'id': 1}, methods=['GET', 'POST', 'DELETE', 'PUT'])
    # @app.route('/test/method/<int:id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
    # def method_test(id):
        # return jsonify({
            # 'id': id,
            # 'request.args': request.args,
            # 'request.form': request.form,
            # 'request.json': request.json
        # })


    # ''' === Routing Practice === '''
    # from flask import jsonify, redirect, url_for
    # from markupsafe import escape

    # @app.route('/test/name/<name>')
    # def name(name):
        # return f'Name is {name}, {escape(type(name))}'

    # @app.route('/test/id/<int:id>')
    # def id(id):
        # return 'Id: %d' % id

    # @app.route('/test/path/<path:subpath>')
    # def path(subpath):
        # return subpath

    # @app.route('/test/json')
    # def json():
        # return jsonify({'hello': 'world'})

    # @app.route('/test/redirect/<path:subpath>')
    # def redirect_url(subpath):
        # return redirect(subpath)

    # @app.route('/test/urlfor/<path:subpath>')
    # def urlfor(subpath):
        # return redirect(url_for('path', subpath=subpath))

    # ''' === Request hook, Context controll  === '''
    # # https://flask.palletsprojects.com/en/1.1.x/api/
    # from flask import g, current_app
    # @app.before_first_request
    # def before_first_request():
        # app.logger.info('BEFORE_FIRST_REQUEST')

    # @app.before_request
    # def before_request():
        # g.test = True
        # app.logger.info('BEFORE_REQUEST')

    # @app.after_request
    # def after_request(response):
        # app.logger.info(f"g.test: {g.test}")
        # app.logger.info(f"current_app.config: {current_app.config}")
        # app.logger.info("AFTER_REQUEST")
        # return response

    # @app.teardown_request
    # def teardown_request(exception):
        # app.logger.info('TEARDOWN_REQUEST')

    # @app.teardown_appcontext
    # def teardown_appcontext(exception):
        # app.logger.info('TEARDOWN_CONTEXT')
        
    return app
