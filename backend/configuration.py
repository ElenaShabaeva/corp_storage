from pydantic.v1 import BaseSettings
from typing import ClassVar
from fastapi.security import HTTPBearer


class Settings(BaseSettings):
    url: str = "http://127.0.0.1:8000"
    get_attachment_url: str = f"{url}/attachment?attachment_id="
    expiration_time_of_access_token: int = 30
    expiration_time_of_refresh_token: int = 20160
    expiration_time_of_access_token_for_browser: int = expiration_time_of_access_token*60
    expiration_time_of_refresh_token_for_browser: int = expiration_time_of_refresh_token*60
    http_bearer: ClassVar = HTTPBearer()


settings = Settings()
