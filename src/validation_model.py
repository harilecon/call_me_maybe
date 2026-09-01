from pydantic import BaseModel, Field
from typing import Annotated


class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(..., min_length=3)]
    description: Annotated[str, Field(..., min_length=10)]
    parameters: Annotated[dict | None, Field(default=None)]
    returns: Annotated[dict | None, Field(default=None)]


class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(...)]
