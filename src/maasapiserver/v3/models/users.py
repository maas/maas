from datetime import datetime
from typing import Optional

from django.contrib.auth.hashers import PBKDF2PasswordHasher

from maasapiserver.v3.models.base import MaasBaseModel


class User(MaasBaseModel):
    username: str
    password: str
    is_superuser: bool
    first_name: str
    last_name: str
    is_staff: bool
    is_active: bool
    date_joined: datetime
    email: Optional[str]
    last_login: Optional[datetime]

    def etag(self) -> str:
        pass

    def check_password(self, password) -> bool:
        return PBKDF2PasswordHasher().verify(password, self.password)
