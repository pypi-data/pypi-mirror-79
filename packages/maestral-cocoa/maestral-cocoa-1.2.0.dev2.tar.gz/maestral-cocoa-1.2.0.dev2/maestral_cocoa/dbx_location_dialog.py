# -*- coding: utf-8 -*-

# system imports
import os.path as osp

# external imports
import toga
from toga.style.pack import Pack, FONT_SIZE_CHOICES
from maestral.utils.appdirs import get_home_dir
from maestral.utils.path import delete

# local imports
from .private.widgets import Icon, Selection
from .dialogs import Dialog


# set default font size to 13 pt, as in macOS
Pack.validated_property('font_size', choices=FONT_SIZE_CHOICES, initial=13)


class DbxLocationDialog(Dialog):

    WINDOW_WIDTH = 600
    CONTENT_WIDTH = (WINDOW_WIDTH - Dialog.PADDING_LEFT - Dialog.PADDING_RIGHT
                     - Dialog.ICON_PADDING_RIGHT - Dialog.ICON_SIZE[0])

    COMBOBOX_CHOOSE = 'Choose...'

    dbx_location_user_selected = 'DBX LOCATION'

    ACCEPTED = 0
    REJECTED = 1

    def __init__(self, app):

        self.mdbx = app.mdbx
        self.config_name = self.mdbx.config_name
        self.exit_status = self.REJECTED

        old_path = self.mdbx.get_conf('main', 'path')

        message = (
            'Your Dropbox folder has been moved or deleted from its original location. '
            'Maestral will not work properly until you move it back. It used to be '
            'located at:\n\n{0}\n\nTo move it back, click "Quit" below, move the '
            'Dropbox folder back to its original location, and launch Maestral again. '
            'To re-download your Dropbox, please select a location for your Dropbox '
            'folder below. Maestral will create a new folder named "{1}" in the '
            'selected location.\n\nTo unlink your Dropbox account from Maestral, '
            'click "Unlink" below.'
        ).format(old_path, self.mdbx.get_conf('main', 'default_dir_name'))

        self.combobox_dbx_location = Selection(
            items=[
                self.dbx_location_user_selected,
                toga.SECTION_BREAK,
                self.COMBOBOX_CHOOSE
            ],
            style=Pack(width=self.CONTENT_WIDTH, padding=(10, 0, 30, 0)),
            on_select=self._on_button_location_pressed
        )

        self._update_comboxbox_location(osp.dirname(old_path))

        # noinspection PyTypeChecker
        super().__init__(title='Cannot find Dropbox folder', message=message,
                         button_labels=('Select', 'Quit', 'Unlink'), default='Select',
                         accessory_view=self.combobox_dbx_location,
                         callback=self.on_dialog_pressed, app=app)

        self.msg_content.style.font_size = 12
        self.msg_content.style.width = 450
        self.msg_content.style.height = 170

    def on_dialog_pressed(self, btn_name):

        self.dialog_buttons.enabled = False

        if btn_name == 'Quit':
            self.exit_status = self.REJECTED
            self.close()

        elif btn_name == 'Unlink':
            self.spinner.start()
            self.mdbx.unlink()
            self.exit_status = self.REJECTED
            self.close()

        elif btn_name == 'Select':
            # apply dropbox path
            chosen_dropbox_folder = osp.join(
                self.dbx_location_user_selected,
                self.mdbx.get_conf('main', 'default_dir_name')
            )

            if osp.exists(chosen_dropbox_folder):

                if osp.isdir(chosen_dropbox_folder):
                    choice = self.alert_sheet(
                        title='Folder already exists',
                        message=(f'The folder "{chosen_dropbox_folder}" already '
                                 'exists. Would you like to replace it or merge its '
                                 'contents with Dropbox?'),
                        button_labels=('Replace', 'Cancel', 'Merge'),
                    )

                else:
                    choice = self.alert_sheet(
                        title='File conflict',
                        message=(
                            'There already is a file named "{}" at this location. Would '
                            'you like to replace it?'.format(
                                self.mdbx.get_conf('main', 'default_dir_name')
                            )
                        ),
                        button_labels=('Replace', 'Cancel'),
                    )

                if choice == 0:  # replace
                    delete(chosen_dropbox_folder)
                elif choice == 1:  # cancel
                    self.dialog_buttons.enabled = True
                    return
                elif choice == 2:  # merge
                    pass

            self.mdbx.create_dropbox_directory(chosen_dropbox_folder)
            self.mdbx.rebuild_index()
            self.exit_status = self.ACCEPTED
            self.close()

    async def _on_button_location_pressed(self, widget):

        if widget.value == self.COMBOBOX_CHOOSE:
            paths = await self.select_folder_sheet()

            if len(paths) > 0:
                path = paths[0]
                self._update_comboxbox_location(path)
            else:
                self.combobox_dbx_location.value = self.combobox_dbx_location.items[0]

    def _update_comboxbox_location(self, path):
        self.dbx_location_user_selected = path
        icon = Icon(for_path=path)
        short_path = self._relpath(path)
        self.combobox_dbx_location.items = [
            (icon, short_path),
            toga.SECTION_BREAK,
            self.COMBOBOX_CHOOSE
        ]

    @staticmethod
    def _relpath(path):
        usr = osp.abspath(osp.join(get_home_dir(), osp.pardir))
        if osp.commonprefix([path, usr]) == usr:
            return osp.relpath(path, usr)
        else:
            return path
