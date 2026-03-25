<!-- markdownlint-disable MD024 -->

# Changelog

## v0.6.0 (2026-03-25)

* Fix an issue where the assets were copied into the first `html_static_path[0]`. This is problematic because the static path can be modified by other extensions. ([#2](https://github.com/jonasehrlich/sphinxcontrib-lightbox2/pull/2))

## v0.5.0 (2025-10-15)

* Switch dependency management to uv

## v0.4.0 (2024-09-19)

* Add support for Sphinx > 8

## v0.3.0 (2024-05-05)

## Added

* Support for mermaid diagrams with the `sphinxcontrib.mermaid` extension

## v0.2.0 (2024-05-04)

### Added

* Support for lightbox2 configuration options through *conf.py*

## v0.1.1 (2024-05-04)

### Added

* Added CI pipelines for test and PyPI releases
* Published documentation on <https://sphinxcontrib-lightbox2.readthedocs.io>

## v0.1.0 (2024-05-04)

Initial release
