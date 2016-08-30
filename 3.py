import webbrowser
from tkinter import *
import time

def timer():
    lab.configure(text='sfsdfsdfsdfsdfsdf')
    a = int(text.get('1.0',END).replace('\n',''))
    a=a*60
    print(a)
    for i in range(a):
        time.sleep(1)
        #lab.configure(text=str(a-i))
    webbrowser.open_new('https://www.youtube.com/watch?v=jCrXuES9vx0&list \
=PLfsXA58dNtiNmPxZZXMTT5zJMYZ_jjHH3&index=8')
    lab.configure(text='Сработал таймер!')

root = Tk()
#root.geometry('100x60+30+50')
root.title('Таймер')

frame = Frame()
text = Text(frame, height = 1, width = 4, font = 'arial 20')
but = Button(frame,text='Запуск', command = timer)
lab = Label(text='')






frame.pack()
text.pack()
but.pack()
lab.pack()
root.mainloop()
