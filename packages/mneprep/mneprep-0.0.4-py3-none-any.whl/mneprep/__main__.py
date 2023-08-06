import sys

from PyQt5.QtWidgets import QApplication

from mneprepV2.prep_classes.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
