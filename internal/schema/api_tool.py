from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL, ValidationError

from internal.model import ApiToolProvider, ApiTool
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


class GetApiToolProviderResp(Schema):
    id = fields.UUID()
    name = fields.String()
    icon = fields.String()
    openapi_schema = fields.String()
    headers = fields.List(fields.Dict, default=[])
    created_at = fields.Integer(default=0)

    @pre_dump
    def process_data(self, data: ApiToolProvider, **kwargs):
        return {
            "id": data.id,
            "name": data.name,
            "icon": data.icon,
            "openapi_schema": data.openapi_schema,
            "headers": data.headers,
            "created_at": int(data.created_at.timestamp())
        }


class GetApiToolResp(Schema):
    """获取API工具参数详情响应"""
    id = fields.UUID()
    name = fields.String()
    description = fields.String()
    inputs = fields.List(fields.Dict, default=[])
    provider = fields.Dict()

    @pre_dump
    def process_data(self, data: ApiTool, **kwargs):
        provider = data.provider
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "inputs": [{k: v for k, v in parameter.items() if k != "in"} for parameter in data.parameters],
            "provider": {
                "id": provider.id,
                "name": provider.name,
                "icon": provider.icon,
                "description": provider.description,
                "headers": provider.headers,
            }
        }
