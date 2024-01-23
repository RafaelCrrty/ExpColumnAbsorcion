import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import numpy as np

class Canvas_grafica(FigureCanvas):
    def __init__(self, sensor, color, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=95, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)
        self.colors = color
        self.sensor = sensor
        self.tiempox = []
        self.temperaturay = []
        self.count = 0
        self.batch_size = 50  # Número de datos por lote
        self.start_index = 0  # Índice de inicio para cada grupo de datos

    def actualizar_temp(self, arrtemp):
        self.datos_arduino_grafica(arrtemp)

    def datos_arduino_grafica(self, arrtemp):
        temperatura = arrtemp
        self.tiempox.append(self.count)
        self.temperaturay.append(float(temperatura[1]))
        self.count += 1

        # Actualizar la gráfica cuando se tenga un múltiplo de batch_size de datos
        if self.count % self.batch_size == 0:
            self.ax.clear()
            self.ax.plot(
                self.tiempox[self.start_index:self.count],
                self.temperaturay[self.start_index:self.count],
                color=self.colors
            )
            self.ax.set_xlabel("Tiempo s")
            self.ax.set_ylabel("Temperatura")
            self.ax.set_title(self.sensor, size=9)
            self.draw()
            self.start_index = self.count

    def obtener_temperatura_desde_arduino(self, partes):
        self.actualizar_temp(partes)

    def close_plt(self):
        plt.close(self.fig)


class Canvas_grafica_promedios(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=100, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)

    def datos_arduino_grafica(self):
        # Realizar el ajuste lineal
        self.a, self.b = np.polyfit(self.xprueba, self.yppromedio, 1)
        
        # Generar los valores predichos por la recta ajustada
        ejey_pred = []
        for x in self.xprueba:
            y_pred =  self.a * x +  self.b
            ejey_pred.append(y_pred)

        # Graficar los puntos y la recta ajustada
        self.scatter_plotP = self.ax.scatter(self.xprueba,self.yppromedio, marker='D' , color='blue')       
        self.ax.plot(self.xprueba,ejey_pred,linestyle = '--', color='red')
        self.ax.set_xlabel("Pruebas")
        self.ax.set_ylabel("Promedios")
        self.ax.set_title("Calibración", size=9)
        self.draw()
        # Agregar leyenda

    def getter_a(self):
        return self.a
    
    def getter_b(self):
        return self.b

    def datos_prueba_(self, x_pruebas, y_promedios):
        self.limpiar_grafica()
        self.xprueba = x_pruebas
        self.yppromedio = y_promedios
        self.datos_arduino_grafica()

    def limpiar_grafica(self):
        self.ax.clear()
        self.draw()

    def close_plt(self):
        plt.close(self.fig)


class Canvas_grafica_exp(FigureCanvas):
    def __init__(self,temp,name,color, parent=None):
        self.fig, self.ax = plt.subplots(1, dpi=95, figsize=(5, 5), sharey=True, facecolor='white')
        super().__init__(self.fig)
        self.datos_arduino_grafica(temp,name,color)
       

    def datos_arduino_grafica(self,arrtemp,name,colors):
        self.limpiar_grafica()
        self.ax.plot(arrtemp, color=colors)
        self.ax.set_xlabel("Tiempo (minutos)")
        self.ax.set_ylabel("Temperatura")
        self.ax.set_title(name, size=9)
        self.draw()

    def limpiar_grafica(self):
        self.ax.clear()
        self.draw()

    def guardar_grafica_como_png(self, ruta):
        self.fig.savefig(ruta, format='png', dpi=300)

    def close_plt(self):
        plt.close(self.fig)  # Cierra