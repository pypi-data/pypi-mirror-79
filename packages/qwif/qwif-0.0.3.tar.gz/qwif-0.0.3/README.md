qwif
=====

Generate QR codes for WIFI and more from the command line.

Requirements
------------

* python 3.8+

Installing
-----------

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```
pip install -U qwif
```

Alternatively, you can package and run `qwif` in a docker container:

```
make image
```

Usage
-----

`qwif` supports a number of QR code content types through subcommands.

To generate a QR code for WIFI configuration:

```
qwif wifi --ssid test --password test
```

To generate a QR code to configure e.g. Google Authenticator:

```
qwif otp --secret test --issuer "Big Corp"  --account_name test@test.local
```

A list of  subcommands can be printed by running `qwif --help`.

Each has its own help menu detailing the supported parameters for each QR code
type.

Authors
--------

* [iwaseatenbyagrue](https://gitlab.com/iwaseatenbyagrue)
