# importing necessary libraries and tools
import tkinter as tk
import stegano
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from stegano import lsb



# creating main window
root = Tk()
root.title("Steganograph")
root.geometry("700x480+150+180")
root.resizable(True, True)
root.configure(bg = '#00246B')




def showimage():
    global Filename
    Filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                          title = "Select Image",
                                          filetypes = (("PNG file", ".png"),
                                                        ("JPG file", ".jpg"),
                                                        ("All file", "*.txt")))

    img = Image.open(Filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image = img, width = 250, height = 250)
    lbl.image = img



def hide():
    global secret
    try:
        if Filename:  # Ensure an image file is selected
            message = text1.get(1.0, END).strip()  # Strip leading/trailing whitespace
            if message:  # Check if the message is not empty after stripping
                secret = lsb.hide(str(Filename), message)
                messagebox.showinfo("Success", "Message hidden successfully!")
            else:
                messagebox.showwarning("Warning", "The message box is empty. Please enter a message to hide.")
        else:
            messagebox.showwarning("Warning", "Please select an image first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def show():
    try:
        if Filename:  # Ensure an image file is selected
            try:
                clear_message = lsb.reveal(Filename)  # Attempt to reveal the message
                if clear_message:  # Check if a message was found
                    text1.delete(1.0, END)
                    text1.insert(END, clear_message)
                    messagebox.showinfo("Success", "Message revealed successfully!")
                else:
                    messagebox.showwarning("No Message", "No hidden message found in the image.")
            except Exception as e:
                messagebox.showerror("Error", "Failed to reveal the message. The image might not have any hidden data or be unsupported.")
        else:
            messagebox.showwarning("Warning", "Please select an image first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: No file Selected")



def saveimage():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if save_path:
        # Save the file to the selected location
        secret.save(save_path)



# Creating Widgets

# Icons
image_icon = PhotoImage(file = "/home/himanshu_27/Desktop/logo.png")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file = "/home/himanshu_27/Desktop/logo(1).png")
Label(root, image = logo, bg = '#00246B').place(x = 10, y = 0)

Label(root, text = "PICTEXT HIDER", bg = '#00246B', fg = "white", font = "arial 25 bold").place(x = 100, y = 20 )




# First Frame
f1 = Frame(root, bd = 3, bg = 'black', width = 340, height = 280, relief = GROOVE)
f1.place(x = 10, y = 80)

lbl = Label(f1, bg = 'black')
lbl.place(x = 40, y = 10)


def clear_image():
    lbl.configure(image = None)
    lbl.image = None

# adding a button to clear the selected picture.
clear_button = Button(f1, text = "x", font = 'arial 12 bold', bg = 'red', fg = 'white', bd = 2, command = clear_image, relief = RAISED)
clear_button.place(x = 300, y = 0)



# Second Frame
f2 = Frame(root, bd = 3, bg = 'white', width = 340, height = 280, relief = GROOVE)
f2.place(x = 350, y = 80)

lbl = Label(f1, bg = 'black')
lbl.place(x = 40, y = 10)

text1 = Text(f2, font = 'Robote 12', bg = 'white', fg = 'black', relief = GROOVE, wrap = WORD)
text1.place(x = 0, y = 0, width = 320, height = 290 )

# Adding Scrollbar
scroolbar1 = Scrollbar(f2)
scroolbar1.place(x = 320, y = 0, height = 300)

scroolbar1.configure(command = text1.yview)
text1.configure(yscrollcommand = scroolbar1.set)




# Third Frame
f3 = Frame(root, bd = 3, bg = '#CADCFC', width = 330, height = 100, relief = RAISED)
f3.place(x = 10, y = 370)

Button(f3, text = 'Open Image', width = 10, height = 2, font = 'arial 14 bold', command = showimage).place(x = 20, y = 30)
Button(f3, text = 'Save Image', width = 10, height = 2, font = 'arial 14 bold', command = saveimage).place(x = 180, y = 30)
Label(f3, text = "Select options", bg = '#CADCFC', fg = '#00246B').place(x = 20, y = 5)




# Fourth Frame
f4 = Frame(root, bd = 3, bg = '#CADCFC', width = 330, height = 100, relief = RAISED)
f4.place(x = 360, y = 370)

Button(f4, text = 'Hide Data', width = 10, height = 2, font = 'arial 14 bold', command = hide).place(x = 20, y = 30)
Button(f4, text = 'Show Data', width = 10, height = 2, font = 'arial 14 bold', command = show).place(x = 180, y = 30)
Label(f4, text = 'Functions', bg = '#CADCFC', fg = '#00246B').place(x = 20, y = 5)




root.mainloop()