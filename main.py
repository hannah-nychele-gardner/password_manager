from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json

# TODO have user create (or generate) key that is used to get into main part of app
# TODO encrypt the data in the app, un-encrypt when key is given

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.insert(0, generated_password)
    # copies the password to your clipboard
    window.clipboard_clear()
    window.clipboard_append(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Field Empty", message="Please fill in all the fields.")
    else:
        try:
            with open("data.json", "r") as file:
                # Loading existing data from the file
                data = json.load(file)
                if website in data:
                    overwrite = messagebox.askyesno(title="Password Already Saved",
                                                    message=f"You have already saved a password for {website}."
                                                            "\nWould you like to overwrite?")
                    if overwrite:
                        data[website]["username"] = username
                        data[website]["password"] = password
                else:
                    messagebox.showinfo(title="Save Successful",
                                        message=f"Your login information for {website} has been saved. The password has"
                                                f" been copied to your clipboard for your convenience.")
                # TODO alter message box so it has a button that user can click to copy to clipboard, delete auto-copy
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Saving the updated data to the file
                json.dump(new_data, file, indent=4)
        else:
            # Adding the new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving the updated data to the file
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ------------------------- FIND PASSWORD ----------------------------- #


def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Password File Unavailable", message="No password file found.")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Username: {data[website]['username']}"
                                                       f"\nPassword: {data[website]['password']}")
        else:
            messagebox.showerror(title="Details Unavailable", message=f"No details found for {website}.")


# ---------------------------- UI SETUP ------------------------------- #
# TODO redo colors in UI so it looks better, hopefully less like Windows XP if possible (look into button formatting)

window = Tk()
window.title("My Pass")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()
username_entry = Entry()
username_entry.grid(column=1, columnspan=2, row=2, sticky="EW")
username_entry.insert(0, "hannah@email.com")
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")
password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky="EW")
add_button = Button(text="Add", width=35, command=save)
add_button.grid(column=1, columnspan=2, row=4, sticky="EW")
# TODO create a command that opens up a window with the .json data formatted in a nice way, ability to copy any password
#  in the list by clicking it
view_data_button = Button(text="View all Logins")
view_data_button.grid(column=1, columnspan=2, row=5, sticky="EW", pady=10)

window.mainloop()
