# ЛР. Работа с БД

import pymysql
import openpyxl

from connect import host, user, password, database

# Обработка исключний
try:
   # Подключение к базе данных при помощи connect()
   connection = pymysql.connect(
       host=host,
       port=3306,
       user=user,
       password=password,
       database=database,
       cursorclass=pymysql.cursors.DictCursor
   )
   print('Successfully connected...')
   print("#" * 20)

   try:
       cursor = connection.cursor()
       wb = openpyxl.load_workbook('C:\\Users\\student\\Desktop\\test.xlsx')
       sheet = wb.active
       print('Данные импортированы успешно!')
       for i in range(6, 37):  # Читаем со 2-й строки (1-я заголовок)
           nz = sheet[f'A{i}'].value
           naimen = sheet[f'B{i}'].value
           max = sheet[f'C{i}'].value
           kons = sheet[f'D{i}'].value
           vsego = sheet[f'E{i}'].value
           lekcii = sheet[f'F{i}'].value
           pract = sheet[f'G{i}'].value
           lr = sheet[f'H{i}'].value
           kursov = sheet[f'I{i}'].value
           samost = sheet[f'J{i}'].value
           ip = sheet[f'K{i}'].value
           zadan = sheet[f'L{i}'].value

           cursor.execute("""insert into excell(nz, naimen, max, kons, vsego, lekcii, pract, lr,kursov, samost, ip, zadan)
                         values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (nz, naimen, max, kons, vsego, lekcii, pract, lr,kursov, samost, ip, zadan ))
           connection.commit()


   finally:
       connection.close()


except Exception as ex:
   print('Connection refused...')
   print(ex)
