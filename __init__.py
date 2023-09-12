from flask import Flask

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    @app.route('/')     # 어떤 url에 route시킬것인가를 지정
    def index():
        app.logger.info('RUN HEELO WORLD')
        return "hello world!!!"

    ''' Routing Practice'''
    from flask import jsonify, redirect, url_for
    from markupsafe import escape

    @app.route('/text/name/<name>')
    def name(name):     #<>꺽새로 넣어주면 해당 parameter에 인자넣어줄것
        return f'Name is {name} {escape(type(name))}'

    @app.route('/text/id/<int:id>')
    def id(id):
        return 'ID: %d' %id
    
    @app.route('/text/path/<path:subpath>')
    def path(subpath):
        return subpath
    
    @app.route('/text/json')
    def json():
        return jsonify({'hello' : 'world'})
    
    @app.route('/text/redirect/<path:subpath>')
    def redirect_url(subpath):
        return redirect(subpath)

    
    @app.route('/text/urlfor/<path:subpath>')
    def urlfor(subpath):
        return redirect(url_for('path',subpath=subpath)) ## url_for의 인자로는 정의된 router의 함수명이 들어가면된다.
            # 받아온 subpath를 url_for의 subpath로 넣어주고, def path는 subpath가 인자로 필요하잖아. 그걸 그대로 url_for의 인자로 subpath로 넣어줫다고 생각해라.
            # 결과로 path함수정의된걸 url에 찍어준다.
            # url 정의할때 굉장히 많이사용한다.

    ''' Request Hook '''
    from flask import g, current_app
    ## 최초 처음만 실행, 그이후에는 실행안됨
    @app.before_first_request
    def before_first_request():
        app.logger.info('BEFORE_FIRST_REQUSET')

    ## def index() 실행전에 후크로 먼저 실행됨, 이놈은 재실행해도 계속 실행됨
    @app.before_request
    def before_request():
        g.test=True
        app.logger.info('BEROFE_REQUEST')

    ## def index() 실행후에 후크로 실행됨
    @app.after_request
    def after_request(response):
        app.logger.info(f'g.test:{g.test}')
        app.logger.info(f'current_app.config : {current_app.config}')
        app.logger.info('AFTER_REQUEST')
        return response
         
    ## request가 끝날때 정의가능
    @app.teardown_request
    def teardown_request(exception):
        app.logger.info('TEARDOWN_REQUSET')

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        app.logger.info('TEARDOWN_APPCONTEXT')


    ''' Method '''
    from flask import request

    @app.route('/test/method/<id>', methods=['GET','POST','DELETE','PUT'])  ## method 열어줘한다.
    def method_test(id):
        return jsonify({
            'request.args' : request.args,
            'request.form' : request.form,
            'request.json' : request.json,
            'request.method' : request.method,
        })

    return app
