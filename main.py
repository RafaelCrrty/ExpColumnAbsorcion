import sys
from PyQt5.QtWidgets import QApplication
from controllers.controller_view_principal import MyApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())