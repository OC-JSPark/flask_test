from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class loginForm(FlaskForm):
    user_id = StringField('user_ID', validators=[DataRequired()])    # front에 노출된 라벨이름을 넣어주면된다.
    password = PasswordField('password', validators=[DataRequired()]) 
    pass

class RegisterForm(loginForm):  ## 위에 loginform을 상속받는다. 즉 레지스터 필드는 user_id도 상속받았으니 총 4개의 필드가 들어간다.
    password = PasswordField(
        'password',
        validators=[DataRequired(), EqualTo(
            'repassword',
            message='Password must match.'      ## error났을때 메시지 띄우기위해.
        )]  ## EuqlTo를 이용해서 동일한 문자열인지 체크(아래 repassword와 비교함)
    )
    ## confirm password : password 입력해서 그 패스워드가 맞는지 확인
    repassword = PasswordField(
        'Confirm Password', 
        validators=[DataRequired()]
    )
    
    user_name = StringField('User Name', validators=[DataRequired() ])