Changelog
==========

This file documents notable changes to `qwif`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[0.0.5] - 2020-09-13
---------------------

Fix formatting/style issues, fix `make image`.

### Added

* partial test coverage for CLI
* improved test coverage for contents module

### Changed

* fixed flake8/pep8 issues
* `make image` now completes (was previously failing due to flake8).


[0.0.4] - 2020-09-12
---------------------

Fractionally clearer CLI, changelog.

### Added

* This changelog.

### Changed

* CLI subcommands help menus have a group header of 'fields' to help distinguish
  content field arguments from common arguments.


[0.0.3] - 2020-09-12
---------------------

Support for otpauth QR codes, readable by Google Authenticator.

### Added

* Support for optauth strings, to generate QR codes to OTP authenticators.
* Usage information in README for generating a QR code for OTP.


[0.0.2] - 2020-09-12
---------------------

Documentation fixes.

### Added

* Usage information in README, including generating a QR code for wifi.

[0.0.1] - 2020-09-12
---------------------

Initial release of `qwif`.

### Added

* generate QR codes for WIFI configuration, URL/bookmark, contact cards,
  calendar events, location, email and raw text.
* support `--output`, printing a scannable QR code to any TTY, or a SVG
  otherwise.
