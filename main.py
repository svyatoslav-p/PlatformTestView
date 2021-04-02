import matplotlib.pyplot as plt
import sys
import os
import design
import pathlib
import numpy

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

class PlatformTestView(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """ Основной класс проекта"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Привязка событий раздела теста скорости
        self.pbSpeedTest.clicked.connect(self.speedTest)
        self.pbFileDataSpeed.clicked.connect(self.setFileSpeedTest)
        self.lePathToDataSpeed.setText("{}{}".format(pathlib.Path(__file__).parent, '/data/dataSpeedTest.txt'))

        # Привязка событий раздела теста наведения
        self.pbAimingTest.clicked.connect(self.aimingTest)
        self.pbFileDataAiming.clicked.connect(self.setFileAimingTest)
        self.lePathToDataAiming.setText("{}{}".format(pathlib.Path(__file__).parent, '/data/dataAimingTest.txt'))

        # Привязка событий раздела теста сопровождения
        self.pbTrackingTest.clicked.connect(self.trackingTest)
        self.pbFileDataTracking.clicked.connect(self.setFileTrackingTest)
        self.lePathToDataTracking.setText("{}{}".format(pathlib.Path(__file__).parent, '/data/dataTrackingTest.txt'))

    def errorMessageBox (self, msg):
        """ Формирование окна с сообщением об ошибке """
        
        error = QMessageBox()
        error.setWindowTitle("Ошибка")
        error.setText(msg)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)

        error.exec_()

    #---------------------------------------------------------------------------
    #                   Методы для теста скорости
    #---------------------------------------------------------------------------
    def setFileSpeedTest (self):
        """ Установка выбранного файла через GUI для теста скорости """
        
        #directory = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор пара")[0]
        self.lePathToDataSpeed.setText(QtWidgets.QFileDialog.getOpenFileName(self, "Выбор файла")[0])

    def speedTest (self):
        """ Функция обработки результатов теста на скорость """
        
        speed = []
        voltage = []

        try:
            with open(self.lePathToDataSpeed.text(), "r") as file:
                # Читаем по строчно файл
                for str in file:
                    speed.append(float(str.split(';')[0])) # добавляем каждый 1-й элемент каждой строки
                    voltage.append(float(str.split(';')[10])) # добавляем каждый 10-й элемент каждой строки

            # Построение графика
            plt.figure("Результат теста скорости")
            plt.xlabel("Напряжение, В")
            plt.ylabel("Скорость, град/сек")
            plt.grid()
            plt.plot(speed, voltage)
            plt.show()
        except IndexError:
            self.errorMessageBox("Не удалость прочитать файл. Возможно файл неверной структуры")
        except IOError:
            self.errorMessageBox("Не удалость найти файл. Проверьте путь")
        except:
            self.errorMessageBox("Неизвестаня ошибка")

    #---------------------------------------------------------------------------
    #                   Методы для теста наведения
    #---------------------------------------------------------------------------
    def setFileAimingTest (self):
        """ Установка выбранного файла через GUI для теста наведения """
        
        #directory = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор пара")[0]
        self.lePathToDataAiming.setText(QtWidgets.QFileDialog.getOpenFileName(self, "Выбор файла")[0])

    def aimingTest (self):
        """ Функция обработки результатов теста наведения """

        try:
            with open(self.lePathToDataAiming.text(), "r") as file:

                f = file.readlines()

            # Формируем массивы из файлов элементы строк разделены `;` и не читаем
            # последний символ т.к. это '\n'
            target_az   = f[0].split(';')[:-1] #Строка 1 в файле
            current_az  = f[1].split(';')[:-1] #Строка 2 в файле
            target_um   = f[3].split(';')[:-1] #Строка 4 в файле
            current_um  = f[4].split(';')[:-1] #Строка 5 в файле
            time        = f[2].split(';')[:-1] #Строка 3 в файле

            # Преобразуем строковые элементы в float
            target_az   = [float(i) for i in target_az]
            current_az  = [float(i) for i in current_az]
            target_um   = [float(i) for i in target_um]
            current_um  = [float(i) for i in current_um]
            time        = [float(i) for i in time]

            # Вывод ошибок наведения
            errAimingAz = round((target_az[-1] - current_az [-1]), 4)
            errAimingUm = round((target_um[-1] - current_um [-1]), 4)

            # Наведение по АЗ
            if self.cbGraphAimingAZ.isChecked():            

                plt.figure("Наведение по азимуту")
                plt.title("{} {} {}".format("Отклонение:", errAimingAz, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, current_az, 
                         time, target_az)
                plt.legend(['Текущие','Целевые'], loc=4)

            # Наведение по УМ
            if self.cbGraphAimingUM.isChecked():

                plt.figure("Наведение по углу места")
                plt.title("{} {} {}".format("Отклонение:", errAimingUm, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.ylabel("град")
                plt.grid(True)
                plt.plot(time, current_um, 
                         time, target_um)
                plt.legend(['Текущие','Целевые'], loc=4)

            # Ошибка наведение по АЗ
            if self.cbGraphAimingErrAZ.isChecked(): 

                errAimingTrackAz = []

                # Вычисляем ошибку для построения графика
                for i in range(len(target_az)):
                    errAimingTrackAz.append(target_az[i] - current_az[i])

                # Ошибка наведение по АЗ
                plt.figure("Ошибка наведение по азимуту")
                plt.title("{} {} {}".format("Отклонение:", errAimingAz, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, errAimingTrackAz)


            # Ошибка наведение по УМ
            if self.cbGraphAimingErrUM.isChecked(): 

                errAimingTrackUm = []

                # Вычисляем ошибку для построения графика
                for i in range(len(target_az)):
                    errAimingTrackUm.append(target_um[i] - current_um[i])

                # Ошибка наведение по АЗ
                plt.figure("Ошибка наведение по углу места")
                plt.title("{} {} {}".format("Отклонение:", errAimingUm, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, errAimingTrackUm)

            plt.show()

        except IndexError:
            self.errorMessageBox("Не удалость прочитать файл. Возможно файл неверной структуры")
        except IOError:
            self.errorMessageBox("Не удалость найти файл. Проверьте путь")
        except:
            self.errorMessageBox("Неизвестаня ошибка")

    #---------------------------------------------------------------------------
    #                   Методы для теста сопровождения
    #---------------------------------------------------------------------------
    def setFileTrackingTest (self):
        """ Установка выбранного файла через GUI для теста сопровождения """

        self.lePathToDataTracking.setText(QtWidgets.QFileDialog.getOpenFileName(self, "Выбор файла")[0])

    def trackingTest (self):
        """ Функция обработки результатов теста сопровождения """

        try:
            with open(self.lePathToDataTracking.text(), "r") as file:

                f = file.readlines()

            # Читаем по строчно кроме первых и последних N отсчетов в каждой строке
            # это нужно делать, так как где-то наведение еще не началось (до 5 град по Ум), 
            # а где-то уже закончилось(после 5 град по Ум), а данные пишутся и ошибка
            # слонячья получается 
            #    [9:-11] - соответсвует обрезанию по 10 отсчетов
            target_az   = f[0].split(';')[9:-11] #Строка 1 в файле
            current_az  = f[1].split(';')[9:-11] #Строка 2 в файле
            target_um   = f[3].split(';')[9:-11] #Строка 4 в файле
            current_um  = f[4].split(';')[9:-11] #Строка 5 в файле
            time        = f[2].split(';')[9:-11] #Строка 3 в файле

            # Преобразуем строковые элементы в float
            target_az   = [float(i) for i in target_az]
            current_az  = [float(i) for i in current_az]
            target_um   = [float(i) for i in target_um]
            current_um  = [float(i) for i in current_um]
            time        = [float(i) for i in time]

            # Вычисление траектории ошибки наведения по АЗ
            errTrackingAz = []
            for i in range(len(target_az)):
                errTrackingAz.append(target_az[i] - current_az[i]) 

            # Вычисление траектории ошибки наведения по УМ
            errTrackingUm = []
            for i in range(len(target_um)):
                errTrackingUm.append(target_um[i] - current_um[i]) 

            # СКО по АЗ
            if self.cbGraphTrackingStdAz.isChecked(): 

                # СКО
                stdAz = round(numpy.std(errTrackingAz), 4)
                
                # Построение графика
                plt.figure("СКО Азимут")
                if stdAz>1:
                    plt.title("{} {} {}".format("СКО АЗ:", stdAz, "град"))
                else:
                    plt.title("{} {} {}".format("СКО АЗ:", stdAz*60, "мин"))

                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, current_az, 
                         time, target_az)

            # СКО по УМ
            if self.cbGraphTrackingStdUm.isChecked(): 

                # СКО
                stdUm = round(numpy.std(errTrackingUm), 4)

                # Построение графика
                plt.figure("СКО Угол места")
                if stdUm>1:
                    plt.title("{} {} {}".format("СКО УМ:", stdUm, "град"))
                else:
                    plt.title("{} {} {}".format("СКО УМ:", stdUm*60, "мин"))

                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, current_um, 
                         time, target_um)

            # Ошибка сопровождения по АЗ
            if self.cbGraphTrackingErrAZ.isChecked(): 

                # Максимальное отклонение
                errTrackingMaxAz = round(numpy.max(numpy.abs(errTrackingAz)), 4)
                # Построение графика
                plt.figure("Ошибка сопровождения по азимуту")
                plt.title("{} {} {}".format("Макс:", errTrackingMaxAz, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, errTrackingAz, linewidth=1.0)

            # Ошибка сопровождения по УМ
            if self.cbGraphTrackingErrUM.isChecked(): 

                # Максимальное отклонение
                errTrackingMaxUm = round(numpy.max(numpy.abs(errTrackingUm)), 4)
                # Построение графика
                plt.figure("Ошибка сопровождения по уголу места")
                plt.title("{} {} {}".format("Макс:", errTrackingMaxUm, "град"))
                plt.xlabel("сек", 
                            fontsize=10,
                            color='gray',
                            loc="right")
                plt.ylabel("град", 
                            fontsize=10,
                            color='gray',
                            loc="center")
                plt.grid(True)
                plt.plot(time, errTrackingUm, linewidth=1.0)

            plt.show()

        except IndexError:
            self.errorMessageBox("Не удалость прочитать файл. Возможно файл неверной структуры")
        except IOError:
            self.errorMessageBox("Не удалость найти файл. Проверьте путь")
        except:
            self.errorMessageBox("Неизвестаня ошибка")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PlatformTestView()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


