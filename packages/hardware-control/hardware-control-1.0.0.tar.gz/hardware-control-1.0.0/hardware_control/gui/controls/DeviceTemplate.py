import logging

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit, QLabel, QGridLayout, QDoubleSpinBox

from ..base import Instrument, Comm

logger = logging.getLogger(__name__)


class DeviceType(Instrument):
    """An example for new GUI element that controls a backend.

    This code can be used as a template to write a new GUI element.
    """

    def __init__(
        self,
        app,
        backend,
        channels: list,
        name: str = "TemplateDevice",
        initialize_with: str = "INSTRUMENT",
        lock_until_sync=False,
    ):
        # initalizing
        super().__init__(app, name, backend, lock_until_sync)

        # Create UI - example
        self.lineEdit = QLineEdit()
        self.lineEdit.setText("10")
        self.lineEdit.editingFinished.connect(
            lambda: self.command(self.lineEdit.text())
        )

        self.text = QLabel()
        self.text.setText("123")

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(0, 10)
        self.spinbox.setSingleStep(0.15)
        self.spinbox.editingFinished.connect(
            lambda: self.update_setting("VOLT_CHANNEL1", str(self.spinbox.value()))
        )

        self.layout = QGridLayout()
        self.layout.addWidget(self.lineEdit, 0, 0)
        self.layout.addWidget(self.text, 0, 1)
        self.layout.addWidget(self.spinbox, 1, 0)
        self.setLayout(self.layout)

        # add your specific settings
        self.settings["VOLT_CHANNEL1"] = 123
        self.settings["VOLT_CHANNEL2"] = 456

        # Create timer to query
        self.readout_timer = QTimer(self)
        self.readout_timer.timeout.connect(self.update_readout)
        self.readout_timer.start(self.globalRefreshRate)

        # Write state to Backend this sends all settings, which are
        # stored in the settings dictionary to the backend
        self.send_state()

    # Updates the readout
    def update_readout(self):
        self.command("RND")  # Sends readout command (for example)
        # recived messige will be stored, once available this will
        # read it out, that way the UI wont freeze
        mess = self.read_values("RND")
        if mess:
            self.text.setText(mess)

    def settings_to_UI(self):
        """ Add code to this function to make the widgets in the GUI update
        to reflect the state of the 'self.settings' dictionary. """

        pass
