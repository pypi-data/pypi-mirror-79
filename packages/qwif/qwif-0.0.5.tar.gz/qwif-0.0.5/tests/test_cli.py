import pytest
import re

from qwif import cli, contents
from sys import stdout


def test_wifi_subcommand():

    args = ("wifi", "--ssid", "test", "--password", "test", "--hidden",)
    data = cli.cli().parse_args(args)

    assert data.klass == contents.Wifi
    assert data.output == stdout

    #
    assert data.hidden is True
    assert data.password == "test"
    assert data.ssid == "test"


def test_otp_subcommand():

    args = (
        "otp", "--secret", "test", "--issuer", "test", "--account-name", "test"
    )

    data = cli.cli().parse_args(args)

    assert data.klass == contents.OTP
    assert data.output == stdout

    #
    assert data.secret == "test"
    assert data.issuer == "test"
    assert data.account_name == "test"


def test_main(capsys):

    # with no subcommand, qwif CLI should print help, then exit(1).
    with pytest.raises(SystemExit):
        cli.main()

    output = capsys.readouterr()
    assert cli.cli().format_usage() in output.err

    # all subcommands have at least one required field, and should have their
    # own help output.
    for subcommand in ["contact", "geo", "mail", "otp", "text", "url", "wifi"]:
        with pytest.raises(SystemExit):
            cli.main((subcommand, ))
        assert subcommand in capsys.readouterr().err

    capsys.readouterr()
    # '--version' should be supported
    with pytest.raises(SystemExit):
        cli.main(("--version", ))
    output = capsys.readouterr()
    assert re.match(r"\d+\.\d+\.\d+", output.out) is not None
