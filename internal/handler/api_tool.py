from dataclasses import dataclass

from injector import inject

from internal.schema.api_tool import ValidateOpenApiSchema, CreateApiTool
from internal.service import ApiToolService
from pkg.response import valid_error_json, success_message


@inject
@dataclass
class ApiToolHandler:
    api_tool_service: ApiToolService

    def vaildate_openapi_schema(self):
        req = ValidateOpenApiSchema()

        if not req.validate():
            return valid_error_json(req.errors)

        self.api_tool_service.parse_openapi_schema(req.openapi_schema.data)

        return success_message("数据校验成功")

    def create_api_tool(self):
        req = CreateApiTool()
        if not req.validate():
            return valid_error_json(req.errors)

        self.api_tool_service.create_api_tool(req)
        return success_message("自定义api插件创建成功")
