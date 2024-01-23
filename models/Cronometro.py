from PyQt5.QtWidgets import QLabel
from threading import Thread
import time

class Cronometro:
    def __init__(self):
        self.start_time = 0
        self.total_time = 0
        self.running = False

    def iniciar_cronometro(self, minutos: int, lbl_minutos: QLabel):
        self.start_time = int(round(time.time() * 1000))
        self.total_time = minutos * 60 * 1000  # Convertir minutos a milisegundos
        self.running = True

        # Actualizar el cronómetro cada segundo
        def update_cronometro():
            while self.running:
                tiempo_transcurrido = int(round(time.time() * 1000)) - self.start_time

                # Verificar si se alcanzó el tiempo total establecido
                if tiempo_transcurrido >= self.total_time:
                    self.detener_cronometro()
                    tiempo_transcurrido = self.total_time

                # Calcular los minutos y segundos transcurridos
                minutos_transcurridos = int(tiempo_transcurrido / 1000 / 60)
                segundos_transcurridos = int(tiempo_transcurrido / 1000 % 60)

                # Actualizar el label con el tiempo transcurrido en minutos y segundos
            
                lbl_minutos.setText("{:02d}:{:02d}".format(minutos_transcurridos, segundos_transcurridos))

                time.sleep(1)  # Esperar 1 segundo antes de actualizar nuevamente

        cronometro_thread = Thread(target=update_cronometro)
        cronometro_thread.start()

    def detener_cronometro(self):
        self.running = False
    
    def getter_cronometro_status(self):
        return self.running

