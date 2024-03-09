import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtChart import QChartView, QChart, QSplineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QPen



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 161, 81))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 120, 161, 81))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(startShow)
        self.pushButton_2.clicked.connect(stopShow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Визуализация функции случайных чисел"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))
        self.pushButton_2.setText(_translate("MainWindow", "Стоп"))

class RandomSpline(QChart):
    def __init__(self):
        super().__init__()
        self.m_step = 0
        self.m_x = 10
        self.m_y = 1
        self.series = QSplineSeries(self)

        pen = QPen(Qt.darkBlue)
        pen.setWidth(3)
        self.series.setPen(pen)
        self.axisX = QValueAxis()
        self.axisY = QValueAxis()
        self.series.append(self.m_x, self.m_y)

        self.addSeries(self.series)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)
        self.axisX.setTickCount(10)
        self.axisX.setRange(0, 10)
        self.axisY.setRange(-1, 1)
        self.axisX.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.handleTimeout)
        self.timer.stop()

    def handleTimeout(self):
        x = self.plotArea().width() / self.axisX.tickCount()
        y = (self.axisX.max() - self.axisX.min()) / self.axisX.tickCount()
        self.m_x += y

        self.m_y = QRandomGenerator.global_().generateDouble()*2 - 1
        self.series.append(self.m_x, self.m_y)
        self.scroll(x, 0)

def startShow():
    chart.timer.start()

def stopShow():
    chart.timer.stop()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    chart = RandomSpline()
    chart.setTitle("Визуализация функции случайных чисел от -1 до 1")
    chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)

    view = QChartView(chart, MainWindow)
    view.setRenderHint(QPainter.Antialiasing)

    view.setGeometry(250, 50, 300, 300)
    view.resize(500, 400)
    view.show()

    sys.exit(app.exec_())
