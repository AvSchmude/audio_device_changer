import pyaudio
# import traceback
# from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QListView,
                             QAbstractItemView, QVBoxLayout, QWidget,
                             QPlainTextEdit, QApplication, QHBoxLayout,
                             QGridLayout, QLabel)
from PyQt6.QtCore import QProcess, QStringListModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Device Changer")

        # Define layouts
        page_layout = QVBoxLayout()
        list_layout = QHBoxLayout()
        input_list_layout = QVBoxLayout()
        output_list_layout = QVBoxLayout()
        btn_layout = QGridLayout()

        # QProcess variables
        self.process = None
        self.pt = None

        # Current default devices
        self.input_device, self.output_device = self.get_default_devices()
        # List of active devices
        self.input_device_list, self.output_device_list = self.get_device_list()

        status_label = QLabel("Current default device")
        status_label.setStyleSheet("background-color: transparent; border: none;")

        self.status_box = QPlainTextEdit()
        self.status_box.setReadOnly(True)

        self.output_model = QStringListModel()
        self.output_model.setStringList(self.output_device_list)

        output_label = QLabel("Output")
        output_label.setStyleSheet("background-color: transparent; border: none;")

        self.output_view = QListView()
        self.output_view.setModel(self.output_model)
        self.output_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.output_view.clicked.connect(self.select_output_item)

        self.input_model = QStringListModel()
        self.input_model.setStringList(self.input_device_list)

        input_label = QLabel("Input")
        input_label.setStyleSheet("background-color: transparent; border: none;")

        self.input_view = QListView()
        self.input_view.setModel(self.input_model)
        self.input_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.input_view.clicked.connect(self.select_input_item)

        size = self.get_list_size()
        self.input_view.setMaximumSize(size)
        self.output_view.setMaximumSize(size)

        pr_btn = QPushButton("Print")
        pr_btn.setCheckable(False)
        pr_btn.clicked.connect(self.print_default_device)

        change_btn = QPushButton("Change default")
        change_btn.setCheckable(False)
        change_btn.clicked.connect(lambda: self.change_devices(self.input_device, self.output_device))

        sounds_btn = QPushButton("Open Sounds")
        sounds_btn.setCheckable(False)
        sounds_btn.clicked.connect(self.open_sounds)
        """
        exit_btn = QPushButton("Exit")
        exit_btn.setCheckable(False)
        exit_btn.clicked.connect(app.exit)
        """
        clear_btn = QPushButton("Clear")
        clear_btn.setCheckable(False)
        clear_btn.clicked.connect(self.clear_box)

        self.display = QPlainTextEdit()
        self.display.setFixedHeight(27)
        self.display.setReadOnly(True)
        self.display.setPlainText(f'{self.input_device}, {self.output_device}')

        page_layout.addWidget(status_label)
        page_layout.addWidget(self.display)
        page_layout.addLayout(list_layout)
        page_layout.addLayout(btn_layout)
        page_layout.addWidget(self.status_box)

        input_list_layout.addWidget(input_label)
        input_list_layout.addWidget(self.input_view)

        output_list_layout.addWidget(output_label)
        output_list_layout.addWidget(self.output_view)

        list_layout.addLayout(input_list_layout)
        list_layout.addLayout(output_list_layout)
        list_layout.setSpacing(0)  # remove the space between the lists

        btn_layout.addWidget(change_btn, 0, 0)
        btn_layout.addWidget(clear_btn, 0, 1)
        btn_layout.addWidget(sounds_btn, 1, 0)
        btn_layout.addWidget(pr_btn, 1, 1)

        container = QWidget()
        container.setLayout(page_layout)

        self.setMaximumWidth(300)
        # app.font().family()
        # self.setFont(QFont(app.font().family(), 9))
        # Set the central widget of the window
        self.setCentralWidget(container)

    def select_output_item(self, index):
        """"""
        self.output_view.setSelectionRectVisible(True)
        item = self.output_model.data(index)
        self.output_device = item

    def select_input_item(self, index):
        """"""
        self.input_view.setSelectionRectVisible(True)
        item = self.input_model.data(index)
        self.input_device = item

    @staticmethod
    def get_default_devices():
        """ Returns the current default audio I/O devices."""
        p = pyaudio.PyAudio()
        i = p.get_default_input_device_info()['name'].split('(')[0].strip()
        # '\"' + p.get_default_input_device_info()['name'].split('(')[0].strip() + '\"'
        o = p.get_default_output_device_info()['name'].split('(')[0].strip()
        # '\"' + p.get_default_output_device_info()['name'].split('(')[0].strip() + '\"'
        p.terminate()
        return i, o

    @staticmethod
    def get_device_list():
        """Return the two separate lists containing the names of in- and output audio devices."""
        p = pyaudio.PyAudio()
        input_list = []
        output_list = []
        for i in range(p.get_device_count()):
            elem = p.get_device_info_by_index(i)
            # device_name = '\"' + elem['name'].split('(')[0].strip() + '\"'
            name = elem['name']
            if name.count('(') > 1:
                index2 = name.find('(', name.find('(') + 1)
                device_name = name[:index2].strip()
            else:
                device_name = name.split('(')[0].strip()

            if "Microsoft Sound Mapper" in elem['name']:
                continue
            elif elem['hostApi'] == 0 and elem['maxInputChannels'] > 0:
                input_list.append(device_name)
            elif elem['hostApi'] == 0 and elem['maxOutputChannels'] > 0:
                output_list.append(device_name)
        p.terminate()
        input_list.sort()
        output_list.sort()
        return input_list, output_list

    def get_list_size(self):
        i = self.input_model.rowCount() + 1
        o = self.output_model.rowCount() + 1
        if i > o:
            size_i = self.input_view.sizeHint()
            size_i.setHeight(self.input_view.sizeHintForRow(0) * i)
            # size_i.setWidth(100)
            return size_i
        else:
            size_o = self.output_view.sizeHint()
            # size_o.setWidth(100)
            size_o.setHeight(self.output_view.sizeHintForRow(0) * o)
            return size_o

    def print_default_device(self):
        """ Prints the current default audio I/0 devices to the terminal and message field."""
        p = pyaudio.PyAudio()
        i = '\"' + p.get_default_input_device_info()['name'].split('(')[0].strip() + '\"'
        o = '\"' + p.get_default_output_device_info()['name'].split('(')[0].strip() + '\"'
        # print("Default audio I/O devices:", i, o)
        self.status_box.appendPlainText(f'Default audio devices:\n{i}, {o}')
        p.terminate()

    def update_default_device(self):
        """ Updates the text field displaying the current default devices."""
        self.status_box.appendPlainText("Refresh requested.")
        i, o = self.get_default_devices()
        self.display.setPlainText(f'{i}, {o}')

    def change_devices(self, out_dev: str, in_dev: str):
        """Calls the batch file which changes both default audio devices (input and output)."""
        # find full path of the batch file
        # path = os.path.dirname(os.path.abspath(__file__)) + '\\change_devices.bat'
        path = '.\\change_devices.bat'
        self.status_box.appendPlainText('Executing process.')
        self.process = QProcess()
        self.process.setProgram('cmd')
        self.process.setArguments(['/C', path, out_dev, in_dev])
        self.process.start()
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.process_error)

    def clear_box(self):
        self.status_box.setPlainText("")

    def open_sounds(self):
        """"""
        self.status_box.appendPlainText('Opening Sounds')
        self.pt = QProcess()
        self.pt.startDetached('cmd', ['/C', 'rundll32.exe', 'Shell32.dll,Control_RunDLL', 'Mmsys.cpl,,0'])
        self.pt.finished.connect(self.sound_process_finished)
        self.pt.errorOccurred.connect(self.process_error)

    """
    def test_batch_input(self, out_dev: str, in_dev: str):
        try:
            test = ".\\test.bat"
            self.status_box.appendPlainText('Testing input')
            self.pt = QProcess()
            self.pt.start('cmd', ['/C', test, out_dev, in_dev])
        except Exception:
            print(traceback.format_exc())
    """

    def process_finished(self):
        """"""
        # print("Process finished with exit code", exit_code, "and exit status: ", exit_status)
        self.update_default_device()
        self.status_box.appendPlainText('Process finished.')
        self.process = None

    def process_error(self):
        # print("An error occurred: ", error)
        self.status_box.appendPlainText('Error occurred.')
        self.process = None

    def sound_process_finished(self):
        self.status_box.appendPlainText('Sound opened')
        self.pt = None


if __name__ == "__main__":
    application = QApplication([])
    application.setStyle('Fusion')
    window = MainWindow()
    window.show()
    application.exec()
