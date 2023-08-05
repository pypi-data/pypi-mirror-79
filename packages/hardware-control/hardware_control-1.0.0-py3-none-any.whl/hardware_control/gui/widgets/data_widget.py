import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
import pyqtgraph as pg  # For some reason, without this line QPushButton won't import
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QAbstractScrollArea,
)
from ..base import Instrument
from .utility import load_icon

logger = logging.getLogger(__name__)


class DataWidget(Instrument):
    def __init__(self, app, name: str = "Data Logger", add_lock_button=False):

        super().__init__(app, name)

        self.settings = {}
        self.ignore = True
        self.ignore_control = True
        self.prevent_overwrite_fields = False
        self.add_lock_button = add_lock_button

        self.allow_edit_data = False

        self.settings = self.default_state()

        # *************************Create GUI************************

        # self.arrow_symbol = QLabel()
        # self.arrow_symbol.setPixmap(load_icon("arrow.png"))
        # self.arrow_symbol.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # # ****** DEFINE TEXT BOXES
        # #

        self.data_select_frame = QWidget()
        self.data_select_layout = QGridLayout()

        self.dispgroup_label = QLabel("Dataset:")
        self.dispgroup_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.dispgroup_drop = QComboBox()
        self.dispgroup_drop.addItems(["----------"])
        self.dispgroup_drop.setCurrentText(self.settings["display_group"])

        self.new_group_button = QPushButton()
        self.new_group_button.setText("New Dataset")
        self.new_group_button.clicked.connect(self.create_new_group)

        self.sidebar_v_spacer = QSpacerItem(
            20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.save_all_button = QPushButton()
        self.save_all_button.setText("Save All Sets")
        self.save_all_button.clicked.connect(self.save_all_data)

        self.data_select_layout.addWidget(self.dispgroup_label, 0, 0)
        self.data_select_layout.addWidget(self.dispgroup_drop, 1, 0)
        self.data_select_layout.addWidget(self.new_group_button, 2, 0)
        self.data_select_layout.addItem(self.sidebar_v_spacer, 3, 0)
        self.data_select_layout.addWidget(self.save_all_button, 4, 0)
        self.data_select_frame.setLayout(self.data_select_layout)

        self.data_disp_frame = QGroupBox("Data")

        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.setRowCount(15)
        self.table.setColumnCount(4)
        self.table.cellChanged.connect(self.data_changed_from_cell)
        if add_lock_button:
            self.table.cellClicked.connect(self.pause_updates)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.autosave_label = QLabel()
        self.autosave_label.setPixmap(load_icon("autosave_label.png"))

        self.resume_updates_button = QPushButton()
        self.resume_updates_button.setText("Enable Editing")
        self.resume_updates_button.clicked.connect(self.pause_unpause_clicked)
        # self.resume_updates_button.setEnabled(False)

        self.save_button = QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save_data)

        self.clear_button = QPushButton()
        self.clear_button.setText("Erase Group Data")
        self.clear_button.clicked.connect(self.erase_group_data)

        self.autosave_check = QCheckBox("Autosave")
        # self.autosave_check.setChecked()
        self.autosave_check.stateChanged.connect(
            lambda: self.autosave_on_off(self.autosave_check.isChecked())
        )

        self.save_interval_label = QLabel("Save Interval Time (s):")
        self.save_interval_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        self.save_format_label = QLabel("Autosave Format:")
        self.save_format_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        self.save_format_drop = QComboBox()
        self.save_format_drop.addItems(["NPY", "CSV", "JSON", "TXT", "Pickle"])
        if self.app is not None:
            for data_format in self.app.additional_save_formats:
                self.save_format_drop.addItems([data_format])
        self.save_format_drop.setCurrentText("JSON")
        self.save_format_drop.currentIndexChanged.connect(
            lambda: self.set_autosave_format(self.save_format_drop.currentText())
        )

        self.save_interval_spacer = QSpacerItem(
            150, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.save_interval_edit = QLineEdit()
        self.save_interval_edit.setValidator(QDoubleValidator())
        self.save_interval_edit.editingFinished.connect(
            lambda: self.set_interval(self.save_interval_edit.text())
        )

        self.save_filename_label = QLabel("Autosave Filename:")
        self.save_filename_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        self.save_filename_edit = QLineEdit()
        self.save_filename_edit.editingFinished.connect(
            lambda: self.set_filename(self.save_filename_edit.text())
        )

        self.autosave_bottom_spacer = QSpacerItem(
            40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.autolog_label = QLabel()
        self.autolog_label.setPixmap(load_icon("async_label.png"))

        self.autolog_button = QPushButton("Change to Async")
        # self.save_button.setText("Save")
        self.autolog_button.clicked.connect(self.change_to_async)

        self.autolog_interval_label = QLabel("Log Interval Time (s):")
        self.autolog_interval_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        self.autolog_interval_spacer = QSpacerItem(
            150, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.autolog_interval_edit = QLineEdit()
        self.autolog_interval_edit.setValidator(QDoubleValidator())
        self.autolog_interval_edit.editingFinished.connect(
            lambda: self.set_autolog_interval(self.autolog_interval_edit.text())
        )

        self.autolog_bottom_spacer = QSpacerItem(
            40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.autolog_enabled_label = QLabel()
        self.autolog_enabled_label.setText("Asynchronous Mode: OFF")

        self.autolog_ind_label = QLabel()
        self.autolog_ind_label.setPixmap(load_icon("ind_darkgrey.png"))

        self.disp_frame_layout = QGridLayout()
        self.table_layout = QGridLayout()
        self.disp_buttons_layout = QGridLayout()
        self.table_layout.addWidget(self.table, 0, 0, 1, 4)

        if add_lock_button:
            self.disp_buttons_layout.addWidget(self.resume_updates_button, 1, 0)
        self.disp_buttons_layout.addWidget(self.save_button, 1, 1)
        self.disp_buttons_layout.addWidget(self.clear_button, 1, 3)

        self.disp_buttons_layout.addWidget(self.autosave_label, 2, 0, 1, 4)
        self.disp_buttons_layout.addWidget(self.autosave_check, 3, 0)
        self.disp_buttons_layout.addWidget(self.save_format_label, 4, 0)
        self.disp_buttons_layout.addWidget(self.save_format_drop, 4, 1)
        self.disp_buttons_layout.addItem(self.save_interval_spacer, 3, 1)
        self.disp_buttons_layout.addWidget(self.save_interval_label, 3, 2)
        self.disp_buttons_layout.addWidget(self.save_interval_edit, 3, 3)
        self.disp_buttons_layout.addWidget(self.save_filename_label, 4, 2)
        self.disp_buttons_layout.addWidget(self.save_filename_edit, 4, 3)
        self.disp_buttons_layout.addItem(self.autosave_bottom_spacer, 5, 0, 1, 4)

        self.disp_buttons_layout.addWidget(self.autolog_label, 6, 0, 1, 4)
        self.disp_buttons_layout.addWidget(self.autolog_button, 7, 0)
        self.disp_buttons_layout.addItem(self.autolog_interval_spacer, 7, 1)
        self.disp_buttons_layout.addWidget(self.autolog_interval_label, 7, 2)
        self.disp_buttons_layout.addWidget(self.autolog_interval_edit, 7, 3)
        self.disp_buttons_layout.addItem(self.autolog_bottom_spacer, 8, 0, 1, 4)
        self.disp_buttons_layout.addWidget(self.autolog_enabled_label, 9, 0)
        self.disp_buttons_layout.addWidget(self.autolog_ind_label, 9, 1)

        self.disp_frame_layout.addLayout(self.table_layout, 0, 0)
        self.disp_frame_layout.addLayout(self.disp_buttons_layout, 1, 0)
        self.data_disp_frame.setLayout(self.disp_frame_layout)

        self.update_groups()
        self.dispgroup_drop.currentIndexChanged.connect(
            lambda: self.set_group(self.dispgroup_drop.currentText())
        )

        # ******* DEFINE OVERALL LAYOUT
        #
        self.master_layout = QGridLayout()
        self.master_layout.addWidget(self.data_select_frame, 0, 0)
        # self.master_layout.addLayout(self.middle_grid, 1, 0, 1, 2)
        # self.master_layout.addLayout(self.progress_grid, 2, 0, 1, 3)
        self.master_layout.addWidget(self.data_disp_frame, 0, 1)
        self.setLayout(self.master_layout)

        self.update_table_timer = QTimer(self)
        self.update_table_timer.timeout.connect(self.update_table)
        self.update_table_timer.start(1000)

        # self.autosave_timer = QTimer(self)
        # self.autosave_timer.timeout.connect(self.exec_autosave)
        # try:
        #     self.autosave_timer.start(1e3*float(self.settings["save_interval"]))
        # except:
        #     self.autosave_timer.start(120*1e3)

    def set_filename(self, fn: str):
        try:
            self.app.data_sets[self.settings["display_group"]].autosave_filename = fn
        except:
            logger.error(f"Failed to set autosave filename to {fn}", exc_info=True)

    def set_autosave_format(self, fmt: str):
        try:
            self.app.data_sets[self.settings["display_group"]].autosave_format = fmt
        except:
            logger.error(f"Failed to set autosave format to {fmt}", exc_info=True)

    def change_to_async(self):
        # Don't allow async mode to be turned on if already on. Also, it can't
        # be switched off after it's turned on

        if self.app.data_sets[self.settings["display_group"]].asynchronous_mode:
            return

        try:
            self.app.data_sets[self.settings["display_group"]].start_asynch()
        except:
            logger.error("Failed to start aynchronous mode", exc_info=True)

        self.autolog_button.setEnabled(False)

    def set_autolog_interval(self, interval: str):
        try:
            self.app.data_sets[self.settings["display_group"]].set_async_interval(
                float(interval)
            )
        except:
            logger.error(f"Failed to set autosave format to {interval}", exc_info=True)

    def pause_unpause_clicked(self):
        if self.prevent_overwrite_fields:
            self.resume_updates()
        else:
            self.pause_updates()

    def pause_updates(self):
        self.resume_updates_button.setText(" Lock Editing ")
        self.prevent_overwrite_fields = True

    def resume_updates(self):
        self.resume_updates_button.setText("Enable Editing")
        self.prevent_overwrite_fields = False

    def create_new_group(self):
        self.app.main_window.create_new_group()

        self.update_groups()

    def autosave_on_off(self, state: bool):
        try:
            self.app.data_sets[self.settings["display_group"]].autosave = state
        except:
            logger.error("Failed to set autosave state", exc_info=True)

    def set_interval(self, t: str):
        """Sets the autosave interval"""

        try:
            self.app.data_sets[self.settings["display_group"]].set_save_interval(
                float(t)
            )
        except:
            logger.error("ERROR: Failed to set interval time", exc_info=True)

    def save_data(self):
        self.app.main_window.save_data(self.settings["display_group"])

    def save_all_data(self):
        self.app.main_window.app.save_all()

    def erase_group_data(self):
        ds_name = self.settings["display_group"]

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("You are about to delete data. Abort?")
        msg.setInformativeText(
            f"Continuing will permanently erase all data in Dataset '{ds_name}'"
        )
        msg.setWindowTitle("Data Erasure Warning")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Abort)
        buttonReply = msg.exec()

        # buttonReply = QMessageBox.warning(self, 'Data Erasure Warning', "You are about to delete unsaved data. Continue?", QMessageBox.Ignore | QMessageBox.Abort, QMessageBox.Abort)
        if buttonReply == QMessageBox.Abort:
            return

        try:
            self.app.data_sets[self.settings["display_group"]].clear()
        except:
            logger.error("Failed to delete group data", exc_info=True)

        self.update_table()

    def data_changed_from_cell(self, row: int, col: int):

        # self.resume_updates()

        pass

    def set_group(self, group):
        if group == "":
            return

        self.resume_updates()

        self.table.setRowCount(0)

        logger.debug(f"LoggerTool display group set to '{group}'")
        self.settings["display_group"] = group
        self.dispgroup_drop.setCurrentText(self.settings["display_group"])
        self.update_table()

        self.table.resizeColumnsToContents()

    def update_table(self):

        # Update which widgets are enabled
        try:
            group = self.app.data_sets[self.settings["display_group"]]

            self.clear_button.setEnabled(
                self.prevent_overwrite_fields or not self.add_lock_button
            )
            self.autosave_check.setEnabled(self.prevent_overwrite_fields)
            self.save_format_drop.setEnabled(self.prevent_overwrite_fields)
            self.save_interval_edit.setEnabled(self.prevent_overwrite_fields)
            self.save_filename_edit.setEnabled(self.prevent_overwrite_fields)
            self.autolog_interval_edit.setEnabled(self.prevent_overwrite_fields)
            # self.autolog_button.setEnabled(self.prevent_overwrite_fields);

            if group.asynchronous_mode or not self.prevent_overwrite_fields:
                self.autolog_button.setEnabled(False)
            else:
                self.autolog_button.setEnabled(True)
        except:
            logger.error("Exception occured while updating table", exc_info=True)

        if self.prevent_overwrite_fields:
            return

        # ********** Update values in table and control panel ****************

        # Get correct group
        group = self.app.data_sets[self.settings["display_group"]]
        # print("Displaying group: ", self.settings["display_group"])

        # Set correct number of columns
        self.table.setColumnCount(len(group.data))
        # print(f"\tCols: {len(group.data)}")

        # Set correct number of rows
        num_rows = group.len_max()
        self.table.setRowCount(num_rows)
        # print(f"\tRows: {num_rows}")
        # print(f"\tTitles:")

        # Title columns
        header_names = []
        for field in group.data:

            # print(f"\t\t{field}", end="")

            # Use custom name if available, otherwise use field name
            if field in group.channel_names:
                header_names.append(group.channel_names[field])
                p = group.channel_names[field]
                # print(f" ({p})")
            else:
                # print(f"")
                # Apply readable name for time column if not specified
                if field == "time:time":
                    header_names.append("Time")
                    continue

                header_names.append(field)

        self.table.setHorizontalHeaderLabels(header_names)

        # Write indeces along vertical
        indeces_str = [str(x) for x in list(range(num_rows))]
        # print(f"\tIndeces: {indeces_str}")

        self.table.setVerticalHeaderLabels(indeces_str)

        # Update data in table
        col = 0
        for field in group.data:

            # print(f"\tData for '{field}':")

            for ridx, val in enumerate(group.data[field]):

                # print(f"\t\t{val}", end="")

                temp_item = QTableWidgetItem()

                # If value can be converted to a string, do so
                if isinstance(val, float) or isinstance(val, int):
                    temp_item.setText(f"{val:g}")
                    # print(" NUM")
                elif isinstance(val, bool):
                    temp_item.setText(str(val))
                    # print(" BOOl")
                elif isinstance(val, str):
                    temp_item.setText(val)
                    # print(" STR")
                elif isinstance(val, list):
                    # print(" LIST")
                    if len(val) > 0:
                        temp_item.setText(f"[{type(val[0])}*{len(val)}]")
                    else:
                        temp_item.setText("List")
                elif isinstance(val, dict):
                    # print(" DICT")
                    temp_item.setText(f"Dict * {len(val)}")
                else:
                    # print(" ?")
                    temp_item.setText(f"Type={type(val)}")
                self.table.setItem(ridx, col, temp_item)

            col += 1

        # Set if autosave is on
        self.autosave_check.setChecked(group.autosave)

        # Set autosave format
        self.save_format_drop.setCurrentText(group.autosave_format)

        # Set autosave interval
        self.save_interval_edit.setText(str(group.autosave_interval))

        # Set autosave filename
        self.save_filename_edit.setText(str(group.autosave_filename))

        # Set if async is on
        # this will:
        #     1.) enable/disable convert to async button
        #     2.) set indicator to blue/grey and write ON/OFF next to it
        #     3.) enable/disable interval edit
        if group.asynchronous_mode:
            self.autolog_enabled_label.setText("Asynchronous Mode: ON ")
            self.autolog_ind_label.setPixmap(load_icon("ind_blue.png"))
        else:
            self.autolog_enabled_label.setText("Asynchronous Mode: OFF")
            self.autolog_ind_label.setPixmap(load_icon("ind_darkgrey.png"))

        # Set log interval time
        self.autolog_interval_edit.setText(str(group.async_log_interval))

    def update_groups(self):
        self.dispgroup_drop.clear()

        # Copy all goup names into dropdown
        names = list(self.app.data_sets.keys())
        self.dispgroup_drop.addItems(names)

        # Select one group and display it if none currently displayed
        if len(names) > 0 and self.settings["display_group"] == "":
            self.set_group(names[-1])

        # if self.settings['display_group'] == "" and len(self.app.data_sets) > 0:
        #     # print('sets:')
        #     print([*self.app.data_sets])
        #     self.set_group([*self.app.data_sets][-1])

    def default_state(self):
        return {"display_group": ""}

    def settings_to_UI(self):
        self.dispgroup_drop.setCurrentText(self.settings["display_group"])
        self.set_group(self.dispgroup_drop.currentText())
