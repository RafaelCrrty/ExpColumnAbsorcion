
import serial.tools.list_ports

class ArduinoManager:
    def __init__(self):
        self.available_ports = self.get_available_ports()

    def get_available_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def get_total_ports(self):
        return len(self.available_ports)

    def connect_to_port(self, port_index: int):
        if port_index >= 0 and port_index < self.get_total_ports():
            selected_port = self.available_ports[port_index]
            try:
                return selected_port # retornando el puerto
            except serial.SerialException:
                return None
        else:
            return None

# Ejemplo de uso
"""
arduino_manager = ArduinoManager()
total_ports = arduino_manager.get_total_ports()
print(f"Total de puertos disponibles: {total_ports}")

# Supongamos que el usuario selecciona el primer puerto (índice 0)
selected_port_index = 0
arduino = arduino_manager.connect_to_port(selected_port_index)
if arduino:
    print(f"Conectado a {arduino.port}")

"""
