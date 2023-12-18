# <ins>Simple-Currency_Converter_App</ins>
![image](https://github.com/yavuzCodiin/Simple-Currency_Converter_App/assets/82445309/3cef242e-569a-463e-a67f-a5d7805ac713)

Have you ever found yourself in need of a quick currency conversion, maybe while planning a vacation or during an international online shopping spree? Currency converter application will be there for you.
## <ins>What is JSON?</ins>

JSON, short for JavaScript Object Notation, is a format I frequently encounter and utilize in my programming projects. It's a standard for storing and transporting data, which I find incredibly useful. JSON is valued because it structures data in a way that is easy for humans to read and write, while also being simple for machines to parse and generate.

Here's an example of a JSON object:

```json
{
  "Name": "John",
  "Surname": "Doe",
  "Phone_Number": 3454543,
  "Features": {
    "hobby": "playing games",
    "job": "Instructor"
  }
}
```
## <ins>What is an API?</ins>

Whenever I dive into the world of development, another term that constantly pops up is 'API', which stands for Application Programming Interface. But what does that really mean? An API can be compared to a menu in a restaurant. It provides a list of 'dishes' — in this case, services and data — that a software program offers. Just like ordering a meal, software can request specific information or services from another application or server using its API.

One aspect of APIs that simplifies my tasks is the concept of abstraction. They conceal all the intricate, technical details of their internal processes. This is akin to driving a car; there's no need to understand every mechanical aspect under the hood. All that's necessary is to know how to operate the steering wheel, accelerator, and brakes. APIs function in a similar manner—I utilize the 'controls' they offer, without concerning myself with the specifics of their operations.
## <ins>What is REST API?</ins>

REST, or Representational State Transfer, is akin to a set of rules for facilitating efficient communication over the internet. It emphasizes simplicity and the use of well-known web standards. For example, when my application needs to retrieve data, it makes a request to a REST API using simple HTTP methods, similar to how we navigate websites.
## <ins>How to Use API?</ins>

First of all, let's go over the documentation together on how to use this API. The documentation site has all we need, so the first step is to sign up and get an API KEY, which is crucial for us to use the service.

You can make a request to the API like this:
```python
data.fixer.io/api/latest?access_key={your API key goes here}
```
With this API request, we get a dictionary-like output.
![image](https://github.com/yavuzCodiin/Simple-Currency_Converter_App/assets/82445309/11cf9d92-5879-429c-9a9b-200dc09f9417)

So we will use these to create our convert currency app. In the following, we have error codes in case you get error check here.
![image](https://github.com/yavuzCodiin/Simple-Currency_Converter_App/assets/82445309/42a56786-1a82-476d-9f6b-aff04d4c760d)

We need 3 parameters to do conversion it is not required in API request but we need it for our application to get conversion rate.
> Endpoint URLs
```python
http://data.fixer.io/api/latest?access_key={YOUR_ACCESS_KEY}&base={base currency}&symbols={target currency}
```
For more detailed information, I recommend checking out their official documentation. Here are some useful links you can use:

- [Quickstart Guide](https://fixer.io/quickstart)
- [API Documentation](https://fixer.io/documentation)
![image](https://github.com/yavuzCodiin/Simple-Currency_Converter_App/assets/82445309/a6881384-8128-43e5-a051-40183779d139)

## <ins>Importing and Initiating</ins>
In this part, I’m loading the GUI, tailoring the app window, initializing variables for both currency conversion and the GUI, and enhancing user interaction within the app.
```python
import sys
import time
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('currency_converter.ui', self) # This will load ui which we created with QtDesigner
        self.setWindowTitle("Currency Converter App")
        self.setFixedSize(703, 503)

        # Initialize currency rate
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
```
## <ins>Updating Conversion Rate</ins>
In this part of the code for currency converter app, I’m handling the crucial task of `updating the conversion rate`. First, I define my API key for accessing the currency data. Then, I fetch the selected currencies from the combo boxes in the GUI, which are the base and target currencies for conversion.

Next, I construct the URL for the API request, dynamically inserting the chosen `base` and `target` currencies along with my `API key`. The request is sent using requests.get, and the response, in `JSON format`, is stored.

I then extract the `conversion rate` from this `response`. If the API call is successful, the app updates the conversion rate. In case the rate is unavailable, or the target currency is not supported, the app shows an error message. Additionally, if there’s any other type of API error, like incorrect parameters or server issues, the app displays the specific error details.

This code is vital for keeping the app’s data current, ensuring that users always get the latest conversion rates based on their selected currencies.
```python
def update_conversion_rate(self):
        api_key = "YOUR API KEY GOES HERE"

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
```
## <ins>Converting the Currency</ins>
The `currency_changed()` function is straightforward. Whenever a user selects a `different` base or target currency, this function clears the input and output on the GUI. This reset ensures that old values don’t interfere with new calculations when the currency selection changes.

The `convert_currency()` function is where the core action happens. It kicks in when there’s a need to convert an amount from the base currency to the target currency. First, it checks if the conversion rate `(self.rate)` is available.

If it is, the function attempts to convert the entered amount (grabbed from base_value) using this rate. The result is displayed on the GUI. To handle scenarios where the user might enter invalid data (like text instead of numbers), I’ve included a try-except block. If the input isn’t a valid number, the app shows a warning and clears the output field.

There’s also a provision for cases where the conversion rate might not be available — maybe due to an issue with the API or an unsupported currency. In such cases, the app alerts the user and clears both input and output fields, readying the app for another attempt once the issue is resolved.

Overall, these functions ensure my app is responsive, accurate, and user-friendly, providing a seamless experience in currency conversion.
```python
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
```
## <ins>Main Part</ins>
This part is also straightforward, it is starting the application and opening the application.
```python
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

