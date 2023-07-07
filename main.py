import pyodbc
import customtkinter
from tkinter import *
from tkcalendar import *
from tkinter import messagebox


def connection_database(driver='', server='', database='', username='', password='', trusted_connection='no'):

    connection_data = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TRUSTED_CONNECTION={trusted_connection};"

    connection = pyodbc.connect(connection_data)
    cursor = connection.cursor()
    return connection, cursor


connection, cursor = connection_database()

window = customtkinter.CTk()

window.geometry('700x500')
window.title("KrahSoft")
window.maxsize(width=900, height=550)
window.minsize(width=500, height=300)
window.resizable(width=False, height=False)
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

password = 'Krah@3118'


def updateContent():

    if password_input.get() == password:
        try:
            format_date_calendar = ''.join(
                filter(str.isalnum, calendar_text_input.get()))
            mes = format_date_calendar[2:4]
            ano = format_date_calendar[4:]
            dia = format_date_calendar[:2]
            format_date = ano + mes + dia
            cursor.execute(
                f'''
                    DECLARE @DTBLOQ VARCHAR (8)

                    SET @DTBLOQ = {format_date}

                    UPDATE SX6020

                    SET X6_CONTEUD = @DTBLOQ, X6_CONTSPA = @DTBLOQ, X6_CONTENG = @DTBLOQ

                    FROM SX6020

                    WHERE X6_VAR = 'MV_DBLQMOV'
                '''
            )
            connection.commit()
            messagebox.showinfo('Sistema', 'Data atualizada com sucesso')
            password_window.destroy()
        except pyodbc.DatabaseError:
            messagebox.showerror('Sistema', 'Erro ao tentar atualizar a data ')
    else:
        messagebox.showerror('Sistema', 'Senha incorreta')


def pick_up_password(event):
    global password_input, password_window

    if calendar_text_input.get() == '':
        messagebox.showwarning(
            'Sistema', 'O campo de data não pode estar vazio. Por favor preencha corretamente')
    else:
        password_window = customtkinter.CTkToplevel(window)
        password_window.geometry("630x350")
        password_window.maxsize(width=630, height=350)
        password_window.minsize(width=630, height=350)
        password_window.resizable(width=False, height=False)
        password_window.title('Coloque a senha')
        password_window.grab_set()
        label_password = customtkinter.CTkLabel(password_window, text='Digite sua senha', font=(
            'arial bold', 20)).place(x=30, y=140)
        password_input = customtkinter.CTkEntry(
            password_window, placeholder_text='Digite sua senha', show='*', width=250)
        password_input.place(x=200, y=140)
        button_password = customtkinter.CTkButton(
            password_window, text='Atualizar', command=updateContent)
        button_password.place(x=470, y=140)


def grab_date():
    calendar_text_input.delete(0, END)
    calendar_text_input.insert(0, calendar_input.get_date())
    date_window.destroy()


def pick_date_calendar(event):
    global calendar_input, date_window

    date_window = customtkinter.CTkToplevel(window)
    date_window.geometry("400x250")
    date_window.title('Escolha uma data')
    date_window.grab_set()
    calendar_input = Calendar(
        date_window, selectmode='day', date_pattern='dd/mm/y')
    calendar_input.pack(pady=12)

    submit_button = customtkinter.CTkButton(
        date_window, text='submit', command=grab_date).place(x=135, y=210)


label1 = customtkinter.CTkLabel(
    window, text='Atualização de data', font=('arial bold', 20)).place(x=30, y=180)

calendar_text_input = customtkinter.CTkEntry(
    window, placeholder_text='dia/mês/ano', width=250)
calendar_text_input.place(x=220, y=180)
calendar_text_input.bind('<1>', pick_date_calendar)

label2 = customtkinter.CTkLabel(window, text='Bloqueia fechamento', font=(
    'arial bold', 20)).place(x=30, y=300)

button1 = customtkinter.CTkButton(window, text='Atualizar')
button1.place(x=230, y=300)
button1.bind('<1>', pick_up_password)

window.mainloop()
