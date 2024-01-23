from views.view_grafica.view_grafica_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QFileDialog,QMessageBox
from models.Mediador import Mediator,Component
from models.Grafica import Canvas_grafica_exp
from PyQt5.QtCore import Qt
from models.Exel import ExcelWriter
import os
import sys

class Controler_graf(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mediator = Mediator()
        self.component = Component(self.mediator,"Controller_grafica")
        self.ui.pushButton.clicked.connect(self.exp_image)
        self.mediator.add(self.component)
        # Variable para almacenar la instancia de Canvas_grafica_exp

        self.canvas_grafica1 = None
        self.canvas_grafica2 = None
        self.canvas_grafica3 = None
        self.canvas_grafica4 = None
        self.nomgraf = None
    def nombre_grafica(self):
        """"""
        message2 = self.mediator.get_message(self.component)
        if not message2 == None:
            """"""
            self.ui.lbl_nomexp.setText(message2)
    
    def grafica_view(self):
        """"""
        message2 = self.mediator.get_message(self.component)
        if not message2 == None:
            """"""
            # Si ya existe una instancia de Canvas_grafica_exp, eliminarla antes de crear una nueva
            if self.canvas_grafica1:
                self.ui.verticalLayout.removeWidget(self.canvas_grafica1)
                self.canvas_grafica1.deleteLater()

            if self.canvas_grafica2:
                self.ui.verticalLayout_2.removeWidget(self.canvas_grafica2)
                self.canvas_grafica2.deleteLater()

            if self.canvas_grafica3:
                self.ui.verticalLayout_3.removeWidget(self.canvas_grafica3)
                self.canvas_grafica3.deleteLater()

            if self.canvas_grafica4:
                self.ui.verticalLayout_4.removeWidget(self.canvas_grafica4)
                self.canvas_grafica4.deleteLater()

            self.canvas_grafica1 = Canvas_grafica_exp(message2['sensor1'],"Temperatura del frasco de suministro de MEA",'#ff6c13')
            self.ui.verticalLayout.addWidget(self.canvas_grafica1)
            self.ui.verticalLayout.setAlignment(Qt.AlignVCenter)
                
            self.canvas_grafica2 = Canvas_grafica_exp(message2['sensor2'],"Temperatura ambiente",'#71ceff')
            self.ui.verticalLayout_2.addWidget(self.canvas_grafica2)
            self.ui.verticalLayout_2.setAlignment(Qt.AlignVCenter)

            self.canvas_grafica3 = Canvas_grafica_exp(message2['sensor3'], "Temperatura Superior de la columna de Absorción",'#009d1e')
            self.ui.verticalLayout_3.addWidget(self.canvas_grafica3)
            self.ui.verticalLayout_3.setAlignment(Qt.AlignVCenter)

            self.canvas_grafica4 = Canvas_grafica_exp(message2['sensor4'],"Temperatura Inferior de la columna de absorción",'#FFD700')
            self.ui.verticalLayout_4.addWidget(self.canvas_grafica4)
            self.ui.verticalLayout_4.setAlignment(Qt.AlignVCenter)

    def exp_image(self):
        resp = self.mostrar_mensaje_advertencia()
        if resp:
           return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta para guardar gráficas", options=options)

        if directory:
            # Check if the directory is empty
            if not os.listdir(directory):
                print("El directorio está vacío. No se pueden guardar las gráficas.")
                return
            
            self.mostrarMensajeinformation(str(directory))

            filenames = ["Temperatura_frasco_mea.png", "Temperatura_ambiente.png",
                        "Temperatura_superior_absorcion.png", "Temperatura_inferior_absorcion.png"]

            # Combine each filename with the directory path and save the graphs.
            file_paths = [os.path.join(directory, filename) for filename in filenames]

            # Save each graph with its respective name.
            self.canvas_grafica1.guardar_grafica_como_png(file_paths[0])
            self.canvas_grafica2.guardar_grafica_como_png(file_paths[1])
            self.canvas_grafica3.guardar_grafica_como_png(file_paths[2])
            self.canvas_grafica4.guardar_grafica_como_png(file_paths[3])

            excel_writer = ExcelWriter(os.path.join(directory, "data.xls"))
            excel_writer.txt_self_exel()

            self.mostrarMensajeinformation("Datos exportados con éxito.")
 
    def mostrarMensajeinformation(self, msj):
        QMessageBox.information(self, "Información", msj)


    def mostrar_mensaje_advertencia(self):
        # Crea una instancia de QMessageBox con un mensaje de advertencia
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Warning)
        mensaje.setText("Por favor, asegúrese de cerrar cualquier archivo de Excel abierto en la misma ubicación antes de reemplazarlo.")
        mensaje.setInformativeText("El reemplazo de un archivo Excel abierto puede causar pérdida de datos no guardados. \nIncluso cerrar el programa perdiendo todos los datos.")
        mensaje.setWindowTitle("Advertencia")
        
        # Agrega botones "Aceptar" y "Cancelar" al mensaje
        mensaje.addButton(QMessageBox.Ok)
        mensaje.addButton(QMessageBox.Cancel)
        
        # Muestra el mensaje y obtén la respuesta del usuario
        respuesta = mensaje.exec_()
        
        # Si el usuario hace clic en "Cancelar", puedes manejarlo según tus necesidades
        if respuesta == QMessageBox.Cancel:
            # Realiza alguna acción aquí si el usuario decide cancelar el reemplazo
            return True
        
        return False


if __name__ == "__main__":
     # Registra el tipo de datos QTextBlock
    app = QDialog(sys.argv)
    window = Controler_graf()
    window.show()
    sys.exit(app.exec_())