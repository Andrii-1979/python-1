import sys
import re

def calculate(file_in,file_out):

    """
    Return a file with table after evaluation table from another file
    """

    # Чтение файла построчно в список. Файл берется из папки с программой.
    with open(sys.path[0]+'/'+file_in,'rt') as file:
        d = file.read()
    lines = d.split('\n')
    
    # Удаление пустой строки - если в конце файла есть лишний переход на строку. 
    if lines[-1] == '': lines.pop() 

    # Создание списка с табуляцией столбцов
    tab_in = {0}
    for line in lines:
        for i in range(len(line)):
            if i > 0 and line[i-1] == ' ' and line[i] != ' ':
                tab_in.add(i)
    tab_in = list(tab_in)
    tab_in.sort()

    # Вспомогательная функция - создание литерала номера столбца
    def f(x):
        cell = ''
        while x > -1:
            a, b = divmod(x,26)
            cell = chr(b+65)+cell
            x = a-1
        return cell

    # Заполнение словаря исходной таблицей
    ss_in = {}
    k_in = set()
    for column in range(len(tab_in)):
        for row in range(len(lines)):
            cell = f(column)+str(row+1)
            if column == len(tab_in)-1:
                ss_in[cell] = lines[row][tab_in[column]:].rstrip()
            else:
                ss_in[cell] = lines[row][tab_in[column]:tab_in[column+1]].rstrip()
    
    # 1-ый проход расчета таблицы - без подстановки значений ссылочных ячеек
    # с обнаружением синтаксических ошибок.
    ss_out = {}
    k_ch = {}
    k_in = set(ss_in.keys())
    for k in k_in:
        s = ss_in[k]
        if s.startswith("'"):
            ss_out[k] = s[1:]
            del ss_in[k]
        elif s.isdigit():
            ss_out[k] = s
            del ss_in[k]
        elif s == '':
            ss_out[k] = ''
            del ss_in[k]
        elif s.startswith('='):
            k_ch[k] = list(set(re.findall('[A-Z]+[0-9]+',s)))
        else:
            ss_out[k] = '#se' # syntax error
            del ss_in[k]
            
    # 2-ой и последующие проходы расчета таблицы - подстановка значений
    # ссылочных ячеек и вычисление выражений, обнаружение ошибок.
    d = {'+','-','*','/','.'}.union(set(range(10)))
    k_in = set(ss_in.keys())
    k_in_new = k_in.copy()
    k_in_new.add('0') # Изменение k_in_new - только перед 2-ым проходом
    while ss_in != {} and k_in != k_in_new:
        k_in = set(ss_in.keys())
        for k in k_in:
            if k in k_ch:
                change = k_ch[k][:]
            if change != []:
                for s in change:
                    if s in ss_out: 
                        ss_in[k] = ss_in[k].replace(s, ss_out[s])
                        k_ch[k].remove(s)
                    else:
                        if s not in ss_in: 
                            ss_out[k] = '#cne' # cell not exist
                            del ss_in[k]
                            del k_ch[k]
                if k not in ss_out:
                    if (set(ss_in[k])).issubset(d):
                        #del ss_in[k]
                        del k_ch[k]
                    
            elif change == []:
                try:
                    ss_out[k] = str(eval(ss_in[k][1:]))
                except ZeroDivisionError:
                   ss_out[k] = '#zde' # zero division error
                except Exception:
                    ss_out[k] = '#eoc' # error of calculation
                del ss_in[k]
                del k_ch[k]
        k_in_new = set(ss_in.keys())
    if k_in == k_in_new and ss_in != {}:
        ss = ss_in.copy()
        for k in ss:
            ss_out[k] = '#clc' # cicled link to cell
            del ss_in[k]
            del k_ch[k]

    # Расчет ширины столбцов для результирующей таблицы
    space = 2 # Количество пробелов между столбцами в конечной таблице
    size = []
    for column in range(len(tab_in)-1):
        max = 1
        for row in range(len(lines)):
            cell = f(column)+str(row+1)
            if max < len(ss_out[cell]):
                max = len(ss_out[cell])
        size.append(max + space)

    # Запись результирующей таблицы в файл - в папке с программой
    with open(sys.path[0]+'/'+file_out,'wt') as file:         
        for row in range(len(lines)):
            a=''
            for column in range(len(tab_in)):
                cell = f(column)+str(row+1)
                if column == len(tab_in)-1:
                    a = a + ss_out[cell]
                else:
                    a = a + ss_out[cell].ljust(size[column])
            file.writelines(a+'\n')

if __name__ == '__main__':
    file_in = input('Введите название файла с исходной таблицей - ')
    file_out = input('Введите название файла для записи результирующей таблицы - ')
    calculate(file_in, file_out)
    print('Расчеты и запись таблицы завершены.')

