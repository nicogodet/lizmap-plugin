"""Definitions for atlas."""

from .base import BaseDefinitions, InputType
from ..qgis_plugin_tools.tools.i18n import tr

__copyright__ = 'Copyright 2020, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class AtlasDefinitions(BaseDefinitions):

    def __init__(self):
        super().__init__()
        self._use_single_row = True
        self._layer_config['layer'] = {
            'type': InputType.Layer,
            'header': tr('Layer'),
            'default': None,
            'tooltip': tr('The vector layer for the atlas.')
        }
        self._layer_config['primaryKey'] = {
            'type': InputType.Field,
            'header': tr('Primary key'),
            'default': None,
            'tooltip': tr('Layer primary key (must be integer for PostgreSQL).)')
        }
        self._layer_config['displayLayerDescription'] = {
            'type': InputType.CheckBox,
            'header': tr('Display layer description'),
            'default': True,
            'tooltip': tr('If you want to display the layer description in the dock of your atlas.')
        }
        self._layer_config['featureLabel'] = {
            'type': InputType.Field,
            'header': tr('Feature label'),
            'default': None,
            'tooltip': tr(
                'Choose the field who contains the name of your features, it will be shown instead '
                'of the primary key in the list of features.')
        }
        self._layer_config['sortField'] = {
            'type': InputType.Field,
            'header': tr('Sort field'),
            'default': None,
            'tooltip': tr('Your atlas will be sorted according to this field.')
        }
        self._layer_config['highlightGeometry'] = {
            'type': InputType.CheckBox,
            'header': tr('Highlight geometry'),
            'default': False,
            'tooltip': tr(
                'You can choose to highlight the feature selected by the atlas, '
                'it will change every time it’s switching to a new feature.')
        }
        self._layer_config['zoom'] = {
            'type': InputType.List,
            'header': tr('Zoom'),
            'default': None,
            'tooltip': tr('Choose between a zoom on the feature or to make it the center of your map.')
        }
        self._layer_config['displayPopup'] = {
            'type': InputType.CheckBox,
            'header': tr('Display popup'),
            'default': False,
            'tooltip': tr('You can choose to display the popup in the feature in the atlas container or not.')
        }
        self._layer_config['triggerFilter'] = {
            'type': InputType.CheckBox,
            'header': tr('Trigger filter'),
            'default': False,
            'tooltip': tr(
                'If you want to activate filter on the feature selected by the atlas, '
                'it will hide all other features of the layer and only show the one selected.')
        }
        self._layer_config['duration'] = {
            'type': InputType.SpinBox,
            'header': tr('Duration'),
            'default': 5,
            'tooltip': tr('You can select the duration between each step when your atlas is in auto-play mode.')
        }

        self._general_config['showAtStartup'] = {
            'type': InputType.CheckBox,
            'default': False,
        }

        self._general_config['autoPlay'] = {
            'type': InputType.CheckBox,
            'default': False,
        }

    def key(self) -> str:
        return 'atlas'
