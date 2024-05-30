# сборка под ubuntu
#pyinstaller --noconfirm --onefile --windowed --hidden-import='PIL._tkinter_finder' --add-data "/home/greglu/www2/latex_cad/latex_gui/assets:assets/" main2.py
# Версия 0.2 от 28.05.24 - вроде все работает
# Версия 0.3 от 29.05.24 - добавлен парсинг строк типв 1(5) в xlsx

from datetime import datetime
from random import choices
import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

import sys
import os

from logger import logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from _get_abbrs.main import start_abbr
from _renew_tables.main import start_renew_tables
from _blanc_maker.main import start_renew_tables_blanc
from _renew_sum_table.main import start_renew_sum_table

from add_scripts import rebuild, tex_opener, pdf_opener

PATH = Path(__file__).parent / 'assets'


class BackMeUp(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.setvar('folder-path', '')
        

        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-to-backup-dark': 'icons8_add_folder_24px.png',
            'add-to-backup-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'logo': 'backup.png',
            'renew-abbrs': 'icons8-long-icon-48px.png',
            'renew-tables': 'icons8-renew-tables-48px.png',
            'open-pdf': 'icons8-pdf-2-48.png',
            'open-tex': 'icons8-tex-48.png',
            'goose': 'icons8-goose2-48.png',
            'reports': 'icons8-reports-48.png',
        }

        

        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        # buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        ## backup
        #_func = lambda: Messagebox.ok(message='Backing up...')
        _func = lambda: check_radio_values()       
        btn = ttk.Button(
            master=buttonbar, 
            text='Пакетное выполнение скриптов с опциями', 
            image='play', 
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## rebuild
        _func = lambda: rebuild_tex(self.getvar('folder-path'))
        btn = ttk.Button(
            master=buttonbar, 
            text='Пересобрать проект', 
            image='refresh',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## stop
        _func = lambda: Messagebox.ok(message='Stopping backup.')
        btn = ttk.Button(
            master=buttonbar, 
            text='Stop', 
            image='stop-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## settings
        _func = lambda: Messagebox.ok(message='Changing settings')
        btn = ttk.Button(
            master=buttonbar, 
            text='Settings', 
            image='properties-light',
            compound=LEFT, 
            command=_func
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

#----------------------------------LEFT PANEL ----------------------------------------

        # left panel
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)


        ## backup summary (collapsible)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill=X, pady=1)

        ## container
        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(
            child=bus_frm, 
            title='Быстрый запуск скриптов', 
            bootstyle=SECONDARY)

    
        ## properties button
        _func = lambda: get_abbrs(self.getvar('folder-path'))
        bus_prop_btn = ttk.Button(
            master=bus_frm, 
            text='Обновить перечень сокращений (РЭ)', 
            image='renew-abbrs', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        bus_prop_btn.grid(row=4, column=0, columnspan=2, sticky=W)

        ## add to backup button
        _func = lambda: _renew_tables(self.getvar('folder-path'))
        add_btn = ttk.Button(
            master=bus_frm, 
            text='Обновить таблицы (РЭ)', 
            image='renew-tables', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        add_btn.grid(row=5, column=0, columnspan=2, sticky=W)

        ## properties button
        _func = lambda: _renew_sum_table(self.getvar('folder-path'))
        run_newA_btn = ttk.Button(
            master=bus_frm, 
            text='Обновить суммарную таблицу сигналов (РЭ, Прил.А)', 
            image='reports', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        run_newA_btn.grid(row=6, column=0, columnspan=2, sticky=W)

        ## add to backup button
        _func = lambda: _renew_tables_blanc(self.getvar('folder-path'))
        add_btn = ttk.Button(
            master=bus_frm, 
            text='Обновить таблицы (бланк уставок)', 
            image='renew-tables', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        add_btn.grid(row=7, column=0, columnspan=2, sticky=W)


        ## properties button
        _func = lambda: Messagebox.ok(message='Changing properties')
        run_newB_btn = ttk.Button(
            master=bus_frm, 
            text='Обновить отчет по GOOSE', 
            image='goose', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        run_newB_btn.grid(row=8, column=0, columnspan=2, sticky=W)


        ## properties button
        _func = lambda: open_pdf(self.getvar('folder-path'))
        open_pdf_btn = ttk.Button(
            master=bus_frm, 
            text='Открыть PDF', 
            image='open-pdf', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        open_pdf_btn.grid(row=9, column=0, columnspan=2, sticky=W)

        ## properties button
        _func = lambda: open_tex(self.getvar('folder-path'))
        open_pdf_btn = ttk.Button(
            master=bus_frm, 
            text='Открыть TEX', 
            image='open-tex', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        open_pdf_btn.grid(row=10, column=0, columnspan=2, sticky=W)



#----------------------------------RIGHT PANEL ----------------------------------------
        # right panel
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        ## file input
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side=TOP, fill=X, padx=2, pady=1)

        file_entry = ttk.Entry(browse_frm, textvariable='folder-path')
        file_entry.pack(side=LEFT, fill=X, expand=YES)

        btn = ttk.Button(
            master=browse_frm, 
            image='opened-folder', 
            bootstyle=(LINK, SECONDARY),
            command=self.get_directory
        )
        btn.pack(side=RIGHT)

#################################
        my_frame = ttk.Frame(right_panel, bootstyle=SECONDARY)
        my_frame.pack(side='left', fill=BOTH, expand=YES, padx=10, pady=10)


        edge = ttk.Labelframe(
            master=my_frame,
            text='Опции',
            padding=(20, 5)
        )
        edge.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        radio_options = [
            'Обновить перечень сокращений', 'Обновить таблицы к функциям', 'Обновить приложение А (сигналы)',
            'Обновить приложение В (ФСУ)', 'Обновить и открыть pdf'
        ]
        # Создаем переменные для радио-кнопок
        self.radio_vars = {opt: ttk.StringVar(value='0') for opt in radio_options}        

        # add radio buttons to each label frame section
        for section in [edge]:
            for opt in radio_options:
                cb = ttk.Checkbutton(section, text=opt, state=NORMAL)
                cb.invoke()
                cb.pack(side=TOP, pady=2, fill=X)

        # Функция для проверки значений радио-кнопок
        def check_radio_values():
            result = Messagebox.okcancel(message='Запуск скриптов по обновлению...', title="Message")
            print(result)
            if result == "Cancel":
                return
            print('let us go!!')


################################## ЗАПУСК ПОИСКА АББРЕВИАТУР #################################################
        def get_abbrs(filepath):
            """Open dialogue to get filename and update variable"""
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return
            if not os.path.isfile(filepath+'/general.pdf'):
                Messagebox.show_error(message='В указанной папке нет файла general.pdf. Пересоберите проект', title="Ошибка")
                return  
            result = start_abbr(filepath)
            if result=='noabbrs':
                Messagebox.show_info(message='Нет распознанных абревиатур в general.pdf', title="Предупреждение")
                return
            if result=='ok':
                Messagebox.show_info(message='Успешная генерация файла аббревиатур toa_general.tex', title="Информация")
                return             
            return
################################## КОНЕЦ ПОИСКА АББРЕВИАТУР ###############################################
################################## ОБНОВЛЯЕМ ТАБЛИЦЫ РЭ ##################################################
        def _renew_tables(filepath):
            """Open dialogue to get filename and update variable"""
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return            
            if not os.path.isfile(filepath+'/general.tex'):
                Messagebox.show_error(message='В указанной папке нет файла general.tex', title="Ошибка")
                return
            result = start_renew_tables(filepath)
            if result=='ok':
                Messagebox.show_info(message='Успешное обновление таблиц РЭ', title="Информация")
                return                         
################################## КОНЕЦ ОБНОВЛЯЕМ ТАБЛИЦЫ РЭ ##############################################
################################## НАЧАЛО ОБНОВЛЯЕМ ТАБЛИЦЫ БУ ##############################################
        def _renew_tables_blanc(filepath):
            """Open dialogue to get filename and update variable"""
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта бланка уставок (где файл general.tex)', title="Ошибка")
                return            
            if not os.path.isfile(filepath+'/general.tex'):
                Messagebox.show_error(message='В указанной папке нет файла general.tex', title="Ошибка")
                return
            result = start_renew_tables_blanc(filepath)
            if result == 'noblancdoc':
                Messagebox.show_error(message='В файле general.tex нет строки определения пути для РЭ', title="Ошибка")
                return
            if result == 'nofile':
                Messagebox.show_error(message='Файл не найден в текущем каталоге', title="Ошибка")
                return                              
            if result=='ok':
                Messagebox.show_info(message='Успешное обновление таблиц бланка уставок', title="Информация")
                return                         
################################## КОНЕЦ ОБНОВЛЯЕМ ТАБЛИЦЫ БУ ##############################################

################################## НАЧАЛО ОБНОВЛЯЕМ СУММАРНУЮ ТАБЛИЦУ ##############################################
        def _renew_sum_table(filepath):
            """Open dialogue to get filename and update variable"""
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return            
            if not os.path.isfile(filepath+'/general.tex'):
                Messagebox.show_error(message='В указанной папке нет файла general.tex', title="Ошибка")
                return
            result = start_renew_sum_table(filepath)
            if result[0] == 'error':
                Messagebox.show_error(message='Файл не найден в текущем каталоге', title="Ошибка")
                return                              
            if result[0]=='ok':
                Messagebox.show_info(message='Успешное обновление суммарной таблицы', title="Информация")
                return                         
################################## КОНЕЦ ОБНОВЛЯЕМ СУММАРНУЮ ТАБЛИЦУ ##############################################





################################## ОТКРЫВАЕМ PDF  ###############################################
        def open_pdf(filepath):
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return
            if not os.path.isfile(filepath+'/general.pdf'):
                Messagebox.show_error(message='В указанной папке нет файла general.pdf. Пересоберите проект', title="Ошибка")
                return             
            result = pdf_opener(filepath)
            return
################################## ОТКРЫВАЕМ PDF  ###################################################
################################## ОТКРЫВАЕМ TEX  ###################################################
        def open_tex(filepath):
            if not os.path.isfile(filepath+'/general.tex'):
                Messagebox.show_error(message='В указанной папке нет основного файла проекта general.tex', title="Ошибка")
                return             
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return
            result = tex_opener(filepath)
            return
################################## ОТКРЫВАЕМ TEX  ####################################################
################################## ПЕРЕСОБИРАЕМ ПРОЕКТ  ###############################################
        def rebuild_tex(filepath):
            #print(filepath)
            ans = Messagebox.okcancel(message='Пересобрать проект?', title="Информация")
            if ans == "Cancel":
                return            
            if not os.path.isfile(filepath+'/general.tex'):
                Messagebox.show_error(message='В указанной папке нет основного файла проекта general.tex', title="Ошибка")
                return                
            if filepath == '':
                Messagebox.show_error(message='Выберите рабочую папку проекта (где файл general.tex)', title="Ошибка")
                return
            result = rebuild(filepath)
            if result=='ok':
                Messagebox.show_info(message='Успешное пересборка проекта', title="Информация")                        
################################## ПЕРЕСОБИРАЕМ ПРОЕКТ ################################################


           
    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)


class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = [
            ttk.PhotoImage(file=PATH/'icons8_double_up_24px.png'),
            ttk.PhotoImage(file=PATH/'icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button 
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])



if __name__ == '__main__':

    app = ttk.Window("GUI Latex v0.3 29.05.24")
    #app.iconbitmap(os.path.join(PATH, 'icon.ico')) # для убунты не нужна эта строка
    BackMeUp(app)
    app.mainloop()
