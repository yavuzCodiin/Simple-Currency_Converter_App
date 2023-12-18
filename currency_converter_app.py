import sys
import time
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('currency_converter.ui', self)
        self.setWindowTitle("Currency Converter App")
        self.setFixedSize(603, 463)

        # Initialize rate
        self.rate = None

        #Defining Variables on the GUI
        self.base_currency = self.findChild(QtWidgets.QComboBox, 'base_comboBox')
        self.target_currency = self.findChild(QtWidgets.QComboBox, 'target_comboBox')
        self.base_value = self.findChild(QtWidgets.QLineEdit, 'basevalue_lineEdit')
        self.target_value = self.findChild(QtWidgets.QLineEdit, 'targetvalue_lineEdit')
        self.rate_currency = self.findChild(QtWidgets.QLineEdit,'currencyrate_lineEdit')

        #Operations
        self.base_currency.currentIndexChanged.connect(self.currency_changed)
        self.target_currency.currentIndexChanged.connect(self.currency_changed)
        self.base_value.editingFinished.connect(self.update_conversion_rate)
        time.sleep(4)
        self.base_value.editingFinished.connect(self.convert_currency)


    def update_conversion_rate(self):
        api_key = "2c0ec96ab61399c54904f4b267b02427"

        base_index = self.base_currency.currentIndex()
        self.base_text = self.base_currency.itemText(base_index)
        
        target_index = self.target_currency.currentIndex()
        self.target_text = self.target_currency.itemText(target_index)

        if self.base_text and self.target_text:
            url ="http://data.fixer.io/api/latest?access_key={}&symbols={}&base={}".format(api_key, self.target_text, self.base_text)
            response = requests.get(url)
            self.data = response.json()

            if self.data["success"]:
                self.rate = self.data['rates']["{}".format(self.target_text)]
                self.rate_currency.setText("{:.2f}".format(self.rate))
                if self.rate is None:
                    QMessageBox.critical(self, "API Error", f"Target currency {self.target_text} is not supported.")
            else:
                self.rate = None
                error_info = self.data.get('error', {})
                QMessageBox.critical(self, "API Error", f"Error {error_info.get('code')}: {error_info.get('info')}")
        else:
            QMessageBox.critical("Select Currencies you want to do conversion")

    def currency_changed(self):
        self.base_value.clear()
        self.target_value.clear()

    def convert_currency(self):
        # Check if rate is available
        if self.rate is not None:
            try:
                amount = float(self.base_value.text())
                converted_amount = self.rate * amount
                self.target_value.setText("{:.2f}".format(converted_amount))
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
                self.target_value.clear()
        else:
            QMessageBox.warning(self, "Conversion Error", "Conversion rate not available. Please check the base currency and try again.")
            self.base_value.clear()
            self.target_value.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
