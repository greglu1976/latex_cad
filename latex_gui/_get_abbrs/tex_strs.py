
intro_strs = []

intro_strs.append("\color{uniblue}\section*{Перечень принятых сокращений}"+"\n")

intro_strs.append("\\addcontentsline{toc}{section}{Перечень принятых сокращений}"+"\n") # строка для включения в содержание
intro_strs.append("\color{black}"+"\n")

intro_strs.append('\\begin{longtable}{>{\\raggedright\\arraybackslash}m{2cm}>{\\raggedright\\arraybackslash}m{0.5cm}>{\\raggedright\\arraybackslash}m{20cm}}'+'\n')
intro_strs.append('\endfirsthead\endhead\endfoot\endlastfoot'+'\n')

outro_strs = []
outro_strs.append('\end{longtable}')