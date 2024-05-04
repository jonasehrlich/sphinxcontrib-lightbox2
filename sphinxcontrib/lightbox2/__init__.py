import importlib.metadata

try:
    # Poetry requires the version to be defined in pyproject.toml, load the version from the metadata,
    # this is the recommended approach https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    # No metadata is available, this could be because the tool is running from source
    __version__ = "unknown"
