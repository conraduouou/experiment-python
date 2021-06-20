from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

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
    if len(website_field.get()) != 0 and len(email_field.get()) != 0 and len(password_field.get()) != 0:

        is_ok = messagebox.askokcancel(title=website_field.get(), message=f"These are the details entered: \n\nEmail: {email_field.get()}"
                                                                        f"\nPassword: {password_field.get()} \n\n\nIs it ok to save?")

        if is_ok:
            with open("DAY 29 - Password Manager/data.txt", mode="a+") as data:
                to_print = (website_field.get(), email_field.get(), password_field.get())
                data.write(" | ".join(to_print) + "\n\n")
            
                website_field.delete(0, END)
                password_field.delete(0, END)
    
    else:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=PADDING, pady=PADDING)

lock_img = PhotoImage(file="DAY 29 - Password Manager\logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_field = Entry(width=39)
website_field.grid(row=1, column=1, columnspan=2)
website_field.focus()

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