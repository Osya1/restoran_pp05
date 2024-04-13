import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Таблицы
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                table_number INTEGER,
                num_guests INTEGER,
                dishes TEXT,
                drinks TEXT)''')
                
cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'adminpass', 'admin'))
cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('chef', 'chefpass', 'chef'))
cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('waiter', 'waiterpass', 'waiter'))

conn.commit()
conn.close()

root = tk.Tk()
root.title("Ресторан")
root.iconbitmap('D:/prog/img/glavnoe.png') 

# Окно авторизации
class AuthorizationWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Авторизация")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png") 
        self.iconphoto(False, self.logo)
        self.geometry("300x200")
        self.configure(bg="white")

        self.label = tk.Label(self, image=self.logo, bg="white")
        self.label.pack(pady=10)

        self.username_label = tk.Label(self, text="Логин:", bg="white")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, bg="white", fg="black")  
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Пароль:", bg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", bg="white", fg="black")  
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                role = user[3]
            if role == "admin":
                self.destroy()
                AdminPanel()
            elif role == "chef":
                self.destroy()
                ChefPanel()
            elif role == "waiter":
                self.destroy()
                WaiterPanel()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Панель Администратора
class AdminPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Панель администратора")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png")  
        self.iconphoto(False, self.logo)
        self.geometry("600x400")
        self.configure(bg="white")

        self.label = tk.Label(self, image=self.logo, bg="white")
        self.label.pack(pady=10)

        # Кнопка для добавления нового сотрудника
        self.add_employee_button = tk.Button(self, text="Добавить нового сотрудника", command=self.add_employee)
        self.add_employee_button.pack(pady=5)

        # Кнопка для перевода пользователей в статус "уволен"
        self.dismiss_button = tk.Button(self, text="Перевод в статус 'уволен'", command=self.dismiss_employee)
        self.dismiss_button.pack(pady=5)

        # Кнопка для назначения официантов и поваров на смены
        self.assign_button = tk.Button(self, text="Назначение на смены", command=self.assign_shifts)
        self.assign_button.pack(pady=5)

        # Кнопка для просмотра всех заказов
        self.orders_button = tk.Button(self, text="Просмотр заказов", command=self.view_orders)
        self.orders_button.pack(pady=5)

    def open_registration(self):
        add_employee_window = AddEmployeeWindow(self)

    def dismiss_employee(self):
        dismiss_window = DismissEmployeeWindow(self)
        messagebox.showinfo("Уведомление", "Пользователь переведен в статус 'уволен'")

    def assign_shifts(self):
        messagebox.showinfo("Уведомление", "Смены успешно назначены")

    def view_orders(self):
        messagebox.showinfo("Уведомление", "Просмотр всех заказов")

    def add_employee(self):
        add_employee_window = AddEmployeeWindow(self)
# Добавление новго сотрудника
class AddEmployeeWindow(tk.Toplevel):
    def __init__(self, admin_panel):
        super().__init__()
        self.title("Добавление нового сотрудника")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png") 
        self.iconphoto(False, self.logo)
        self.geometry("300x200")
        self.configure(bg="white")
        self.admin_panel = admin_panel

        self.label = tk.Label(self, image=self.logo, bg="white")
        self.label.pack(pady=10)

        self.username_label = tk.Label(self, text="Логин:", bg="white")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, bg="white", fg="black")
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Пароль:", bg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", bg="white", fg="black")
        self.password_entry.pack()

        self.role_label = tk.Label(self, text="Роль (admin/chef/waiter):", bg="white")
        self.role_label.pack()
        self.role_entry = tk.Entry(self, bg="white", fg="black")
        self.role_entry.pack()

        self.add_button = tk.Button(self, text="Добавить", command=self.add_employee)
        self.add_button.pack(pady=10)

    def add_employee(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        status = True

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()

        conn.close()

        messagebox.showinfo("Уведомление", "Новый сотрудник успешно добавлен")

        self.destroy()
        self.admin_panel.lift()
# Увольнение сотрудника
class DismissEmployeeWindow(tk.Toplevel):
    def __init__(self, admin_panel):
        super().__init__()
        self.title("Увольнение сотрудника")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png") 
        self.iconphoto(False, self.logo)
        self.geometry("300x200")
        self.configure(bg="white")
        self.admin_panel = admin_panel

        self.label = tk.Label(self, image=self.logo, bg="white")
        self.label.pack(pady=10)

        self.username_label = tk.Label(self, text="Логин:", bg="white")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, bg="white", fg="black")
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Пароль:", bg="white")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", bg="white", fg="black")
        self.password_entry.pack()

        self.dismiss_button = tk.Button(self, text="Уволить", command=self.dismiss_employee)
        self.dismiss_button.pack(pady=10)

    def dismiss_employee(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Удаление пользователя из базы данных
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
            
        messagebox.showinfo("Уведомление", f"Пользователь с логином '{username}' уволен")
        self.destroy()
        self.admin_panel.lift()

# Создаем класс для панели повара
class ChefPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Панель повара")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png") 
        self.iconphoto(False, self.logo)
        self.geometry("400x300")
        self.configure(bg="white")
        
        # отображение заказов
        self.table = ttk.Treeview(self)
        self.table["columns"] = ("table_number", "num_of_people", "dishes", "drinks", "status")
        self.table.heading("table_number", text="Столик")
        self.table.heading("num_of_people", text="Количество людей")
        self.table.heading("dishes", text="Блюда")
        self.table.heading("drinks", text="Напитки")
        self.table.heading("status", text="Статус")
        self.table.pack()

        self.status_var = tk.StringVar(self)
        self.status_var.set("готовится")  # Значение по умолчанию
        self.status_combobox = ttk.Combobox(self, textvariable=self.status_var, values=["готовится", "готов"])
        self.status_combobox.pack()
        
        self.update_status_button = tk.Button(self, text="Изменить статус", command=self.update_status)
        self.update_status_button.pack()


        self.update_orders_table()

    def update_orders_table(self):
   
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE status = 'Принят'")
        orders = c.fetchall()
        conn.close()

        # Очищение таблицы перед обновлением
        for row in self.table.get_children():
            self.table.delete(row)

        for order in orders:
            self.table.insert("", "end", values=order)

    def update_status(self):

        selected_item = self.table.selection()[0]
        order_id = self.table.item(selected_item)['values'][0]
        new_status = self.status_var.get()
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET status = ? WHERE id = ?",
                  (new_status, order_id))
        conn.commit()
        conn.close()

        self.update_orders_table()

# Создаем класс для панели официанта
class WaiterPanel(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Панель официанта")
        self.logo = tk.PhotoImage(file="D:/prog/img/logotip.png") 
        self.iconphoto(False, self.logo)
        self.geometry("600x400")
        self.configure(bg="white")
        
        # Создаем интерфейс для ввода информации о заказе
        self.order_id_label = tk.Label(self, text="ID заказа:")
        self.order_id_label.pack()
        self.order_id_entry = tk.Entry(self)
        self.order_id_entry.pack()

        self.table_number_label = tk.Label(self, text="Номер стола:")
        self.table_number_label.pack()
        self.table_number_entry = tk.Entry(self)
        self.table_number_entry.pack()

        self.num_guests_label = tk.Label(self, text="Количество человек:")
        self.num_guests_label.pack()
        self.num_guests_entry = tk.Entry(self)
        self.num_guests_entry.pack()

        self.dishes_label = tk.Label(self, text="Блюда:")
        self.dishes_label.pack()
        self.dishes_entry = tk.Entry(self)
        self.dishes_entry.pack()

        self.drinks_label = tk.Label(self, text="Напитки:")
        self.drinks_label.pack()
        self.drinks_entry = tk.Entry(self)
        self.drinks_entry.pack()

        # Добавление элемента управления для выбора статуса
        self.status_var = tk.StringVar(self)
        self.status_var.set("Принят")
        self.status_dropdown = tk.OptionMenu(self, self.status_var, "Принят", "Оплачен")
        self.status_dropdown.pack()

        self.submit_button = tk.Button(self, text="Сохранить заказ", command=self.save_order)
        self.submit_button.pack()

        self.update_status_button = tk.Button(self, text="Обновить статус", command=self.update_status)
        self.update_status_button.pack()
        
        self.view_orders_button = tk.Button(self, text="Просмотр заказов за смену", command=self.view_orders)
        self.view_orders_button.pack()

        self.orders_text = tk.Text(self)
        self.orders_text.pack()

    def save_order(self):
        table_number = self.table_number_entry.get()
        num_guests = self.num_guests_entry.get()
        dishes = self.dishes_entry.get()
        drinks = self.drinks_entry.get()
        status = self.status_var.get() 

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO orders (table_number, num_guests, dishes, drinks, status) VALUES (?, ?, ?, ?, ?)",
                  (table_number, num_guests, dishes, drinks, status))
        conn.commit()
        conn.close()

    def update_status(self):
        order_id = self.order_id_entry.get()

        status = self.status_var.get()
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE orders SET status = ? WHERE id = ?",
                  (status, order_id))
        messagebox.showinfo("Уведомление", "Статус заказа обновлен")
        self.view_orders()

        conn.commit()
        conn.close()
        
    def view_orders(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders")
        orders = c.fetchall()
        conn.close()

        self.orders_text.delete(1.0, tk.END)

        for order in orders:
            self.orders_text.insert(tk.END, f"ID: {order[0]}\n")
            self.orders_text.insert(tk.END, f"Номер стола: {order[1]}\n")
            self.orders_text.insert(tk.END, f"Количество человек: {order[2]}\n")
            self.orders_text.insert(tk.END, f"Блюда: {order[3]}\n")
            self.orders_text.insert(tk.END, f"Напитки: {order[4]}\n")
            self.orders_text.insert(tk.END, f"Статус: {order[5]}\n")
            self.orders_text.insert(tk.END, "\n")

# Запуск программы
if __name__ == "__main__":
    auth_window = AuthorizationWindow()
    root.mainloop()