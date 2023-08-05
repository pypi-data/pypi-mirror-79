from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
from .core import GCSFileSystem
from .mapping import GCSMap

__all__ = ["GCSFileSystem", "GCSMap"]
