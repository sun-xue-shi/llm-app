from dataclasses import dataclass
from uuid import UUID

from injector import inject

from internal.schema.api_tool import ValidateOpenApiSchema, CreateApiTool, GetApiToolProviderResp, GetApiToolResp
from internal.service import ApiToolService
from pkg.response import valid_error_json, success_message, success_json


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

    def get_api_tool(self, provider_id: UUID, tool_name: str):
        """根据传递的provider_id+tool_name获取工具的详情信息"""
        api_tool = self.api_tool_service.get_api_tool(provider_id, tool_name)

        resp = GetApiToolResp()

        return success_json(resp.dump(api_tool))

    def get_api_tool_provider(self, provider_id: UUID):
        api_tool_provider = self.api_tool_service.get_api_tool_provider(provider_id)

        resp = GetApiToolProviderResp()

        return success_json(resp.dump(api_tool_provider))

    def delete_api_tool_provider(self, provider_id: UUID):
        """根据传递的provider_id删除对应的工具提供者信息"""
        self.api_tool_service.delete_api_tool_provider(provider_id)

        return success_message("删除自定义API插件成功")
