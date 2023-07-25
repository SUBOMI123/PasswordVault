from cypher import *
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from datetime import datetime
import json


NAVY = '#6387BA'
GREY = '#bbbbbb'
BEIGE = '#ffe3d8'


def saved_entries():

    # GETTING THE USER INPUTS
    user_website = website_entry.get().lower()
    user_email = email_entry.get()
    user_password = password_entry.get()

    #"result of your encryption function"
    #at this point, you want to convert user_password to an encrypted form and store that in the json dict
    key, encrypted_password, iv = encrypt(user_password)

    

    new_data = {
        user_website: {
            'email': user_email,
            'encrypted_form': encrypted_password,
            'key': key,
            'iv' : iv
        }
    }
    if len(user_website) != 0 and len(user_password) != 0:

        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            is_correct = messagebox.askyesno(
                title=f"{user_website}",
                message=
                f"\n'email': {user_email}\n'password': {user_password}\n\nPlease confirm before saving!"
            )
            if is_correct:
                with open('data.json', 'w') as data_file:
                    json.dump(data, data_file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
    else:
        # IF WEBSITE OR EMAIL ENTRY IS BLANK
        messagebox.showwarning(title='Oops',
                               message="Please don't leave any fields empty!")


#SEARCH FUNCTION
def search_website():

    user_website = website_entry.get()

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            user_password = data[user_website]['encrypted_form']
            key = data[user_website]['key']
            iv = data[user_website]['iv']

            #decrypt the encrpted form and store in user_password
           
            user_password = decrypt(key, user_password, iv)
            #decrypt the encrpted form and store in user_password
           
            
            username = data[user_website]['email']
            password_entry.delete(0, END)
            password_entry.insert(0, user_password)
            email_entry.delete(0, END)
            email_entry.insert(0, username)
    except KeyError as error_msg:
        messagebox.showinfo(title="Key Error",
                            message=f"{error_msg} password does not exist")
    except FileNotFoundError as error_msg:
        messagebox.showinfo(
            message="File does not exist. Try using Add instead")


# GUI SETUP

root = Tk()
root.title("Password Vault")
root.config(padx=50, pady=50, bg=NAVY)

canvas = Canvas(height=200, width=200, bg=NAVY, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(120, 80, image=img)
canvas.grid(row=0, column=1)

website_label = Label(text='Website:', bg=NAVY, fg=BEIGE)
website_label.grid(row=1, column=0, sticky="W")

website_entry = Entry(font=('Arial', 15))
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

website_search = Button(text='Search', bg=GREY, command=search_website)
website_search.grid(row=1, column=2, sticky="EW")

email_label = Label(text='Email/Username:', bg=NAVY, fg=BEIGE)
email_label.grid(row=2, column=0, sticky="W")

email_entry = Entry(font=('Arial', 15))
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, '')

password_label = Label(text='Password:', bg=NAVY, fg=BEIGE)
password_label.grid(row=3, column=0, sticky="W")

password_entry = Entry(font=('Arial', 15))
password_entry.grid(row=3, column=1, sticky="EW")

button = Button(text='Add', bg=GREY, command=saved_entries)
button.grid(row=4, column=1, columnspan=2, sticky="EW")
button.config(pady=2)

root.mainloop()
