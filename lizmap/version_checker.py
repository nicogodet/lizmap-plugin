__copyright__ = 'Copyright 2020, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

import json
import logging

from qgis.core import QgsNetworkContentFetcher
from qgis.PyQt.QtCore import QDate, QLocale, QUrl
from qgis.PyQt.QtWidgets import QDialog

from lizmap.definitions.definitions import (
    LwcVersionComboData,
    LwcVersions,
    ReleaseStatus,
)
from lizmap.qgis_plugin_tools.tools.i18n import tr
from lizmap.tools import lizmap_user_folder

LOGGER = logging.getLogger('Lizmap')


class VersionChecker:

    def __init__(self, dialog: QDialog, url):
        """ Update the dialog when versions have been fetched. """
        self.dialog = dialog
        self.url = url
        self.fetcher = None
        self.json = None

    def fetch(self):
        """ Fetch the JSON file and call the function when it's finished. """
        self.fetcher = QgsNetworkContentFetcher()
        self.fetcher.finished.connect(self.request_finished)
        self.fetcher.fetchContent(QUrl(self.url))

    def request_finished(self):
        """ Dispatch the answer to update the GUI. """
        content = self.fetcher.contentAsString()
        if not content:
            return

        # Update the UI
        released_versions = json.loads(content)
        self.update_lwc_releases(released_versions)
        self.update_lwc_selector(released_versions)

        # Cache the file
        content += '\n'
        with open(lizmap_user_folder().joinpath("released_versions.json"), "w") as output:
            output.write(content)

    def update_lwc_selector(self, released_versions: dict):
        """ Update LWC selector showing outdated versions. """
        # TODO remove this variable as well soon
        first_stable_release = False
        for i, json_version in enumerate(released_versions):
            try:
                lwc_version = LwcVersions(json_version['branch'])
            except ValueError:
                # The version is found in the online JSON file
                # But not in the Lizmap source code, in the "definitions.py" file
                # We can continue, we do nothing with this version. It's not displayed in the UI.
                continue

            index = self.dialog.combo_lwc_version.findData(lwc_version, LwcVersionComboData.LwcVersion.value)
            status = json_version.get('status')
            if status:
                if status == 'dev':
                    flag = ReleaseStatus.Dev
                    suffix = tr('Next')
                elif status == 'feature_freeze':
                    flag = ReleaseStatus.ReleaseCandidate
                    suffix = tr('Feature freeze')
                elif status == 'stable':
                    flag = ReleaseStatus.Stable
                    suffix = tr('Stable')
                elif status == 'retired':
                    flag = ReleaseStatus.NotMaintained
                    suffix = tr('Not maintained')
                else:
                    flag = ReleaseStatus.Unknown
                    suffix = tr('Inconnu')

                text = self.dialog.combo_lwc_version.itemText(index)
                if suffix:
                    text += ' - ' + suffix
                    self.dialog.combo_lwc_version.setItemText(index, text)
                self.dialog.combo_lwc_version.setItemData(index, flag, LwcVersionComboData.LwcBranchStatus.value)

            else:
                # Legacy
                # TODO remove in a few weeks
                # ET 1/12/2022
                if not json_version['maintained']:
                    if not index and json_version['branch'] != LwcVersions.Lizmap_3_1.value:
                        LOGGER.warning(
                            "We did not find the version {} in the selector version".format(
                                json_version['branch'])
                        )
                        continue
                    text = self.dialog.combo_lwc_version.itemText(index)

                    if not first_stable_release:
                        # All dev version are for now tagged "not maintained" in the JSON file
                        new_text = text + ' - ' + tr('Next')
                        flag = ReleaseStatus.Dev
                    else:
                        new_text = text + ' - ' + tr('Not maintained')
                        flag = ReleaseStatus.NotMaintained
                    self.dialog.combo_lwc_version.setItemText(index, new_text)
                else:
                    first_stable_release = True
                    flag = ReleaseStatus.Stable
                self.dialog.combo_lwc_version.setItemData(index, flag, LwcVersionComboData.LwcBranchStatus.value)
                # End of legacy

    def update_lwc_releases(self, released_versions: dict):
        """ Update labels about latest releases. """
        template = (
            '<a href="https://github.com/3liz/lizmap-web-client/releases/tag/{tag}">'
            '{tag}   -    {date}'
            '</a>')

        i = 0
        for json_version in released_versions:
            qdate = QDate.fromString(
                json_version['latest_release_date'],
                "yyyy-MM-dd")
            date_string = qdate.toString(QLocale().dateFormat(QLocale.ShortFormat))
            if json_version['maintained']:
                if i == 0:
                    text = template.format(
                        tag=json_version['latest_release_version'],
                        date=date_string,
                    )
                    self.dialog.lwc_version_latest.setText(text)
                elif i == 1:
                    text = template.format(
                        tag=json_version['latest_release_version'],
                        date=date_string,
                    )
                    self.dialog.lwc_version_oldest.setText(text)
                i += 1
