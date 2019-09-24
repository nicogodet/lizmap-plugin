[![logo](icons/icon.png "3Liz")][3liz]Lizmap 3.1.0
==============================================

**WARNING** the master branch is compatible only with QGIS 3.x from August 23rd 2018. The branch *qgis2* targets QGIS 2.x compatibiliy.

Publication plugin for Lizmap Web Application, by 3LIZ.

    begin       : 2011-11-01
    copyright   : (C) 2011 by 3liz
    authors     : René-Luc D'Hont and Michaël Douchin
    email       : info@3liz.com
    website     : http://www.3liz.com

Lizmap QGIS plugin aims to be used to configure a web application dynamically generated by Lizmap (php/html/css/js) with the help of QGIS Server ( [QGIS Server Tutorial] ).
With this plugin, you can configure one web map per QGIS project. The Lizmap web application must be installed on the server.

The Original Code is 3liz code.

You can find help and news by subscribing to the mailing list: https://lists.osgeo.org/mailman/listinfo/lizmap.

Authors
-------

The Initial Developer of the Original Code are René-Luc D'Hont <rldhont@3liz.com> and Michael Douchin <mdouchin@3liz.com>.
Portions created by the Initial Developer are Copyright (C) 2011 the Initial Developer.
All Rights Reserved.

Contributors
--------------

* Salvatore Larosa  @slarosa
* Paolo Cavallini @pcav
* Arnaud Deleurme
* @ewsterrenburg
* Sławomir Bienias @SaekBinko
* Petr Tsymbarovich @mentaljam
* Víctor Herreros @vherreros
* João Gaspar
* Felix Kuehne
* Kari Salovaara
* Xan Vieiro
* Etienne Trimaille @Gustry
* José Macau

*Please propose a PR to add yourself if you are missing*

Installation
-----------

From GitHub repository:

1. Clone the repo: `git clone --recursive git@github.com:3liz/lizmap-plugin.git Lizmap`
2. `mv Lizmap ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`

or from QGIS application:

1. Plugins menu -> Manage and Install Plugins...
2. Select LizMap plugin from Not installed list
3. Install plugin

Documentation
--------------

[French doc]: http://docs.3liz.com/
[English doc translated via Google Translate]: http://translate.google.fr/translate?sl=fr&tl=en&js=n&prev=_t&hl=fr&ie=UTF-8&eotf=1&u=http%3A%2F%2Fdocs.3liz.Com

Translation
-----------

You can use the Makefile to update and compile the strings for translation.
These files are stored in a Git submodule https://github.com/3liz/lizmap-locales

```bash
# Prepare TS files
make i18n_1_prepare

# Push to Transifex
make i18n_2_push

# Pull from Transifex
make i18n_3_pull

# Compile TS fiels to QM files.
make i18n_4_compile
```

License
-------
Version: MPL 2.0/GPL 2.0/LGPL 2.1

The contents of this file are subject to the Mozilla Public License Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.mozilla.org/MPL/

Alternatively, the contents of this file may be used under the terms of either of the GNU General Public License Version 2 or later (the "GPL"), or the GNU Lesser General Public License Version 2.1 or later (the "LGPL"), in which case the provisions of the GPL or the LGPL are applicable instead of those above. If you wish to allow use of your version of this file only under the terms of either the GPL or the LGPL, and not to allow others to use your version of this file under the terms of the MPL, indicate your decision by deleting the provisions above and replace them with the notice and other provisions required by the GPL or the LGPL. If you do not delete the provisions above, a recipient may use your version of this file under the terms of any one of the MPL, the GPL or the LGPL.

Software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the specific language governing rights and limitations under the License.


  [QGIS Server Tutorial]: http://www.qgis.org/wiki/QGIS_Server_Tutorial
  [3liz]:http://www.3liz.com

API
----

You can use the `lizmap_api` class of `lizmap.py` to get the Lizmap JSON configuration for a specific project.

For example:

```python3
import sys,os
qgisPrefixPath = "/usr/local/"
sys.path.append(os.path.join(qgisPrefixPath, "share/qgis/python/"))
sys.path.append(os.path.join(qgisPrefixPath, "share/qgis/python/plugins/"))
os.environ["QGIS_DEBUG"] = '-1'
os.environ['QGIS_PREFIX_PATH'] = qgisPrefixPath

from qgis.core import QgsApplication
QgsApplication.setPrefixPath(qgisPrefixPath, True)
app = QgsApplication([], False)
app.initQgis()

# Run the lizmap config exporter
from lizmap import lizmap
project_path = '/home/mdouchin/test_a_sup.qgs'
lv = lizmap.LizmapConfig(project_path)
if lv:
    # get the JSON content with default values
    json_content = lv.to_json()

    # OR:

    # get the JSON content with user defined values
    my_global_options = {
        'mapScales': [1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000], # set the map scales
        'osmMapnik': True, # add the OSM mapnik baselayer
        'osmStamenToner': True, # add the OSM Stamen Toner baselayer
        'print': True # activate the print tool
    }
    my_layer_options = {
        'MY LAYER NAME': {
            'title': 'My new title', # change title
            'popup': True, # active popup
            'cached': True, # activate server cache
            'singleTile': False, # set tiled mode on
            'imageFormat': "image/jpeg", # set image format
            'toggled': False # do not display the layer at project startup
        }
    }
    json_content = lv.to_json(
        p_global_options=my_global_options,
        p_layer_options=my_layer_options
    )
    print(json_content)

    # get the configuration as dictionary
    dic_content = lv.lizmap_json_config

# Exit
QgsApplication.exitQgis()
app.exit()
```
