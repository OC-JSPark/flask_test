from flask import Flask
from flask import render_template

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    if app.config['DEBUG']: #true일때
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1 # 1s로 바꾸니 바로 갱신될것이다.

    @app.route('/')     # 어떤 url에 route시킬것인가를 지정
    def index():
        return render_template('index.html')    # 자동으로 상대경로를 templates를 받는다.

    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html')
    return app
