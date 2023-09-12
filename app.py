from flask import Flask

app = Flask(__name__)

print('__name__', __name__)
print('DEBUG', app.config['DEBUG'])


@app.route('/')     # 어떤 url에 route시킬것인가를 지정
def index():
    return "hello world!!!"


if __name__ == '__main__':
    print('run')
    app.run(debug=True, port=5051, host='localhost')