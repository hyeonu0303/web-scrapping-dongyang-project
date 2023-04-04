import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class WeatherWidget(QWidget):
    def __init__(self, humidity, wind, precipitation, pm25, pm10, temperature):
        super().__init__()
        self.humidity = humidity
        self.wind = wind
        self.precipitation = precipitation
        self.pm25 = pm25
        self.pm10 = pm10
        self.temperature = temperature
        self.initUI()

    def initUI(self):
        humidity_label = QLabel("Humidity: " + str(self.humidity) + "%")
        wind_label = QLabel("Wind: " + str(self.wind) + " m/s")
        precipitation_label = QLabel("Precipitation: " + str(self.precipitation) + "mm/h")
        pm25_label = QLabel("PM2.5: " + str(self.pm25) + "μg/m3")
        pm10_label = QLabel("PM10: " + str(self.pm10) + "μg/m3")
        temperature_label = QLabel("Temperature: " + str(self.temperature) + "℃")

        vbox = QVBoxLayout()
        vbox.addWidget(humidity_label)
        vbox.addWidget(wind_label)
        vbox.addWidget(precipitation_label)
        vbox.addWidget(pm25_label)
        vbox.addWidget(pm10_label)
        vbox.addWidget(temperature_label)

        self.setLayout(vbox)
        self.setWindowTitle('Weather Information')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherWidget(humidity=80, wind=2.5, precipitation=0.2, pm25=35, pm10=60, temperature=15)
    ex.show()
    sys.exit(app.exec_())
