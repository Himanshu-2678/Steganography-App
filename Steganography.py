# importing necessary libraries and tools
import tkinter as tk
import stegano
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb
import pyperclip
from tkinterdnd2 import DND_FILES, TkinterDnD


# Creating the main window
root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop
root.title("Steganograph")
root.geometry("700x480+150+180")
root.resizable(True, True)
root.configure(bg='#00246B')

# Global Variables
Filename = None
secret = None


# Copy Button Functionality
def copy_text():
    text_content = text1.get(1.0, END).strip()  # Get text from the textbox
    if text_content:
        pyperclip.copy(text_content)  # Copy text to clipboard
        messagebox.showinfo("Copied", "Text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Textbox is empty. Nothing to copy.")


# Drag-and-Drop Handler
def on_drop(event):
    global Filename
    dropped_file = event.data.strip()
    if os.path.isfile(dropped_file):  # Check if it's a valid file
        try:
            # Check if it's a valid image file
            img = Image.open(dropped_file)
            img.verify()
            img = Image.open(dropped_file)  # Reload for display
            img = ImageTk.PhotoImage(img)

            Filename = dropped_file  # Update the global Filename
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
            messagebox.showinfo("File Dropped", f"Loaded file: {os.path.basename(dropped_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid file. Please drop a valid image. Error: {e}")
    else:
        messagebox.showwarning("Warning", "Invalid file dropped. Please drop an image file.")

# Show Image Functionality
def showimage():
    global Filename
    Filename = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
            ("All files", "*.*"),
        ],
    )
    if Filename:
        try:
            img = Image.open(Filename)
            img.verify()
            img = Image.open(Filename)
            img = ImageTk.PhotoImage(img)
            lbl.configure(image=img, width=250, height=250)
            lbl.image = img
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")


# Hide and Show Functions
def hide():
    global secret
    if Filename:
        message = text1.get(1.0, END).strip()
        if message:
            secret = lsb.hide(Filename, message)
            messagebox.showinfo("Success", "Message hidden successfully!")
        else:
            messagebox.showwarning("Warning", "The message box is empty. Please enter a message to hide.")
    else:
        messagebox.showwarning("Warning", "Please select an image first.")


def show():
    if Filename:
        try:
            clear_message = lsb.reveal(Filename)
            if clear_message:
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
                messagebox.showinfo("Success", "Message revealed successfully!")
            else:
                messagebox.showwarning("No Message", "No hidden message found in the image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal the message: Message box might be empty.")


def saveimage():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        secret.save(save_path)


# Clear Image Functionality
def clear_image():
    lbl.configure(image=None)
    lbl.image = None


# Widgets and Frames

# Icons
image_icon = PhotoImage(file="/home/himanshu_27/Downloads/logo.png")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file="/home/himanshu_27/Downloads/logo(1).png")
Label(root, image=logo, bg='#00246B').place(x=10, y=0)

Label(root, text="PICTEXT HIDER", bg='#00246B', fg="white", font="arial 25 bold").place(x=100, y=20)

# First Frame
f1 = Frame(root, bd=3, bg='black', width=340, height=280, relief=GROOVE)
f1.place(x=10, y=80)

lbl = Label(f1, text="Drop your Files here", fg="white", bg='black', font=("Arial 15"))
lbl.place(relx=0.5, rely=0.5, anchor="center")

clear_button = Button(f1, text="x", font='arial 12 bold', bg='red', fg='white', bd=2, command=clear_image, relief=RAISED)
clear_button.place(x=300, y=0)

# Enabling drag-and-drop on the label
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Second Frame
f2 = Frame(root, bd=3, bg='white', width=340, height=280, relief=GROOVE)
f2.place(x=360, y=80)

text1 = Text(f2, font='Robote 12', bg='white', fg='black', relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=290)

scroolbar1 = Scrollbar(f2)
scroolbar1.place(x=320, y=0, height=300)

scroolbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scroolbar1.set)

# Third Frame
f3 = Frame(root, bd=3, bg='#CADCFC', width=330, height=100, relief=RAISED)
f3.place(x=15, y=380)

Button(f3, text='Open Image', width=10, height=2, font='arial 14 bold', command=showimage).place(x=20, y=30)
Button(f3, text='Save Image', width=10, height=2, font='arial 14 bold', command=saveimage).place(x=180, y=30)
Label(f3, text="Select options", bg='#CADCFC', fg='#00246B').place(x=20, y=5)

# Fourth Frame
f4 = Frame(root, bd=3, bg='#CADCFC', width=330, height=100, relief=RAISED)
f4.place(x=370, y=380)

Button(f4, text='Hide Data', width=10, height=2, font='arial 14 bold', command=hide).place(x=20, y=30)
Button(f4, text='Show Data', width=10, height=2, font='arial 14 bold', command=show).place(x=180, y=30)
Label(f4, text='Functions', bg='#CADCFC', fg='#00246B').place(x=20, y=5)

root.mainloop()