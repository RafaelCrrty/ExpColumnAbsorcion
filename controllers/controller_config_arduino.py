from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from models.Arduino import ArduinoManager
from views.View_Arduino_setting.view_ardiono_setting_ui import Ui_Dialog
import time
class ArduinoSettingDialog(QtWidgets.QDialog):
    data_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.arduino_manager = ArduinoManager()

        # Llena el combo box con los puertos disponibles
        self.ui.cmb_puertosA.addItems(self.arduino_manager.available_ports)

        # Conecta los botones aceptar y cancelar a sus respectivos métodos
        self.ui.btn_aceptar.clicked.connect(self.aceptar)
        self.ui.btn_cancelar.clicked.connect(self.cancelar)

    def aceptar(self):
        # Método llamado cuando se presiona el botón Aceptar
        # Puedes implementar aquí la lógica que deseas realizar al aceptar

        # Ejemplo: Imprimir el texto seleccionado en el combo box
        selected_puerto = self.ui.cmb_puertosA.currentIndex()
        arduino_puerto = self.arduino_manager.connect_to_port(selected_puerto)
        if arduino_puerto:
            self.ui.lbl_msj.setText(f"Conexión exitosa: {arduino_puerto}")
            self.data_signal.emit(arduino_puerto)
            # Cerrar la ventana después de 3 segundos (3000 ms)
            QtCore.QTimer.singleShot(2000, self.close)
            self.mostrarMensajeinformation(f"Conexión exitosa: {arduino_puerto}")
        else:
             self.ui.lbl_msj.setText("No se pudo establecer\n la conexión.")

        print("Puerto seleccionado:", selected_puerto)

    def mostrarMensajeinformation(self, msj):
        QMessageBox.information(self, "Información", msj)

    def cancelar(self):
        # Método llamado cuando se presiona el botón Cancelar
        # Puedes implementar aquí la lógica que deseas realizar al cancelar
        self.reject()

# Aquí debes añadir la definición de la clase Ui_Dialog, tal como está en tu archivo generado por pyuic5

# Ejemplo de uso
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = ArduinoSettingDialog()
    dialog.show()
    sys.exit(app.exec_())