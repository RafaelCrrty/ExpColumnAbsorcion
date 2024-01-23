import xlwt
import os

class ExcelWriter:
    def __init__(self, output_excel_file):
        self.output_excel_file = output_excel_file
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet('Sensor Data')
        self.column_offset = 0
        self.column_order = ['sensor1', 'sensor2', 'sensor3', 'sensor4']
        
    def read_text_file(self, file_path):
        data = []
        current_entry = {}  # Inicializa un diccionario vacío para almacenar los datos actuales
        with open(file_path, 'r') as file:
            lines = file.readlines()
            sensor_order = ['sensor1', 'sensor2', 'sensor3', 'sensor4']
            sensor_index = 0  # Índice del sensor actual en el grupo
            for line in lines:
                line = line.strip()
                parts = line.split()
                if len(parts) == 2:
                    key, value = parts
                    current_entry[key] = float(value)
                    sensor_index += 1
                    if sensor_index == 4:
                        # Hemos recopilado lecturas de los cuatro sensores, agregamos la entrada actual
                        # y reiniciamos el diccionario y el índice
                        ordered_entry = {sensor: current_entry.get(sensor, 0.0) for sensor in sensor_order}
                        data.append(ordered_entry)
                        current_entry = {}
                        sensor_index = 0
                else:
                    # Si la línea no tiene el formato esperado, puedes manejarla de acuerdo a tus necesidades
                    print("Línea con formato no válido, se ignora:", line)
                    continue

            # Si al final del archivo todavía quedan lecturas pendientes, agrégalas con valores predeterminados
            if sensor_index > 0:
                while sensor_index < 4:
                    sensor_index += 1
                    ordered_entry = {sensor: current_entry.get(sensor, 0.0) for sensor in sensor_order}
                    data.append(ordered_entry)
        return data

    def write_excel_file(self, data):
        headers = list(data[0].keys())
        for col, header in enumerate(headers):
            self.sheet.write(0, col + self.column_offset, header)

        for row, entry in enumerate(data):
            for col, header in enumerate(headers):
                self.sheet.write(row + 1, col + self.column_offset, entry.get(header, ""))

    def count_text_files(self,folder_path):
        txt_files_count = 0
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                txt_files_count += 1
        return txt_files_count

    def txt_self_exel(self):
        count = self.count_text_files('data_sensors')
        print(str(count) + " - - - - - ")
        if count != 0:
            self.process_text_files(count)
            self.save_excel_file()

    def process_text_files(self, num_files):
        for i in range(num_files):
            print(i)
            text_file_path = f'data_sensors/temperaturas_{i}.txt'
            sensor_data = self.read_text_file(text_file_path)
            
            # Reorganiza los datos según el orden deseado de las columnas
            reordered_data = []
            for entry in sensor_data:
                reordered_entry = {key: entry[key] for key in self.column_order}
                reordered_data.append(reordered_entry)
            
            self.write_excel_file(reordered_data)
            self.column_offset += len(self.column_order) + 1 

    def save_excel_file(self):
        self.workbook.save(self.output_excel_file)
        print(f"Data successfully saved to {self.output_excel_file}")