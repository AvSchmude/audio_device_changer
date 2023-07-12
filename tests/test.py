import unittest
from audio_device_changer import MainWindow as mw
from PyQt6.QtWidgets import QApplication


class TestWindow(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        app = QApplication([])
        self.window = mw.MainWindow()
        self.available_devices = ["G733 Headset", "G430 Headset", "Anlage", "G733 Mikro", "G430 Mikro"]

    def test_default_devices(self):
        devices = self.window.get_default_devices()
        self.assertIn(devices[0], self.available_devices)
        self.assertIn(devices[1], self.available_devices)

    def test_select_device(self):
        print("Nothing in here yet")

if __name__== '__main__':
    unittest.main()



