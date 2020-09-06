# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2]
### Added
- Config file is now an optional parameter.
- Log level choice.

## [0.2.1]
Test release

## [0.2.0]
### Fixed
- Error when missing temperature range in config file.

### Added
- InfluxDB connector
- Tests

### Changed
- `adafruit` to `io_adafruit` in the config.

## [0.1.0] - 2020-08-11
### Added
- InfluxDB connector
- Temperature range validation, see `temperature_ranges` in `jocasta_config.ini`.

## [0.0.2] - 2020-08-09
### Fixed
- Handle no connectors config for missing `jocasta_config.ini` file.

## [0.0.1] - 2020-08-09
### Added
- Initial release
