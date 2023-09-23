from flask_restx import Api
from flask import Blueprint

## 1. bp = Blueprint(NAME, __name__, url_prefix='/auth') # blueprint아래에 작성되는 라우터는 모두 prefix를 auth를 갖게된다.공통관리가능. 
## 1-1. blueprint initialize한거와 동일한 구조이다.
blueprint = Blueprint (
    'api',
    __name__,
    url_prefix='/api'
)

## 2. Api를 initialize해주자
## 2-1. API를 자동으로 만들어주는데 문서의 버전,경로등을 지정  
api = Api(
    blueprint,
    title='Google Kaap API',
    version='1.0',
    doc='/docs',
    description='Welcome my api docs'
)

# TODO: add namespace to Blueprint 



