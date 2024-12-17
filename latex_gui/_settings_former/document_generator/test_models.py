# заполнение шаблона данными

from docxtpl import DocxTemplate

from .relay import create_relay, create_binary, create_binary_outs, create_leds, create_fks, create_reg, get_general_data

from pathlib import Path

def starter_test_models(path_to_hw_ied):

    #root = Path(__file__).resolve().parents[1]
    #descriptions_path = root / "descriptions"
    general_data, versions = get_general_data(path_to_hw_ied)
    #doc = DocxTemplate(doc_path)
    doc = DocxTemplate('templ2.docx')
    #print('doc_path===', descriptions_path)
    # забираем словарь РЗА
    rza_funcs = create_relay()
    bin_inputs = create_binary()
    regs = create_reg()
    outs = create_binary_outs()
    leds = create_leds()
    fks = create_fks()

    #print('rza_funcs=================')
    #print(rza_funcs)
    #print('bin_inputs=================')
    #print(bin_inputs)
    #print('regs=================')
    #print(regs)
    #print('outs=================')
    #print(leds)
    #print('fks=================')
    #print(fks)

    # Заполнение шаблона данными
    context = {
        "versions": versions,
        "general_data": general_data,
        "bin_inputs": bin_inputs,
        "bin_outputs": outs,
        "rza_funcs": rza_funcs,
        "regs": regs,
        "leds": leds,
        "fks": fks,    
        }
    doc.render(context)

    #doc_path2 = templates_path / 'output.docx'
    # Сохранение документа
    doc.save('output.docx')