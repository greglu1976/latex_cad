# Временное решение для тестирования устройства

from models.BinInput import BinInput
from models.BinModule import BinModule, BinModules

def create_reg():
    properties = {
        'Status': {
            'name': 'УРОВ смежной секции',
            'fsu': 'УРОВ СС',
            'log': 'SGF1',
            'oscill_start': '0 = Не предусмотрено\n1 = Предусмотрено',
            'oscill_reg': '-',
        },
        'Mode': {
            'name': 'Защита автотрансформатора',
            'fsu': 'Защита АТ',
            'log': 'SGF1',
            'oscill_start': '0 = Не предусмотрено\n1 = Предусмотрено',
            'oscill_reg': '-',
        },
        'Mode2': {
            'name': 'Защита автотрансформатора',
            'fsu': 'Защита АТ',
            'log': 'SGF1',
            'oscill_start': '0 = Не предусмотрено\n1 = Предусмотрено',
            'oscill_reg': '-',
        },              
    }

    input1 = BinInput(properties, 'Общие сигналы')
    input2 = BinInput(properties, 'Сигналы ФСУ')


    # Создаем функциональный блок  и добавляем входы(функции)
    module = BinModule(inserted_in_slot='-', type='Максимальная токовая защита (МТЗ)')
    module.add_input(input1)
    module.add_input(input2)



    # Получаем словарь для использования в шаблоне Jinja
    module_dict = module.to_dict()

    return module_dict

if __name__ == '__main__':
    t = create_reg()
    print(t)
