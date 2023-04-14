from tkinter import*
from tkinter import ttk
import tkinter.messagebox as mb
import datetime
import pymysql
import tkinter as tk

#import self as self

#from conm import host, user, password, db_name

#устанавливает соединение с БД
connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database= 'testbd',
        cursorclass=pymysql.cursors.DictCursor
    )


# устанавливает соединение с БД
# connection = pymysql.connect(
#         host='localhost',
#         port=3306,
#         user='root',
#         password='',
#         database= 'testbd',
#         cursorclass=pymysql.cursors.DictCursor
#     )




def toString(text) -> str:
    return "".join(text)

def save_to_bdysl():
    #Функция авторизации и вывода
    with connection.cursor() as cursor:
        log = txt_one.get()
        pas = txt_two.get()

        sql = f"SELECT * FROM `users` WHERE login = '{log}' and password = '{pas}'"

        cursor.execute(sql)
        res = cursor.fetchone()
        if res == None:
            msg = "Неверный логин или пароль"
            mb.showerror("Ошибка", msg)
        else:
            sqll = f"SELECT * FROM `users` WHERE login = '{log}' and password= '{pas}'"
            cursor.execute(sqll)
            ress = cursor.fetchall()
            for i in ress:
                uid = i['id_us']
                sqll = f"SELECT * FROM `users` WHERE id_us = '{uid}'"
                cursor.execute(sqll)
                ress = cursor.fetchall()
                root1.destroy()
                for i in ress:
                    ass = i['FIO']
                    uidd = i['id_us']

                    window = Tk()
                    window.configure(background='#66CDAA')
                    window.title("Книги")
                    window.geometry('1210x450')
                    lbl_one12 = Label(window, text=f"Добро пожаловать! {ass}. Книги в наличии - ниже.",bg='#66CDAA').grid(row=5, column=1)
                    columns = ("id", "name", "pages", "age","kolvo","price")
                    tree = ttk.Treeview(window, columns=columns, show="headings")
                    tree.grid(row=10, column=1, columnspan=2, sticky=EW, padx=1, pady=1)
                    tree.heading("id", text="Идентификатор книги")
                    tree.heading("name", text="Название книги")
                    tree.heading("pages", text="Количество листов")
                    tree.heading("age", text="Возраст книги")
                    tree.heading("kolvo", text="Количество книг")
                    tree.heading("price", text="Цена книги [1 шт.]")
                    cur1 = (f"SELECT * FROM `books`")
                    cursor.execute(cur1)
                    reess = cursor.fetchall()
                    for row in reess:
                        a = (row['ID_B'])
                        b = (row['nazvanie'])
                        c = (row['pages'])
                        c1 = (row['age'])
                        c2 = (row['kolvo_kn'])
                        c3 = (row['price'])
                        d = [(a), (b), (c), (c1), (c2), (c3)]
                        tree.insert("", tk.END, values=(d))

                    now = datetime.datetime.now()
                    pp = 'Авторизация успешна'
                    k = (now.strftime("%Y-%m-%d %H:%M"))
                    inset_cheque = f"INSERT INTO avtorizac (id_us , data, navtrc) VALUES ('{uidd}','{k}','{pp}')"
                    cursor.execute(inset_cheque)
                    connection.commit()



        def basket():

            for i in tree.get_children():
                tree.delete(i)
            with connection.cursor() as cursor:
                cur1 = (f"SELECT basket.id_c,basket.id_b, basket.quantity_b , books.ID_B, books.pages, books.age, books.nazvanie, books.price FROM `basket`,`books`  WHERE basket.id_c = '{uid}' and basket.id_b = books.ID_B;")
                cursor.execute(cur1)
                reess = cursor.fetchall()
                for row in reess:
                    a = (row['ID_B'])
                    b = (row['nazvanie'])
                    c = (row['pages'])
                    c1 = (row['age'])
                    c2 = (row['quantity_b'])
                    c3 = (row['price'])
                    d = [(a), (b), (c), (c1),(c2), (c3)]
                    tree.insert("", tk.END, values=(d))
    btn_sel= Button(window, text='Вывести cписок корзины', command=basket).grid(row=25,column=1,ipadx=27)


    def books():
        for i in tree.get_children():
            tree.delete(i)
        with connection.cursor() as cursor:
            cur1 = (f"SELECT * FROM `books`")
            cursor.execute(cur1)
            reess = cursor.fetchall()
            for row in reess:
                a = (row['ID_B'])
                b = (row['nazvanie'])
                c = (row['pages'])
                c1 = (row['age'])
                c2 = (row['kolvo_kn'])
                c3 = (row['price'])
                d = [(a), (b), (c), (c1), (c2), (c3)]
                tree.insert("", tk.END, values=(d))
    btn_sel2= Button(window, text='Вывести список книг', command=books).grid(row=25,column=2,ipadx=37)

    def addbooks():
        addb = Tk()
        addb.title("Добавление книги")
        addb.geometry('270x200')
        addb.configure(background='#66CDAA')
        # Лейблы
        lbl_one0 = Label(addb, text='Идентификатор книги', bg='#66CDAA').grid(row=6, column=1)
        lbl_one1 = Label(addb, text='Количество', bg='#66CDAA').grid(row=8, column=1)

        # Поля для ввода
        txt_one = Entry(addb, width=20)
        txt_one.grid(row=7, column=1)
        txt_two = Entry(addb, width=20)
        txt_two.grid(row=9, column=1)

        def saveadd():
            id_cnigi = txt_one.get()
            kolvvo = txt_two.get()
            with connection.cursor() as cursor:

                sqll = f"SELECT * FROM `books` WHERE ID_B = '{id_cnigi}' "
                cursor.execute(sqll)
                ress = cursor.fetchall()
                for i in ress:
                    id_alb = i['ID_B']
                    rez = i['rezerv']
                    kolknig = i['kolvo_kn']
                    prices = i['price']

                kolvbks = 0

                sqs = f"SELECT * FROM `basket`"
                cursor.execute(sqs)
                ress = cursor.fetchall()
                for i in ress:
                    kolvbks = i['id_b']


                if int(kolvvo) > int(kolknig) or int(kolvvo) == 0:
                    msg = "Введеное количество книг превышает допустимое количество! Либо значение равно 0. "
                    mb.showerror("Ошибка", msg)

                if int(id_alb) < int(id_cnigi):
                    msg = "Введеный идентификатор не существует!"
                    mb.showerror("Ошибка", msg)

                if int(id_cnigi) == int(kolvbks):
                    msg = "Данная книга уже добавлена в список!"
                    mb.showerror("Ошибка", msg)
                elif int(kolvvo) <= int(kolknig):
                    rezerv = int(rez) + int(kolvvo)

                    print(rez,kolvvo)

                    inset_rezbook = f"UPDATE `books` SET rezerv = '{rezerv}' WHERE ID_B = '{id_cnigi}'  "
                    cursor.execute(inset_rezbook)
                    connection.commit()
                    itog_summs = int(kolvvo) * int(prices)
                    inset_bsk = f"INSERT INTO `basket` (id_c , id_b, quantity_b,itog_sum ) VALUES ('{uidd}','{id_cnigi}','{kolvvo}', '{itog_summs}')"
                    cursor.execute(inset_bsk)
                    connection.commit()



                    msg = "Добавление успешно!"
                    mb.showinfo("Информация", msg)
                    addb.destroy()

        btn_addd = Button(addb, text='Сохранить', command=saveadd).grid(row=11, column=1, padx= 100, pady = 5)
###############
    btn_addb = Button(window, text='Добавить книгу в корзину', command=addbooks).grid(row=26, column=2,ipadx=24)

    def updateadd():
        updb = Tk()
        updb.title("Обновление записи")
        updb.geometry('270x200')
        updb.configure(background='#66CDAA')
        # Лейблы
        lbl_one0 = Label(updb, text='Идентификатор книги', bg='#66CDAA').grid(row=6, column=1)
        lbl_one1 = Label(updb, text='Новое количество', bg='#66CDAA').grid(row=8, column=1)

        # Поля для ввода
        txt_one = Entry(updb, width=20)
        txt_one.grid(row=7, column=1)
        txt_two = Entry(updb, width=20)
        txt_two.grid(row=9, column=1)

        def saveupdateadd():
            id_knigi = txt_one.get()
            updkolvvo = txt_two.get()
            with connection.cursor() as cursor:
                sqll = f"SELECT * FROM `books` WHERE ID_B = '{id_knigi}'"
                cursor.execute(sqll)
                ress = cursor.fetchall()
                for i in ress:
                    id_alb = i['ID_B']
                    rezze = i['rezerv']
                    kolknig = i['kolvo_kn']


                sqll2 = f"SELECT * FROM `basket` WHERE id_b =  '{id_knigi}' ; "
                cursor.execute(sqll2)
                ress2 = cursor.fetchall()
                for i in ress2:
                    quan = i['quantity_b']

                rezerv2 = int(rezze) - int(quan)


                if int(updkolvvo) > int(kolknig) or int(updkolvvo) == 0:
                    msg = "Введеное количество книг превышает допустимое количество! Либо значение равно 0."
                    mb.showerror("Ошибка", msg)

                elif int(id_alb) < int(id_knigi):
                    msg = "Введеный идентификатор не существует!"
                    mb.showerror("Ошибка", msg)

                elif int(updkolvvo) <= int(kolknig):

                    dell_rezbook = f"UPDATE `books` SET rezerv = '{rezerv2}' WHERE ID_B = '{id_knigi}'  "
                    cursor.execute(dell_rezbook)
                    connection.commit()

                    dell_bsk = f"DELETE FROM `basket` WHERE id_b =  '{id_knigi}' ; "
                    cursor.execute(dell_bsk)
                    connection.commit()

                    sqll = f"SELECT * FROM `books` WHERE ID_B = '{id_knigi}'"
                    cursor.execute(sqll)
                    ress = cursor.fetchall()
                    for i in ress:
                        rezze2 = i['rezerv']
                        pricee = i['price']

                    rezerv = int(rezze2) + int(updkolvvo)

                    inset_rezbook = f"UPDATE `books` SET rezerv = '{rezerv}' WHERE ID_B = '{id_knigi}'  "
                    cursor.execute(inset_rezbook)
                    connection.commit()

                    itog_summ = int(pricee)* int(updkolvvo)
                    inset_bsk = f"INSERT INTO `basket` (id_c , id_b, quantity_b, itog_sum) VALUES ('{uidd}','{id_knigi}','{updkolvvo}', '{itog_summ}')"
                    cursor.execute(inset_bsk)
                    connection.commit()

                    msg = "Изменение успешно!"
                    mb.showinfo("Информация", msg)
                    updb.destroy()

        btn_addd = Button(updb, text='Сохранить', command=saveupdateadd).grid(row=11, column=1, padx=100, pady=5)
    btn_upd = Button(window, text='Изменить количество книг', command=updateadd).grid(row=26, column=1,ipadx=22)


    def deleteadd():
        dellb = Tk()
        dellb.title("Удаление записи")
        dellb.geometry('270x200')
        dellb.configure(background='#66CDAA')
        # Лейблы
        lbl_one0 = Label(dellb, text='Идентификатор книги', bg='#66CDAA').grid(row=6, column=1)

        # Поля для ввода
        txt_one = Entry(dellb, width=20)
        txt_one.grid(row=7, column=1)

        def savedeleteadd():
            id_knigi = txt_one.get()
            with connection.cursor() as cursor:
                sqll = f"SELECT * FROM `books` WHERE id_b =  '{id_knigi}'  ;"
                cursor.execute(sqll)
                ress = cursor.fetchall()
                for i in ress:
                    rezze = i['rezerv']

                sqll2 = f"SELECT * FROM `basket` WHERE id_b =  '{id_knigi}' ; "
                cursor.execute(sqll2)
                ress2 = cursor.fetchall()
                for i in ress2:
                    quan = i['quantity_b']


                rezerv2 = int(rezze) - int(quan)

                dell_rezbook = f"UPDATE `books` SET rezerv = '{rezerv2}' WHERE ID_B = '{id_knigi}'  "
                cursor.execute(dell_rezbook)
                connection.commit()

                dell_bsk = f"DELETE FROM `basket` WHERE id_b =  '{id_knigi}' ; "
                cursor.execute(dell_bsk)
                connection.commit()

            msg = "Удаление успешно!"
            mb.showinfo("Информация", msg)
            dellb.destroy()

        btn_dellb = Button(dellb, text='Сохранить', command=savedeleteadd).grid(row=11, column=1, padx=100, pady=5)

    btn_dellbs = Button(window, text='Удалить позицию из заказа', command=deleteadd).grid(row=28, column=1,ipadx=22)



    def check():
        msg = "Перепроверьте данные!"
        mb.showinfo("Информация", msg)

        check0 = Tk()
        check0.configure(background='#66CDAA')
        check0.title("Оформление заказа")
        check0.geometry('1007x450')
        lbl_one12 = Label(check0, text=f"Таблица с итоговыми данными по заказанным книгам. ", bg='#66CDAA').grid(row=5,column=1)
        columns = ("id", "name", "kolvo", "price1", "price")
        tree = ttk.Treeview(check0, columns=columns, show="headings")
        tree.grid(row=10, column=1, columnspan=2, sticky=EW, padx=1, pady=1)
        tree.heading("id", text="Идентификатор книги")
        tree.heading("name", text="Название книги")
        tree.heading("kolvo", text="Количество книг")
        tree.heading("price1", text="Цена книги 1 шт.")
        tree.heading("price", text="Итоговая сумма за книгу ")

        with connection.cursor() as cursor:
            cur1 = (f"SELECT basket.id_c,basket.id_b, basket.quantity_b, basket.itog_sum, books.ID_B, books.nazvanie, books.price FROM `basket`,`books`  WHERE basket.id_c = '{uid}' and basket.id_b = books.ID_B;")
            cursor.execute(cur1)
            reess = cursor.fetchall()
            for row in reess:
                a = (row['ID_B'])
                b = (row['nazvanie'])
                c = (row['quantity_b'])
                r = (row['price'])
                e = (row['itog_sum'])
                d = [(a), (b), (c), (r), (e)]
                tree.insert("", tk.END, values=(d))




        def check2():

            msg = "В разработке!"
            mb.showinfo("Информация", msg)


        btn_dellb = Button(check0, text='Перейти к оформлению чека >>', command=check2).grid(row=11, column=1)

    btn_check = Button(window, text='Перейти к оформлению заказа>>', command=check).grid(row=28, column=2,ipadx=1)

def registr():
        window2 = Tk()
        window2.title("Регистрация")
        window2.geometry('290x200')
        window2.configure(background='#66CDAA')
        txt_1 = Entry(window2, width=20)
        txt_1.grid(row=5, column=2)
        txt_2 = Entry(window2, width=20)
        txt_2.grid(row=6, column=2)
        txt_3 = Entry(window2, width=20)
        txt_3.grid(row=7, column=2)
        txt_4 = Entry(window2, width=20)
        txt_4.grid(row=8, column=2)
        txt_5 = Entry(window2, width=20)
        txt_5.grid(row=9, column=2)
        txt_6 = Entry(window2, width=20)
        txt_6.grid(row=10, column=2)
        lbl_one0 = Label(window2, text='ФИО',bg='#66CDAA').grid(row=5, column=1)
        lbl_one1 = Label(window2, text='Логин',bg='#66CDAA').grid(row=6, column=1)
        lbl_one2 = Label(window2, text='Пароль',bg='#66CDAA').grid(row=7, column=1)
        lbl_one3 = Label(window2, text='Номер телефона',bg='#66CDAA').grid(row=8, column=1)
        lbl_one4 = Label(window2, text='Почта',bg='#66CDAA').grid(row=9, column=1)
        lbl_one4 = Label(window2, text='Паспорт',bg='#66CDAA').grid(row=10, column=1)


        def registr2():
            with connection.cursor() as cursor:
                q = txt_1.get()
                w = txt_2.get()
                e = txt_3.get()
                r = txt_4.get()
                t = txt_5.get()
                y = txt_6.get()

                if q == '' or w == '' or e == '' or r == '' or t == '' or y == '':
                    msg = "Поля не заполнены"
                    mb.showerror("Ошибка", msg)
                else:
                    sqll = f"SELECT * FROM `users`"
                    cursor.execute(sqll)
                    ress = cursor.fetchall()
                    for i in ress:
                        loginss = i['login']

                        if loginss == w:
                            msg = "Данный логин уже существует!"
                            mb.showerror("Ошибка", msg)
                if len(e)<8:
                    msg = "Невозможный пароль!"
                    mb.showerror("Ошибка", msg)
                if len(e)>8:
                        sql = f"INSERT INTO `users` (FIO,login,password,phone,email,passport) VALUES ('{q}','{w}','{e}','{r}','{t}','{y}')"
                        cursor.execute(sql)
                        connection.commit()
                        msg = "Добавление успешно!"
                        mb.showinfo("Информация", msg)
                        window2.destroy()


        btn_reg = Button(window2, text='Зарегистрироваться', command=registr2).grid(row=12, column=2)
        window2.mainloop()


def manageravtoriz():
    # Функция авторизации и вывода
    with connection.cursor() as cursor:
        log2 = txt_one.get()
        pas2 = txt_two.get()

        sql = f"SELECT * FROM `manager` WHERE login = '{log2}' and password = '{pas2}'"

        cursor.execute(sql)
        res = cursor.fetchone()
        if res == None:
            msg = "Неверный логин или пароль"
            mb.showerror("Ошибка", msg)
        else:
            sqll = f"SELECT * FROM `manager` WHERE login = '{log2}' and password= '{pas2}'"
            cursor.execute(sqll)
            ress = cursor.fetchall()
            for i in ress:
                muid = i['id_m']
                sqll = f"SELECT * FROM `manager` WHERE id_m = '{muid}'"
                cursor.execute(sqll)
                ress = cursor.fetchall()
                root1.destroy()
                for i in ress:
                    ass = i['FIO']
                    uidd = i['id_m']

                    mwindow = Tk()
                    mwindow.configure(background='#66CDAA')
                    mwindow.title("Книги ")
                    mwindow.geometry('1402x450')
                    columns = ("id", "name", "pages", "age", "kolvo", "price", "rezerv")
                    tree = ttk.Treeview(mwindow, columns=columns, show="headings")
                    tree.grid(row=10, column=1, columnspan=2, sticky=EW, padx=1, pady=1)
                    tree.heading("id", text="Идентификатор книги")
                    tree.heading("name", text="Название книги")
                    tree.heading("pages", text="Количество листов")
                    tree.heading("age", text="Возраст книги")
                    tree.heading("kolvo", text="Количество книг")
                    tree.heading("price", text="Цена книги [1 шт.]")
                    tree.heading("rezerv", text="Зарезервированные книги")
                    cur1 = (f"SELECT * FROM `books`")
                    cursor.execute(cur1)
                    reess = cursor.fetchall()
                    for row in reess:
                        a = (row['ID_B'])
                        b = (row['nazvanie'])
                        c = (row['pages'])
                        c1 = (row['age'])
                        c2 = (row['kolvo_kn'])
                        c3 = (row['price'])
                        c4 = (row['rezerv'])
                        d = [(a), (b), (c), (c1), (c2), (c3), (c4)]
                        tree.insert("", tk.END, values=(d))

    def madd():
        maddb = Tk()
        maddb.title("Добавление книги")
        maddb.geometry('270x300')
        maddb.configure(background='#66CDAA')
        # Лейблы
        lbl_one0 = Label(maddb, text='Название книги', bg='#66CDAA').grid(row=6, column=1)
        lbl_one1 = Label(maddb, text='Количество листов', bg='#66CDAA').grid(row=8, column=1)
        lbl_one2 = Label(maddb, text='Возраст книги', bg='#66CDAA').grid(row=10, column=1)
        lbl_one3 = Label(maddb, text='Количество книг (всего) ', bg='#66CDAA').grid(row=12, column=1)
        lbl_one4 = Label(maddb, text='Цена за 1 шт.', bg='#66CDAA').grid(row=14, column=1)

        # Поля для ввода
        txt_one = Entry(maddb, width=20)
        txt_one.grid(row=7, column=1)
        txt_two = Entry(maddb, width=20)
        txt_two.grid(row=9, column=1)
        txt_tree = Entry(maddb, width=20)
        txt_tree.grid(row=11, column=1)
        txt_fr = Entry(maddb, width=20)
        txt_fr.grid(row=13, column=1)
        txt_fv = Entry(maddb, width=20)
        txt_fv.grid(row=15, column=1)

        def msaveadd():
            name_book = txt_one.get()
            pages = txt_two.get()
            age = txt_tree.get()
            kolvo = txt_fr.get()
            price = txt_fv.get()

            with connection.cursor() as cursor:
                a = 0
                inset_bk = f"INSERT INTO `books` (nazvanie , pages, age, kolvo_kn, price, rezerv ) VALUES ('{name_book}','{pages}','{age}','{kolvo}','{price}','{a}' );"
                cursor.execute(inset_bk)
                connection.commit()

                msg = "Добавление успешно!"
                mb.showinfo("Информация", msg)
                maddb.destroy()

        btn_addd = Button(maddb, text='Сохранить', command=msaveadd).grid(row=20, column=1, padx=100, pady=5)

    btn_addb = Button(mwindow, text='Добавить книгу', command=madd).grid(row=26, column=1)



    def mupdbooks():
        mupdb = Tk()
        mupdb.title("Изменение книги")
        mupdb.geometry('270x300')
        mupdb.configure(background='#66CDAA')
        # Лейблы
        lbl_one00 = Label(mupdb, text='Идентификатор книги', bg='#66CDAA').grid(row=6, column=1)
        lbl_one0 = Label(mupdb, text='Название книги', bg='#66CDAA').grid(row=8, column=1)
        lbl_one1 = Label(mupdb, text='Количество страниц', bg='#66CDAA').grid(row=10, column=1)
        lbl_one2 = Label(mupdb, text='Возраст книги', bg='#66CDAA').grid(row=12, column=1)
        lbl_one3 = Label(mupdb, text='Количество книг (всего) ', bg='#66CDAA').grid(row=14, column=1)
        lbl_one4 = Label(mupdb, text='Цена за 1 шт.', bg='#66CDAA').grid(row=16, column=1)

        # Поля для ввода
        txt_zr = Entry(mupdb, width=20)
        txt_zr.grid(row=7, column=1)
        txt_one = Entry(mupdb, width=20)
        txt_one.grid(row=9, column=1)
        txt_two = Entry(mupdb, width=20)
        txt_two.grid(row=11, column=1)
        txt_tree = Entry(mupdb, width=20)
        txt_tree.grid(row=13, column=1)
        txt_fr = Entry(mupdb, width=20)
        txt_fr.grid(row=15, column=1)
        txt_fv = Entry(mupdb, width=20)
        txt_fv.grid(row=17, column=1)

        def msaveupd():
            id_b = txt_zr.get()
            name_book = txt_one.get()
            pages = txt_two.get()
            age = txt_tree.get()
            kolvo = txt_fr.get()
            price = txt_fv.get()

            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            if name_book == '':
                a = a + 1
            else:
                with connection.cursor() as cursor:
                    upd_bk0 = f"UPDATE `books` SET nazvanie = '{name_book}' WHERE ID_B = '{id_b}'  "
                    cursor.execute(upd_bk0)
                connection.commit()

            if pages == '':
                b = b + 1
            else:
                with connection.cursor() as cursor:
                    upd_bk1 = f"UPDATE `books` SET pages = '{pages}' WHERE ID_B = '{id_b}'  "
                    cursor.execute(upd_bk1)
                connection.commit()

            if age == '':
                c = c + 1
            else:
                with connection.cursor() as cursor:
                    upd_bk2 = f"UPDATE `books` SET age = '{age}' WHERE ID_B = '{id_b}'  "
                    cursor.execute(upd_bk2)
                connection.commit()

            if kolvo == '':
                d = d + 1
            else:
                with connection.cursor() as cursor:
                    upd_bk3 = f"UPDATE `books` SET kolvo_kn = '{kolvo}' WHERE ID_B = '{id_b}'  "
                    cursor.execute(upd_bk3)
                connection.commit()

            if price == '':
                e = e + 1
            else:
                with connection.cursor() as cursor:
                    upd_bk4 = f"UPDATE `books` SET price = '{price}' WHERE ID_B = '{id_b}'  "
                    cursor.execute(upd_bk4)
                connection.commit()


            msg = "Обновление успешно!"
            mb.showinfo("Информация", msg)
            mupdb.destroy()

        btn_addd = Button(mupdb, text='Сохранить', command=msaveupd).grid(row=22, column=1, padx=100, pady=5)

    btn_addb = Button(mwindow, text='Обновить информацию о книге', command=mupdbooks).grid(row=25, column=2)


    def books2():
        for i in tree.get_children():
            tree.delete(i)
        with connection.cursor() as cursor:
            cur1 = (f"SELECT * FROM `books`")
            cursor.execute(cur1)
            reess = cursor.fetchall()
            for row in reess:
                a = (row['ID_B'])
                b = (row['nazvanie'])
                c = (row['pages'])
                c1 = (row['age'])
                c2 = (row['kolvo_kn'])
                c3 = (row['price'])
                c4 = (row['rezerv'])
                d = [(a), (b), (c), (c1), (c2), (c3), (c4)]
                tree.insert("", tk.END, values=(d))
    btn_sel2= Button(mwindow, text='Вывести список книг', command=books2).grid(row=25,column=1)

    def mdeleteadd():
        dellb = Tk()
        dellb.title("Удаление записи")
        dellb.geometry('270x200')
        dellb.configure(background='#66CDAA')
        # Лейблы
        lbl_one0 = Label(dellb, text='Идентификатор книги', bg='#66CDAA').grid(row=6, column=1)

        # Поля для ввода
        txt_one = Entry(dellb, width=20)
        txt_one.grid(row=7, column=1)

        def msavedeleteadd():
            id_bk = txt_one.get()
            with connection.cursor() as cursor:
                dell_bsk = f"DELETE FROM `books` WHERE id_b =  '{id_bk}' ; "
                cursor.execute(dell_bsk)
                connection.commit()

            msg = "Удаление успешно!"
            mb.showinfo("Информация", msg)
            dellb.destroy()

        btn_dellb = Button(dellb, text='Сохранить', command=msavedeleteadd).grid(row=11, column=1, padx=100, pady=5)

    btn_dellbs = Button(mwindow, text='Удалить книгу', command=mdeleteadd).grid(row=26, column=2)



#Авторизация
root1 = Tk()
root1.title("Авториация")
root1.geometry('290x200')
root1.configure(background='#66CDAA')
#Лейблы
lbl_one0 = Label(root1, text='Логин',bg='#66CDAA').grid(row=6, column=5)
lbl_one1 = Label(root1, text='Пароль',bg='#66CDAA').grid(row=8, column=5)
#Поля для ввода
txt_one = Entry(root1, width=20)
txt_one.grid(row=7, column=5)
txt_two = Entry(root1, width=20)
txt_two.grid(row=9, column=5)
#Поля для ввода
#Кнопки
btn_save = Button(text='Авторизоваться', command=save_to_bdysl).grid(row=25, column=5, padx= 100, pady = 5)
btn_reg = Button(text='Зарегистрироваться', command=registr).grid(row=26, column=5, pady = 5)
btn_mng = Button(text='Авторизация менеджера', command=manageravtoriz).grid(row=27, column=5, pady = 5)
#Кнопки
root1.mainloop()

