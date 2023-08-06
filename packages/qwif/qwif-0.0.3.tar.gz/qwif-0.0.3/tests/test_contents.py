import dataclasses
import pytest

from qwif import contents


def test_format_base_escape_string():

    base = contents.ContentBase()

    base.escape_character = "\\"

    # The order in which special characters are defined should be irrelevant.
    # It should specifically not result escape characters getting escaped.
    base.special_characters = [ "\\", ";" ]
    assert base.escape_string("\\;") == "\\\\\\;"
    base.special_characters = [  ";", "\\" ]
    assert base.escape_string("\\;") == "\\\\\\;"
    assert base.escape_string(";;") == "\\;\\;"


def test_format_base_encode():

    # ContentBase should expose any field keys as format fields by default.
    base_cls = dataclasses.make_dataclass('ContentTest',
        fields=[
            ('test', str, dataclasses.field(default="true")),
            ('time', int, dataclasses.field(default=0)),
        ],
        bases=(contents.ContentBase,)
    )
    base = base_cls()
    assert str(base) == "test:true;time:0;;"

    # fields with a value of `None` should not be present in encoded output
    base = base_cls()
    base.__dict__["time"] = None
    assert str(base) == "test:true;;"

    # If field_names are set, only those should be present in encoded output.
    # Additionally, instance fields names should be mapped to the proper target
    # name specified in `field_names`
    base = base_cls()
    base.field_names = dict(time="T")
    assert str(base) == "T:0;;"
    base.field_names["test"] = "t"
    assert str(base) == "t:true;T:0;;"

    # Setting field_order should ensure only specified fields are present in
    # encoded output, and that fields are listed in the stated order.
    base = base_cls()
    base.field_order = ["time", "test"]
    assert str(base) == "time:0;test:true;;"
    base.__dict__["time"] = None
    assert str(base) == "test:true;;"

    # Setting a `prefix` should result in that prefix being prepended to the
    # encoded output
    base = base_cls()
    base.prefix = "RES"

    assert str(base) == "RES:test:true;time:0;;"


def test_url():

    url = contents.Url(url="https://test")
    assert str(url) == "https://test"
    url.bookmark = True
    assert str(url) == "URL:https://test;;"
    url.title = "test"
    assert str(url) == "TITLE:test;URL:https://test;;"


def test_email():

    email = contents.Email("test@test.test")
    assert str(email) == "mailto:test@test.test"

    email = contents.Email("test@test.test?subject=Meeting&cc=info@test.test")
    assert str(email) == "mailto:test@test.test?subject=Meeting&cc=info@test.test"


def test_text():

    text = contents.Text("test")
    assert str(text) == "test"


def test_sms():

    sms = contents.Sms(number="1111")
    assert str(sms) == "sms:1111"
    sms.message="hello"
    assert str(sms) == "sms:1111:hello"
    sms.number = ""
    assert str(sms) == "sms::hello"


def test_mms():
    mms = contents.Mms(number="1111")
    assert str(mms) == "mms:1111"
    mms.message="hello"
    assert str(mms) == "mms:1111:hello"
    mms.number = ""
    assert str(mms) == "mms::hello"


def test_wifi():

    wifi = contents.Wifi(ssid="test", password="test")
    assert str(wifi) == "WIFI:H:false;P:test;S:test;T:WPA;;"
    wifi.authentication_type = "WEP"
    assert str(wifi) == "WIFI:H:false;P:test;S:test;T:WEP;;"
    wifi.authentication_type = "nopass"
    assert str(wifi) == "WIFI:H:false;S:test;;"
    wifi.authentication_type = "WPA2-EAP"
    wifi.eap_anonymous_identity = "anon"
    wifi.eap_identity = "user"
    assert str(wifi) == "WIFI:A:anon;E:TTLS;H:false;I:user;P:test;PH2:MSCHAPV2;S:test;T:WPA2-EAP;;"


def test_otp():
    otp = contents.OTP(secret="ORSXG5AK", issuer="test issuer", account_name="test")

    assert str(otp) == str(
        "optauth://totp/test%20issuer:test/?secret=ORSXG5AK"
        "&issuer=test%20issuer&algorithm=SHA256&digits=6&period=30"
    )
    otp.type = "hotp"
    assert str(otp) == str(
        "optauth://hotp/test%20issuer:test/?secret=ORSXG5AK"
        "&issuer=test%20issuer&algorithm=SHA256&digits=6&counter=0"
    )

    with pytest.raises(ValueError):
        otp.type = "whatever"
        otp.validate()

    otp.type = "totp"

    with pytest.raises(ValueError):
        otp.algorithm = "whatever"
        otp.validate()
