from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

from . import icons  # noqa install ('icons.fbp', *) icons
from .button_home import ButtonHomeRoot  # noqa
