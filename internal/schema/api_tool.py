from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL, ValidationError

from internal.schema import ListField


class ValidateOpenApiSchema(FlaskForm):
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="OpenAPI schema is required")
    ])


class CreateApiTool(FlaskForm):
    name = StringField("name", validators=[
        DataRequired(message="Name is required"),
        Length(min=1, max=64, message="Name length must be between 1 and 64")
    ])
    icon = StringField("icon", validators=[
        DataRequired(message="Icon is required"),
        URL(message="Icon must be a valid URL"),
    ])
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="OpenAPI schema is required")
    ])
    headers = ListField("headers")

    @classmethod
    def validate_headers(cls, form, field):
        for header in field.data:
            if not isinstance(header, dict):
                raise ValidationError("Header must be a dictionary")
            if set(header.keys()) != {"key", "value"}:
                raise ValidationError("Header must have 'key' and 'value' keys")
