from pydantic import BaseModel, Field
from typing import Annotated, Any
from enum import Enum


class AllowedValue(Enum):
    NUMBER = 'number'
    NULL = None
    STRING = 'string'


class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(..., min_length=3)]
    description: Annotated[str, Field(..., min_length=10)]
    parameters: Annotated[dict[str, Any] | None, Field(...)]
    returns: Annotated[dict[str, Any] | None, Field(...)]


class ValidateParameter(BaseModel):
    type: AllowedValue


class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict[str, Any] | None, Field(...)]
