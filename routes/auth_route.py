from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from googlekaap.forms.auth_form import loginForm, RegisterForm
from googlekaap.models.user import User as UserModel
from werkzeug import security


NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth') # blueprint아래에 작성되는 라우터는 모두 prefix를 auth를 갖게된다.공통관리가능. 


""" only for testing """
from dataclasses import dataclass
USERS = []

@dataclass
class User:
    """
        class User:
            def __init__(self, user_id, user_name, password):
                self.user_id = user_id
                self.user_name = user_name
                self.password = password
    와 아래는 동일한 의미다.
    """
    user_id:str
    user_name:str
    password:str

USERS.append(User('hidekuma','hidekuma',security.generate_password_hash('1234')))
USERS.append(User('admin','admin',security.generate_password_hash('1234')))
USERS.append(User('tester','tester',security.generate_password_hash('1234')))






@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))


@bp.route('/login', methods=['GET','POST'])
def login():

    form = loginForm()

    # POST,validate OK
    if form.validate_on_submit():
        ## TODO
        # 1) 유저조회
        # 2) 유저 이미 존재하는지 체크
        # 3) 패스워드 정합확인
        # 4) 로그인유지(세션)
        
        
        user_id = form.data.get('user_id')
        password = form.data.get('password') 
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            user = user[0]
            if not security.check_password_hash(user.password,password):
                flash('Password is not valid')
            else:
                ## session context추가
                session['user_id'] = user_id
                ## redirect 해줘라. index page에!
                return redirect(url_for('base.index'))
        

        else:
 
            flash('User ID is not exists.')
    else:
        # TODO: Error
        flash_form_errors(form) 

    return render_template(f'{NAME}/login.html', form=form)

@bp.route('/register',methods=['GET','POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        ## TODO
        # 1) 유저조회
        # 2) 유저 이미 존재하는지 체크
        # 3) 없으면 유저 생성
        # 4) 로그인유지(세션)
        
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        password = form.data.get('password') 
        repassword = form.data.get('repassword')
        
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            flash('User ID is already exists.')
            return redirect(request.path)
        else:
            USERS.append(
                User(
                    user_id=user_id,
                    user_name=user_name,
                    password=security.generate_password_hash(password)
                )
            )

            session['user_id'] = user_id
            return redirect(url_for('base.index'))
        return f'{user_id}, {user_name},{password},{repassword}'
    else:
        # TODO: Error
        flash_form_errors(form)  

    return render_template(f'{NAME}/register.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('user_id',None) # None은 만약 user_id 없을경우!
    return redirect(url_for(f'{NAME}.login'))


def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)