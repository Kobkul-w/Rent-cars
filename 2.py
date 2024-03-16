import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from tkinter import filedialog 
from tkcalendar import DateEntry
import PyPDF2
import re
import os
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
import yagmail
from yagmail.error import YagConnectionClosed
from datetime import datetime
from tkinter import Toplevel




conn = sqlite3.connect(r'D:\Phyton\project\new.db')
cursor = conn.cursor()
try :
    cursor.execute('''CREATE TABLE car_order(id INTEGER PRIMARY KEY,
                    username TEXT,
                    phone_num INTEGER,
                    car_type TEXT,
                    rental_days DATE,
                    rental_date DATE,
                    return_day DATE,
                    driver_age INTEGER,
                    payment TEXT,
                    late_fee REAL,
                    damages TEXT,
                    return_status TEXT)''')

    cursor.execute('''CREATE TABLE customers (id INTEGER PRIMARY KEY,
                    username TEXT,
                    billing_name TEXT,
                    email TEXT,
                    phone_number TEXT,
                    file_pdf BLOB,
                    flight_number TEXT,
                    billing_phone_number TEXT,
                    billing_country TEXT,
                    billing_address TEXT,
                    billing_city_province TEXT,
                    billing_zip_code TEXT)''')
    cursor.execute('''CREATE TABLE orders (id INTEGER PRIMARY KEY,
                    username TEXT,
                    phone_num INTEGER,
                    car_type TEXT,
                    rental_days DATE,
                    rental_date DATE,
                    driver_age INTEGER)''')
    conn.commit()
except :
    pass
available_cars = {
    'รถกะบะ': {'name': 'All New ISUZU D-MAX', 'type': 'S', 'price_per_day': 2000},
    'รถเก๋ง': {'name': 'MERCEDES BENZ A CLASS 220D', 'type': 'M', 'price_per_day': 9000},
    'รถSUV': {'name': 'Honda HR-V', 'type': 'L', 'price_per_day': 3000},
    'รถตู้': {'name': 'TOYOTA ALPHARD (7 ที่นั่ง)', 'type': 'XL', 'price_per_day': 12000}
}

def calculate_total_cost(car_type, rental_days):
    price_per_day = int(available_cars[car_type]['price_per_day'])
    deposit = 5000
    total_cost = deposit + (int(price_per_day) * int(rental_days))
    return total_cost
def rent_car () :
    rent = Toplevel(root)
    rent.title("จองรถ")
    rent.geometry("800x600+250+20")
    
    rent_image = Image.open(r"D:\Phyton\project\BG-rent.png")
    rent_photo = ImageTk.PhotoImage(rent_image)
    rent_label = tk.Label(rent,image=rent_photo)
    rent_label.photo =rent_photo
    rent_label.place(x=0, y=0) 

    rate_button = tk.Button(rent, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
    rate_button.config(font=("Arial", 12,'bold'))
    rate_button.place(x=240, y=23)

    menu_button = tk.Button(rent, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
    menu_button.config(font=("Arial", 12,'bold'))
    menu_button.place(x=340, y=23)

    booking_button = tk.Button(rent, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
    booking_button.config(font=("Arial", 12,'bold'))
    booking_button.place(x=440, y=23)

    contact_button = tk.Button(rent, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
    contact_button.config(font=("Arial", 12,'bold'))
    contact_button.place(x=540, y=23)

    admin_button = tk.Button(rent, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
    admin_button.config(font=("Arial", 12,'bold'))
    admin_button.place(x=655, y=23)

    exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
    exit_photo = ImageTk.PhotoImage(exit_image)
    exit_label = tk.Label(rent,image=exit_photo)
    exit_label.photo = exit_photo
    exit_button = tk.Button(rent,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
    exit_button.place(x=740, y=20)

    result_label=tk.Label(rent, text="")
    result_label.pack() 


    def book_car() :
        def calculate_total_cost(rental_days, rental_date):
            deposit = 5000 
            price_per_day = available_cars[car_type]['price_per_day']
            rental_days = (rental_days - rental_date).days
            total_cost = deposit + (int(price_per_day) * rental_days)
            return total_cost
        def send_email():
            email = email_entry.get()
            rental_days = rental_days_entry.get_date()
            deposit = 5000 
            total_cost = calculate_total_cost(rental_days, rental_date)
            try:
                email_sender = "minesunshy3@gmail.com"
                app_password = "rimb qhyl xtdd cylu" 
                recipients = [email]
                text=f"ขอบคุณที่ใช้บริการ เจ๊นุ้ยทรงเชง \nUsernameของคุณคือ:  {username} \nคุณได้เช่ารถ:  {car_type} \nตั้งแต่วันที่: {rental_date} \nจนถึงวันที่: {rental_days} \nค่ามัดจำ:  {deposit} \nรวมเป็นเงิน:  {total_cost}",
                yag = yagmail.SMTP(email_sender, app_password)
                yag.send(
                    to=recipients,
                    subject="recipe",
                    contents=text 
                )
                messagebox.showinfo("Success", "Email sent successfully!")
                yag.close()
            except YagConnectionClosed:
                messagebox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")


        username = username_entry.get()
        car_type = car_type_var.get()
        rental_days = rental_days_entry.get_date()
        rental_date = rental_date_entry.get_date()
        driver_age = driver_age_entry.get()
        email = email_entry.get()
        phone = phone_entry.get() 
        flight = flight_entry.get() 
        pdf = pdf_entry.get() 
        name = name_entry.get()  
        phone_number = billing_phone_entry.get() 
        country = billing_country_entry.get() 
        address = billing_address_entry.get()  
        province = billing_city_entry.get() 
        zip = billing_zip_entry.get()
        
        conn = sqlite3.connect(r'D:\Phyton\project\new.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM customers WHERE username = ?', (username,))
        count = cursor.fetchone()[0]
        current_date = datetime.now()
        if rental_date < current_date:
            return False
        elif count > 0:
            messagebox.showinfo("Error", "Username นี้ถูกใช้ไปแล้ว\nกรุณากรอกข้อมูลใหม่.")
            return False
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$',username):
            print("OK3")
            messagebox.showinfo("EROR", "Username ต้องประกอบด้วยตัวอักษรและเลข")
            return False
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showinfo("Error", "Invalid email address. Please enter a valid email.")
            return False
        elif isinstance (rental_days,(int)):
            messagebox.showinfo("EROR","กรอกเป็นตัวเลขเท่านั้น!!")      
            return False       
        elif isinstance (driver_age,(int)) :
            messagebox.showinfo("EROR","กรอกเป็นตัวเลขเท่านั้น")
            if driver_age < 18:
                messagebox.showinfo("EROR","คนขับต้องมีอายุมากกว่ากรือเท่ากับ 18 ปี")
                return False
        elif len(phone) != 10:
            messagebox.showinfo("EROR","เบอร์โทรศัพท์ต้องมี 10 หลัก")
            return False
        elif not all([pdf,name,phone_number,country,address,province,zip,email,
                    username,car_type,rental_days,rental_date,driver_age,phone]):
            print("OK1")
            messagebox.showinfo("EROR,กรุณากรอกข้อมูลให้ครบถ้วน")
        elif isinstance (zip,(int)):
            messagebox.showinfo("EROR","กรอกเป็นตัวเลขเท่านั้น!!")      
            return False  
        elif len(phone_number) != 10:
            messagebox.showinfo("EROR","เบอร์โทรศัพท์ต้องมี 10 หลัก")
            return False    
        else:
            try:
                print("OK2")
                conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO orders (username,phone_num, car_type, rental_days, rental_date, driver_age)
                                        VALUES (?, ?, ?, ?, ?, ?)
                                        ''', (username,phone, car_type, rental_days, rental_date, driver_age,))
                cursor.execute('''INSERT INTO car_order (username, phone_num, car_type, rental_days, rental_date, driver_age)
                                            VALUES (?, ?, ?, ?, ? ,?)
                                            ''', (username,phone, car_type, rental_days, rental_date, driver_age))
                cursor.execute('''INSERT INTO customers (username, email, file_pdf, phone_number, flight_number, billing_name, 
                                        billing_phone_number, billing_country, billing_address, 
                                        billing_city_province, billing_zip_code)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                        ''', (username, email, pdf, phone, flight, name, phone_number, country, address, province, zip))
                
                messagebox.showinfo("จองรถสำเร็จ!", f"User {username} อายุ {driver_age} ปี ได้เช่า {available_cars[car_type]['name']} ประเภท {available_cars[car_type]['type']} เป็นเวลา {rental_days} วัน ตั้งแต่ {rental_date} เรียบร้อยแล้ว")
                conn.commit()
                conn.close()
                print("4444")
                send_email()
                print("5555")
                rent.destroy()
            except ValueError:
                print("22222")
                messagebox.showinfo("EROR","กรุณากรอกข้อมูลให้ถูกต้อง!!")
                return False
           
    username_label = tk.Label(rent, text="Username :",bg='white',fg='black')
    username_label.config(font=("Arial", 7,'bold'))
    username_label.place(x=262,y=165)
    username_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    username_entry.place (x=320,y=165,width=95)

    car_type_label = tk.Label(rent, text="ประเภทรถ :",bg='white',fg='black')
    car_type_label.config(font=("Arial", 7,'bold'))
    car_type_label.place(x=432,y=163)
    available_car_types = list(available_cars.keys())
    car_type_var = tk.StringVar(rent)
    car_type_var.set(available_car_types[0])
    car_type_option_menu = tk.OptionMenu(rent, car_type_var, *available_car_types)
    car_type_option_menu.place (x=485,y=157,width=95)

    rental_label = tk.Label(rent, text="วันที่รับรถ :",bg='white',fg='black')
    rental_label.config(font=("Arial", 7,'bold'))
    rental_label.place(x=262,y=205)
    rental_date_entry = DateEntry(rent, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy,mm,dd')
    rental_date_entry.place(x=321,y=202,width=95)

    rental_days__label = tk.Label(rent, text="เช่าถึงวันที่ :",bg='white',fg='black')
    rental_days__label.config(font=("Arial", 7,'bold'))
    rental_days__label.place(x=432,y=205)
    rental_days_entry = DateEntry(rent, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy,mm,dd')
    rental_days_entry.place (x=485,y=202,width=93)

    cc_label = tk.Label(rent, text="ข้อมูลผู้ขับขี่ (ชื่อผู้ขับขี่ต้องเป็นชื่อเดียวกับผู้ที่มารับรถ)",bg='white',fg='black')
    cc_label.config(font=("Arial", 9,'bold'))
    cc_label.place(x=277,y=230)
    

    name_label = tk.Label(rent, text="ชื่อ :",bg='white',fg='black')
    name_label.config(font=("Arial", 7,'bold'))
    name_label.place(x=265,y=260)
    name_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    name_entry.place(x=290,y=260,width=285)

    email_label = tk.Label(rent, text="email :",bg='white',fg='black')
    email_label.config(font=("Arial", 7,'bold'))
    email_label.place(x=264,y=300)
    email_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    email_entry.place(x=305,y=300,width=272)

    phone_label = tk.Label(rent, text="หมายเลขโทรศัพท์ :",bg='white',fg='black')
    phone_label.config(font=("Arial", 7,'bold'))
    phone_label.place(x=263,y=340)
    phone_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    phone_entry.place(x=350,y=340,width=227)

    address_label = tk.Label(rent, text="ที่อยู่ :",bg='white',fg='black')
    address_label.config(font=("Arial", 7,'bold'))
    address_label.place(x=263,y=380)
    billing_address_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    billing_address_entry.place(x=297,y=380,width=110)

    city_label = tk.Label(rent, text="จังหวัด :",bg='white',fg='black')
    city_label.config(font=("Arial", 7,'bold'))
    city_label.place(x=430,y=379)
    billing_city_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    billing_city_entry.place(x=465,y=379,width=112)

    zip_label = tk.Label(rent, text="รหัสไปรษณีย์ :",bg='white',fg='black')
    zip_label.config(font=("Arial", 7,'bold'))
    zip_label.place(x=263,y=421,)
    billing_zip_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    billing_zip_entry.place(x=322,y=421,width=87)

    country_label = tk.Label(rent, text="ประเทศ :",bg='white',fg='black')
    country_label.config(font=("Arial", 7,'bold'))
    country_label.place(x=432,y=421,)
    billing_country_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    billing_country_entry.place(x=470,y=420,width=100)

    age_label = tk.Label(rent, text="อายุคนขับ :",bg='white',fg='black')
    age_label.config(font=("Arial", 7,'bold'))
    age_label.place(x=263,y=468)
    driver_age_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    driver_age_entry.place(x=322,y=468,width=75)

    flight_label = tk.Label(rent, text="หมายเลขเที่ยวบิน :",bg='white',fg='black')
    flight_label.config(font=("Arial", 7,'bold'))
    flight_label.place(x=430,y=468)
    flight_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    flight_entry.place(x=507,y=468,width=70)

    pdf_label = tk.Label(rent, text="ไฟล์pdf :",bg='white',fg='black')
    pdf_label.config(font=("Arial", 7,'bold'))
    pdf_label.place(x=430,y=518)
    pdf_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0, width=40)
    pdf_entry.place(x=474,y=516,width=95)
    pdf_button = tk.Button(rent, text="Browse", command=lambda: browse_pdf(pdf_entry))
    pdf_button.place(x=588,y=513,width=60)
    def browse_pdf(pdf_entry):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf_entry.delete(0, tk.END)  
            pdf_entry.insert(0, file_path)
            return False
    
    phone_label = tk.Label(rent, text="หมายเลขโทรศัพท์ :",bg='white',fg='black')
    phone_label.config(font=("Arial", 7,'bold'))
    phone_label.place(x=260,y=519)
    billing_phone_entry = tk.Entry(rent,borderwidth=0, highlightthickness=0)
    billing_phone_entry.place(x=341,y=517,width=70)

    save_image = Image.open(r"D:\Phyton\project\B-rental.png")
    save_photo = ImageTk.PhotoImage(save_image)
    save_label = tk.Label(rent,image=save_photo)
    save_label.photo = save_photo
    save_button = tk.Button(rent, image=save_photo,width=50, height=25,borderwidth=0, highlightthickness=0, command=book_car)
    save_button.place(x=390,y=570)

    back_image = Image.open(r"D:\Phyton\project\B-back.png")
    back_photo = ImageTk.PhotoImage(back_image)
    back_label = tk.Label(rent,image=back_photo)
    back_label.photo = back_photo
    back_button = tk.Button(rent, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=rent.destroy)
    back_button.place(x=9, y=556)
    
    home_image = Image.open(r"D:\Phyton\project\B-home.png")
    home_photo = ImageTk.PhotoImage(home_image)
    homes_label = tk.Label(rent,image=home_photo)
    homes_label.photo = home_photo
    home_button = tk.Button(rent, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=rent.destroy)
    home_button.place(x=54, y=556)



global rental_days
def menu () :
    menu = Toplevel(root)
    menu.title("menu")
    menu.geometry("800x600+250+20")
    result_label=tk.Label(menu, text="")
    result_label.pack()

    menu_image = Image.open(r"D:\Phyton\project\BG-menu.png")
    menu_photo = ImageTk.PhotoImage(menu_image)
    menu_label = tk.Label(menu,image=menu_photo)
    menu_label.photo =menu_photo
    menu_label.place(x=0, y=0) 
  
    
    def cancel_order () :
        cancel_wind = Toplevel(root)
        cancel_wind.title("เจ้นุยทรงเชง")
        cancel_wind.geometry("800x600+250+20")

        def home () :
            cancel_wind.destroy()
            menu.destroy()

        def cancel () :
            print('1')
            id =cancel_username.get()
            conn = sqlite3.connect(r'D:\Phyton\project\new.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE username=?", (id,))
            selected_car = cursor.fetchone()
            def send_email():
                email = selected_car[3]
                username = selected_car[1] 
                try:
                    email_sender = "minesunshy3@gmail.com"
                    app_password = "rimb qhyl xtdd cylu" 
                    recipients = [email]
                    text=f"ขอบคุณที่ใช้บริการ เจ๊นุ้ยทรงเชง \nusername{username}ได้ยกเลิกการจองเรียบร้อยแล้ว\nโอกาศหน้าเชิญใหม่นะจ๊ะ",
                    yag = yagmail.SMTP(email_sender, app_password)
                    yag.send(
                        to=recipients,
                        subject="recipe",
                        contents=text 
                    )
                    messagebox.showinfo("Success", "Email sent successfully!")
                    yag.close()
                except YagConnectionClosed:
                    messagebox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")

            if selected_car:
                print("2")
                cursor.execute("DELETE FROM orders WHERE username=?", (id,))
                print('3')
                cursor.execute("UPDATE car_order SET payment='ยกเลิกการจอง' WHERE username=?", (id,))
                send_email()
                messagebox.showinfo("ยกเลิกการจอง", f"ยกเลิกการจองคุณ {id} เรียบร้อย")
            else:
                messagebox.showerror("ไม่พบการจอง", f"ไม่พบการจองสำหรับคุณ {id}")
            cancel_wind.destroy()
            conn.commit()
            conn.close()

        
        cancel_image = Image.open(r"D:\Phyton\project\BG-cancel.png")
        cancel_photo = ImageTk.PhotoImage(cancel_image)
        cancel_label = tk.Label(cancel_wind,image=cancel_photo)
        cancel_label.photo =cancel_photo
        cancel_label.place(x=0, y=0)
        
        cancel_label = tk.Label(cancel_wind,bg='#FDFDFC',fg='black', text="กรุณากรอก username เพื่อยกเลิกการจอง")
        cancel_label.place(x=285,y=235)
        cancel_username=tk.Entry(cancel_wind,borderwidth=0, highlightthickness=0)
        cancel_username.place(x=291,y=265,width=220)
        search_botton=tk.Button(cancel_wind, text="ยกเลิก",bg='#000000',fg='white',width =5, command=cancel)
        search_botton.place(x=380,y=310)

        rate_button = tk.Button(cancel_wind, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
        rate_button.config(font=("Arial", 12,'bold'))
        rate_button.place(x=240, y=23)

        menu_button = tk.Button(cancel_wind, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
        menu_button.config(font=("Arial", 12,'bold'))
        menu_button.place(x=340, y=23)

        booking_button = tk.Button(cancel_wind, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
        booking_button.config(font=("Arial", 12,'bold'))
        booking_button.place(x=440, y=23)

        contact_button = tk.Button(cancel_wind, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
        contact_button.config(font=("Arial", 12,'bold'))
        contact_button.place(x=540, y=23)

        admin_button = tk.Button(cancel_wind, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
        admin_button.config(font=("Arial", 12,'bold'))
        admin_button.place(x=655, y=23)

        exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
        exit_photo = ImageTk.PhotoImage(exit_image)
        exit_label = tk.Label(cancel_wind,image=exit_photo)
        exit_label.photo = exit_photo
        exit_button = tk.Button(cancel_wind,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
        exit_button.place(x=740, y=20)

        back_image = Image.open(r"D:\Phyton\project\B-back.png")
        back_photo = ImageTk.PhotoImage(back_image)
        back_label = tk.Label(cancel_wind,image=back_photo)
        back_label.photo = back_photo
        back_button = tk.Button(cancel_wind, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=cancel_wind.destroy)
        back_button.place(x=9, y=556)
        
        home_image = Image.open(r"D:\Phyton\project\B-home.png")
        home_photo = ImageTk.PhotoImage(home_image)
        homes_label = tk.Label(cancel_wind,image=home_photo)
        homes_label.photo = home_photo
        home_button = tk.Button(cancel_wind, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=home)
        home_button.place(x=54, y=556)
        
    def payment () :
        payment = Toplevel(root)
        payment.title("Payment")
        payment.geometry("800x600+250+20")
        def home () :
            payment.destroy()
            menu.destroy()
        def calculate_total_cost(car_type,rental_days, rental_date):
                deposit = 5000  # ใช้ค่า deposit ที่คงที่หรือต้องการ
                # ดึงราคาต่อวันของรถจาก available_cars
                price_per_day = available_cars[car_type]['price_per_day']

                # คำนวณจำนวนวันระหว่างวันเริ่มต้นและวันสิ้นสุด
                rental_days = (rental_days - rental_date).days

                # คำนวณราคารวม
                total_cost = deposit + (int(price_per_day) * rental_days)
                return total_cost
        def confirm():
            global car_type
            id_pay = payment_entry.get()
    

            try:
                conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM car_order WHERE username=?", (id_pay,))
                selected_car = cursor.fetchone()
                car_type = selected_car[2]

                if not selected_car:
                    messagebox.showerror("Error", f"ไม่พบการจองสำหรับ User {id_pay}")
                elif selected_car[5] == 'จ่ายแล้ว':
                    messagebox.showinfo("Payment", f"User {id_pay} ได้ทำการชำระเงินเรียบร้อยแล้ว")
                else:
                    car_type = selected_car[3]
                    print({car_type})
                    rental_days_str = selected_car[4]
                    rental_days = datetime.strptime(rental_days_str, '%Y-%m-%d').date()
                    rental_date_str = selected_car[5]
                    rental_date = datetime.strptime(rental_date_str, '%Y-%m-%d').date()

                    print({rental_days})
                    print ({rental_date})
                    total_cost = calculate_total_cost(car_type,rental_days, rental_date)
                    print({total_cost})
                    payment_message = (
                            f"รายละเอียดการชำระเงินสำหรับ {id_pay}:\n"
                            f"รถที่เช่า: {available_cars[car_type]['name']} ({available_cars[car_type]['type']})\n"
                            f"จำนวนวันเช่า: {rental_days} วัน\n"
                            f"วันที่เช่า: {rental_date}\n"
                            f"ราคาเช่ารวม: {total_cost:.2f} บาท\n\n"
                            "คุณทำการชำระเงินเรียบร้อยแล้วใช่หรือไม่?"
                        )
                    def send_email():
                        try:
                            cursor.execute("SELECT * FROM customers WHERE username=?", (id_pay,))
                            selected= cursor.fetchone()
                            email =selected[3]
                            email_sender = "minesunshy3@gmail.com"
                            app_password = "rimb qhyl xtdd cylu" 
                            recipients = [email]
                            qr_path = r'C:\Users\Admin\Desktop\qr.jpg'
                            attachments = (qr_path,) 
                            payment_message = (
                                f"รายละเอียดการชำระเงินสำหรับ {id_pay}:\n"
                                f"รถที่เช่า: {available_cars[car_type]['name']} ({available_cars[car_type]['type']})\n"
                                f"เริ่มเช่าวันที่: {rental_date} วัน\n"
                                f"เช่าถึงวันที่: {rental_days}\n"
                                f"ราคาเช่ารวม: {total_cost:.2f} บาท\n\n"
                                "กรุณาชำระเงินให้เรียบร้อย"
                            )

                            yag = yagmail.SMTP(email_sender, app_password)
                            if os.path.exists(qr_path):
                                yag.send(
                                    to=recipients,
                                    subject="recipe",
                                    contents=(payment_message,),
                                    attachments=attachments
                                )
                            else:
                                messagebox.showerror("Error", f"The QR image file '{qr_path}' does not exist or is invalid.")

                            messagebox.showinfo("Success", "Email sent successfully!")
                            yag.close()
                        except YagConnectionClosed:
                            messagebox.showerror("Error", "Connection to the email server failed. Please check your credentials and internet connection.")
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")
                    send_email()
                    payment_confirmed = messagebox.askyesno("Payment Confirmation", payment_message)
                    if payment_confirmed is not None and payment_confirmed:
                        cursor.execute("UPDATE car_order SET payment='จ่ายแล้ว' WHERE username=?", (id_pay,))
                        messagebox.showinfo("Payment", "ชำระเงินสำเร็จ!")
                        payment.destroy()
                    elif payment_confirmed is not None and not payment_confirmed:
                        messagebox.showinfo("Payment", "ยกเลิกการชำระเงิน")
                        payment.destroy()
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                conn.commit()
                conn.close()
        
        payment_image = Image.open(r"D:\Phyton\project\BG-pay.png")
        payment_photo = ImageTk.PhotoImage(payment_image)
        payment_label = tk.Label(payment,image=payment_photo)
        payment_label.photo =payment_photo
        payment_label.place(x=0, y=0)

        rate_button = tk.Button(payment, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
        rate_button.config(font=("Arial", 12,'bold'))
        rate_button.place(x=240, y=23)

        menu_button = tk.Button(payment, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
        menu_button.config(font=("Arial", 12,'bold'))
        menu_button.place(x=340, y=23)

        booking_button = tk.Button(payment, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
        booking_button.config(font=("Arial", 12,'bold'))
        booking_button.place(x=440, y=23)

        contact_button = tk.Button(payment, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
        contact_button.config(font=("Arial", 12,'bold'))
        contact_button.place(x=540, y=23)

        admin_button = tk.Button(payment, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
        admin_button.config(font=("Arial", 12,'bold'))
        admin_button.place(x=655, y=23)

        exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
        exit_photo = ImageTk.PhotoImage(exit_image)
        exit_label = tk.Label(payment,image=exit_photo)
        exit_label.photo = exit_photo
        exit_button = tk.Button(payment,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
        exit_button.place(x=740, y=20)

        back_image = Image.open(r"D:\Phyton\project\B-back.png")
        back_photo = ImageTk.PhotoImage(back_image)
        back_label = tk.Label(payment,image=back_photo)
        back_label.photo = back_photo
        back_button = tk.Button(payment, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=payment.destroy)
        back_button.place(x=9, y=556)
        
        home_image = Image.open(r"D:\Phyton\project\B-home.png")
        home_photo = ImageTk.PhotoImage(home_image)
        homes_label = tk.Label(payment,image=home_photo)
        homes_label.photo = home_photo
        home_button = tk.Button(payment, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=home)
        home_button.place(x=54, y=556)

        label_payment = tk.Label(payment,bg='#FDFDFC',fg='black', text="ป้อน USER ที่ต้องการชำระเงิน")
        label_payment.place(x=285,y=235)
        payment_entry = tk.Entry(payment,borderwidth=0, highlightthickness=0)
        payment_entry.place(x=291,y=265,width=220)

        button_pay = tk.Button(payment,bg='#FDFDFC',fg='black', text="ชำระเงิน", command=confirm)
        button_pay.place(x=380,y=310)

    def edit_customer_info () :
        edit = Toplevel(root) 
        edit.title("Edit Customer Info")
        edit.geometry("800x600+250+20")
        def home () :
            edit.destroy()
            menu.destroy()
        def find () :
            def home () :
                edit_wind.destroy()
                edit.destroy()
                menu.destroy()
            id_edit = entry_username.get()
            conn = sqlite3.connect(r'D:\Phyton\project\new.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customers WHERE username=?", (id_edit,))
            customer_info = cursor.fetchone()
            if not customer_info:
                messagebox.showerror("Error", f"ไม่พบusername {id_edit}")
            else:
                edit_wind =Toplevel(root)
                edit_wind.title("Edit Customer Info")
                edit_wind.geometry("800x600+250+20")
                def save () :
                    updated_name = name_entry.get()
                    updated_email = email_entry.get()
                    updated_phone = phone_entry.get()
                    updated_flight = flight_entry.get() 
                    updated_pdf = pdf_entry.get() 
                    updated_name = name_entry.get()  
                    updated_phone_number =billing_phone_entry.get()
                    updated_country = billing_country_entry.get() 
                    updated_address = billing_address_entry.get()  
                    updated_province = billing_city_entry.get() 
                    updated_zip = billing_zip_entry.get()
                    
                    conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                    cursor = conn.cursor()
                    try :
                        cursor.execute("UPDATE customers SET billing_name=?, email=?, phone_number=?, file_pdf=?, flight_number=?, phone_number=?, billing_country=?, billing_address=?, billing_city_province=?, billing_zip_code=? WHERE username=?",
                            (updated_name, updated_email, updated_phone, updated_pdf, updated_flight, updated_phone_number, updated_country, updated_address, updated_province, updated_zip, id_edit))
                        cursor.execute("UPDATE orders SET phone_num=? WHERE username=?", (updated_phone, id_edit))
                        cursor.execute("UPDATE car_order SET phone_num=? WHERE username=?", (updated_phone, id_edit))
                        conn.commit()
                        messagebox.showinfo("Success", "แก้ไขข้อมูลเรียบร้อยแล่ว!!.")
                        edit_wind.destroy()
                    except :
                        messagebox.showerror("Error", f"เกิดข้อผิดพลาด!!")

                editinfo_image = Image.open(r"D:\Phyton\project\BG-editinfo.png")
                editinfo_photo = ImageTk.PhotoImage(editinfo_image)
                editinfo_label = tk.Label(edit_wind,image=editinfo_photo)
                editinfo_label.photo =editinfo_photo
                editinfo_label.place(x=0, y=0) 

                rate_button = tk.Button(edit_wind, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
                rate_button.config(font=("Arial", 12,'bold'))
                rate_button.place(x=240, y=23)

                menu_button = tk.Button(edit_wind, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
                menu_button.config(font=("Arial", 12,'bold'))
                menu_button.place(x=340, y=23)

                booking_button = tk.Button(edit_wind, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
                booking_button.config(font=("Arial", 12,'bold'))
                booking_button.place(x=440, y=23)

                contact_button = tk.Button(edit_wind, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
                contact_button.config(font=("Arial", 12,'bold'))
                contact_button.place(x=540, y=23)

                admin_button = tk.Button(edit_wind, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
                admin_button.config(font=("Arial", 12,'bold'))
                admin_button.place(x=655, y=23)

                exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
                exit_photo = ImageTk.PhotoImage(exit_image)
                exit_label = tk.Label(edit_wind,image=exit_photo)
                exit_label.photo = exit_photo
                exit_button = tk.Button(edit_wind,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
                exit_button.place(x=740, y=20)

                username_label = tk.Label(edit_wind, text="Username :",bg='white',fg='black')
                username_label.config(font=("Arial", 7,'bold'))
                username_label.place(x=262,y=165)
                username_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                username_entry.insert(0, customer_info[1])  
                username_entry.place (x=320,y=165,width=95)

                car_type_label = tk.Label(edit_wind, text="ประเภทรถ :",bg='white',fg='black')
                car_type_label.config(font=("Arial", 7,'bold'))
                car_type_label.place(x=432,y=163)
                available_car_types = list(available_cars.keys())
                car_type_var = tk.StringVar(edit_wind)
                car_type_var.set(available_car_types[0])
                car_type_option_menu = tk.OptionMenu(edit_wind, car_type_var, *available_car_types)
                car_type_option_menu.place (x=485,y=157,width=95)

                rental_label = tk.Label(edit_wind, text="วันที่รับรถ :",bg='white',fg='black')
                rental_label.config(font=("Arial", 7,'bold'))
                rental_label.place(x=262,y=205)
                rental_date_entry = DateEntry(edit_wind, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy,mm,dd')
                rental_date_entry.place(x=321,y=202,width=95)

                rental_days__label = tk.Label(edit_wind, text="เช่าถึงวันที่ :",bg='white',fg='black')
                rental_days__label.config(font=("Arial", 7,'bold'))
                rental_days__label.place(x=432,y=205)
                rental_days_entry = DateEntry(edit_wind, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy,mm,dd')
                rental_days_entry.place (x=485,y=202,width=93)

                cc_label = tk.Label(edit_wind, text="ข้อมูลผู้ขับขี่ (ชื่อผู้ขับขี่ต้องเป็นชื่อเดียวกับผู้ที่มารับรถ)",bg='white',fg='black')
                cc_label.config(font=("Arial", 9,'bold'))
                cc_label.place(x=277,y=230)
                
                name_label = tk.Label(edit_wind, text="ชื่อ - สกุล :",bg='white',fg='black')
                name_label.place(x=262,y=260)
                name_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                name_entry.insert(0, customer_info[2])  
                name_entry.place (x=315,y=262,width=285)

                email_label = tk.Label(edit_wind,bg='white',fg='black', text="E-mail:")
                email_label.config(font=("Arial", 7,'bold'))
                email_label.place(x=264,y=300)
                email_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                email_entry.insert(0, customer_info[3]) 
                email_entry.place(x=305,y=300,width=272)

                phone_label = tk.Label(edit_wind,bg='white',fg='black' ,text="เบอร์โทรศัพท์ :")
                phone_label.config(font=("Arial", 7,'bold'))
                phone_label.place(x=263,y=340)
                phone_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                phone_entry.insert(0, customer_info[4])  
                phone_entry.place(x=335,y=340,width=227)
                
                pdf_label = tk.Label(edit_wind,bg='white',fg='black', text="PDF File:")
                pdf_label.config(font=("Arial", 7,'bold'))
                pdf_label.place(x=305,y=519)
                pdf_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0, width=40)
                pdf_entry.insert(0, customer_info[5]) 
                pdf_entry.place(x=359,y=519,width=80)
                pdf_button = tk.Button(edit_wind, text="Browse", command=lambda: browse_pdf(pdf_entry))
                pdf_button.place(x=593,y=515,width=60)
                def browse_pdf(pdf_entry):
                    previous_file_path = pdf_entry.get()
                    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
                    if file_path:
                        if os.path.exists(previous_file_path):
                            os.remove(previous_file_path)
                        pdf_entry.delete(0, tk.END)
                        pdf_entry.insert(0, file_path)
            
                flight_label = tk.Label(edit_wind,bg='white',fg='black', text="หมายเลขเที่ยวบิน (ถ้ามี) :")
                flight_label.config(font=("Arial", 7,'bold'))
                flight_label.place(x=430,y=468)
                flight_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                flight_entry.insert(0, customer_info[6]) 
                flight_entry.place(x=535,y=468,width=60)

                billing_phone_label = tk.Label(edit_wind,bg='white',fg='black', text="เบอร์โทรศัพท์ :")
                billing_phone_label.config(font=("Arial", 7,'bold'))
                billing_phone_label.place(x=263,y=468)
                billing_phone_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                billing_phone_entry.insert(0, customer_info[7]) 
                billing_phone_entry.place(x=322,y=468,width=75)

                billing_country_label = tk.Label(edit_wind,bg='white',fg='black', text="ประเทศ:")
                billing_country_label.config(font=("Arial", 7,'bold'))
                billing_country_label.place(x=432,y=421,)
                billing_country_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                billing_country_entry.insert(0, customer_info[8]) 
                billing_country_entry.place(x=470,y=420,width=100)

                billing_address_label = tk.Label(edit_wind,bg='white',fg='black', text="บ้านเลขที่:")
                billing_address_label.config(font=("Arial", 7,'bold'))
                billing_address_label.place(x=265,y=380)
                billing_address_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                billing_address_entry.insert(0, customer_info[9]) 
                billing_address_entry.place(x=310,y=380,width=103)

                billing_city_label = tk.Label(edit_wind,bg='white',fg='black', text="เมือง/จังหวัด:")
                billing_city_label.config(font=("Arial", 7,'bold'))
                billing_city_label.place(x=435,y=379)
                billing_city_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                billing_city_entry .insert(0, customer_info[10]) 
                billing_city_entry.place(x=487,y=379,width=107)
                
                billing_zip_label = tk.Label(edit_wind,bg='white',fg='black', text="รหัสไปรษณีย์ :")
                billing_zip_label.config(font=("Arial", 7,'bold'))
                billing_zip_label.place(x=263,y=421,)
                billing_zip_entry = tk.Entry(edit_wind,borderwidth=0, highlightthickness=0)
                billing_zip_entry.insert(0, customer_info[11]) 
                billing_zip_entry.place(x=325,y=421,width=85)


                save_button = tk.Button(edit_wind,bg='#4D4D4F',fg='black',borderwidth=0, highlightthickness=0, text="บันทึก", command=save)
                save_button.place(x=403,y=572)

                back_image = Image.open(r"D:\Phyton\project\B-back.png")
                back_photo = ImageTk.PhotoImage(back_image)
                back_label = tk.Label(edit_wind,image=back_photo)
                back_label.photo = back_photo
                back_button = tk.Button(edit_wind, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=edit_wind.destroy)
                back_button.place(x=9, y=556)
                
                home_image = Image.open(r"D:\Phyton\project\B-home.png")
                home_photo = ImageTk.PhotoImage(home_image)
                homes_label = tk.Label(edit_wind,image=home_photo)
                homes_label.photo = home_photo
                home_button = tk.Button(edit_wind, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=home)
                home_button.place(x=54, y=556)


            edit.destroy()
            conn.commit()
            conn.close()

        edit_image = Image.open(r"D:\Phyton\project\BG-edit.png")
        edit_photo = ImageTk.PhotoImage(edit_image)
        edit_label = tk.Label(edit,image=edit_photo)
        edit_label.photo =edit_photo
        edit_label.place(x=0, y=0)

        rate_button = tk.Button(edit, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
        rate_button.config(font=("Arial", 12,'bold'))
        rate_button.place(x=240, y=23)

        menu_button = tk.Button(edit, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
        menu_button.config(font=("Arial", 12,'bold'))
        menu_button.place(x=340, y=23)

        booking_button = tk.Button(edit, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
        booking_button.config(font=("Arial", 12,'bold'))
        booking_button.place(x=440, y=23)

        contact_button = tk.Button(edit, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
        contact_button.config(font=("Arial", 12,'bold'))
        contact_button.place(x=540, y=23)

        admin_button = tk.Button(edit, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
        admin_button.config(font=("Arial", 12,'bold'))
        admin_button.place(x=655, y=23)

        exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
        exit_photo = ImageTk.PhotoImage(exit_image)
        exit_label = tk.Label(edit,image=exit_photo)
        exit_label.photo = exit_photo
        exit_button = tk.Button(edit,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
        exit_button.place(x=740, y=20)

        back_image = Image.open(r"D:\Phyton\project\B-back.png")
        back_photo = ImageTk.PhotoImage(back_image)
        back_label = tk.Label(edit,image=back_photo)
        back_label.photo = back_photo
        back_button = tk.Button(edit, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=edit.destroy)
        back_button.place(x=9, y=556)
        
        home_image = Image.open(r"D:\Phyton\project\B-home.png")
        home_photo = ImageTk.PhotoImage(home_image)
        homes_label = tk.Label(edit,image=home_photo)
        homes_label.photo = home_photo
        home_button = tk.Button(edit, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=home)
        home_button.place(x=54, y=556)

        username_label = tk.Label(edit,bg='#FDFDFC',fg='black', text="ป้อนUSERของลูกค้าที่ต้องการแก้ไข")
        username_label.place(x=285,y=235)
        entry_username = tk.Entry(edit,borderwidth=0, highlightthickness=0)
        entry_username.place(x=291,y=265,width=220)

        search_button = tk.Button(edit,bg='#FDFDFC',fg='black', text="แก้ไข", command=find)
        search_button.place(x=380,y=310)

    
    def return_car_info():
        return_window = Toplevel(root)
        return_window.title("Return Car")
        return_window.geometry("800x600+250+20")

        def home () :
            return_window.destroy()
            menu.destroy()
        def calculate_late_fee(return_date,rental_days):
            late_fee_per_day = 5000
            penalty_days = (return_date - rental_days).days
            penalty_days = max(penalty_days, 0) #0เพื่อไม่ให้ค่าติดลบ
            penalty_amount = penalty_days * late_fee_per_day
            return penalty_amount
        
        
        def return_car():
            id_edit = entry_user.get() 
            conn = sqlite3.connect
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM car_order WHERE username=?", (id_edit,))
            rental_info = cursor.fetchone()

            if rental_info:
                customer_id = id_edit
                car_type = rental_info[3]
                rental_days_str = rental_info[4]
                rental_days = datetime.strptime(rental_days_str, '%Y-%m-%d').date()
                rental_date = rental_info[5]
                return_date = return_date_entry.get_date()
                damage = int(rental_info[10])

                late_fee = calculate_late_fee(return_date, rental_days)
                total_penalty = late_fee + damage
                total =total_penalty - 5000
                return_summary = (
                    f"Rental Information:\n"
                    f"USER: {customer_id}\n"
                    f"Car Type: {available_cars[car_type]['name']} ({available_cars[car_type]['type']})\n"
                    f"เริ่มเช่าวันที่: {rental_date} days\n"
                    f"เช่าถึงวันที่: {rental_days}\n"
                    f"วันที่คืนรถ: {return_date}\n"
                    f"ค่าปรับ: {late_fee:.2f} THB\n"
                    f"รวมเป็นเงิน: {total:.2f} THB"
                )
                def send_email():
                    cursor.execute("SELECT * FROM customers WHERE username=?", (id_edit,))
                    rental_info = cursor.fetchone()
                    email = rental_info[3]
                    try:
                        email_sender = "minesunshy3@gmail.com"
                        app_password = "rimb qhyl xtdd cylu" 
                        recipients = [email]
                        text=f"ขอบคุณที่ใช้บริการ เจ๊นุ้ยทรงเชง \n{return_summary}",
                        yag = yagmail.SMTP(email_sender, app_password)
                        yag.send(
                            to=recipients,
                            subject="เจ๊นุ้ยทรงเชง",
                            contents=text,
                        )
                        messagebox.showinfo("Success", "Email sent successfully!")
                        yag.close()
                    except YagConnectionClosed:
                        messagebox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")
                send_email()
                messagebox.showinfo("Summary", return_summary)
                cursor.execute("UPDATE car_order SET return_status='Returned', late_fee=? WHERE username=?", (late_fee, customer_id))
                conn.commit()
            else:
                messagebox.showerror("Error", f"No rental information found for customer ID {id_edit}")
            conn.close()
            return_window.destroy()

        edit_image = Image.open(r"D:\Phyton\project\BG-return.png")
        edit_photo = ImageTk.PhotoImage(edit_image)
        edit_label = tk.Label(return_window,image=edit_photo)
        edit_label.photo =edit_photo
        edit_label.place(x=0, y=0)

        rate_button = tk.Button(return_window, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
        rate_button.config(font=("Arial", 12,'bold'))
        rate_button.place(x=240, y=23)

        menu_button = tk.Button(return_window, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
        menu_button.config(font=("Arial", 12,'bold'))
        menu_button.place(x=340, y=23)

        booking_button = tk.Button(return_window, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
        booking_button.config(font=("Arial", 12,'bold'))
        booking_button.place(x=440, y=23)

        contact_button = tk.Button(return_window, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
        contact_button.config(font=("Arial", 12,'bold'))
        contact_button.place(x=540, y=23)

        admin_button = tk.Button(return_window, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
        admin_button.config(font=("Arial", 12,'bold'))
        admin_button.place(x=655, y=23)

        exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
        exit_photo = ImageTk.PhotoImage(exit_image)
        exit_label = tk.Label(return_window,image=exit_photo)
        exit_label.photo = exit_photo
        exit_button = tk.Button(return_window,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
        exit_button.place(x=740, y=20)

        back_image = Image.open(r"D:\Phyton\project\B-back.png")
        back_photo = ImageTk.PhotoImage(back_image)
        back_label = tk.Label(return_window,image=back_photo)
        back_label.photo = back_photo
        back_button = tk.Button(return_window, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=return_window.destroy)
        back_button.place(x=9, y=556)
        
        home_image = Image.open(r"D:\Phyton\project\B-home.png")
        home_photo = ImageTk.PhotoImage(home_image)
        homes_label = tk.Label(return_window,image=home_photo)
        homes_label.photo = home_photo
        home_button = tk.Button(return_window, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=home)
        home_button.place(x=54, y=556)

        username_label = tk.Label(return_window,bg='#FDFDFC',fg='black', text="ป้อนUSERของลูกค้า")
        username_label.place(x=285,y=235)
        entry_user= tk.Entry(return_window,borderwidth=0, highlightthickness=0)
        entry_user.place(x=291,y=265,width=220)

        button_return = tk.Button(return_window,bg='#FDFDFC',fg='black', text="คืนรถ", command=return_car)
        button_return.place(x=390,y=350)

        label_return_date = tk.Label(return_window,bg='#FDFDFC',fg='black', text="วันที่คืนรถ (yyyy-mm-dd):")
        label_return_date.place(x=285,y=290)
        return_date_entry = DateEntry(return_window, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy,mm,dd')
        return_date_entry.place(x=291,y=310,width=220)
        


    
    rate_button = tk.Button(menu, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
    rate_button.config(font=("Arial", 12,'bold'))
    rate_button.place(x=240, y=23)

    menu_button = tk.Button(menu, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
    menu_button.config(font=("Arial", 12,'bold'))
    menu_button.place(x=340, y=23)

    booking_button = tk.Button(menu, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
    booking_button.config(font=("Arial", 12,'bold'))
    booking_button.place(x=440, y=23)

    contact_button = tk.Button(menu, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
    contact_button.config(font=("Arial", 12,'bold'))
    contact_button.place(x=540, y=23)

    admin_button = tk.Button(menu, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
    admin_button.config(font=("Arial", 12,'bold'))
    admin_button.place(x=655, y=23)

    exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
    exit_photo = ImageTk.PhotoImage(exit_image)
    exit_label = tk.Label(menu,image=exit_photo)
    exit_label.photo = exit_photo
    exit_button = tk.Button(menu,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
    exit_button.place(x=740, y=20)

    back_image = Image.open(r"D:\Phyton\project\B-back.png")
    back_photo = ImageTk.PhotoImage(back_image)
    back_label = tk.Label(menu,image=back_photo)
    back_label.photo = back_photo
    back_button = tk.Button(menu, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=menu.destroy)
    back_button.place(x=9, y=556)
    
    home_image = Image.open(r"D:\Phyton\project\B-home.png")
    home_photo = ImageTk.PhotoImage(home_image)
    homes_label = tk.Label(menu,image=home_photo)
    homes_label.photo = home_photo
    home_button = tk.Button(menu, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=menu.destroy)
    home_button.place(x=54, y=556)

    aa_label = tk.Label(menu, text="MENU",bg='white',fg='black')
    aa_label.config(font=("Arial",15,'bold'))
    aa_label.place(x=380,y=197)

    cancel_order_button = tk.Button(menu,borderwidth=0, highlightthickness=0,width=25, bg='#FDFDFC', text="ยกเลิกคำสั่งซื้อ", command=cancel_order)
    cancel_order_button.place(x=310,y=278)

    payment_button = tk.Button(menu,borderwidth=0, highlightthickness=0,width=25, bg='#FDFDFC',text="ชำระเงิน", command= payment)
    payment_button.place(x=310,y=323)

    edit_customer_info_button = tk.Button(menu,borderwidth=0, highlightthickness=0,width=25, bg='#FDFDFC', text="แก้ไขข้อมูลลูกค้า", command=edit_customer_info)
    edit_customer_info_button.place(x=310,y=373)

    return_car_button = tk.Button(menu,borderwidth=0, highlightthickness=0,width=25, bg='#FDFDFC', text="คืนรถ", command=return_car_info)
    return_car_button.place(x=310,y=420)
      



def admin_menu () :
    ad = Toplevel(root)
    ad.title("Admin Login")
    ad.geometry("300x200+500+200")
    def login_admin():
        admin_password = 'admin'
        entered_password = entry_password.get()
        if entered_password == admin_password:
            admin()
            ad.destroy()
        else:
            messagebox.showinfo("ERROR", "รหัสผ่าน admin ไม่ถูกต้อง!!")
            return False
    edit_image = Image.open(r"D:\Phyton\project\BG-login.png")
    edit_photo = ImageTk.PhotoImage(edit_image)
    edit_label = tk.Label(ad,image=edit_photo)
    edit_label.photo =edit_photo
    edit_label.place(x=0, y=0)
    
    # label_password = tk.Label(ad, text="ป้อนรหัสผ่าน admin:")
    # label_password.pack(pady=10)
    entry_password = tk.Entry(ad,borderwidth=0, highlightthickness=0, show='*')
    entry_password.place (x=83,y=108,width=140)
    botton_login = tk.Button(ad,bg='#ffffff',fg='black', text="Login", command=login_admin)
    botton_login.place (x=130,y=147)

    label_message = tk.Label(ad, text="", fg="red")
    label_message.pack()

    label_info = tk.Label(ad, text="", justify="left")
    label_info.pack()
    
    def admin ():
        menu = Toplevel(root)
        menu.title("เมนูผู้ดูแลระบบ")
        menu.geometry("800x600+250+20")
        

        def view_customer_list():
            conn = sqlite3.connect(r'D:\Phyton\project\new.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            customer_data = cursor.fetchall()
            if customer_data:
                text = "ข้อมูลลูกค้า:\n\n"
                for customer in customer_data:
                    text += f"ID: {customer[0]}\n"
                    text += f"ชื่อ: {customer[1]}\n"
                    text += f"E-mail: {customer[2]}\n"
                    text += f"เบอร์โทรศัพท์: {customer[3]}\n"
                    text += f"หมายเลขเที่ยวบิน: {customer[4]}\n"
                    text += f"ที่อยู่สำหรับออกใบเสร็จ: {customer[5]}\n"
                    text += f"เมือง/จังหวัด: {customer[6]}\n"
                    text += f"รหัสไปรษณีย์: {customer[7]}\n\n"
                messagebox.showinfo("ข้อมูลลูกค้า", text)
            else:
                messagebox.showinfo("ERROR","ไม่พบข้อมูลลูกค้า")

            conn.close()

        def view_rented_cars():
            conn = sqlite3.connect(r'D:\Phyton\project\new.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM car_order")
            rented_cars = cursor.fetchall()

            if rented_cars:
                text = "ข้อมูลการจองรถ:\n\n"
                for car in rented_cars:
                    text += f"ID: {car[0]}\n"
                    text += f"userลูกค้า: {car[1]}\n"
                    text += f"ประเภทรถ: {car[2]}\n"
                    text += f"จำนวนวันเช่า: {car[3]}\n"
                    text += f"วันที่รับรถ: {car[4]}\n"
                    text += f"อายุคนขับ: {car[5]}\n\n"

                info_window = Toplevel(root)
                info_window.title("ข้อมูลการจองรถ")
                info_window.geometry("800x600+250+20")
                info_label = tk.Label(info_window, text=text, justify="left")
                info_label.pack(padx=10, pady=10)
            else:
                messagebox.showinfo("Error", "ไม่พบข้อมูลการจองรถ")

            conn.close()

        def change_admin_password():
            changes = Toplevel(root)
            changes.title("เมนูผู้ดูแลระบบ")
            changes.geometry("800x600+250+20")
            label_new_password = tk.Label(changes, text="รหัสผ่านใหม่สำหรับผู้ดูแลระบบ:")
            label_new_password.pack(pady=10)

            entry_new_password = tk.Entry(changes)
            entry_new_password.pack(pady=10)

            button_change_password = tk.Button(changes, text="เปลี่ยนรหัสผ่าน", command=change)
            button_change_password.pack(pady=10)
            def change () :
                global admin_password
                new_password =entry_new_password.get()
                admin_password = new_password
                messagebox.showinfo("success","รหัสผ่านถูกเปลี่ยนเป็น {new_password}")
                admin_menu()

        def delete () :
            delete = Toplevel()
            delete.title("Delete Customer Information")
            delete.geometry("800x600+250+20")
            delete_image = Image.open(r"D:\Phyton\project\BG-deleteinfo.png")
            delete_photo = ImageTk.PhotoImage(delete_image)
            delete_label = tk.Label(delete,image=delete_photo)
            delete_label.photo =delete_photo
            delete_label.place(x=0, y=0) 
            
            def delete_customer_info():
                customer_id_to_delete = entry_customer_id.get()
                conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                cursor = conn.cursor()

                cursor.execute("SELECT username FROM customers WHERE username=?", (customer_id_to_delete,))
                customer = cursor.fetchone()

                if not customer:
                    messagebox.showerror("Error", f"ไม่พบข้อมูลลูกค้าชื่อ {customer_id_to_delete}")
                else:
                    cursor.execute("DELETE FROM orders WHERE username=?", (customer_id_to_delete,))
                    conn.commit()
                    messagebox.showinfo("Success", f"ลบข้อมูลลูกค้า {customer_id_to_delete} และข้อมูลที่เกี่ยวข้องเรียบร้อยแล้ว")

                conn.close()

            exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
            exit_photo = ImageTk.PhotoImage(exit_image)
            exit_label = tk.Label(delete,image=exit_photo)
            exit_label.photo = exit_photo
            exit_button = tk.Button(delete,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
            exit_button.place(x=740, y=20)

            back_image = Image.open(r"D:\Phyton\project\B-back.png")
            back_photo = ImageTk.PhotoImage(back_image)
            back_label = tk.Label(delete,image=back_photo)
            back_label.photo = back_photo
            back_button = tk.Button(delete, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=delete.destroy)
            back_button.place(x=25, y=556)
            
            home_image = Image.open(r"D:\Phyton\project\B-home.png")
            home_photo = ImageTk.PhotoImage(home_image)
            homes_label = tk.Label(delete,image=home_photo)
            homes_label.photo = home_photo
            home_button = tk.Button(delete, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=delete.destroy)
            home_button.place(x=62, y=556)

            label_customer_id = tk.Label(delete,bg='#FDFDFC',fg='black', text="ป้อนusernameลูกค้า")
            label_customer_id.place(x=285,y=235)
            entry_customer_id=tk.Entry(delete,borderwidth=0, highlightthickness=0)
            entry_customer_id.place(x=291,y=265,width=220)
            delete_button=tk.Button(delete, text="ลบข้อมูล",bg='#000000',fg='white',width =5, command=delete_customer_info)
            delete_button.place(x=380,y=310)

        def damages () :
            damages = Toplevel()
            damages.geometry("800x600+250+20")
            conn = sqlite3.connect(r'D:\Phyton\project\new.db')
            edit_image = Image.open(r"D:\Phyton\project\BG-d.png")
            edit_photo = ImageTk.PhotoImage(edit_image)
            edit_label = tk.Label(damages,image=edit_photo)
            edit_label.photo =edit_photo
            edit_label.place(x=0, y=0)
            # ค้นหาข้อมูลลูกค้าโดยใช้ชื่อของลูกค้าเป็นเงื่อนไข
            def calculate_damages():
                customer_id = customer_id_entry.get()
                if entry_fuel and entry_scratches:
                    try:
                        fuel_shortage_liters= int(entry_scratches.get())
                        scratches_count = int(entry_scratches.get())
                        # ทำสิ่งที่ต้องการกับ fuel_amount และ scratches_count
                    except ValueError:
                        messagebox.showerror("Error", "โปรดป้อนจำนวนเต็มเท่านั้น")
                        return False
                else:
                    messagebox.showerror("Error", "โปรดป้อนข้อมูล")
                    return False
                acident = messagebox.askyesno("Accident", "Did the car have an accident?")
                if acident:
                    messagebox.showinfo("Contact Insurance", "Contact insurance at 098765432")

                    # Update the database with the damages information
                    conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE car_order SET damages='เกิดอุบัติเหตุ' WHERE username=?", (customer_id,))
                else :
                    

                    # Calculate penalties
                    fuel_penalty_per_liter = 1500
                    fuel_penalty = fuel_shortage_liters * fuel_penalty_per_liter
                    scratches_number = 500
                    scratches_penalty = scratches_count * scratches_number
                    total_penalty = scratches_penalty + fuel_penalty

                    # Update the database
                    conn = sqlite3.connect(r'D:\Phyton\project\new.db')
                    cursor = conn.cursor()

                    # Update the damages for the specific customer
                    cursor.execute("UPDATE car_order SET damages=? WHERE username=?", (total_penalty, customer_id))
                    messagebox.showinfo("Success", f"Fuel Penalty: {fuel_penalty}\nScratches Penalty: {scratches_penalty}\nTotal Damages: {total_penalty}")

                conn.commit()
                conn.close()
            back_image = Image.open(r"D:\Phyton\project\B-back.png")
            back_photo = ImageTk.PhotoImage(back_image)
            back_label = tk.Label(damages,image=back_photo)
            back_label.photo = back_photo
            back_button = tk.Button(damages, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=damages.destroy)
            back_button.place(x=25, y=556)
            
            home_image = Image.open(r"D:\Phyton\project\B-home.png")
            home_photo = ImageTk.PhotoImage(home_image)
            homes_label = tk.Label(damages,image=home_photo)
            homes_label.photo = home_photo
            home_button = tk.Button(damages, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=damages.destroy)
            home_button.place(x=62, y=556)

            label_customer_id = tk.Label(damages,bg='#FDFDFC',fg='black', text="Enter customer ID:")
            label_customer_id.place(x=285,y=235)

            customer_id_entry = tk.Entry(damages,borderwidth=0, highlightthickness=0)
            customer_id_entry.place(x=291,y=265,width=220)

            fuel_label = tk.Label(damages,bg='#FDFDFC',fg='black', text="จำนวนน้ำมัน")
            fuel_label.place(x=287,y=300)
            entry_fuel= tk.Entry(damages,borderwidth=0, highlightthickness=0)
            entry_fuel.place(x=291,y=325,width=220)

            scratches_label = tk.Label(damages,bg='#FDFDFC',fg='black', text="จำนวนรอยขีดข่วน")
            scratches_label.place(x=287,y=365)
            entry_scratches= tk.Entry(damages,borderwidth=0, highlightthickness=0)
            entry_scratches.place(x=291,y=395,width=220)
            # Button to calculate damages
            calculate_button = tk.Button(damages, text="Calculate Damages", command=calculate_damages)
            calculate_button.place(x=291,y=425,width=220)

        admin_image = Image.open(r"D:\Phyton\project\B.png")
        admin_photo = ImageTk.PhotoImage(admin_image)
        admin_label = tk.Label(menu,image=admin_photo)
        admin_label.photo =admin_photo
        admin_label.place(x=0, y=0)

        exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
        exit_photo = ImageTk.PhotoImage(exit_image)
        exit_label = tk.Label(menu,image=exit_photo)
        exit_label.photo = exit_photo
        exit_button = tk.Button(menu,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
        exit_button.place(x=740, y=20)


        botton_view_rented_cars = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="ข้อมูลการเช่ารถ", command=view_rented_cars)
        botton_view_customer_list = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="ข้อมูลลูกค้า", command=view_customer_list)
        botton_change_password = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="เปลี่ยนรหัสผ่าน", command=change_admin_password)
        botton_delete = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="ลบข้อมูลลูกค้า", command=delete)
        botton_damages = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="ค่าปรับ", command=damages)
        botton_exit = tk.Button(menu,borderwidth=0, highlightthickness=0,bg='#ffffff',fg='black', text="ออก", command=menu.destroy)

        botton_view_rented_cars.place(x=380,y=210,width=95)
        botton_view_customer_list.place(x=380,y=255,width=95)
        botton_change_password.place(x=380,y=303,width=95)
        botton_delete.place(x=380,y=351,width=95)
        botton_damages.place(x=380,y=399,width=95)
        botton_exit.place(x=380,y=446,width=95)

def exit_application():
    root.destroy()
def show_car () :
    show = Toplevel(root)
    show.title(f"จ่ายตัง")
    show.geometry("800x600+250+20") 
    show_image = Image.open(r"D:\Phyton\project\BG-show.png")
    show_photo = ImageTk.PhotoImage(show_image)
    show_label = tk.Label(show,image=show_photo)
    show_label.photo = show_photo
    show_label.place(x=0, y=0) 

    rate_button = tk.Button(show, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
    rate_button.config(font=("Arial", 12,'bold'))
    rate_button.place(x=240, y=23)

    menu_button = tk.Button(show, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
    menu_button.config(font=("Arial", 12,'bold'))
    menu_button.place(x=340, y=23)

    booking_button = tk.Button(show, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
    booking_button.config(font=("Arial", 12,'bold'))
    booking_button.place(x=440, y=23)

    contact_button = tk.Button(show, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=admin_menu,borderwidth=0, highlightthickness=0)
    contact_button.config(font=("Arial", 12,'bold'))
    contact_button.place(x=540, y=23)

    admin_button = tk.Button(show, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
    admin_button.config(font=("Arial", 12,'bold'))
    admin_button.place(x=655, y=23)

    exit_image = Image.open(r"D:\Phyton\project\B-exit.png")
    exit_photo = ImageTk.PhotoImage(exit_image)
    exit_label = tk.Label(show,image=exit_photo)
    exit_label.photo = exit_photo
    exit_button = tk.Button(show,image=exit_photo,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
    exit_button.place(x=740, y=20)

    dmax_image = Image.open(r"D:\Phyton\project\dmax.png")
    dmax_photo = ImageTk.PhotoImage(dmax_image)
    dmax_label = tk.Label(show,image=dmax_photo)
    dmax_label.photo =dmax_photo
    dmax_button = tk.Button(show,image=dmax_photo,width=400, height=102,borderwidth=0, highlightthickness=0, command=rent_car)
    dmax_button.place(x=0, y=300)

    hrv_image = Image.open(r"D:\Phyton\project\hrv.png")
    hrv_photo = ImageTk.PhotoImage(hrv_image)
    hrv_label = tk.Label(show,image=hrv_photo)
    hrv_label.photo =hrv_photo
    hrv_button = tk.Button(show,image=hrv_photo,width=400, height=102,borderwidth=0, highlightthickness=0, command=rent_car)
    hrv_button.place(x=400, y=300)

    alp_image = Image.open(r"D:\Phyton\project\alp.png")
    alp_photo = ImageTk.PhotoImage(alp_image)
    alp_label = tk.Label(show,image=alp_photo)
    alp_label.photo =alp_photo
    alp_button = tk.Button(show,image=alp_photo,width=400, height=102,borderwidth=0, highlightthickness=0, command=rent_car)
    alp_button.place(x=0, y=402)

    Benz_image = Image.open(r"D:\Phyton\project\Benz.png")
    Benz_photo = ImageTk.PhotoImage(Benz_image)
    Benz_label = tk.Label(show,image=Benz_photo)
    Benz_label.photo = Benz_photo
    Benz_button = tk.Button(show, image=Benz_photo, width=400, height=102, borderwidth=0, highlightthickness=0, command=rent_car)
    Benz_button.place(x=400, y=402)

    Benz_image = Image.open(r"D:\Phyton\project\Benz.png")
    Benz_photo = ImageTk.PhotoImage(Benz_image)
    Benz_label = tk.Label(show,image=Benz_photo)
    Benz_label.photo = Benz_photo
    Benz_button = tk.Button(show, image=Benz_photo, width=400, height=102, borderwidth=0, highlightthickness=0, command=rent_car)
    Benz_button.place(x=400, y=402)

    back_image = Image.open(r"D:\Phyton\project\B-back.png")
    back_photo = ImageTk.PhotoImage(back_image)
    back_label = tk.Label(show,image=back_photo)
    back_label.photo = back_photo
    back_button = tk.Button(show, image=back_photo,width=37, height=33,borderwidth=0, highlightthickness=0, command=show.destroy)
    back_button.place(x=9, y=535)
    
    home_image = Image.open(r"D:\Phyton\project\B-home.png")
    home_photo = ImageTk.PhotoImage(home_image)
    homes_label = tk.Label(show,image=home_photo)
    homes_label.photo = home_photo
    home_button = tk.Button(show, image=home_photo,width=37, height=33,borderwidth=0, highlightthickness=0, command=show.destroy)
    home_button.place(x=54, y=535)

def contact () :
    contact = Toplevel(root)
    contact.title("contact")
    contact.geometry("800x600+250+20")

    contact_image = Image.open(r"D:\Phyton\project\contact.png")
    contact_photo = ImageTk.PhotoImage(contact_image)
    contact_label = tk.Label(contact,image=contact_photo)
    contact_label.photo =contact_photo
    contact_label.place(x=0, y=0) 

    back_image = Image.open(r"D:\Phyton\project\B-back.png")
    back_photo = ImageTk.PhotoImage(back_image)
    back_label = tk.Label(contact,image=back_photo)
    back_label.photo = back_photo
    back_button = tk.Button(contact, image=back_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=contact.destroy)
    back_button.place(x=25, y=556)
    
    home_image = Image.open(r"D:\Phyton\project\B-home.png")
    home_photo = ImageTk.PhotoImage(home_image)
    homes_label = tk.Label(contact,image=home_photo)
    homes_label.photo = home_photo
    home_button = tk.Button(contact, image=home_photo,width=37, height=30,borderwidth=0, highlightthickness=0, command=contact.destroy)
    home_button.place(x=70, y=556)


root = tk.Tk()
root.title("เจ้นุยทรงเชง")
root.geometry("800x600+250+20")


home_image = tk.PhotoImage(file=r"D:\Phyton\project\BG-home.png")
home_label = tk.Label(root, image=home_image)
home_label.place(x=0, y=0) 

button_width = 7
button_height = 2


rate_button = tk.Button(root, text='Rates', bg='#ffffff',fg='black', font=45,width = button_width,command=show_car,borderwidth=0, highlightthickness=0)
rate_button.config(font=("Arial", 12,'bold'))
rate_button.place(x=240, y=23)

menu_button = tk.Button(root, text='Menu', bg='#ffffff',fg='black', font=45,width = button_width,command=menu,borderwidth=0, highlightthickness=0)
menu_button.config(font=("Arial", 12,'bold'))
menu_button.place(x=340, y=23)

booking_button = tk.Button(root, text='Booking', bg='#FF3131',fg='white',width = button_width, font=45,command=rent_car,borderwidth=0, highlightthickness=0)
booking_button.config(font=("Arial", 12,'bold'))
booking_button.place(x=440, y=23)

contact_button = tk.Button(root, text='Contact US', bg='#ffffff',fg='black', font=45,width = 9,command=contact,borderwidth=0, highlightthickness=0)
contact_button.config(font=("Arial", 12,'bold'))
contact_button.place(x=540, y=23)

admin_button = tk.Button(root, text='ADMIN', bg='#ffffff',fg='black', font=45,width = button_width,command=admin_menu,borderwidth=0, highlightthickness=0)
admin_button.config(font=("Arial", 12,'bold'))
admin_button.place(x=655, y=23)

exit = tk.PhotoImage(file=r"D:\Phyton\project\B-exit.png")
exit_button = tk.Button(root,image=exit,width=50, height=35,borderwidth=0, highlightthickness=0, command=lambda:exit_application())
exit_button.place(x=740, y=20)

root.mainloop()

conn.commit()
conn.close()

