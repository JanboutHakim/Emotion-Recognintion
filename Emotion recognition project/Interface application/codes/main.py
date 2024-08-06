import customtkinter as ctk
from tkinter import IntVar, END, StringVar, DoubleVar

app = ctk.CTk()

app.geometry("720x480")  #window size

app.title("TK STARTER")  #Window label

customFont = ctk.CTkFont(family="arial", size=26, weight='bold', slant='italic', overstrike=True)

ctk.set_widget_scaling(1)
ctk.set_window_scaling(1)
ctk.set_default_color_theme("blue")

x = IntVar()
sp = DoubleVar()

t = StringVar()
t.set("Heelo")


def screenMode():
    if switch.get() == 1:
        ctk.set_appearance_mode("Dark")  #Dark Light System
    else:
        ctk.set_appearance_mode("Light")  #Dark Light System


def my_fun():
    label.configure(text="HIII")
    print(label.cget())


def getText():
    text1 = textarea.get("0.0", END)
    textarea.delete('0.0', END)
    print(text1)
    textarea.insert("0.0", "I'Fine How are you")
    txt = entry.get()
    entry.delete(0, END)
    label.configure(text=txt)
    print(x.get())
    print(slider.get() * 100)
    top = ctk.CTkToplevel()


def cechkbox():
    print(chkbox.get())


ctk.set_appearance_mode("Dark")  #Dark Light System
ctk.set_default_color_theme("green")  # all compponent colors [green bluee dark-blue]


def radioPreesed():
    print(radio.grab_set())


def spinnerFun(value):
    print(value)


frame = ctk.CTkScrollableFrame(app, corner_radius=8, height=100, width=200, border_color="green",
                               border_width=5)  #Have a label
#The frame is a container


frame.pack(padx=20, pady=20, fill="both", expand=True)  #pack - grid - place

button = ctk.CTkButton(frame, text="Hello", command=getText, hover_color=("red"))
button.pack(pady=100)

label = ctk.CTkLabel(frame, text="First Label", text_color="cyan", font=customFont)
label.pack()

switch = ctk.CTkSwitch(frame, text="Mode", command=screenMode)
switch.pack()

sbt = ctk.CTkSegmentedButton(frame, dynamic_resizing=True, values=['FerPlus', 'RAFDataset', 'l'], selected_color='red',
                             unselected_color='blue', selected_hover_color='green', unselected_hover_color='black')
sbt.pack()

entry = ctk.CTkEntry(frame, width=200, placeholder_text="user name", textvariable=t)
entry.pack()

textarea = ctk.CTkTextbox(frame)
textarea.pack()

chkbox = ctk.CTkCheckBox(frame, text="facial", command=cechkbox)
chkbox.pack()

radio = ctk.CTkRadioButton(frame, text="Male", variable=x, value=1)
radio.pack()
radio1 = ctk.CTkRadioButton(frame, text="Female", variable=x, value=2)
radio1.pack()

progress = ctk.CTkProgressBar(frame, variable=sp, width=150, height=20, corner_radius=0)
progress.pack()

slider = ctk.CTkSlider(frame, command=spinnerFun, variable=sp)
slider.set(0.25)
slider.pack()

opMenu = ctk.CTkOptionMenu(frame,
                           values=['Female', 'Male'])  #value = the values qrray the function return the selected value
opMenu.pack()

comboBox = ctk.CTkOptionMenu(frame, values=['Female', 'Male'])  #Like the Option Menu
comboBox.pack()

tabview = ctk.CTkTabview(frame)
tabview.place(y=20)
tabview.add('win1')
tabview.add('win2')

label1 = ctk.CTkLabel(tabview.tab('win1'), text="JAVA")
label1.pack()
label2 = ctk.CTkLabel(tabview.tab('win2'), text="PYTHON")
label2.pack()

inputDialog = ctk.CTkInputDialog()  #inputDialog.get_input(), fot dialog title:title

canvas = ctk.CTkCanvas(frame)  #empty frame
canvas.pack()

app.mainloop()
