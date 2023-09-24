from flask_restx import Namespace,Resource, fields, reqparse
from googlekaap.models.user import User as UserModel  ## 아래 /api 들은 모두 model에 대한 정보를 가져와야 하기에 이렇게 import 해주자.
from flask import g
from werkzeug import security

ns = Namespace(
  'users',  ## users는 URL에 들어가게 된다.
  description='유저 관련 api'
)

user = ns.model('User', {
  ## 그리고 프론트엔드에 노출시키고 싶은 정의들을 적으면 된다.
  'id' : fields.Integer(required=True, description='유저고유번호'),
  'user_id' : fields.String(required=True, description='유저 아이디'),
  'user_name' : fields.String(required=True, description='유저 이름'),
  'created_at' : fields.DateTime(description='가입일자') 
})

post_parser = reqparse.RequestParser()  #initialize해주자
post_parser.add_argument('user_id',required=True, help='유저고유아이디')  # 우리가 받아올 정보들을 여기다 넣어주자.
post_parser.add_argument('user_name',required=True, help='유저 이름')
post_parser.add_argument('password',required=True, help='유저 패스워드')


# /api/users  ## (복수표현해주기) 이 URL은 모든 users 정보를 가져오는걸 목적으로 한다.
@ns.route('')
@ns.response(409, 'User Id is already exists')  ## 이렇게 문서화해줄수 있다.
class UserList(Resource):
  @ns.marshal_with(user, skip_none=True) ## 복수일때는  marshal_list_with, 단수일때는 marshal_with해주면 된다.그리고 여기에 우리가 만든 user를 넣어주고, skip_none=True를 넣어준다. skip_none은 특정 필드가 null이거나 데이터가 없을 경우 아예 key값을 안만들어 준다.  
  ## 우리가 배웠던 method를 함수로 정의해주면 된다.
  def get(self):
    ## 비지니스 로직을 만들어보자.
    """유저 복수 조회"""
    data = UserModel.query.all()
    return data
  
  @ns.expect(post_parser)
  @ns.marshal_list_with(user,skip_none=True)  
  def post(self):
    """ 유저 생성"""
    args = post_parser.parse_args()
    user_id = args['user_id']
    user = UserModel.find_one_by_user_id(user_id)
    if user:
      ns.abort(409) ## 유저아이디가 있는경우기 떄문에 장애가 나와야한다. abort 해주면 409 response가 가게 된다. 409 method로 이미 존재하기에 conflict된다고 표현해준다.
    user = UserModel(
      user_id = user_id,
      user_name = args['user_name'],
      password=security.generate_password_hash(args['password'])  ## 암호화해주기
       
    )
    ## g context에 있는 db section을 이용해서 user 넣어주고 commit해준다.
    ## 그리고 여기서 만든걸 return 해줄때 user를 return해주고 정상적으로 생성되면 response가 201 날려주면서 생성되었다고 전달해주자.
    g.db.add(user)
    g.db.commit()
    return user,201

# /api/users/1  ## (단수표현해주기) 모든 users중에 아이디값이 1을 갖는 고유한 user의 정보만 가져와서 보여준다. 
@ns.route('/<int:id>')
@ns.param('id', '유저 고유 번호') ## id는 유저고유번호를 의미함을 나타낸다.
class User(Resource):
  @ns.marshal_with(user, skip_none=True)
  def get(self, id):
    """ 유저 단수 조회"""
    data = UserModel.query.get_or_404(id)   ## get_or_404 : id에 해당하는애가 없으면 404를 띄워준다. 
    return data