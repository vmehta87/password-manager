from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for char in range(randint(8, 10))]
    symbol_list = [choice(symbols) for char in range(randint(2, 4))]
    number_list = [choice(numbers) for char in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list
    shuffle(password_list)

    pass_input.delete(0, END)
    pass_input.insert(0, ''.join(password_list))
    pyperclip.copy(''.join(password_list))
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = web_input.get()
    email = email_input.get()
    password = pass_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) > 1 and len(password) > 1:
        is_ok = messagebox.askokcancel(title=website, message=f"confirm entry:\nEmail:{email}\n Password:{password}")
        if is_ok:
            try:
                with open('data.json', 'r') as data_file:

                    data = json.load(data_file)
            except FileNotFoundError:
                with open('data.json', 'w'):
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open('data.json', 'w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                web_input.delete(0, END)
                pass_input.delete(0, END)
        else:
            web_input.delete(0, END)
            pass_input.delete(0, END)
    else:
        messagebox.showinfo(title="Oh shit...", message="Don't leave anything empty!!")
# ---------------------------- FIND PASSWORD ------------------------------- #


def search_password():
    website = web_input.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(text='Error', message='No data file found..')
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email:{email}\nPassword:{password}')
        else:
            messagebox.showinfo(title=website, message=f'{website} not found. Set a password and add it!')


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_pic = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_pic)
canvas.grid(column=1, row=0)

website = Label(text='Website:')
website.grid(column=0, row=1)

web_input = Entry(width=20)
web_input.grid(column=1, row=1, sticky="EW")
web_input.focus()

search = Button(text='Search', width=5, command=search_password)
search.grid(column=2, row=1, sticky="EW")

email = Label(text='Email/Username')
email.grid(column=0, row=2)

email_input = Entry(width=35)
email_input.grid(column=1, columnspan=2, row=2, sticky="EW")
email_input.insert(0, '87vmehta@gmail.com')

password = Label(text='Password:')
password.grid(column=0, row=3)

pass_input = Entry(width=25)
pass_input.grid(column=1, row=3, sticky="EW")

gen_pass = Button(text='Generate Password', command=gen_pass)
gen_pass.grid(column=2, row=3, sticky="EW")

add = Button(text='Add', width=36, command=save_data)
add.grid(column=1, columnspan=2, row=4, sticky="EW")

window.mainloop()
