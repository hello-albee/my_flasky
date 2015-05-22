from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我（网吧或别人的电脑请不要勾选）')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母、数字、下划线和点号')])
    password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='两次输入的密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('这个Email已经被使用了 (▔﹏▔)')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('这个用户名已经被使用了 (▔﹏▔)')

class ChangePasswordForm(Form):
    old_password = PasswordField('旧的密码', validators=[Required()])
    password = PasswordField('新的密码', validators=[Required(), EqualTo('password2', message='两次输入的密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    submit = SubmitField('提交')

class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    password = PasswordField('新的密码', validators=[Required(), EqualTo('password2', message='两次输入的密码必须相同')])
    password2 = PasswordField('确认新的密码', validators=[Required()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('该邮箱未注册.')

class ChangeEmailForm(Form):
    email = StringField('新的邮箱', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('这个Email已经被使用了 (▔﹏▔)')
