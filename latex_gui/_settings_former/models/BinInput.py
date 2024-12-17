class BinInput:
    def __init__(self, properties, name=None):
        self.properties = properties
        self.name = name  # Добавляем переменную name

    def to_dict(self):
        #result = self.properties.copy()
        #result['name'] = self.name  # Добавляем имя в словарь

        result = {
            "name": self.name,
            "properties": self.properties.copy(),
        }
        return result

    #def __str__(self):
        #return "\n".join([f"{key}: {value}" for key, value in self.properties.items()])

    def __str__(self):
        return str(self.to_dict()) 

    # Методы для работы с переменной name
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

