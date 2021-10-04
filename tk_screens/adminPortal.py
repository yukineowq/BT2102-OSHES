import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Entry
from db_connections.mysqldb import SQLDatabase
from tk_screens.adminCategorySearch import AdminCategorySearch 
from tk_screens.adminItemSearch import AdminItemSearch

db = SQLDatabase()

class AdminPortal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.domain = tk.StringVar(self)

        # Reset Button
        resetButton = ttk.Button(self, text="Reset SQLDB", command=self.resetDB)
        resetButton.grid(row=0, column=1, padx=10, pady=10)
        #  Dummy Display 
        options = ("Customer", "Administrator")

        dropdownlist = ttk.OptionMenu(self, self.domain, options[0], *options)
        
        dropdownlist.grid(row=1, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Search Product",
                             command=lambda: controller.show_frame(AdminCategorySearch))
        button1.grid(row=4, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Search Item",
                             command=lambda: controller.show_frame(AdminItemSearch))
        button2.grid(row=4, column=2, padx=10, pady=10)

    def resetDB(self):
        db.resetMySQLState()
        db.dataInit()
# In addition, provide a MYSQL database initialization function under the Administrator login. 
# At the beginning of your  presentation, you are required to apply this function to reinitialize the MYSQL database. 
# When the MYSQL database is initialized,  provide a function to allow the Administrator to display the following information (Purchase status= “SOLD” and  Purchase status=“UNSOLD”) on the items in the MySQL tables:


# Winy can try with her table code too

 # table = Table(parent= parent,columns=("FName", "LName", "Roll No"))
        # table.insertRow(('Amit', 'Kumar', '17701'))
        # table.insertRow(('Ankush', 'Mathur', '17702'))
        # tree = table.getTree()
        # tree.grid(row=4, column=1, padx=10, pady=10)

# class Table:
#     def __init__(self, parent, columns, num_visible_rows=5):
#         self.tree = ttk.Treeview(parent, column=columns, show='headings', height=num_visible_rows)
#         self.tree.column("# 1", anchor="center")
#         self.tree.heading("# 1", text="FName")
#         self.tree.column("# 2", anchor="center")
#         self.tree.heading("# 2", text="LName")
#         self.tree.column("# 3", anchor="center")
#         self.tree.heading("# 3", text="Roll No")


#     def insertRow(self, values):
#         self.tree.insert('', 'end', text="1", values=values)

#     def getTree(self):
#         return self.tree