from typing import Dict, Iterator, List

from pydantic import BaseModel

from .icloud_contacts import read_icloud_contacts
from .vcard import VCard
from .models import (
    Adresse,
    Config,
    Contact,
    ContactsAdresse,
    Email,
    Experience,
    Organisation,
    OrganisationsAdresse,
    Telephone,
)
from .directus_backend import (
    read_contacts,
    read_adresses,
    read_contact_adresses,
    read_email,
    read_experience,
    read_organisation,
    read_organisation_adresses,
    read_telephone,
)


class DirectusDatabase(BaseModel):
    contacts: Dict[int, Contact] = {}
    adresses: Dict[int, Adresse] = {}
    contact_adresses: Dict[int, ContactsAdresse] = {}
    experiences: Dict[int, Experience] = {}
    organisations: Dict[int, Organisation] = {}
    organisation_adresses: Dict[int, OrganisationsAdresse] = {}
    telephones: Dict[int, Telephone] = {}
    emails: Dict[int, Email] = {}

    def load_from_icloud(self, config: Config) -> Iterator[Contact]:
        for icontact in read_icloud_contacts(config):
            filtered_url: List[str]
            if icontact.urls is None:
                filtered_url = []
            else:
                filtered_url = [
                    iurl.field for iurl in icontact.urls if not iurl.field.startswith("uphabit://")
                ]

            contact = Contact(
                Nom=icontact.lastName if icontact.lastName is not None else "",
                Prenom=icontact.firstName if icontact.firstName is not None else "",
                # TODO Improve Particule detection from iCloud
                Particule="",
                # TODO Improve Civilite detection from iCloud
                Civilite="",
                Nom_de_naissance="",
                Date_de_naissance=icontact.birthday,
                Site_web=filtered_url[0] if len(filtered_url) > 0 else "",
                Notes=icontact.notes,
                Photo=icontact.photo.url if icontact.photo is not None else None,
                # TODO Download photo raw bytes
                # TODO Fill other directus tables
                # Adresses=[adr for adr in icontact.streetAddresses]
            )

            yield contact

    def load_from_directus(self, config: Config):
        for contact in read_contacts(config):
            self.contacts[contact.id] = contact

        for adresse in read_adresses(config):
            self.adresses[adresse.id] = adresse

        for con_adr in read_contact_adresses(config):
            self.contact_adresses[con_adr.id] = con_adr

        for expe in read_experience(config):
            self.experiences[expe.id] = expe

        for orga in read_organisation(config):
            self.organisations[orga.id] = orga

        for orga_adr in read_organisation_adresses(config):
            self.organisation_adresses[orga_adr.id] = orga_adr

        for tel in read_telephone(config):
            self.telephones[tel.id] = tel

        for mail in read_email(config):
            self.emails[mail.id] = mail

    def convert_contacts(self) -> List[VCard]:
        list_vcard: List[VCard] = []
        for contact in self.contacts.values():
            vcard = contact.to_vcard(
                self.adresses,
                self.contact_adresses,
                self.experiences,
                self.organisations,
                self.organisation_adresses,
                self.telephones,
                self.emails,
            )
            list_vcard.append(vcard)

        return list_vcard
