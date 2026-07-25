from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    api_key: str = Field(..., description="Cle API complete (format pp_<prefix>_<secret>)")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
