import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
import os

# Генерация ключа шифрования и сохранение его в файл
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Загрузка ключа шифрования из файла
def load_key():
    return open("secret.key", "rb").read()

# Шифрование данных
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Дешифрование данных
def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data).decode()

# Проверка существования ключа, если нет - создание
if not os.path.exists("secret.key"):
    generate_key()

key = load_key()

# Функция для регистрации
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        encrypted_data = encrypt_data(f"{username}:{password}", key)
        with open("accounts.txt", "ab") as f:
            f.write(encrypted_data + b"\n")
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

# Функция для входа
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username and password:
        with open("accounts.txt", "rb") as f:
            accounts = f.readlines()
        
        for account in accounts:
            decrypted_data = decrypt_data(account.strip(), key)
            stored_username, stored_password = decrypted_data.split(":")
            if stored_username == username and stored_password == password:
                messagebox.showinfo("Успех", "Вход выполнен успешно!")
                root.destroy()  # Закрываем окно авторизации
                start_game()  # Запускаем игру
                return
        
        messagebox.showwarning("Ошибка", "Неверный никнейм или пароль.")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

# Функция для запуска игры
def start_game():
    app = CheckersBoard()  # Создаем экземпляр класса CheckersBoard
    app.mainloop()  # Запускаем главный цикл игры

# Создание окна авторизации
root = tk.Tk()
root.title("Авторизация")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

# Создаем главный контейнер
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Заголовок
title_label = tk.Label(
    main_frame,
    text="Добро пожаловать в игру\n Русские шашки 80",
    font=("Helvetica", 24, "bold"),
    bg="#f0f0f0",
    fg="#333333"
)
title_label.pack(pady=20)

# Стиль для полей ввода
style = ttk.Style()
style.configure(
    "Custom.TEntry",
    fieldbackground="#ffffff",
    borderwidth=0,
    relief="flat"
)

# Фрейм для полей ввода
input_frame = tk.Frame(main_frame, bg="#f0f0f0")
input_frame.pack(pady=20)

# Поле для ввода никнейма
username_frame = tk.Frame(input_frame, bg="#f0f0f0")
username_frame.pack(pady=10)

username_label = tk.Label(
    username_frame,
    text="Никнейм",
    font=("Helvetica", 12),
    bg="#f0f0f0",
    fg="#666666"
)
username_label.pack(anchor="w")

entry_username = ttk.Entry(
    username_frame,
    width=30,
    style="Custom.TEntry",
    font=("Helvetica", 11)
)
entry_username.pack(pady=5)

# Поле для ввода пароля
password_frame = tk.Frame(input_frame, bg="#f0f0f0")
password_frame.pack(pady=10)

password_label = tk.Label(
    password_frame,
    text="Пароль",
    font=("Helvetica", 12),
    bg="#f0f0f0",
    fg="#666666"
)
password_label.pack(anchor="w")

entry_password = ttk.Entry(
    password_frame,
    width=30,
    style="Custom.TEntry",
    font=("Helvetica", 11),
    show="•"
)
entry_password.pack(pady=5)

# Фрейм для кнопок
button_frame = tk.Frame(main_frame, bg="#f0f0f0")
button_frame.pack(pady=30)

# Кнопка входа
btn_login = tk.Button(
    button_frame,
    text="Войти",
    font=("Helvetica", 12, "bold"),
    width=15,
    bg="#4CAF50",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=login
)
btn_login.pack(pady=5)

# Кнопка регистрации
btn_register = tk.Button(
    button_frame,
    text="Зарегистрироваться",
    font=("Helvetica", 12),
    width=20,
    bg="#2196F3",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=register
)
btn_register.pack(pady=5)

# Центрирование окна на экране
window_width = 420
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

class Checker:
    def __init__(self,canvas,x,y,r,color,tags,board,checkers,move):
        self.king = False
        self.canvas = canvas
        self.tags = tags
        self.move = move
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.width = 1
        self.draw_circle()
        self.board = board
        self.selected = False
        self.checkers = checkers



    def draw_circle(self):
        x1 = 30 + (self.x * 60)
        y1 = 30 + (self.y * 60)
        if self.color == "black" and self.king == False:
            self.canvas.create_oval(x1 - self.r, y1 - self.r, x1 + self.r, y1 + self.r, fill=self.color,
                                    outline='white', tags=self.tags, width=self.width)
        elif self.color == "white" and self.king == False:
            self.canvas.create_oval(x1 - self.r, y1 - self.r, x1 + self.r, y1 + self.r, fill=self.color,
                                    outline='black', tags=self.tags, width=self.width)
        self.canvas.tag_bind(self.tags, '<Button-1>', self.select_circle)
        if self.king:
            self.canvas.create_oval(x1 - self.r, y1 - self.r, x1 + self.r, y1 + self.r, fill=self.color,outline='DarkGoldenrod2', tags=self.tags, width=self.width)
            self.canvas.tag_bind(self.tags, '<Button-1>', self.select_circle)
            return


    def selected_circle_cheak(self):
        print("selected_circle_cheak")
        for checker in self.checkers.massive_checkers:
            if checker.selected:
                return True
        return False


    def check_king(self):
        if self.king:
            return
        if self.color == "black" and self.y == 7:
            self.king = True
            self.width = 10
            print(self.tags)
            return
        if self.color == "white" and self.y == 0:
            self.king = True
            self.width = 10
            print(self.tags)
            return


    def king_cheak_move_range(self):
        range = [0,0,0,0]
        x1 = self.x - 1
        y1 = self.y - 1
        pawn_line = False
        while x1 >= 0 and y1 >= 0:
            if self.board.matrix_board[y1][x1] == "0":
                range[0] = range[0] + 1
                pawn_line = False
            if self.color == "white":
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'w'):
                    break
            else:
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'b'):
                    break
            if self.board.matrix_board[y1][x1] != "0":
                pawn_line = True
                range[0] = range[0] + 1
            x1 = x1 - 1
            y1 = y1 - 1

        x1 = self.x + 1
        y1 = self.y - 1
        pawn_line = False
        while x1 < 10 and y1 >= 0:
            if self.board.matrix_board[y1][x1] == "0":
                range[1] = range[1] + 1
                pawn_line = False
            if self.color == "white":
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'w'):
                    break
            else:
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'b'):
                    break
            if self.board.matrix_board[y1][x1] != "0":
                pawn_line = True
                range[1] = range[1] + 1
            x1 = x1 + 1
            y1 = y1 - 1

        x1 = self.x + 1
        y1 = self.y + 1
        pawn_line = False
        while x1 < 10 and y1 < 8:
            if self.board.matrix_board[y1][x1] == "0":
                range[2] = range[2] + 1
                pawn_line = False
            if self.color == "white":
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'w'):
                    break
            else:
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith(
                        'b'):
                    break
            if self.board.matrix_board[y1][x1] != "0":
                pawn_line = True
                range[2] = range[2] + 1
            x1 = x1 + 1
            y1 = y1 + 1

        x1 = self.x - 1
        y1 = self.y + 1
        pawn_line = False
        while x1 >= 0 and y1 < 8:
            if self.board.matrix_board[y1][x1] == "0":
                range[3] = range[3] + 1
                pawn_line = False
            if self.color == "white":
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith('w'):
                    break
            else:
                if (pawn_line and self.board.matrix_board[y1][x1] != "0") or self.board.matrix_board[y1][x1].startswith('b'):
                    break
            if self.board.matrix_board[y1][x1] != "0":
                pawn_line = True
                range[3] = range[3] + 1
            x1 = x1 - 1
            y1 = y1 + 1
        print(range)
        return range


    def king_cheak_move_range_multi(self):

        range = [[0,0],[0,0],[0,0],[0,0]]
        x1 = self.x - 1
        y1 = self.y - 1

        enemy = False
        pawn_line = False
        while x1 >= 0 and y1 >= 0:
            if self.board.matrix_board[y1][x1] == "0" and enemy == False:
                range[0][0] = range[0][0] + 1
            elif enemy == True and self.board.matrix_board[y1][x1] == "0":
                pawn_line = False
                range[0][1] = range[0][1] + 1
            if self.color == "white":
                if self.board.matrix_board[y1][x1].startswith('w') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('b'):
                    enemy = True
                    pawn_line = True
                    range[0][0] = range[0][0] + 1
            elif self.color == "black":
                if self.board.matrix_board[y1][x1].startswith('b') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('w'):
                    enemy = True
                    pawn_line = True
                    range[0][0]= range[0][0] + 1

            x1 = x1 - 1
            y1 = y1 - 1

        x1 = self.x + 1
        y1 = self.y - 1

        enemy = False
        pawn_line = False
        while x1 < 10 and y1 >= 0:
            if self.board.matrix_board[y1][x1] == "0" and enemy == False:
                range[1][0] = range[1][0] + 1
            elif enemy == True and self.board.matrix_board[y1][x1] == "0":
                pawn_line = False
                range[1][1] = range[1][1] + 1
            if self.color == "white":
                if self.board.matrix_board[y1][x1].startswith('w') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('b'):
                    enemy = True
                    pawn_line = True
                    range[1][0] = range[1][0] + 1
            elif self.color == "black":
                if self.board.matrix_board[y1][x1].startswith('b') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('w'):
                    enemy = True
                    pawn_line = True
                    range[1][0]= range[1][0] + 1
            x1 = x1 + 1
            y1 = y1 - 1

        x1 = self.x + 1
        y1 = self.y + 1

        enemy = False
        pawn_line = False
        while x1 < 10 and y1 < 8:
            if self.board.matrix_board[y1][x1] == "0" and enemy == False:
                range[2][0] = range[2][0] + 1
            elif enemy == True and self.board.matrix_board[y1][x1] == "0":
                pawn_line = False
                range[2][1] = range[2][1] + 1
            if self.color == "white":
                if self.board.matrix_board[y1][x1].startswith('w') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('b'):
                    enemy = True
                    pawn_line = True
                    range[2][0] = range[2][0] + 1
            elif self.color == "black":
                if self.board.matrix_board[y1][x1].startswith('b') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('w'):
                    enemy = True
                    pawn_line = True
                    range[2][0]= range[2][0] + 1
            if enemy == True and self.board.matrix_board[y1][x1] == 0:
                pawn_line = False
                range[2][1] = range[2][1] + 1
            x1 = x1 + 1
            y1 = y1 + 1

        x1 = self.x - 1
        y1 = self.y + 1

        enemy = False
        pawn_line = False
        while x1 >= 0 and y1 < 8:
            if self.board.matrix_board[y1][x1] == "0" and enemy == False:
                range[3][0] = range[3][0] + 1
            elif enemy == True and self.board.matrix_board[y1][x1] == "0":
                pawn_line = False
                range[3][1] = range[3][1] + 1
            if self.color == "white":
                if self.board.matrix_board[y1][x1].startswith('w') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('b'):
                    enemy = True
                    pawn_line = True
                    range[3][0] = range[3][0] + 1
            elif self.color == "black":
                if self.board.matrix_board[y1][x1].startswith('b') or pawn_line == True:
                    break
                elif self.board.matrix_board[y1][x1].startswith('w'):
                    enemy = True
                    pawn_line = True
                    range[3][0]= range[3][0] + 1
            x1 = x1 - 1
            y1 = y1 + 1
        print(range)
        return range


    def game_cheak(self):
        self.check_king()

    def move_king(self,event, par):
        self.delete_selected_circle()
        y, x = par
        take = False
        while self.x > x and self.y > y:
            self.remove_checkers(self.board.matrix_board[y][x])
            if self.board.matrix_board[y][x] != '0':
                take = True
            self.board.matrix_board[y][x] = '0'
            x += 1
            y += 1
        y, x = par
        while self.x < x and self.y < y:
            self.remove_checkers(self.board.matrix_board[y][x])
            if self.board.matrix_board[y][x] != '0':
                take = True
            self.board.matrix_board[y][x] = '0'
            x -= 1
            y -= 1
        y, x = par
        while self.x < x and self.y > y:
            self.remove_checkers(self.board.matrix_board[y][x])
            if self.board.matrix_board[y][x] != '0':
                take = True
            self.board.matrix_board[y][x] = '0'
            x -= 1
            y += 1
        y, x = par
        while self.x > x and self.y < y:
            self.remove_checkers(self.board.matrix_board[y][x])
            if self.board.matrix_board[y][x] != '0':
                take = True
            self.board.matrix_board[y][x] = '0'
            x += 1
            y -= 1
        self.board.matrix_board[self.y][self.x] = '0'
        self.x = par[1]
        self.y = par[0]

        self.board.matrix_board[self.y][self.x] = self.tags
        self.print_board()
        if self.color == "black":
            rang = self.king_cheak_move_range_multi()
            sum = rang[0][1]+rang[1][1]+rang[2][1]+rang[3][1]
            if sum >0 and take:
                self.king_cheak_move_multi(rang)
            else:
                self.move.revers()
                self.selected = False
        elif self.color == "white":
            rang = self.king_cheak_move_range_multi()
            sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
            if sum > 0 and take:
                self.king_cheak_move_multi(rang)
            else:
                self.move.revers()
                self.selected = False
        self.game_cheak()


    def king_cheak_move(self):
        rang = self.king_cheak_move_range()
        for g in range(1, rang[0] + 1):
            x1 = 30 + ((self.x - (g)) * 60)
            y1 = 30 + ((self.y - (g)) * 60)
            tags = self.tags + 'king_move_up_left' + str(g)
            self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
            self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y - g, self.x - g)))
        for g in range(1, rang[1] + 1):
            x1 = 30 + ((self.x + (g)) * 60)
            y1 = 30 + ((self.y - (g)) * 60)
            tags = self.tags + 'king_move_up_right' + str(g)
            self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
            self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y - g, self.x + g)))
        for g in range(1, rang[2] + 1):
            x1 = 30 + ((self.x + (g)) * 60)
            y1 = 30 + ((self.y + (g)) * 60)
            tags = self.tags + 'king_move_down_right' + str(g)
            self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
            self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y + g, self.x + g)))
        for g in range(1, rang[3] + 1):
            x1 = 30 + ((self.x - (g)) * 60)
            y1 = 30 + ((self.y + (g)) * 60)
            tags = self.tags + 'king_move_down_left' + str(g)
            self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
            self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y + g, self.x - g)))


    def king_cheak_move_multi(self,rang):
        if rang[0][1] != 0:
            for g in range(rang[0][0], rang[0][0]+rang[0][1] + 1):
                x1 = 30 + ((self.x - (g)) * 60)
                y1 = 30 + ((self.y - (g)) * 60)
                tags = self.tags + 'king_move_up_left' + str(g)
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y - g, self.x - g)))
        if rang[1][1] != 0:
            for g in range(rang[1][0], rang[1][0]+rang[1][1] + 1):
                x1 = 30 + ((self.x + (g)) * 60)
                y1 = 30 + ((self.y - (g)) * 60)
                tags = self.tags + 'king_move_up_right' + str(g)
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y - g, self.x + g)))
        if rang[2][1] != 0:
            for g in range(rang[2][0], rang[2][0]+rang[2][1] + 1):
                x1 = 30 + ((self.x + (g)) * 60)
                y1 = 30 + ((self.y + (g)) * 60)
                tags = self.tags + 'king_move_down_right' + str(g)
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y + g, self.x + g)))
        if rang[3][1] != 0:
            for g in range(rang[3][0], rang[3][0]+rang[3][1] + 1):
                x1 = 30 + ((self.x - (g)) * 60)
                y1 = 30 + ((self.y + (g)) * 60)
                tags = self.tags + 'king_move_down_left' + str(g)
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', lambda event, g=g: self.move_king(event, (self.y + g, self.x - g)))


    def select_circle(self,event):
        if self.selected:
            self.selected = False
            self.delete_selected_circle()
            return
        for i in self.checkers.massive_checkers:
            if self.take_check(i.x, i.y, i.color) and i.color == self.move.side and i.king == False:
                self.selected = True
                if i.color == "white":
                    self.take_white_chackers()
                elif self.color == "black":
                    self.take_black_chackers()
        for i in self.checkers.massive_checkers:
            a = i.king_cheak_move_range_multi()
            sum = a[0][1] + a[1][1] + a[2][1] + a[3][1]
            if sum != 0 and i.color == self.move.side and i.king == True:
                i.selected = True
                i.king_cheak_move_multi(a)

        if self.color == "black" and self.move.side == "black" and self.king and self.selected_circle_cheak() == False:
            self.selected = True
            self.king_cheak_move()
        elif self.color == "white" and self.move.side == "white" and self.king and self.selected_circle_cheak() == False:
            self.selected = True
            self.king_cheak_move()

        if self.color == "black" and self.move.side == "black" and self.selected_circle_cheak() == False:
            self.selected = True
            if self.x+1<10 and self.y+1<8:
                if self.board.matrix_board[self.y+1][self.x+1] == "0":
                    x1 = 30 + ((self.x+1) * 60)
                    y1 = 30 + ((self.y+1) * 60)
                    tags = self.tags + 'move_right'
                    self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='',tags=tags)
                    self.canvas.tag_bind(tags, '<Button-1>', self.select_move_right)
            if self.x-1>=0 and self.y+1<8:
                if self.board.matrix_board[self.y+1][self.x-1] == "0":
                    x1 = 30 + ((self.x-1) * 60)
                    y1 = 30 + ((self.y+1) * 60)
                    tags = self.tags + 'move_left'
                    self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='',tags=tags)
                    self.canvas.tag_bind(tags, '<Button-1>', self.select_move_left)
            self.take_black_chackers()

        elif self.color == "white" and self.move.side == "white" and self.selected_circle_cheak() == False:
            self.selected = True
            if self.x-1>=0 and self.y-1>=0:
                if self.board.matrix_board[self.y-1][self.x-1] == "0":
                    x1 = 30 + ((self.x-1) * 60)
                    y1 = 30 + ((self.y-1) * 60)
                    tags = self.tags + 'move_right'
                    self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='',tags=tags)
                    self.canvas.tag_bind(tags, '<Button-1>', self.select_move_left)
            if self.x+1<10 and self.y-1>=0:
                if self.board.matrix_board[self.y-1][self.x+1] == "0":
                    x1 = 30 + ((self.x+1) * 60)
                    y1 = 30 + ((self.y-1) * 60)
                    tags = self.tags + 'move_left'
                    self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='',tags=tags)
                    self.canvas.tag_bind(tags, '<Button-1>', self.select_move_right)
            self.take_white_chackers()

    def take_white_chackers(self):
        print("take_white_chackers")
        if self.x + 2 < 10 and self.y - 2 >= 0:
            if self.board.matrix_board[self.y - 2][self.x + 2] == "0" and self.board.matrix_board[self.y - 1][
                self.x + 1].startswith('b'):
                x1 = 30 + ((self.x + 2) * 60)
                y1 = 30 + ((self.y - 2) * 60)
                tags = self.tags + 'move_up_right'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_up_right)
        if self.x - 2 >= 0 and self.y - 2 >= 0:
            if self.board.matrix_board[self.y - 2][self.x - 2] == "0" and self.board.matrix_board[self.y - 1][
                self.x - 1].startswith('b'):
                x1 = 30 + ((self.x - 2) * 60)
                y1 = 30 + ((self.y - 2) * 60)
                tags = self.tags + 'move_up_left'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_up_left)
        if self.x + 2 < 10 and self.y + 2 < 8:
            if self.board.matrix_board[self.y + 2][self.x + 2] == "0" and self.board.matrix_board[self.y + 1][
                self.x + 1].startswith('b'):
                x1 = 30 + ((self.x + 2) * 60)
                y1 = 30 + ((self.y + 2) * 60)
                tags = self.tags + 'move_down_right'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_down_right)
        if self.x - 2 >= 0 and self.y + 2 < 8:
            if self.board.matrix_board[self.y + 2][self.x - 2] == "0" and self.board.matrix_board[self.y + 1][
                self.x - 1].startswith('b'):
                x1 = 30 + ((self.x - 2) * 60)
                y1 = 30 + ((self.y + 2) * 60)
                tags = self.tags + 'move_down_left'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_down_left)

    def take_check(self,x,y,color):
        if color == 'white':
            char = "b"
        else:
            char = "w"
        if x + 2 < 10 and y - 2 >= 0:
            if self.board.matrix_board[y - 2][x + 2] == "0" and self.board.matrix_board[y - 1][
                x + 1].startswith(char):
                return True
        if x - 2 >= 0 and y - 2 >= 0:
            if self.board.matrix_board[y - 2][x - 2] == "0" and self.board.matrix_board[y - 1][
                x - 1].startswith(char):
                return True
        if x + 2 < 10 and y + 2 < 8:
            if self.board.matrix_board[y + 2][x + 2] == "0" and self.board.matrix_board[y + 1][
                x + 1].startswith(char):
                return True
        if x - 2 >= 0 and y + 2 < 8:
            if self.board.matrix_board[y + 2][x - 2] == "0" and self.board.matrix_board[y + 1][
                x - 1].startswith(char):
                return True
        return False




    def take_black_chackers(self):
        print("take_black_chackers")
        if self.x + 2 < 10 and self.y - 2 >= 0:
            if self.board.matrix_board[self.y - 2][self.x + 2] == "0" and self.board.matrix_board[self.y - 1][
                self.x + 1].startswith('w'):
                x1 = 30 + ((self.x + 2) * 60)
                y1 = 30 + ((self.y - 2) * 60)
                tags = self.tags + 'move_up_right'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_up_right)
        if self.x - 2 >= 0 and self.y - 2 >= 0:
            if self.board.matrix_board[self.y - 2][self.x - 2] == "0" and self.board.matrix_board[self.y - 1][
                self.x - 1].startswith('w'):
                x1 = 30 + ((self.x - 2) * 60)
                y1 = 30 + ((self.y - 2) * 60)
                tags = self.tags + 'move_up_left'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_up_left)
        if self.x + 2 < 10 and self.y + 2 < 8:
            if self.board.matrix_board[self.y + 2][self.x + 2] == "0" and self.board.matrix_board[self.y + 1][
                self.x + 1].startswith('w'):
                x1 = 30 + ((self.x + 2) * 60)
                y1 = 30 + ((self.y + 2) * 60)
                tags = self.tags + 'move_down_right'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_down_right)
        if self.x - 2 >= 0 and self.y + 2 < 8:
            if self.board.matrix_board[self.y + 2][self.x - 2] == "0" and self.board.matrix_board[self.y + 1][
                self.x - 1].startswith('w'):
                x1 = 30 + ((self.x - 2) * 60)
                y1 = 30 + ((self.y + 2) * 60)
                tags = self.tags + 'move_down_left'
                self.canvas.create_oval(x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="green", outline='', tags=tags)
                self.canvas.tag_bind(tags, '<Button-1>', self.select_move_down_left)

    def delete_selected_circle(self):
        self.canvas.delete(self.tags + 'move_up_right')
        self.canvas.delete(self.tags + 'move_up_left')
        self.canvas.delete(self.tags + 'move_down_right')
        self.canvas.delete(self.tags + 'move_down_left')
        self.canvas.delete(self.tags + 'move_right')
        self.canvas.delete(self.tags + 'move_left')
        for iter in range(1,10+1):
            self.canvas.delete(self.tags + 'king_move_up_left' + str(iter))
            self.canvas.delete(self.tags + 'king_move_up_right' + str(iter))
            self.canvas.delete(self.tags + 'king_move_down_right' + str(iter))
            self.canvas.delete(self.tags + 'king_move_down_left' + str(iter))


    def select_move_up_right(self,event):
        print("select_move_up_right")
        self.delete_selected_circle()
        self.board.matrix_board[self.y][self.x] = '0'
        self.remove_checkers(self.board.matrix_board[self.y - 1][self.x + 1])
        self.board.matrix_board[self.y - 1][self.x + 1] = '0'
        self.x = self.x + 2
        self.y = self.y - 2
        self.board.matrix_board[self.y][self.x] = self.tags
        self.print_board()
        check = False
        if self.color == "black":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_black_chackers()
                check = True
        elif self.color == "white":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_white_chackers()
                check = True
        if self.selected == True and check == False:
            self.move.revers()
            self.selected = False
        self.game_cheak()

    def select_move_up_left(self,event):
        print("select_move_up_left")
        self.delete_selected_circle()
        self.board.matrix_board[self.y][self.x] = '0'
        self.remove_checkers(self.board.matrix_board[self.y - 1][self.x - 1])
        self.board.matrix_board[self.y - 1][self.x - 1] = '0'
        self.x = self.x - 2
        self.y = self.y - 2
        self.board.matrix_board[self.y][self.x] = self.tags
        self.print_board()
        check = False
        if self.color == "black":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_black_chackers()
                check = True
        elif self.color == "white":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_white_chackers()
                check = True
        if self.selected == True and check == False:
            self.move.revers()
            self.selected = False
        self.game_cheak()

    def select_move_down_right(self,event):
        print("select_move_down_right")
        self.delete_selected_circle()
        self.board.matrix_board[self.y][self.x] = '0'
        self.remove_checkers(self.board.matrix_board[self.y + 1][self.x + 1])
        self.board.matrix_board[self.y + 1][self.x + 1] = '0'
        self.x = self.x + 2
        self.y = self.y + 2
        self.board.matrix_board[self.y][self.x] = self.tags
        self.print_board()
        check = False
        if self.color == "black":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_black_chackers()
                check = True
        elif self.color == "white":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_white_chackers()
                check = True
        if self.selected == True and check == False:
            self.move.revers()
            self.selected = False
        self.game_cheak()

    def select_move_down_left(self,event):
        print("select_move_down_left")
        self.delete_selected_circle()
        self.board.matrix_board[self.y][self.x] = '0'
        self.remove_checkers(self.board.matrix_board[self.y + 1][self.x - 1])
        self.board.matrix_board[self.y + 1][self.x - 1] = '0'
        self.x = self.x - 2
        self.y = self.y + 2
        self.board.matrix_board[self.y][self.x] = self.tags
        self.print_board()
        check = False
        if self.color == "black":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_black_chackers()
                check = True
        elif self.color == "white":
            self.check_king()
            if self.king:
                rang = self.king_cheak_move_range_multi()
                sum = rang[0][1] + rang[1][1] + rang[2][1] + rang[3][1]
                if sum > 0:
                    self.king_cheak_move_multi(rang)
                    check = True
            elif self.take_check(self.x,self.y,self.color):
                self.take_white_chackers()
                check = True
        if self.selected == True and check == False:
            self.move.revers()
            self.selected = False
        self.game_cheak()

    def print_board(self):
        for row in self.board.matrix_board:
            print(row)

    def remove_checkers(self, tags):
        self.checkers.massive_checkers = [checker for checker in self.checkers.massive_checkers if checker.tags != tags]
        self.canvas.delete(tags)

    def select_move_right(self, event):
        if self.color == "black":
            self.delete_selected_circle()
            self.board.matrix_board[self.y][self.x] = '0'
            self.x = self.x + 1
            self.y = self.y + 1
            self.board.matrix_board[self.y][self.x] = self.tags
            self.print_board()
            self.move.revers()
        elif self.color == "white":
            self.delete_selected_circle()
            self.board.matrix_board[self.y][self.x] = '0'
            self.x = self.x + 1
            self.y = self.y - 1
            self.board.matrix_board[self.y][self.x] = self.tags
            self.print_board()
            self.move.revers()
        self.selected = False
        self.game_cheak()


    def select_move_left(self, event):
        if self.color == "black":
            self.delete_selected_circle()
            self.board.matrix_board[self.y][self.x] = '0'
            self.x = self.x - 1
            self.y = self.y + 1
            self.board.matrix_board[self.y][self.x] = self.tags
            self.print_board()
            self.move.revers()
        elif self.color == "white":
            self.delete_selected_circle()
            self.board.matrix_board[self.y][self.x] = '0'
            self.x = self.x - 1
            self.y = self.y - 1
            self.board.matrix_board[self.y][self.x] = self.tags
            self.print_board()
            self.move.revers()
        self.selected = False
        self.game_cheak()

    def update(self):
        self.canvas.delete(self.tags)
        self.draw_circle()



class MatrixBoard:
    matrix_board = []

class Move:
    side = "white"
    num = 0
    def revers(self):
        if self.side == "white":
            self.side = "black"
        else:
            self.side = "white"
        self.num += 1

class CheckerClass:
    massive_checkers = []


class CheckersBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checkers Board")
        self.main_frame = tk.Frame(self)  # Изменен цвет фона на светлый голубой
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.move = Move()
        self.create_widgets()  # Вызов нового метода для создания кнопок и меток
        self.canvas = tk.Canvas(self.main_frame, height=600, width=600, bg="#ffffff")  # Белый фон для холста
        self.canvas.pack(pady=20)
        
        self.matrix_board = MatrixBoard()
        self.create_new_board()
        self.print_board()
        self.checkers = CheckerClass
        self.create_checkers()
        self.update()

    def create_widgets(self):
        # Стиль для кнопок
        style = ttk.Style()
        style.configure("TButton",
                        font=("Helvetica", 14, "bold"),  # Увеличен размер шрифта и сделан жирным
                        padding=10,
                        relief="flat",
                        background="#007BFF",  # Изменен цвет фона на более читаемый
                        foreground="white")
        style.map("TButton",
                background=[("active", "#0056b3")],  # Цвет при наведении
                relief=[("pressed", "sunken")])

        # Кнопка рестарта
        button = ttk.Button(self.main_frame, text="РЕСТАРТ", command=self.restart)
        button.pack(pady=10)

        # Кнопка смены пользователя
        btn_switch_user = ttk.Button(
            self.main_frame,
            text="Сменить пользователя",
            command=self.switch_user
        )
        btn_switch_user.pack(pady=10)

        # Стиль для меток
        label_style = {
            "font": ("Helvetica", 12),
            "bg": "#f0f0f0",
            "fg": "#333333"
        }

        # Метка для счета белых
        self.label_white = tk.Label(self.main_frame, text="Счет белых: 0", **label_style)
        self.label_white.pack(pady=5)

        # Метка для счета черных
        self.label_black = tk.Label(self.main_frame, text="Счет черных: 0", **label_style)
        self.label_black.pack(pady=5)

        # Метка для текущего хода
        self.text_move = tk.Label(self.main_frame, text=f"Ход: {self.move.num}", **label_style)
        self.text_move.pack(pady=5)

        # Метка для номера хода
        self.text_num_move = tk.Label(self.main_frame, text=f"Номер хода: {self.move.num}", **label_style)
        self.text_num_move.pack(pady=5)

        
    def switch_user(self):
  # Закрываем текущее окно
        import main  # Импортируем файл с окном авторизации
        main.root.deiconify()  # Показываем окно авторизации
        self.destroy()


    def restart(self):
        self.canvas.delete("all")
        self.move.side = Move()
        self.move.side = "white"
        self.move.num = 0
        self.matrix_board = MatrixBoard()
        self.matrix_board.matrix_board = []
        self.create_new_board()
        self.print_board()
        self.checkers = CheckerClass
        self.checkers.massive_checkers = []
        self.create_checkers()

    def update(self):
        for i in self.checkers.massive_checkers:
            i.update()
        self.text_move.config(text=f"Ход: {self.move.side}")
        black,white = self.cheak_win()
        self.label_white.config(text=f"Cчет белых: {white}")
        self.label_black.config(text=f"Cчет черных: {black}")
        self.text_num_move.config(text=f"Ход номер: {self.move.num}")
        self.after(16, self.update)

    def create_new_board(self):
        temp = []
        b_id = 0
        w_id = 0
        for row in range(8):
            for col in range(10):
                if row < 3:
                    if (row + col) % 2 == 0:
                        temp.append("0")
                    else:
                        b_id +=1
                        temp.append("b"+str(b_id))

                if row > 2 and row < 5:
                    temp.append("0")
                if row > 4:
                    if (row + col) % 2 == 0:
                        temp.append("0")
                    else:
                        w_id +=1
                        temp.append("w"+str(w_id))
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(col*60,row*60,(col+1)*60,(row+1)*60,fill='grey83')
                else:
                    self.canvas.create_rectangle(col * 60, row * 60, (col + 1) * 60, (row + 1) * 60, fill='grey25')
            self.matrix_board.matrix_board.append(temp)
            temp = []

    def print_board(self):
        for row in self.matrix_board.matrix_board:
            print(row)

    def create_checkers(self):
        row_n = 0
        col_n = 0
        for row in self.matrix_board.matrix_board:
            for col in row:
                if col.count("b") == 1:
                    checker = Checker(self.canvas,col_n, row_n, 20,"black",col,self.matrix_board,self.checkers,self.move)
                    self.checkers.massive_checkers.append(checker)
                if col.count("w") == 1:
                    checker = Checker(self.canvas, col_n, row_n, 20, "white", col,self.matrix_board,self.checkers,self.move)
                    self.checkers.massive_checkers.append(checker)
                col_n += 1
            col_n = 0
            row_n += 1

    def update_board(self):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(10):
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(col * 60, row * 60, (col + 1) * 60, (row + 1) * 60, fill='grey83')
                else:
                    self.canvas.create_rectangle(col * 60, row * 60, (col + 1) * 60, (row + 1) * 60, fill='grey25')
        for checker in self.checkers.massive_checkers:
            checker.update()

    def cheak_win(self):
        black = 0
        white = 0
        for i in self.checkers.massive_checkers:
            if i.color == "white":
                white += 1
            else:
                black += 1
        if black == 0:
            self.show_winner("White wins")
            return
        elif white == 0:
            self.show_winner("Black wins")
            return
        else:
            return [black, white]

    def show_winner(self, winner_text):
        # Создаем новое окно для сообщения о победе
        win_window = tk.Toplevel(self)
        win_window.title("Победа!")
        win_window.geometry("300x200")

        label = tk.Label(win_window, text=winner_text, font=("Helvetica", 16))
        label.pack(pady=20)

        restart_button = tk.Button(win_window, text="Рестарт", command=self.restart)
        restart_button.pack(pady=10)

        # Отключаем основное окно до тех пор, пока не закроется окно победы
        win_window.transient(self)
        win_window.grab_set()
        self.wait_window(win_window)


if __name__ == "__main__":
    root.mainloop()