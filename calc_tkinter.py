from tkinter import *


class Calculator():
    def __init__(self, first_num='0', second_num='0', operator=''):
        self.first_num = first_num
        self.second_num = second_num
        self.operator = operator

    def add(self):
        return round((float(self.first_num) + float(self.second_num)), 4)

    def sub(self):
        return round((float(self.first_num) - float(self.second_num)), 4)

    def mult(self):
        return round((float(self.first_num) * float(self.second_num)), 4)

    def div(self):
        try:
            return round((float(self.first_num) / float(self.second_num)), 4)
        except:
            return 'ERROR'


def press_button(num):
    typed_num = e.get()
    e.delete(0, END)
    e.insert(0, str(typed_num) + str(num))


def operate(calc, op):
    if e.get():
        calc.first_num = e.get()
        calc.operator = op
        e.delete(0, END)
    else:
        calc.first_num = '0'
        calc.operator = op


def _eql(calc):
    if calc.operator == '+':
        calc.second_num = e.get()
        e.delete(0, END)
        e.insert(0, str(calc.add()))
    if calc.operator == '-':
        calc.second_num = e.get()
        e.delete(0, END)
        e.insert(0, str(calc.sub()))
    if calc.operator == '*':
        calc.second_num = e.get()
        e.delete(0, END)
        e.insert(0, str(calc.mult()))
    if calc.operator == '/':
        calc.second_num = e.get()
        e.delete(0, END)
        e.insert(0, str(calc.div()))
    else:
        pass


def _clr(calc):
    e.delete(0, END)
    calc.first_num = '0'
    calc.second_num = '0'
    calc.operator = ''


my_calc = Calculator()
root = Tk()
root.title("Calculator")
root.option_add('*Font', 'Calibri')
root.minsize(415, 450)
root.maxsize(415, 500)
e = Entry(borderwidth=15, width=30)

button_0 = Button(text='0', command=lambda: press_button(0), padx=35, pady=25)
button_1 = Button(text='1', command=lambda: press_button(1), padx=35, pady=25)
button_2 = Button(text='2', command=lambda: press_button(2), padx=35, pady=25)
button_3 = Button(text='3', command=lambda: press_button(3), padx=35, pady=25)
button_4 = Button(text='4', command=lambda: press_button(4), padx=35, pady=25)
button_5 = Button(text='5', command=lambda: press_button(5), padx=35, pady=25)
button_6 = Button(text='6', command=lambda: press_button(6), padx=35, pady=25)
button_7 = Button(text='7', command=lambda: press_button(7), padx=35, pady=25)
button_8 = Button(text='8', command=lambda: press_button(8), padx=35, pady=25)
button_9 = Button(text='9', command=lambda: press_button(9), padx=35, pady=25)
button_point = Button(
    text='.', command=lambda: press_button('.'), padx=35, pady=25)
button_add = Button(
    text='+', command=lambda: operate(my_calc, '+'), padx=35, pady=25)
button_sub = Button(
    text='-', command=lambda: operate(my_calc, '-'), padx=25, pady=25)
button_mult = Button(
    text='*', command=lambda: operate(my_calc, '*'), padx=25, pady=25)
button_div = Button(
    text='/', command=lambda: operate(my_calc, '/'), padx=25, pady=25)
button_eql = Button(text='=', command=lambda: _eql(my_calc), padx=25, pady=25)
button_clr = Button(text='C', command=lambda: _clr(my_calc), padx=25, pady=25)


button_0.grid(row=4, column=1)
button_1.grid(row=1, column=0)
button_2.grid(row=1, column=1)
button_3.grid(row=1, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_7.grid(row=3, column=0)
button_8.grid(row=3, column=1)
button_9.grid(row=3, column=2)
button_point.grid(row=4, column=2)

button_add.grid(row=4, column=0)
button_sub.grid(row=1, column=3)
button_mult.grid(row=2, column=3)
button_div.grid(row=3, column=3)
button_eql.grid(row=4, column=3)
button_clr.grid(row=0, column=3)

e.grid(row=0, column=0, columnspan=3)
root.mainloop()
