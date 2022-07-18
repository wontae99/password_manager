from tkinter import *
from tkinter import messagebox
import pyperclip
import json

FONT = ('', 10, 'normal')
# ----------------------- PASSWORD GENERATOR -------------------------- #
from random import choice, shuffle, randint
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def make_password():

    password_list = [choice(letters) for _ in range(randint(6, 8))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password_gen = ''.join(password_list)

    if password_input.get() != '':
        password_input.delete(0, END)
    password_input.insert(0, password_gen)
    pyperclip.copy(password_input.get())

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_username_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title='Warning', message="Empty field has been found.")
    else:
        try:
            with open("my_password.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("my_password.json", 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("my_password.json", 'w') as file:
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0, END)
            email_username_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- FIND PASSWORD ----------------------------- #
def search_password():
    with open("my_password.json", mode='r') as file:
        data = json.load(file)
        try:
            website = website_input.get().lower()
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title="Search Result",
                                message=f"Website: {website}\nEmail: {email}\nPassword: {password}")
        except KeyError:
            messagebox.showerror(title='Error', message="Can't find such website.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=50, bg='white')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website: ", font=FONT, bg='white')
website_label.grid(row=1, column=0)
email_username_label = Label(text="Email/Username: ", font=FONT, bg='white')
email_username_label.grid(row=2, column=0)
password_label = Label(text="Password: ", font=FONT, bg='white')
password_label.grid(row=3, column=0)


website_input = Entry(width=28)
website_input.grid(row=1, column=1, pady=4)
email_username_input = Entry(width=38)
email_username_input.grid(row=2, column=1, columnspan=2, pady=4, padx=(0, 10))
password_input = Entry(width=28)
password_input.grid(row=3, column=1, pady=4)
generate_password = Button(text='Generate', bg='white', font=('', 9), width=8, command=make_password)
generate_password.grid(row=3, column=2, pady=4, padx=(0, 10))
add_button = Button(text='Add', bg='white', font=FONT, width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=4, padx=(0, 10))
search_button = Button(text='Search', bg='white', font=('', 9), width=8, command=search_password)
search_button.grid(row=1, column=2, pady=4, padx=(0, 10))

window.mainloop()
