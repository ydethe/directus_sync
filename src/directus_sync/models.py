from datetime import date, datetime
from typing import Dict, List, Optional
from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from .vcard import Gender, Name, VCard
from .vcard import Address as VAddress
from .vcard import Telephone as VTelephone
from .vcard import Email as VEmail


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


class Coordinate(BaseModel):
    type: str
    coordinates: List[float]


class Adresse(BaseDirectusModel):
    Adresse: str
    Code_postal: str
    Ville: str
    Pays: str
    Coordonnees: Coordinate

    def to_vcard(self) -> VAddress:
        adr = VAddress(
            street=self.Adresse,
            locality=self.Ville,
            postal_code=self.Code_postal,
            country=self.Pays,
        )
        return adr


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

    def to_vcard(self) -> VTelephone:
        vtel = VTelephone(value=self.Telephone, type=[self.Type], pref=2 - int(self.Prefere))
        return vtel


class Email(BaseDirectusModel):
    Email: str
    Contact: int
    Prefere: bool
    Type: str

    def to_vcard(self) -> VEmail:
        vmail = VEmail(value=self.Email, type=[self.Type], pref=2 - int(self.Prefere))
        return vmail


class Contact(BaseDirectusModel):
    Nom: str
    Prenom: str
    Particule: str
    Civilite: str
    Nom_de_naissance: Optional[str] = ""
    Date_de_naissance: date
    Site_web: Optional[str] = ""
    Profile_LinkedIn: Optional[str] = ""
    Notes: Optional[str] = ""
    Photo: Optional[str] = ""
    Photo_Content: Optional[bytes] = b""
    Directus_User: Optional[str] = ""
    Adresses: List[int] = []

    def to_vcard(
        self,
        adresses: Dict[int, Adresse],
        contact_adresses: Dict[int, ContactsAdresse],
        experiences: Dict[int, Experience],
        organisations: Dict[int, Organisation],
        organisation_adresses: Dict[int, OrganisationsAdresse],
        telephones: Dict[int, Telephone],
        emails: Dict[int, Email],
    ) -> VCard:
        list_adr: List[VAddress] = []
        for ca in contact_adresses.values():
            if ca.Contacts_id == self.id:
                vadr = adresses[ca.Adresse_id].to_vcard()
                vadr.label = ca.Type
                list_adr.append(vadr)

        list_tel: List[VTelephone] = []
        for tel in telephones.values():
            if tel.Contact == self.id:
                vtel = tel.to_vcard()
                list_tel.append(vtel)

        list_mail: List[VEmail] = []
        for mail in emails.values():
            if mail.Contact == self.id:
                vmail = mail.to_vcard()
                list_mail.append(vmail)

        last_expe: Experience | None = None
        last_expe_date = self.Date_de_naissance
        for exp in experiences.values():
            if exp.Date_debut > last_expe_date:
                last_expe_date = exp.Date_debut
                last_expe = exp

        role = None
        if last_expe is not None:
            orga = organisations[last_expe.Organisation]

            role = f"{last_expe.Intitule} @ {orga.Nom}"

            for org_adr in organisation_adresses.values():
                if org_adr.Organisation_id == orga.id:
                    exp_adr = adresses[org_adr.Adresse_id]

                    vadr = exp_adr.to_vcard()
                    vadr.label = "Pro"
                    list_adr.append(vadr)

                    break

        vcard = VCard(
            prodid=f"{self.id}",
            fn=f"{self.Prenom}{self.Particule}{self.Nom}",
            n=Name(
                family=f"{self.Particule}{self.Nom}".strip(),
                given=self.Prenom,
                prefixes=[self.Civilite],
            ),
            anniversary=self.Date_de_naissance,
            gender=Gender.M if self.Civilite in ["Mr", "Frère", "Père"] else Gender.F,
            adr=list_adr,
            tel=list_tel,
            email=list_mail,
            title=self.Civilite,
            role=role,
        )
        return vcard
