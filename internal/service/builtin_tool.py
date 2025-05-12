from dataclasses import dataclass

from injector import inject
from pydantic.v1 import BaseModel

from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.exception import NotFoundException


@inject
@dataclass
class BuiltinToolService:
    builtin_provider_manager: BuiltinProviderManager

    def get_builtin_tools(self):
        providers = self.builtin_provider_manager.get_providers()

        builtin_tools = []

        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": [],
            }

            for tool_entity in provider.get_tool_entities():
                tool = provider.get_tool(tool_entity.name)
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": self.get_tool_inputs(tool)
                }

                builtin_tool["tools"].append(tool_dict)
            builtin_tools.append(builtin_tool)
        return builtin_tools

    def get_builtin_tool(self, provider_name: str, tool_name: str):
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"Provider {provider_name} not found")

        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"Tool {tool_name} not found in provider {provider_name}")

        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_name)

        builtin_tool = {
            "provider": {**provider_entity.model_dump(exclude=["icon", "created_at"])},
            **tool_entity.model_dump(),
            "created_at": provider_entity.created_at,
            "inputs": self.get_tool_inputs(tool)
        }
        return builtin_tool

    @classmethod
    def get_tool_inputs(cls, tool):
        inputs = []

        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):

            for field_name, model_field in tool.args_schema.__fields__.items():
                inputs.append({
                    "name": field_name,
                    "type": model_field.outer_type_.__name__,
                    "description": model_field.field_info.description or "",
                    "required": model_field.required
                })
        return inputs
