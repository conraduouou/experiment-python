from tkinter import *

window = Tk()
window.title("my first gui")
window.minsize(width=300, height=150)
window.config(padx=50, pady=50)

def convert():
    label_in_km.config(text=f"{round(int(textfield.get()) * 1.60934)}")

# Components
textfield = Entry()
textfield.grid(row=0, column=1)
textfield.config(width=15)

label_miles = Label()
label_miles.config(text="Miles", padx=5)
label_miles.grid(row=0, column=2)

label_equal = Label()
label_equal.config(text="is equal to", padx=5)
label_equal.grid(row=1, column=0)

label_in_km = Label()
label_in_km.config(text="0")
label_in_km.grid(row=1, column=1)

label_km = Label()
label_km.config(text="Km", padx=5)
label_km.grid(row=1, column=2)

calculate_button = Button()
calculate_button.config(text="Calculate", command=convert)
calculate_button.grid(row=2, column=1)



window.mainloop()