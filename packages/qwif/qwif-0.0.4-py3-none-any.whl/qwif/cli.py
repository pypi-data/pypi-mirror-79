import argparse
import dataclasses
import qrcode
import qrcode.image.svg
import qwif.contents as codes

from pkg_resources import get_distribution
from sys import stderr, exit


def populate_dataclass_parser(
    parser: argparse.ArgumentParser,
    group_name: str = "fields"
):
    """ Populate an argparse.ArgumentParser from a dataclass.

    This expects an argparse.ArgumentParser (typically created with add_parser),
    with a default set for 'klass' that is a dataclass.

    Fields from this dataclass are then added as arguments to the parser.
    """

    group = parser.add_argument_group(group_name)

    for field in dataclasses.fields(parser.get_default('klass')):
        default = field.default
        required = False
        action = "store"
        help = f"Set {field.name.replace('_', ' ')} (default: %(default)s)"

        if isinstance(field.default, dataclasses._MISSING_TYPE):
            default = ""
            required = True
            help = f"Set {field.name.replace('_', ' ')} (required)"

        if field.default is True:
            action = "store_false"

        if field.default is False:
            action = "store_true"

        group.add_argument(
            f"--{field.name.replace('_', '-')}",
            help=help,
            default=default,
            required=required,
            action=action
        )

    return parser


def cli():
    """ Get an argparse.ArgumentParser implementing a CLI for qwif.
    """
    parser = argparse.ArgumentParser(
        description="Generate QR code for WIFI and more.",
    )

    parser.add_argument(
        "--version", action='version', version=get_distribution('qwif').version
    )

    # Common is a parent parser for all subparsers that provides common CLI
    # switches/options.

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-o", "--output",
        type=argparse.FileType('wb'),
        default="-",
        help="Output file (default: stdout)"
    )

    sub = parser.add_subparsers()

    contact = sub.add_parser(
        'contact',
        help="Encode contact details",
        parents=[common],
        aliases=["c"],
        allow_abbrev=True
    )
    contact.set_defaults(klass=codes.Mecard)
    populate_dataclass_parser(contact)

    event = sub.add_parser(
        'event',
        help="Encode event",
        parents=[common],
        aliases=["e"],
    )

    event.set_defaults(klass=codes.Event)
    populate_dataclass_parser(event)

    geo = sub.add_parser(
        'geo',
        help="Encode geographic location",
        parents=[common],
        aliases=["g"],
    )
    geo.set_defaults(klass=codes.Geo)
    populate_dataclass_parser(geo)

    mail = sub.add_parser(
        'mail',
        help="Encode an email address",
        parents=[common],
        aliases=["m", "email"],
    )
    mail.set_defaults(klass=codes.Email)
    populate_dataclass_parser(mail)

    otp = sub.add_parser(
        'otp',
        help="Encode (T|H)OTP keys",
        parents=[common],
        aliases=["o"],
    )
    otp.set_defaults(klass=codes.OTP)
    populate_dataclass_parser(otp)

    text = sub.add_parser(
        'text',
        help="Encode arbitrary text",
        parents=[common],
        aliases=["t"],
    )
    text.set_defaults(klass=codes.Text)
    populate_dataclass_parser(text)

    url = sub.add_parser(
        'url',
        help="Encode a URL",
        parents=[common],
        aliases=["u"],
    )
    url.set_defaults(klass=codes.Url)
    populate_dataclass_parser(url)

    wifi = sub.add_parser(
        'wifi',
        help="Encode WIFI configuration",
        parents=[common],
        aliases=["w"],
    )
    wifi.set_defaults(klass=codes.Wifi)
    populate_dataclass_parser(wifi)

    return parser


def main():
    parser = cli()
    args = vars(parser.parse_args())

    if not args:
        parser.print_help()
        exit(1)

    output = args.pop('output')

    try:
        code = args.pop('klass')(**args)
        code.validate()
    except ValueError as e:
        print(f"ERROR: {e}", file=stderr)
        exit(1)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )

    qr.add_data(code)

    if output.isatty():
        qr.print_tty(out=output)
    else:
        qr.image_factory = qrcode.image.svg.SvgPathImage
        qr.make_image().save(
            output.buffer if hasattr(output, 'buffer') else output
        )
