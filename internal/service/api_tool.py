import json
from dataclasses import dataclass
from uuid import UUID

from injector import inject

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidateException, NotFoundException
from internal.model import ApiToolProvider, ApiTool
from internal.schema.api_tool import CreateApiTool
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class ApiToolService:
    db: SQLAlchemy

    @classmethod
    def parse_openapi_schema(cls, schema: str):
        try:
            data = json.loads(schema.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidateException("传递数据必须符合openapi规范")

        return OpenAPISchema(**data)

    def create_api_tool(self, req: CreateApiTool):
        account_id = "kfdhisjhfdihfiuhgivsnfdjvhsdjhvjfsn"

        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            name=req.name.data,
            account_id=account_id
        ).one_or_none()

        if api_tool_provider:
            raise ValidateException("api tool name already exists")

        with self.db.auto_commit():
            api_tool_provider = ApiToolProvider(
                name=req.name.data,
                account_id=account_id,
                openapi_schema=req.openapi_schema.data,
                headers=req.headers.data,
                description=openapi_schema.description,
                icon=req.icon.data,
            )
            self.db.session.add(api_tool_provider)
            self.db.session.flush()

            for path, path_item in openapi_schema.paths.items():
                for method, method_item in path_item.items():
                    api_tool = ApiTool(
                        account_id=account_id,
                        provider_id=api_tool_provider.id,
                        name=method_item.get("operationId"),
                        description=method_item.get("description"),
                        method=method,
                        url=f"{openapi_schema.server}{path}",
                        parameters=method_item.get("parameters", [])
                    )
                    self.db.session.add(api_tool)

    def get_api_tool_provider(self, provider_id: UUID):
        account_id = "kfdhisjhfdihfiuhgivsnfdjvhsdjhvjfsn"

        api_tool_provider = self.db.session.query(ApiToolProvider).get(provider_id)

        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise ValidateException("api tool provider not found")

        return api_tool_provider

    def get_api_tool(self, provider_id: UUID, tool_name: str) -> ApiTool:
        """根据传递的provider_id+tool_name获取对应工具的参数详情信息"""
        # todo:等待授权认证模块完成进行切换调整
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"

        api_tool = self.db.session.query(ApiTool).filter_by(
            provider_id=provider_id,
            name=tool_name,
        ).one_or_none()

        if api_tool is None or str(api_tool.account_id) != account_id:
            raise NotFoundException("该工具不存在")

        return api_tool

    def delete_api_tool_provider(self, provider_id: UUID):
        """根据传递的provider_id删除对应的工具提供商+工具的所有信息"""
        # todo:等待授权认证模块完成进行切换调整
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"

        # 1.先查找数据，检测下provider_id对应的数据是否存在，权限是否正确
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException("该工具提供者不存在")

        # 2.开启数据库的自动提交
        with self.db.auto_commit():
            # 3.先来删除提供者对应的工具信息
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == provider_id,
                ApiTool.account_id == account_id,
            ).delete()

            # 4.删除服务提供者
            self.db.session.delete(api_tool_provider)
