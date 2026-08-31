from pydantic import BaseModel, Field
from typing import Annotated


class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(..., ge=3)]
    description: Annotated[str, Field(..., ge=10)]
    parameters: Annotated[dict | None, Field(default=None)]
    returns: Annotated[dict | None, Field(default=None)]


class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(..., ge=1)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(...)]
