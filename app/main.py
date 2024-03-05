import os
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern, constants
from datetime import *
import time
import sqlite3

root = Tk()

class Functions():
    def variables(self):
        self.codigo = self.codigo_entry.get()
        self.data = self.dia_entry.get_date()
        self.hora_ini = self.hora_inicio_entry.hours24()
        self.hora_fim = self.hora_fim_entry.hours24()
        self.descricao = self.descricao_entry.get()
        self.status = self.status_entry.get()
        
    def limpar(self):
        self.codigo_entry.delete(0, END)
        self.descricao_entry.delete(0, END)
        self.status_entry.set('Local')
        
    def connect_db(self):
        print("Conectando ao banco...")
        self.connect = sqlite3.connect("C:\workspace\pentare\Appointment_Reminder\database.sqlite")
        self.cursor = self.connect.cursor()
        
    def disconnect_db(self):
        print("Desconectando do banco...")
        self.connect.close()
        
    def make_table(self):
        self.connect_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS apontamento (
                code INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE NOT NULL,
                hora_inicio INTEGER NOT NULL,
                hora_fim INTEGER NOT NULL,
                descricao CHAR(100),
                status CHAR(20)
            );
        """)
        self.connect.commit(); print("Banco de dados criado")
        self.select_appointment()
        self.disconnect_db()
        
    def add_appointment(self):
        self.variables()
        self.connect_db()
        
        self.cursor.execute(""" INSERT INTO apontamento (data, hora_inicio, hora_fim, descricao, status)
            VALUES (?, ?, ?, ?, ?) """, (self.data, self.hora_ini, self.hora_fim, self.descricao, self.status))
        
        self.connect.commit(); print("Apontamento", self.descricao," criado")
        self.disconnect_db()
        self.select_appointment()
        self.limpar()
        
    def select_appointment(self):
        self.lista.delete(*self.lista.get_children())
        self.connect_db()
        
        lista = self.cursor.execute(""" SELECT status, code, data, hora_inicio, hora_fim, descricao FROM apontamento
            ORDER BY data,hora_inicio ASC; """)
        for i in lista:
            self.lista.insert("", END, values=i)
        self.disconnect_db()
    
    def OnDoubleClick(self, event):
        self.limpar()
        
        for n in self.lista.selection():
            col1, col2, col3, col4, col5, col6 = self.lista.item(n, "values")
            self.codigo_entry.insert(END, col2)
            self.dia_entry.set_date(date=datetime.strptime(col3, "%Y-%m-%d").date())
            self.hora_inicio_entry.set24Hrs(val=col4)
            self.hora_fim_entry.set24Hrs(val=col5)
            self.descricao_entry.insert(END, col6)
            self.status_entry.set(col1)
        
    def order_table(self):
        self.lista.delete(*self.lista.get_children())
        self.connect_db()
        
        if self.order == 'ASC':
            lista = self.cursor.execute(""" SELECT status, code, data, hora_inicio, hora_fim, descricao FROM apontamento
                ORDER BY code DESC; """)
            self.order = 'DESC'
        elif self.order == 'DESC':
            lista = self.cursor.execute(""" SELECT status, code, data, hora_inicio, hora_fim, descricao FROM apontamento
                ORDER BY code ASC; """)
            self.order = 'ASC'
        
        for i in lista:
            self.lista.insert("", END, values=i)
        self.disconnect_db()
        
    def delete_appointment(self):
        self.variables()
        self.connect_db()
        self.cursor.execute(""" DELETE FROM apontamento 
            WHERE data = ? AND hora_inicio = ? AND hora_fim = ? """, (self.data, self.hora_ini, self.hora_fim))
        self.connect.commit()
        self.disconnect_db()
        self.limpar()
        self.select_appointment()
    
    def modify_appointment(self):
        self.variables()
        self.connect_db()
        self.cursor.execute(""" UPDATE apontamento SET data = ?, hora_inicio = ?, hora_fim = ?, descricao = ?, status = ?
            WHERE code = ?""", (self.data, self.hora_ini, self.hora_fim, self.descricao, self.status, self.codigo))
        self.connect.commit()
        self.disconnect_db()
        self.limpar()
        self.select_appointment()
   
    def compact_appointment(self):
        self.connect_db()
        self.cursor.execute(""" SELECT status, data, hora_inicio, hora_fim, descricao FROM apontamento
            ORDER BY data, hora_inicio ASC; """)
        lista = self.cursor.fetchall()
        
        for i in range(len(lista)):
            if i < len(lista) - 1:
                if lista[i][0] == lista[i+1][0] and lista[i][3] == lista[i+1][3] and lista[i][2] == lista[i+1][1]:
                    print("Compactado apontamento: ", lista[i][0], " - ", lista[i][1], " - ", lista[i][2], " - ", lista[i][3], "\nCom apontamento: ", lista[i+1][0], " - ", lista[i+1][1], " - ", lista[i+1][2], " - ", lista[i+1][3])
                    self.cursor.execute(""" UPDATE apontamento SET hora_fim = ? WHERE data = ? AND hora_inicio = ? AND descricao = ? """,
                        (lista[i+1][2], lista[i][0], lista[i][1], lista[i][3]))
                    self.cursor.execute(""" DELETE FROM apontamento WHERE data = ? AND hora_inicio = ? AND descricao = ? """,
                        (lista[i+1][0], lista[i+1][1], lista[i+1][3]))
                    self.connect.commit()
                    
                    self.cursor.execute(""" SELECT status, data, hora_inicio, hora_fim, descricao FROM apontamento
                        ORDER BY data, hora_inicio ASC; """)
                    lista = self.cursor.fetchall()
                else:
                    continue
            else:
                break
        
        self.disconnect_db()
        self.select_appointment()
    
    def change_status(self):
        config = Toplevel()
        config.title("Alterar Status")
        config.configure(background="#27374D")
        config.geometry("400x300")
        config.resizable(FALSE, FALSE)
        config.transient(root)
        config.focus_force()

        self.altera_frame = Frame(config, bg="#DDE6ED", highlightbackground="#526D82", highlightthickness=2)
        self.altera_frame.place(relx= 0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        
        self.lb_codigo_inicial = Label(config, text="Código Inicial", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_codigo_inicial.place(relx=0.05, rely=0.05)
        self.codigo_entry_inicial = Entry(config)
        self.codigo_entry_inicial.place(relx=0.05, rely=0.15, relwidth=0.3)

        self.lb_codigo_final = Label(config, text="Código Final", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_codigo_final.place(relx=0.05, rely=0.25)
        self.codigo_entry_final = Entry(config)
        self.codigo_entry_final.place(relx=0.05, rely=0.35, relwidth=0.3)

        self.lb_altera_status = Label(config, text="Status", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_altera_status.place(relx=0.05, rely=0.45)
        self.altera_status_entry = ttk.Combobox(config)
        self.altera_status_entry['values'] = ('Local', 'Rascunho', 'Enviado', 'Devolvido', 'Aprovado')
        self.altera_status_entry['state'] = 'readonly'
        self.altera_status_entry.place(relx=0.05, rely=0.55, relwidth=0.3)

        self.bt_altera_status = Button(config, text="Alterar", bg="#9DB2BF", command=self.change_status_appointment)
        self.bt_altera_status.place(relx=0.22, rely=0.75, relwidth=0.5, relheight=0.1)
    
    def change_status_appointment(self):
        self.codigo_inicial = self.codigo_entry_inicial.get()
        self.codigo_final = self.codigo_entry_final.get()
        self.connect_db()
        for i in range(int(self.codigo_inicial), int(self.codigo_final)+1):
            self.cursor.execute(""" UPDATE apontamento SET status = ? WHERE code = ? """, (self.altera_status_entry.get(), i))
        self.connect.commit()
        self.disconnect_db()
        self.select_appointment()

class Application(Functions):
    def __init__(self) -> None:
        self.root = root
        self.window()
        self.frame()
        self.widgets()
        self.widget_list()
        self.make_table()
        root.mainloop()
    
    def window(self):
        self.root.title("Apontamentos")
        self.root.configure(background="#27374D")
        self.root.geometry("800x600")
        self.root.resizable(TRUE, TRUE)
        self.root.maxsize(width=1280, height=720)
        self.root.minsize(width=600, height=500)
    def frame(self):
        self.frame_1 = Frame(self.root, bg="#DDE6ED", highlightbackground="#526D82", highlightthickness=2)
        self.frame_1.place(relx= 0.01, rely=0.01, relwidth=0.98, relheight=0.48)
        
        self.frame_2 = Frame(self.root, bg="#DDE6ED", highlightbackground="#526D82", highlightthickness=2)
        self.frame_2.place(relx= 0.01, rely=0.5, relwidth=0.98, relheight=0.48)   
    def widgets(self):
        self.lb_codigo = Label(self.frame_1, text="Código", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_codigo.place(relx=0.01, rely=0.05)
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.01, rely=0.15, relwidth=0.1)

        self.lb_status = Label(self.frame_1, text="Status", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_status.place(relx=0.15, rely=0.05)
        self.status_entry = ttk.Combobox(self.frame_1)
        self.status_entry['values'] = ('Local', 'Rascunho', 'Enviado', 'Devolvido', 'Aprovado')
        self.status_entry['state'] = 'readonly'
        self.status_entry.place(relx=0.15, rely=0.15, relwidth=0.1)
        
        self.lb_dia = Label(self.frame_1, text="Dia", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_dia.place(relx=0.01, rely=0.25)
        
        self.dia_entry = DateEntry(self.frame_1, locale="pt_BR", date=date.today())
        self.dia_entry.place(relx=0.01, rely=0.35, relwidth=0.2)
        
        self.lb_hora_inicio = Label(self.frame_1, text="Hora Início", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_hora_inicio.place(relx=0.01, rely=0.45)
        self.hora_inicio_entry = SpinTimePickerModern(self.frame_1)
        self.hora_inicio_entry.addAll(constants.HOURS24)
        self.hora_inicio_entry.set24Hrs(val=int(time.strftime("%H", time.localtime())) - 1)
        self.hora_inicio_entry.setMins(val=0)
        self.hora_inicio_entry.place(relx=0.01, rely=0.55, relwidth=0.2)
        
        self.lb_hora_fim = Label(self.frame_1, text="Hora Fim", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_hora_fim.place(relx=0.25, rely=0.45)
        self.hora_fim_entry = SpinTimePickerModern(self.frame_1)
        self.hora_fim_entry.addAll(constants.HOURS24)
        self.hora_fim_entry.set24Hrs(val=int(time.strftime("%H", time.localtime())))
        self.hora_fim_entry.setMins(val=0)
        self.hora_fim_entry.place(relx=0.25, rely=0.55, relwidth=0.2)
        
        self.lb_descricao = Label(self.frame_1, text="Descrição", bg="#DDE6ED", font=('arial', 12, 'bold'))
        self.lb_descricao.place(relx=0.01, rely=0.65)
        self.descricao_entry = Entry(self.frame_1, highlightbackground="#526D82", highlightthickness=2)
        self.descricao_entry.place(relx=0.01, rely=0.75, relwidth=0.8)
        
        self.bt_compacta = Button(self.frame_1, text="Compactar", bg="#9DB2BF", command=self.compact_appointment)
        self.bt_compacta.place(relx=0.45, rely=0.05, relwidth=0.1, relheight=0.1)
        
        self.bt_limpa = Button(self.frame_1, text="Limpar", bg="#9DB2BF", command=self.limpar)
        self.bt_limpa.place(relx=0.55, rely=0.05, relwidth=0.1, relheight=0.1)
        
        self.bt_registro = Button(self.frame_1, text="Registrar", bg="#9DB2BF", command=self.add_appointment)
        self.bt_registro.place(relx=0.69, rely=0.05, relwidth=0.1, relheight=0.1)
        
        self.bt_altera = Button(self.frame_1, text="Alterar", bg="#9DB2BF", command=self.modify_appointment)
        self.bt_altera.place(relx=0.79, rely=0.05, relwidth=0.1, relheight=0.1)
        
        self.bt_apaga = Button(self.frame_1, text="Apagar", bg="#9DB2BF", command=self.delete_appointment)
        self.bt_apaga.place(relx=0.89, rely=0.05, relwidth=0.1, relheight=0.1)

        self.bt_altera_status = Button(self.frame_1, text="Alterar Status", bg="#9DB2BF", command=self.change_status)
        self.bt_altera_status.place(relx=0.79, rely=0.15, relwidth=0.1, relheight=0.1)
    def widget_list(self):
        self.order = 'ASC'
        self.lista = ttk.Treeview(self.frame_2, height= 3, columns=(1,2,3,4,5,6))
        self.lista.heading("#0", text="")
        self.lista.heading(1, text="Status", command=self.order_table)
        self.lista.heading(2, text="Código", command=self.order_table)
        self.lista.heading(3, text="Data", command=self.order_table)
        self.lista.heading(4, text="Hora Inicio", command=self.order_table)
        self.lista.heading(5, text="Hora Fim", command=self.order_table)
        self.lista.heading(6, text="Descrição", command=self.order_table)

        self.lista.column("#0", width=1)
        self.lista.column(1, width=25)
        self.lista.column(2, width=25)
        self.lista.column(3, width=100)
        self.lista.column(4, width=50)
        self.lista.column(5, width=50)
        self.lista.column(6, width=250)
        
        self.lista.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        self.lista.bind("<Double-1>", self.OnDoubleClick)
        self.lista.bind()
    

Application()