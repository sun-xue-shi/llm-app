from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """聊天接口请求验证"""
    query = StringField("query", validators=[
        DataRequired(message="用户输入必填"),
        Length(max=2000, message="输入最大长度为2000")
    ])
