from PyQt5 import QtWidgets, uic, QtCore, QtGui

import sys
from random import shuffle

LIMIT_WORDS = 10


class Ui_Game(QtWidgets.QDialog, uic.loadUiType("uis/game.ui")[0]):
    """
        Окно игры
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.vbox = QtWidgets.QVBoxLayout()

        self.input_lines_scroll_area = self.findChild(QtWidgets.QScrollArea, "input_lines_scroll_area")
        self.input_lines_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.input_lines_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.input_lines_scroll_area.setWidgetResizable(True)

        self.check_button = self.findChild(QtWidgets.QPushButton, "check_button")

        self.restart_button = self.findChild(QtWidgets.QPushButton, "restart_button")

        self.quit_button = self.findChild(QtWidgets.QPushButton, "quit_button")
        self.quit_button.setIcon(QtGui.QIcon('source/icons8-close-window-64.png'))
        self.quit_button.setIconSize(QtCore.QSize(50, 50))
        self.quit_button.clicked.connect(lambda: self.close())

        self.result_label = self.findChild(QtWidgets.QLabel, "result_label")

    def closeEvent(self, event):
        """
            Обработчик события закрытия окна, когда закрываем окно "Игра" то мы показываем новое окно с
            перезагруженными словами
        """
        main_window = Ui_Main_Window()
        main_window.show_main_window()
        event.accept()


class Ui_Settings(QtWidgets.QDialog, uic.loadUiType("uis/settings.ui")[0]):
    """
        Окно настроек
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.limit_words_input_field = self.findChild(QtWidgets.QLineEdit, "limit_words_input_field")
        self.limit_words_input_field.setText(str(LIMIT_WORDS))
        self.save_settings_button = self.findChild(QtWidgets.QPushButton, "save_settings_button")
        self.save_settings_button.clicked.connect(self.change_limit_words)

    def change_limit_words(self):
        """
            Обработчик нажатия на кнопку "Сохранить", при нажатие сохраняется значение введённое в Количество слов.
            Если мы вводим больше 50, то сбрасываем значение и обводим поле красным, если вводим текст также.
            Если пользователь ввёл всё верно сохраняем.
        """
        global LIMIT_WORDS
        try:
            if int(self.limit_words_input_field.text()) < 50:
                self.limit_words_input_field.setStyleSheet("border: 1.5px solid green;")
                LIMIT_WORDS = int(self.limit_words_input_field.text())
            else:
                self.limit_words_input_field.setStyleSheet("border: 1.5px solid red;")
                self.limit_words_input_field.setText("")
        except:
            self.limit_words_input_field.setStyleSheet("border: 1.5px solid red;")
            self.limit_words_input_field.setText("")
            return


class Ui_Main_Window(QtWidgets.QWidget):
    """
        Главное меню
    """

    def __init__(self):
        """
            Заполняем Scroll Area случайными значениями в цикле, также перемешиваем список слов который подгрузили
            используя word_rus.txt
        """
        super(Ui_Main_Window, self).__init__()
        uic.loadUi('uis/main.ui', self)
        words = self.load_words()
        shuffle(words)
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        for word in words[:LIMIT_WORDS]:
            object = QtWidgets.QLabel(word)
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        self.hints_scroll_area = self.findChild(QtWidgets.QScrollArea, "hints_scroll_area")
        self.hints_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.hints_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hints_scroll_area.setWidgetResizable(True)
        self.hints_scroll_area.setWidget(self.widget)

        self.start_game_button = self.findChild(QtWidgets.QPushButton, "start_game_button")
        self.start_game_button.clicked.connect(self.show_game_window)

        self.restart_button = self.findChild(QtWidgets.QPushButton, "restart_button")
        self.restart_button.clicked.connect(self.restart_game_main_menu)

        self.settings_button = self.findChild(QtWidgets.QPushButton, "settings_button")
        self.settings_button.setIcon(QtGui.QIcon('source/icons8-automatic-50.png'))
        self.settings_button.setIconSize(QtCore.QSize(50, 50))
        self.settings_button.clicked.connect(self.show_settings_window)

        self.quit_button = self.findChild(QtWidgets.QPushButton, "quit_button")
        self.quit_button.setIcon(QtGui.QIcon('source/icons8-close-window-64.png'))
        self.quit_button.setIconSize(QtCore.QSize(50, 50))
        self.quit_button.clicked.connect(lambda: self.close())

        self.show()

    def restart_game_main_menu(self):
        """
            При нажатие на кнопке "Перезагрузить" обновляется список слов в главном меню
        """
        words = self.load_words()
        shuffle(words)
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        for word in words[:LIMIT_WORDS]:
            object = QtWidgets.QLabel(word)
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        self.hints_scroll_area.setWidget(self.widget)

    @staticmethod
    def load_words():
        """
            Метод для загрузки слов с word_rus.txt файла
        """
        with open("word_rus.txt", "r", encoding="utf-8") as file:
            return file.read().split("\n")

    @staticmethod
    def show_settings_window():
        """
            Метод для отображения окна "Настройки"
        """
        settings_ui = Ui_Settings()
        settings_ui.exec_()

    def show_game_window(self):
        """
            Метод для отображения окна "Игра". При отображение закрывается окно "Главное меню", чтобы скрыть слова.
        """
        self.hide()
        self.game_window_iu = Ui_Game()
        widget = QtWidgets.QWidget()

        for i in range(LIMIT_WORDS):
            object = QtWidgets.QLineEdit()
            self.game_window_iu.vbox.addWidget(object)

        widget.setLayout(self.game_window_iu.vbox)
        self.game_window_iu.input_lines_scroll_area.setWidget(widget)

        self.game_window_iu.check_button.clicked.connect(self.check_words)
        self.game_window_iu.restart_button.clicked.connect(self.restart_game)

        self.game_window_iu.exec_()

    def check_words(self):
        """
            Метод для проверки какие слова были введены верно.
        """
        found_wrong_words = 0
        for i in range(LIMIT_WORDS):
            if self.vbox.itemAt(i).widget().text().lower() == self.game_window_iu.vbox.itemAt(
                    i).widget().text().lower():
                self.game_window_iu.vbox.itemAt(i).widget().setStyleSheet("border: 1.5px solid green;")
            else:
                self.game_window_iu.vbox.itemAt(i).widget().setStyleSheet("border: 1.5px solid red;")
                found_wrong_words += 1
        if found_wrong_words == 0:
            self.game_window_iu.result_label.setText("Всё правильно!")
        else:
            self.game_window_iu.result_label.setText("Есть ошибки!")

    def restart_game(self):
        """
            Метод для перезагруки игры и назначения новых рандомных слов.
        """
        words = self.load_words()
        shuffle(words)
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        for word in words[:LIMIT_WORDS]:
            object = QtWidgets.QLabel(word)
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)
        self.hints_scroll_area.setWidget(self.widget)

        widget = QtWidgets.QWidget()
        self.game_window_iu.vbox = QtWidgets.QVBoxLayout()

        for i in range(LIMIT_WORDS):
            object = QtWidgets.QLineEdit()
            self.game_window_iu.vbox.addWidget(object)

        widget.setLayout(self.game_window_iu.vbox)
        self.game_window_iu.input_lines_scroll_area.setWidget(widget)

    def show_main_window(self):
        """
            Метод для отображения "Главное меню".
        """
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_Main_Window()
    app.exec_()
