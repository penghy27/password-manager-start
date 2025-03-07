from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

from matplotlib.pyplot import title


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pasword():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _  in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Ooops", message="Please make sure you haven't left any fields empty")
    else:
        # is_ok = messagebox.askokcancel(title=website,
        #                        message=f"These are the details entered: \nEmail: {email}"
        #                                f"\nPassword: {password} \n Is it ok to save?")

        try:
            with open("data.json", "r") as data_file:
                ## Use write mode
                # data_file.write(f"{website} | {email} | {password}\n")
                # Read old data with json
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # update old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # save update data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_text = Label(text="Website:")
website_text.grid(column=0, row=1)
email_username = Label(text="Email/Username: ")
email_username.grid(column=0, row=2)
password_text = Label(text="Password: ")
password_text.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row= 1, column= 1)
website_entry.focus()

email_entry = Entry(width=38)
email_entry.grid(row= 2, column= 1,columnspan = 2)
email_entry.insert(0, "test@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column = 1)

# Button
search_button = Button(text="Search", width = 13, command=search_password)
search_button.grid(row=1, column=2)

generate_password = Button(text="Generate Password", command=generate_pasword)
generate_password.grid(row=3, column = 2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan = 2)

window.mainloop()