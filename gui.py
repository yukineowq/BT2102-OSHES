# code referenced and modified from this tutorial : https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
from db_connections.mysqldb import SQLDatabase
from db_connections.mongodb import MongoDB

LARGEFONT = ("Verdana", 35)

from tk_screens.authScreens import *
from tk_screens.customerPortal import *
from tk_screens.adminPortal import *
from tk_screens.adminApproveRequestsPage import *
from tk_screens.adminCompleteServicesPage import *


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        #reset database on load
        db = MongoDB()
        items, products = db.convertMongotoSQL()
        db = SQLDatabase()
        db.resetMySQLState()
        db.loadMongo(items, products)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('1500x800')
        # self.grid_propagate(0)
        self.title("OSHES Group 9")

        # initializing frames to an empty array
        self.frames = {}

        # Variables that persist through frames
        self.domain = None
        self.userID = None # If none, not logged in. Else logged in

        # iterating through a tuple consisting
        # of the different page layouts
        # all new pages created add here

        for F in (StartPage, LoginPage, RegisterPage, CustomerPortal, AdminPortal, CreateAdminPage, AdminProductSearch, AdminItemSearch, AdminAdvancedSearch, AdminApproveRequestsPage, AdminCompleteServicesPage):
    
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, domain=None, userID=None):
        frame = self.frames[cont]
        frame.tkraise()

        if (cont == LoginPage or cont == RegisterPage or cont == StartPage):
            if domain:
                frame = self.frames[cont]
                frame.setUserType(domain)
                frame.tkraise()
                self.domain = domain
            else:
                frame = self.frames[cont]
                frame.tkraise()

        elif cont == CustomerPortal or cont == AdminPortal or cont == AdminApproveRequestsPage or cont == AdminCompleteServicesPage: # Or cont == Mypurchases 
            menubar = frame.menuBar(self)
            self.configure(menu=menubar)
    
            # if not domain or not userID:
            #     frame = self.frames[cont]
            #     frame.tkraise()
            # else:
            frame = self.frames[cont]
            frame.domain = domain
            frame.userID = userID
            frame.tkraise()

        # elif (cont == MyPurchases):
        #     if not domain or not userID:
        #         menubar = frame.menuBar(self)
        #         self.configure(menu=menubar)
        #     else:
        #         menubar = frame.menuBar(self, domain = self.domain, userID = self.userID)
        #         self.configure(menu=menubar)

    def logout(self):
        self.show_frame(StartPage)
        self.domain = None
        self.userID = None

    # Getters
    def getDomain(self):
        return self.domain

    def getUserID(self):
        return self.userID

    # Setters
    def setUserID(self, userID):
        self.userID = userID

    def setDomain(self, domain):
        self.domain = domain
        print("Auth State changed:{} {}".format(self.domain, self.userID))




# Driver Code
app = tkinterApp()
app.mainloop()
