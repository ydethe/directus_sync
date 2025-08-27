from datetime import date, datetime
from typing import List
from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
    )

    directus_url: HttpUrl
    directus_token: str


class Contact(BaseModel):
    id: int
    user_created: str
    date_created: datetime
    user_updated: str
    date_updated: datetime
    Nom: str
    Prenom: str
    Particule: str
    Civilite: str
    Nom_de_naissance: str | None
    Date_de_naissance: date
    Site_web: str
    Profile_LinkedIn: str
    Notes: str | None
    Photo: str
    Directus_User: str | None
    Adresses: List[int]
