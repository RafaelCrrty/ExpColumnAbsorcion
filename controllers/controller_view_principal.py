import datetime
import threading
import time
import sys
import re
import csv
import os
import random
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel,QHBoxLayout,QMessageBox
from PyQt5 import QtWidgets
from views.View_Principal.view_principal_ui import Ui_MainWindow
from controllers.controller_view_grafica import Controler_graf
from controllers.controller_config_arduino import ArduinoSettingDialog
from models.Mediador import Mediator,Component

from models.Cronometro import Cronometro
from models.Grafica import Canvas_grafica
import serial

class MyApplication(QMainWindow):
    datos_actualizados = pyqtSignal(str)
    def __init__(self):
        super(MyApplication, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cronometro = Cronometro()
        self.sensores = ["sensor1", "sensor2", "sensor3", "sensor4"]
        # self.ui.comboBox_configuration.currentText()
        self.datos_actualizados.connect(self.actualizar_txt_area_temperaturas)
        self.ui.btn_inicio_config.clicked.connect(self.cronometro_funtion)
        self.ui.btn_detener_prueba.clicked.connect(self.detener_experimentacion)
        self.ui.btn_detener_cronometro.clicked.connect(self.detener_cronometro)
        self.ui.btn_grafica_exp.clicked.connect(self.view_emergentgraf)
        self.ui.btn_config_arduinoP.clicked.connect(self.view_configarduino)
        self.data_sensors = {'sensor1': [],'sensor2': [],'sensor3': [],'sensor4': []}

        """
        self.exp_data = {
            'saturacion': [],
            'continua': [],
        }
        """
        self.mediator = Mediator()
        self.component = Component(self.mediator,"Controller_principal")
        self.mediator.add(self.component)

        self.ui.btn_calcular_exp.clicked.connect(self.calcular_temp)
        # Conectar el evento activated del QComboBox a un método específico
        self.ui.cmb_prueba.activated.connect(self.on_combobox_activated)
        self.limitarLongitudTextField(8, self.ui.txt_ms_total, 2)
        self.limitarLongitudTextField(8, self.ui.txt_mea_composition, 2)
        self.limitarLongitudTextField(8, self.ui.txt_ms_mea, 2)
        self.selected_option = "Saturación"
        self.actualizar_hora()

        self.view_configardui = ArduinoSettingDialog()
        self.view_emerggrat = Controler_graf()

         # Deshabilita los campos de texto
        self.ui.txt_ms_mea.setReadOnly(True)
        self.ui.txt_mol_mea.setReadOnly(True)
        self.ui.txt_moles_co_dos.setReadOnly(True)
        self.ui.txt_flujo_molar_co_dos.setReadOnly(True)
        self.ui.txt_temp_saturation.setReadOnly(True)
        self.ui.txt_error.setReadOnly(True)

        self.puerto_ardui = None
        self.bool_check = False

    def detener_experimentacion(self):
        """"""
        # Muestra un cuadro de diálogo de confirmación
        result = QtWidgets.QMessageBox.question(self, "Confirmación", "¿Deseas detener la experimentación?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # Verifica la selección del usuario
        if result == QtWidgets.QMessageBox.Yes:
            print("El usuario hizo clic en 'Aceptar'")
            # Realiza acciones adicionales si el usuario acepta
            self.ui.btn_detener_prueba.lower()
            self.bool_check = True
            return True
        else:
            print("El usuario hizo clic en 'Cancelar'")
            # Realiza acciones adicionales si el usuario cancela
        
        return False
    

    def view_configarduino(self):
        self.view_configardui.setWindowTitle("Configuración de puerto arduino")
        self.view_configardui.setGeometry(410,150,263, 476)
        self.view_configardui.data_signal.connect(self.puerto_arduino)
        self.view_configardui.exec_()

    def puerto_arduino(self,obj_puerto):
        """"""
        self.puerto_ardui = obj_puerto
        print("El puerto a conectarse es, ", obj_puerto)
    
    def view_emergentgraf(self):
        """"""
        self.view_emerggrat.setWindowTitle("Gráfica de experimentación")
        self.view_emerggrat.setGeometry(410,150,1303, 765)
        self.component.notify("Experimentación en "+str(self.selected_option))
        self.view_emerggrat.nombre_grafica()

        self.component.notify(self.data_sensors)
        self.view_emerggrat.grafica_view()
        self.view_emerggrat.exec_()

    def actualizar_hora(self):
            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now()
            self.ui.lbl_fecha_actual.setText(str(fecha_actual.date()))

    def calcular_temp(self):
        """"""
        # Realiza las acciones deseadas según la opción seleccionada
        if not self.selected_option == "":
            if self.selected_option == "Saturación":
                """"""
                # Constante de gases
                gas_cons = 0.082
                mea = 61.08
                precion_atp = 0.8

                masa_total_str = self.ui.txt_ms_total.text()
                composicion_mea_str = self.ui.txt_mea_composition.text()
                flujo_volum_str = self.ui.txt_flujo_vco_dos.text()
                temp_ambiente_str = self.ui.txt_temp_ambiente.text()
                temp_satur_str = self.ui.txt_temp_saturation.text()
                temp_exp_str = self.ui.txt_temp_exp.text()

                # Convierte los valores de texto a números flotantes
                masa_total = float(masa_total_str) if masa_total_str else 0.0
                composicion_mea = float(composicion_mea_str) if composicion_mea_str else 0.0
                flujo_volum = float(flujo_volum_str) if flujo_volum_str else 0.0
                temp_ambiente = float(temp_ambiente_str) if temp_ambiente_str else 0.0
                temp_satur = float(temp_satur_str) if temp_satur_str else 0.0

                self.ui.txt_ms_mea.setText(str(masa_total * composicion_mea))
                masa_mea = float(self.ui.txt_ms_mea.text())

                if mea != 0:
                    self.ui.txt_mol_mea.setText(str(masa_mea / mea))
                    mol_mea = float(self.ui.txt_mol_mea.text())
                else:
                    self.ui.txt_mol_mea.setText(str(0))
                    mol_mea = float(self.ui.txt_mol_mea.text())
                    
                if mol_mea != 0:
                    self.ui.txt_moles_co_dos.setText(str(mol_mea / 2))
                    mol_co2 = float(self.ui.txt_moles_co_dos.text())
                else:
                    self.ui.txt_moles_co_dos.setText(str(0))
                    mol_co2 = float(self.ui.txt_moles_co_dos.text())

                if temp_ambiente != 0:
                    self.ui.txt_flujo_molar_co_dos.setText(str((precion_atp * flujo_volum) / (gas_cons * (temp_ambiente + 273.15))))
                    flujo_molar_co2 = float(self.ui.txt_flujo_molar_co_dos.text())
                else:
                    self.ui.txt_flujo_molar_co_dos.setText(str(0))
                    flujo_molar_co2 = float(self.ui.txt_flujo_molar_co_dos.text())

                if flujo_molar_co2 != 0.0:
                    self.ui.txt_temp_saturation.setText(str(mol_co2 / flujo_molar_co2))
                    temp_satur_str = self.ui.txt_temp_saturation.text()
                else:
                    self.ui.txt_temp_saturation.setText(str(0))
                    temp_satur_str = self.ui.txt_temp_saturation.text()

                # Convierte los valores de texto a números flotantes
                temp_satur = float(temp_satur_str) if temp_satur_str else 0.0

                # Verifica si temp_exp_str está vacío o es None
                temp_exp = float(temp_exp_str) if temp_exp_str else 0.0

                # Verifica si temp_satur es diferente de 0 antes de calcular el error
                if temp_satur != 0.0:
                    error = abs(temp_satur - temp_exp) / temp_satur
                else:
                    error = 0.0

                # Asigna el valor del error al widget txt_error
                self.ui.txt_error.setText(str(error))

            elif self.selected_option == "Continuo":
                """"""
                masat_str = self.ui.txt_ms_total_C.text()
                temps_str = self.ui.txt_temp_saturacion_C.text()

                # Convierte los valores de texto a números flotantes
                masat = float(masat_str) if masat_str else 0.0
                temps = float(temps_str) if temps_str else 0.0

                if temps != 0.0:
                    self.ui.txt_q_calculada.setText(str(masat / temps))
                    qcal = float(self.ui.txt_q_calculada.text())
                else:
                    self.ui.txt_q_calculada.setText(str(0))
                    qcal = float(self.ui.txt_q_calculada.text())

                self.ui.txt_bomba_peris_C.setText(str(round(qcal * 0.8, 0)))
                qreal = float(self.ui.txt_bomba_peris_C.text())

                self.ui.txt_q_real.setText(str(qreal * 0.8))

                temp_satur_str = self.ui.txt_temp_saturation.text()
                temp_satur = float(temp_satur_str) if temp_satur_str else 0.0

                self.ui.txt_temp_C.setText(str(temp_satur * 2))
                tpruba_str = self.ui.txt_temp_C.text()

                # Convierte los valores de texto a números flotantes
                tpruba = float(tpruba_str) if tpruba_str else 0.0

                self.ui.txt_v_preb_C.setText(str(qreal * tpruba))
                vprueba_str = self.ui.txt_v_preb_C.text()

                # Convierte los valores de texto a números flotantes
                vprueba = float(vprueba_str) if vprueba_str else 0.0

                if vprueba != 0.0:
                    self.ui.txt_vtotal_solution_C.setText(str(masat / vprueba))
                else:
                    self.ui.txt_vtotal_solution_C.setText(str(0))


    def on_combobox_activated(self, index):
        self.selected_option = self.ui.cmb_prueba.itemText(index)

        # Realiza las acciones deseadas según la opción seleccionada
        if self.selected_option == "Saturación":
           self.ui.stackedWidget.setCurrentIndex(0)
        elif self.selected_option == "Continuo":
           self.ui.txt_ms_total_C.setText(self.ui.txt_ms_total.text())
           self.ui.stackedWidget.setCurrentIndex(1)
        else:
            # Acción para otras opciones
            print("Opción seleccionada:", self.selected_option)

    def cronometro_funtion(self):
        """"""
        # Envía el botón al fondo

        duracion_m = int(self.ui.sb_duracion_m.value())
        captura_s = int(self.ui.sb_captura_s.value())
        espera_m = int(self.ui.sb_espera_m.value())

        # Validación y eliminación de objetos existentes de las gráficas y layouts
        if hasattr(self, 'grafica1'):
            self.ui.grafica_temperaturas.removeWidget(self.grafica1)
            self.grafica1.deleteLater()

        if hasattr(self, 'grafica2'):
            self.ui.grafica_temperaturas_3.removeWidget(self.grafica2)
            self.grafica2.deleteLater()

        if hasattr(self, 'grafica3'):
            self.ui.grafica_temperaturas_4.removeWidget(self.grafica3)
            self.grafica3.deleteLater()

        if hasattr(self, 'grafica4'):
            self.ui.grafica_temperaturas_5.removeWidget(self.grafica4)
            self.grafica4.deleteLater()

        self.ui.txt_area_tiempos.clear()
        self.ui.txt_area_temperaturas.clear()

        if self.puerto_ardui == None:
            self.mostrarMensajeinformation("Por favor configura el puerto de Arduino.\nSi el puerto no aparece, cierre y abra de nuevo el programa, pero recuerde tener conectado el Arduino USB a su computadora.")
            return

        self.data_sensors = {'sensor1': [],'sensor2': [],'sensor3': [],'sensor4': []}
        self.ui.btn_inicio_config.lower()
        self.bool_check = False

        self.borrar_archivos_txt_en_carpeta("data_sensors")
        lbl_minutos = self.ui.lbl_cronometro
        self.cronometro.iniciar_cronometro(100000, lbl_minutos)

        # Creación de nuevos objetos de las gráficas
        self.grafica1 = Canvas_grafica(str(self.sensores[0] + " Temperatura del fluido"), '#ff6c13')
        self.grafica2 = Canvas_grafica(str(self.sensores[1] + " Temperatura ambiente"), '#71ceff')
        self.grafica3 = Canvas_grafica(str(self.sensores[2] + " Temperatura superior"), '#009d1e')
        self.grafica4 = Canvas_grafica(str(self.sensores[3] + " Temperatura inferior"), '#FFD700')

        # Creación y ejecución del hilo para los datos de absorción
        thread = threading.Thread(target=self.datos_absorcion_temp, args=(duracion_m, captura_s, espera_m))
        thread.start()

        # Agregar las nuevas gráficas a los layouts correspondientes
        self.ui.grafica_temperaturas.addWidget(self.grafica1)
        self.ui.grafica_temperaturas_3.addWidget(self.grafica2)
        self.ui.grafica_temperaturas_4.addWidget(self.grafica3)
        self.ui.grafica_temperaturas_5.addWidget(self.grafica4)

    def detener_cronometro(self):
        if self.bool_check == False:
           resp = self.detener_experimentacion()
           if resp:
              self.cronometro.detener_cronometro()
        else:
            self.cronometro.detener_cronometro()

    def borrar_archivos_txt_en_carpeta(self,carpeta):
        try:
            # Obtenemos la lista de archivos en la carpeta
            archivos = os.listdir(carpeta)
            for archivo in archivos:
                # Verificamos si el archivo tiene la extensión ".txt"
                if archivo.endswith(".txt"):
                    # Construimos la ruta completa al archivo
                    ruta_archivo = os.path.join(carpeta, archivo)
                    # Eliminamos el archivo
                    os.remove(ruta_archivo)
            print("Archivos TXT borrados exitosamente.")
        except Exception as e:
            print(f"Error al borrar archivos: {e}")

    def datos_absorcion_temp(self,duracion_m,captura_s,espera_m):
        vals = True
        sum1 = 0
        count1 = 0
        sum2 = 0
        count2 = 0
        sum3 = 0
        count3 = 0
        sum4 = 0
        count4 = 0
        minutos = 0
        """"""
        numfile = 0
        numsperam = espera_m
        file_name = f"data_sensors/temperaturas_{numfile}.txt"

        """
        file_name = None
        if self.selected_option == "Saturación":
            file_name = f"data_sensors/temperaturas_S{numfile}.txt"
        if self.selected_option == "Continuo":
            file_name = f"data_sensors/temperaturas_C{numfile}.txt"
        """
        self.ser = serial.Serial(self.puerto_ardui, baudrate=9600)
        
        while True:
            cronometro_texto = self.ui.lbl_cronometro.text()
            minutos_str, segundos_str = cronometro_texto.split(":")
            minutos = int(minutos_str)
            segundos = int(segundos_str)
            with open(file_name, "a") as file:
                rawString = self.ser.readline().strip()
                partes = [item.decode() for item in rawString.split()]  # ['sensor1', '-127.00']
                
                # Verifica si partes tiene al menos dos elementos antes de intentar acceder a partes[1]
                if len(partes) >= 2:
                    try:
                        valor_sensor = float(partes[1])
                    except ValueError as e:
                        print("Error al convertir el valor del sensor a un número flotante:", e)
                        continue  # Otra opción podría ser hacer algo diferente en lugar de continuar, dependiendo de tus necesidades
                else:
                    print("La lista 'partes' no tiene suficientes elementos para acceder a partes[1]")
                    continue  # Otra opción podría ser hacer algo diferente en lugar de continuar, dependiendo de tus necesidades

                if self.bool_check:
                    self.grafica1.close_plt()
                    self.grafica2.close_plt()
                    self.grafica3.close_plt()
                    self.grafica4.close_plt()
                    self.ser.close()
                    break

                if not self.cronometro.getter_cronometro_status():
                    self.grafica1.close_plt()
                    self.grafica2.close_plt()
                    self.grafica3.close_plt()
                    self.grafica4.close_plt()
                    self.ser.close()
                    break
                if partes[0] == self.sensores[0]:
                    a = 1.0069
                    b = -1.058
                    tem = (a * float(partes[1])) + b
                    partes[1] = str(round(tem,2))
                    self.ui.lbl_sensor1.setText(str(partes[1])+ " ºC")
                    self.grafica1.obtener_temperatura_desde_arduino(partes)
                    sum1 += float(partes[1])
                    count1 += 1
                if partes[0] == self.sensores[1]:
                    a = 1.0104
                    b = -0.593
                    tem = (a * float(partes[1])) + b
                    partes[1] = str(round(tem,2))
                    self.ui.lbl_sensor2.setText(str(partes[1])+ " ºC")
                    self.grafica2.obtener_temperatura_desde_arduino(partes)
                    sum2 += float(partes[1])
                    count2 += 1
                if partes[0] == self.sensores[2]:
                    a = 1.016
                    b = -1.3995
                    tem = (a * float(partes[1])) + b
                    partes[1] = str(round(tem,2))
                    self.ui.lbl_sensor3.setText(str(partes[1])+ " ºC")
                    self.grafica3.obtener_temperatura_desde_arduino(partes)
                    sum3 += float(partes[1])
                    count3 += 1
                if partes[0] == self.sensores[3]:
                    a = 1.0069
                    b = -0.3571
                    tem = (a * float(partes[1])) + b
                    partes[1] = str(round(tem,2))
                    self.ui.lbl_sensor4.setText(str(partes[1])+ " ºC")
                    self.grafica4.obtener_temperatura_desde_arduino(partes)
                    sum4 += float(partes[1])
                    count4 += 1

                if segundos < captura_s and vals:
                    file.write(" ".join(partes) + "\n")
                    self.datos_actualizados.emit(str(partes))
                else: 
                    vals = False

                if minutos == espera_m:
                    espera_m += numsperam                    
                    self.actualizar_txt_area_tiempos(str(captura_s)+" : "+self.ui.lbl_cronometro.text()+" Tiempo - "+str(numfile))
                    self.datos_actualizados.emit("\n")
                    numfile += 1
                    vals = True
                    """
                    if self.selected_option == "Saturación":
                        file_name = f"data_sensors/temperaturas_S{numfile}.txt"
                        self.exp_data['saturacion'].append(float((sum4 / count4) if count4 != 0 else 0))
                    if self.selected_option == "Continuo":
                        file_name = f"data_sensors/temperaturas_C{numfile}.txt"
                        self.exp_data['continua'].append(float((sum4 / count4) if count4 != 0 else 0))
                    
                    """
                    file_name = f"data_sensors/temperaturas_{numfile}.txt"

                    self.data_sensors['sensor1'].append(float((sum1 / count1) if count1 != 0 else 0))
                    self.data_sensors['sensor2'].append(float((sum2 / count2) if count2 != 0 else 0))
                    self.data_sensors['sensor3'].append(float((sum3 / count3) if count3 != 0 else 0))
                    self.data_sensors['sensor4'].append(float((sum4 / count4) if count4 != 0 else 0))
                    #espero el tiempo necesario para hacer una captura en el tiempo siguiente
                    print("º")

                print(str(minutos)+" ------ "+str(duracion_m))
                if minutos == duracion_m:
                   self.ser.close()
                   print("-")
                   break
                   
            #time.sleep(0.15)

    # Definir un slot para recibir la señal y actualizar el QTextEdit en el hilo principal
    @pyqtSlot(str)
    def actualizar_txt_area_temperaturas(self, datos):
        self.ui.txt_area_temperaturas.appendPlainText(datos)

    @pyqtSlot(str)
    def actualizar_txt_area_tiempos(self, datos):
        self.ui.txt_area_tiempos.appendPlainText(datos)

    def mostrarMensajeinformation(self, msj):
        QMessageBox.information(self, "Información", msj)

    def mostrarMensajeError(self, msj):
        QMessageBox.warning(self, "Error", msj)

    def limitarLongitudTextField(self, maxLength, textField, id_text):
        textField.textChanged.connect(lambda: self.onTextChanged(textField, maxLength, id_text))

    def onTextChanged(self, textField, maxLength, id_text):
        text = textField.text()
        if len(text) > maxLength:
            textField.setText(text[:maxLength])
        elif id_text == 1:
            textField.setText(text.upper())
        elif id_text == 2:
            decimal_pattern = r'^\d*\.?\d*$'
            if not re.match(decimal_pattern, text):
                # Filtrar caracteres no válidos para números decimales
                filtered_text = re.sub(r'[^0-9.]', '', text)
                # Eliminar puntos adicionales
                filtered_text = filtered_text.replace('.', '', filtered_text.count('.') - 1)
                textField.setText(filtered_text)

if __name__ == "__main__":
     # Registra el tipo de datos QTextBlock
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())

# agregar si hay cambios en la vista de este controller:
# import resources.images.fondos.images_colum_rc