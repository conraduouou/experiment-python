from json.decoder import JSONDecodeError
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

PADDING = 50

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list = [choice(letters) for i in range(randint(8, 10))]
    password_list += [choice(numbers) for i in range(randint(2, 4))]
    password_list += [choice(symbols) for i in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)

    password_field.delete(0, END)
    password_field.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    new_data = {
        website_field.get().lower(): {
            "email": email_field.get(),
            "password": password_field.get()
        } 
    }

    if len(website_field.get()) != 0 and len(email_field.get()) != 0 and len(password_field.get()) != 0:
        try:
            with open("DAY 30 - Password Manager 2/data.json", mode="r") as data:
                contents = json.load(data)
        except FileNotFoundError:
            with open("DAY 30 - Password Manager 2/data.json", mode="w") as data:
                json.dump(new_data, data, indent=4)
        else:
            contents.update(new_data)
            with open("DAY 30 - Password Manager 2/data.json", mode="w") as data:
                json.dump(contents, data, indent=4)
        finally:
            website_field.delete(0, END)
            password_field.delete(0, END)
    else:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")

# ------------------------- SEARCH FUNCTION --------------------------- #
def search():
    try:
        with open("DAY 30 - Password Manager 2/data.json", "r") as data:
            contents = json.load(data)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No data file found!")
    else:
        if website_field.get().lower() in contents:
            website = contents[website_field.get()]
            messagebox.showinfo(title="Account details", 
                                message=f"Email: {website['email']}\nPassword: {website['password']}")

        else:
            messagebox.showerror(title="Oops", message=f"No details for {website_field.get()}!")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=PADDING, pady=PADDING)

lock_img = PhotoImage(file="DAY 30 - Password Manager 2/logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_field = Entry(width=21)
website_field.grid(row=1, column=1)
website_field.focus()

search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_field = Entry(width=39)
email_field.grid(row=2, column=1, columnspan=2)
email_field.insert(END, "louise@email.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_field = Entry(width=21)
password_field.grid(row=3, column=1)

generate_button = Button(text="Generate Password", command=generate)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()