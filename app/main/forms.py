from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('来自', validators=[Length(0, 64)])
    about_me = TextAreaField('签名')
    submit = SubmitField('提交')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email(message='email地址无效！')])
    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母、数字、下划线和点号')])
    confirmed = BooleanField('已确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('来自', validators=[Length(0, 64)])
    about_me = TextAreaField('签名')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.id).all()] # 下拉实现
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('这个Email已经被使用了 (▔﹏▔)')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('这个用户名已经被使用了 (▔﹏▔)')


class PostForm(Form):
    # body = TextAreaField("有什么新鲜事抑或想到点什么，写下来呗！", validators=[Required()])
    body = PageDownField("有什么新鲜事 或者 想到点什么，写下来呗！", validators=[Required()])
    submit = SubmitField('发布')
