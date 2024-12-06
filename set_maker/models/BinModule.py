class BinModule:
    def __init__(self, inputs=None):
        self.inputs = inputs or []  # Более лаконичный способ

    def add_input(self, input_obj):
        self.inputs.append(input_obj)

    def to_dict(self):
        result = {}
        for i, item in enumerate(self.inputs):
            key = f"Дискретный вход {i+1}"
            result[key] = item.to_dict()
        #for input_obj in self.inputs:
            #name = input_obj.properties['name_in_software']
            #result[name] = input_obj.to_dict()
        return result



    def __str__(self):
        result = "BinModule:\n"
        for i, item in enumerate(self.inputs):
            result += f"Input {i+1}:\n{item}\n"
        return result

    def __len__(self):
        return len(self.inputs)  # Полезный метод для подсчета входов