# Создание шаблона разделов на основе шаблона origin.docx

from docxtpl import DocxTemplate
from tables import add_table_settings
from docx import Document

from add_sect_relay import add_sect_relay
from add_sect_binaries import add_sect_binaries

doc = Document('origin.docx')


add_sect_binaries(doc, 'Модули дискретных входов', 'bin_input' )
add_sect_binaries(doc, 'Модули дискретных выходов', 'bin_output' )

#add_sect_relay(doc, '1')


doc.save('templ2.docx')