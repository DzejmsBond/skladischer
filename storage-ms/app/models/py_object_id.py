# Author: Jure
# Date created: 17.12.2024

from typing import Type, Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.__validate

    @classmethod
    def __validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @staticmethod
    def __serialize(value: 'PyObjectId') -> str:
        return str(value)

    @classmethod
    #def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler) -> JsonSchemaValue:
    def __get_pydantic_json_schema__(cls) -> JsonSchemaValue:
        return {"type": "string"}

    # TODO: it works as is. read documentation and write it more proper?
    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source is PyObjectId
        return core_schema.no_info_after_validator_function(
            function=cls.__validate,
            schema=core_schema.any_schema(), #works, but probably can be made better?
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.__serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )



