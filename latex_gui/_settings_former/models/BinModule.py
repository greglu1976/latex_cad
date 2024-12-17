class BinModule: # Функция
    def __init__(self, inputs=None, inserted_in_slot=None, type=None):
        self.inputs = inputs or []  # Более лаконичный способ
        self.inserted_in_slot = inserted_in_slot  # Добавляем переменную inserted_in_slot
        self.type = type  # Добавляем переменную type

    def add_input(self, input_obj):
        self.inputs.append(input_obj)

    def to_dict(self):
        result = {
            "type": self.type,
            "inserted_in_slot": self.inserted_in_slot,
            "inputs": {}
        }
        for i, item in enumerate(self.inputs):
            key = f"Дискретный вход {i+1}"
            result["inputs"][key] = item.to_dict()
        return result

    def __str__(self):
        result = f"BinModule (Slot: {self.inserted_in_slot}, Type: {self.type}):\n"
        for i, item in enumerate(self.inputs):
            result += f"Input {i+1}:\n{item}\n"
        return result

    def __len__(self):
        return len(self.inputs)  # Полезный метод для подсчета входов

    # Методы для работы с переменными inserted_in_slot и type
    def set_slot(self, slot):
        self.inserted_in_slot = slot

    def get_slot(self):
        return self.inserted_in_slot

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type        


class BinModules: # Функциональный блок
    def __init__(self, name=None):
        self.modules = []
        self.name = name  # Добавляем переменную name

    def add_module(self, module):
        self.modules.append(module)

    def to_dict(self):
        result = {
            "name": self.name,  # Добавляем имя в словарь
            "modules": {}
        }
        for i, module in enumerate(self.modules):
            key = f"Модуль {i+1}"
            result["modules"][key] = module.to_dict()
        return result

    def __str__(self):
        result = f"BinModules (Name: {self.name}):\n"
        for i, module in enumerate(self.modules):
            result += f"Module {i+1}:\n{module}\n"
        return result

    def __len__(self):
        return len(self.modules)

    # Методы для работы с переменной name
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Prot:  # Устройство РЗА
    def __init__(self):
        self.bin_modules = []  # Список объектов BinModules

    def add_bin_module(self, bin_module):
        self.bin_modules.append(bin_module)

    def to_dict(self):
        result = {}
        for i, bin_module in enumerate(self.bin_modules):
            key = f"Функциональный блок {i+1}"
            result[key] = bin_module.to_dict()
        return result

    def __str__(self):
        result = "Prot:\n"
        for i, bin_module in enumerate(self.bin_modules):
            result += f"Функциональный блок {i+1}:\n{bin_module}\n"
        return result

    def __len__(self):
        return len(self.bin_modules)

