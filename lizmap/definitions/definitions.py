"""Definitions used in Lizmap"""

__copyright__ = 'Copyright 2023, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

from enum import Enum, unique
from functools import total_ordering

from qgis.PyQt.QtCore import Qt


@unique
@total_ordering
class LwcVersions(Enum):
    Lizmap_3_1 = '3.1'
    Lizmap_3_2 = '3.2'
    Lizmap_3_3 = '3.3'
    Lizmap_3_4 = '3.4'
    Lizmap_3_5 = '3.5'
    Lizmap_3_6 = '3.6'
    Lizmap_3_7 = '3.7'

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


# Possible prefix before a stable release
# Note that 'pre' is not supported by the QGIS Desktop plugin manager
# Master and dev is for internal purpose only, name of the current branch. It's not supported as well by QGIS Desktop
UNSTABLE_VERSION_PREFIX = ('master', 'dev', 'pre', 'alpha', 'beta', 'rc')
DEV_VERSION_PREFIX = ('master', 'dev')


@unique
@total_ordering
class ReleaseStatus(Enum):
    Unknown = 'Unknown'
    NotMaintained = 'NotMaintained'
    Stable = 'Stable'
    ReleaseCandidate = 'ReleaseCandidate'
    Dev = 'Dev'

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


@unique
class LayerProperties(Enum):
    DataUrl = 'DataUrl'


DOMAIN = 'https://docs.lizmap.com'
VERSION = 'current'
DOC_URL = '{domain}/{version}/'.format(domain=DOMAIN, version=VERSION)
ONLINE_HELP_LANGUAGES = ('en', 'es', 'it', 'ja', 'pt', 'fi', 'fr')


@unique
class ServerComboData(Enum):
    """ The server combobox. """
    AuthId = Qt.UserRole  # String with the authentication ID
    ServerUrl = Qt.UserRole + 1  # String with the server URL
    JsonMetadata = Qt.UserRole + 2  # JSON from the server, raw


@unique
class LwcVersionComboData(Enum):
    """ The LWC version combo. """
    LwcVersion = Qt.UserRole  # Enum item with the LWC version
    LwcBranchStatus = Qt.UserRole + 1  # Enum item about the release status at that time.
