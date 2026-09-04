from pydantic import BaseModel


class RegisterRequest(BaseModel):

    username: str
    password: str
    textbee_device_id: str | None = None
    textbee_api_key: str | None = None


class LoginRequest(BaseModel):

    username: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str