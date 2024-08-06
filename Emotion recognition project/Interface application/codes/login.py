import customtkinter as ctk

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title='Login Window'
        self.geometry("720x480")
        self.frame=ctk.CTkFrame(self)
        self.frame.pack(padx=100,pady=100,fill="both",expand=True)

        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)

        self.button=ctk.CTkButton(self.frame,text="HOME",command=self.newWindow)
        self.button.grid(row=2,column=0)

        self.label=ctk.CTkLabel(self.frame,text="Hello")
        self.label.grid(row=1,column=0)

    def newWindow(self):
        self.withdraw()
        self.mainWindow=ctk.CTkToplevel()
        
        

app=Login()
app.mainloop()


#     Grid Sticky option
#           N
#           ^
#           |
#w      <--   -->        E
#           |
#          \ /
#           .
#           S 
# se,sw,sn,snwe ....