import json
from dataclasses import dataclass

from injector import inject

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidateException
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
