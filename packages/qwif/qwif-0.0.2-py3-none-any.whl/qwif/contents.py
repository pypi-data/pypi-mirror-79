""" A collection of formatters for common QR code types.

This module aims to implement helpers for QR types listed at
https://github.com/zxing/zxing/wiki/Barcode-Contents.
"""

import dataclasses

from dataclasses import dataclass
from datetime import datetime
from os import getpid
from socket import getfqdn
from typing import ClassVar, Dict, List


@dataclass
class ContentBase(object):

    special_characters: ClassVar[List[str]] = []
    escape_character: ClassVar[str] = "\\"
    field_names: ClassVar[Dict[str, str]] = dict()
    field_order: ClassVar[List[str]] = []
    prefix: ClassVar[str] = ""

    def validate(self):
        pass

    def encode(self):

        self.validate()

        format_fields = self.field_order

        if not format_fields:
            format_fields = sorted(
                self.field_names.keys() or (field.name for field in dataclasses.fields(self))
            )

        fragments = [
            "".join([
                f"{self.field_names.get(field, field)}",
                ":",
                f"{self.escape_string(self.__dict__[field])}"
            ]) for field in filter(lambda k: self.__dict__.get(k) not in ["", None], format_fields)
        ]

        if len(self.prefix):
            return f"{self.prefix}:{';'.join(fragments)};;"

        return f"{';'.join(fragments)};;"


    def __str__(self):
        return self.encode()

    def escape_string(self, data: str):
        """ Return a string with any special characters escaped as needed.
        """

        if not len(self.special_characters):
            return data

        special_charset = set(self.special_characters)

        return data.translate(
            str.maketrans(
                dict(
                    zip(
                        special_charset,
                        [f"{self.escape_character}{char}" for char in special_charset]
                    )
                )
            )
        )



@dataclass
class Text(ContentBase):
    text: str

    def encode(self):
        return self.text or ""


@dataclass
class Email(ContentBase):
    mailto: str

    def validate(self):
        if not len(self.mailto):
            raise ValueError("mailto must be a non-empty string")

    def encode(self):
        return f"mailto:{self.mailto}"


@dataclass
class Telephone(ContentBase):
    number: str

    def validate(self):
        if not len(self.number):
            raise ValueError("number must be a non-empty string")

        if self.number.startswith("00"):
            self.number = "+" + self.number[2:]

        if not self.number[0] == "+":
            raise ValueError("number must be a +-prefixed international dial code")

    def encode(self):
        return f"tel:{self.number}"


@dataclass
class Sms(ContentBase):

    number: str = ""
    message: str = ""

    def encode(self):
        if len(self.message) == 0:
            return f"sms:{self.number}"

        return f"sms:{self.number}:{self.message}"


class Mms(Sms):

    def encode(self):
        if len(self.message) == 0:
            return f"mms:{self.number}"

        return f"mms:{self.number}:{self.message}"


@dataclass
class Url(ContentBase):

    field_names: ClassVar[Dict[str,str]] = dict(
        title="TITLE",
        url="URL"
    )
    url: str
    title: str = ""
    bookmark: bool = False

    def validate(self):
        if not len(self.url):
            raise ValueError("url must be a non-empty string.")

    def encode(self):
        if not self.bookmark:
            return self.url

        return super().encode()


@dataclass
class Wifi(ContentBase):

    # instance vars
    ssid: str
    password: str = ""
    authentication_type: str = "WPA"
    hidden: bool = False
    eap_method: str = "TTLS"
    eap_anonymous_identity: str = ""
    eap_identity: str = ""
    eap_phase_two_method: str = "MSCHAPV2"

    # class vars
    valid_authentication_types: ClassVar[List[str]] = [
        "WPA2-EAP", "WPA", "WEP", "nopass"
    ]
    special_characters: ClassVar[List[str]] = ["\\", ";", ",", ":"]
    escape_character: ClassVar[str] = "\\"

    def validate(self):

        if len(self.ssid) < 1:
            raise ValueError("ssid must be a non-empty string")

        if not self.authentication_type in self.valid_authentication_types:
            raise ValueError(
                "".join(
                    "authentication_type must be one of:",
                     ','.join(self.valid_authentication_types)
                )
            )

        if not self.authentication_type == "nopass":
            if len(self.password) < 1:
                raise ValueError("password must be a non-empty string.")

    def encode(self):
        self.validate()

        fields: Dict[str, str] = dict(
            H=str(self.hidden).lower(),
            S=self.escape_string(self.ssid),
        )

        if self.authentication_type != "nopass":
            fields.update(
                dict(
                    P=self.escape_string(self.password),
                    T=self.authentication_type
                )
            )

        if self.authentication_type == "WPA2-EAP":
            fields.update(
                dict(
                    A=self.escape_string(self.eap_anonymous_identity),
                    E=self.eap_method,
                    I=self.escape_string(self.eap_identity),
                    PH2=self.eap_phase_two_method,
                )
            )

        return "".join(
            [
                "WIFI:",
                ';'.join(
                    [f"{field}:{fields[field]}" for field in sorted(fields.keys())]
                ),
                ";",
                ";"
            ]
        )


@dataclass
class Mecard(ContentBase):
    name: str
    address: str = ""
    birthday: str = ""
    email: str = ""
    memo: str = ""
    nickname: str = ""
    number: str = ""
    url: str = ""

    #
    prefix: ClassVar[str] = "MECARD"
    field_names: ClassVar[Dict[str, str]] = dict(
        address="ADR",
        birthday="BDAY",
        email="EMAIL",
        memo="NOTE",
        name="N",
        nickname="NICKNAME",
        number="TEL",
        url="URL",
    )


    def validate(self):
        if not len(self.name):
            raise ValueError("name must be a non-empty string.")

@dataclass
class Geo(ContentBase):
    latitude: float
    longitude: float
    elevation: float = 0.0

    prefix: ClassVar[str] = "geo"

    def encode(self):
        return f"{self.prefix}:{self.latitude},{self.longitude},{self.elevation}"


@dataclass
class Event(ContentBase):
    #
    dtformat: ClassVar[str] = "%Y%m%dT%H%M%SZ"

    # Required instance fields
    summary: str
    dtstart: str
    # Optional fields.
    # Not _all_ fields from vevent are supported.
    # * class is not supported
    # * last-mod is not supported
    # * x-prop, iana-prop are not supported.
    categories: str = ""
    comment: str = ""
    contact: str = ""
    created: str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    description: str = ""
    duration: str = ""
    geo: str = ""
    location: str = ""
    organizer: str = ""
    priority: str = ""
    seq: str = ""
    status: str = ""
    dtstamp: str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dtend: str = ""
    uid: str = f"{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{getpid()}@{getfqdn()}"
    url: str = ""


    def validate(self):

        if self.dtstart == "":
            raise ValueError("dstart is required")

        if "" in [self.dtstart, self.uid, self.dtstamp]:
            raise ValueError("dstart, dstamp and uid are required")

        if self.dtend == "" and self.duration == "":
            raise ValueError("dtend or duration must be provided")

    def encode(self):

        self.validate()

        format_fields = self.field_order

        if not format_fields:
            format_fields = sorted(
                self.field_names.keys() or (field.name for field in dataclasses.fields(self))
            )

        fragments = [
            "".join([
                f"{self.field_names.get(field, field).upper()}",
                ":",
                f"{self.escape_string(self.__dict__[field])}"
            ]) for field in filter(lambda k: self.__dict__.get(k) not in ["", None], format_fields)
        ]

        return "\r\n".join(["BEGIN:VEVENT", "\r\n".join(fragments), "END:VEVENT"])
