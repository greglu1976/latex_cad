
intro_strs = []

intro_strs.append("\phantomsection"+"\n") # чтобы правильно генерировать ссылку
intro_strs.append("\color{uniblue}\section*{\centering{\large{ПЕРЕЧЕНЬ СОКРАЩЕНИЙ}\color{white!0}<BEGABBRS>}}"+"\n") # в соответствии с ГОСТ 7.32 
intro_strs.append("\\addcontentsline{toc}{section}{Перечень сокращений}"+"\n") # строка для включения в содержание
intro_strs.append("\color{black}"+"\n")

intro_strs.append('\\begin{longtable}{>{\\raggedright\\arraybackslash}m{2cm}>{\\raggedright\\arraybackslash}m{0.5cm}>{\\raggedright\\arraybackslash}m{20cm}}'+'\n')
intro_strs.append('\endfirsthead\endhead\endfoot\endlastfoot'+'\n')

outro_strs = []
outro_strs.append('\end{longtable}')