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


class BaseDirectusModel(BaseModel):
    id: int
    user_created: str
    date_created: datetime
    user_updated: str | None
    date_updated: datetime | None


class Contact(BaseDirectusModel):
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


class Coordinate(BaseModel):
    type: str
    coordinates: List[float]


class Adresse(BaseDirectusModel):
    Adresse: str
    Code_postal: str
    Ville: str
    Pays: str
    Coordonnees: Coordinate


class ContactsAdresse(BaseModel):
    id: int
    Contacts_id: int
    Adresse_id: int
    Type: str


class Experience(BaseDirectusModel):
    Contact: int
    Type: str
    Organisation: int
    Date_debut: date
    Date_fin: date | None
    Intitule: str
    Description: str | None


class Organisation(BaseDirectusModel):
    Nom: str
    Site_web: str | None
    Type: str
    Adresse: List[int]


class OrganisationsAdresse(BaseModel):
    id: int
    Organisation_id: int
    Adresse_id: int


class Telephone(BaseDirectusModel):
    Telephone: str
    Contact: int
    Prefere: bool
    Type: str
