from tkinter import Toplevel, Label
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from datetime import date
from db_connections.mysqldb import SQLDatabase
from db_connections.mongodb import MongoDB

#connect to mongoDB to search
global client
global db
global products
mymongodb = MongoDB()
client = mymongodb.getClient()
db = client["oshes"]
products = db["products"]

#connect to mysql database to register purchases
global con
mysqlinit = SQLDatabase()
con = mysqlinit.getConnection()

class searchWindow(Toplevel):
    
    def __init__(self, master = None):
        # Pass in the controller from the other frames as master
        super().__init__(master = master)
        self.title("Search Products")
        self.geometry('1050x600')
        self.homeButton = ttk.Button(self)
        self.homeButton.configure(text='Home')
        self.homeButton.grid(column='1', padx='3', pady='3', row='1')

        self.searchButton = ttk.Button(self)
        self.searchButton.configure(text='Search')
        self.searchButton.grid(column='7', padx='5', pady='5', row='9')
        self.searchButton.bind('<1>', self.search, add='')

        self.buyButton = ttk.Button(self)
        self.buyButton.configure(text='Buy')
        self.buyButton.grid(column='7', pady='20', row='11', sticky='e')
        self.buyButton.bind('<Button-1>', self.buyItem)

        

        ####Comboboxes####
        vModel=[]
        self.modelBox = ttk.Combobox(self, values = vModel)
        self.modelBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.modelBox.grid(column='4', padx='5', pady='5', row='3')

        #ensure that only the right model shows when category selected
        def categoryAndModel(event):
            if self.categoryBox.get()=="Lights":
                vModel = ["Light1", "Light2", "SmartHome1",""]
            elif self.categoryBox.get()=="Locks":
                vModel = ["Safe1", "Safe2", "Safe3", "SmartHome1",""]
            else:
                vModel = []
            self.modelBox.configure(values = vModel)


        self.categoryBox = ttk.Combobox(self, values = ["Lights", "Locks",""])
        self.categoryBox.bind('<<ComboboxSelected>>', categoryAndModel)
        self.categoryBox.configure(state='readonly')
        self.categoryBox.grid(column='4', padx='5', pady='5', row='2')
        
        self.priceBox = ttk.Combobox(self,values = ["50", "60",
        "70","100","120","125","200",""])
        self.priceBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.priceBox.grid(column='7', padx='5', pady='5', row='2')
        
        self.colorBox = ttk.Combobox(self, values = ["White", "Blue",
        "Yellow", "Green", "Black",""])
        self.colorBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.colorBox.grid(column='7', padx='5', pady='5', row='3')

        self.factoryBox = ttk.Combobox(self, values = ["Malaysia", "China", "Philippines",""])
        self.factoryBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.factoryBox.grid(column='7', padx='5', pady='5', row='4')

        self.productionYearBox = ttk.Combobox(self, values = ["2014", "2015",
        "2016", "2017", "2018", "2019", "2020",""])
        self.productionYearBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.productionYearBox.grid(column='7', padx='5', pady='5', row='5')

        self.powerSupplyBox = ttk.Combobox(self, values = ["Battery", "USB",""])
        self.powerSupplyBox.configure(cursor='arrow', state='readonly', takefocus=False)
        self.powerSupplyBox.grid(column='7', padx='5', pady='5', row='6')

        ####Labels####
        self.simpleSearchLabel = ttk.Label(self)
        self.simpleSearchLabel.configure(background='#a6f991', text='Simple Search')
        self.simpleSearchLabel.grid(column='2', padx='5', pady='5', row='2')

        self.advancedSearchLabel = ttk.Label(self)
        self.advancedSearchLabel.configure(background='#b19bee', text='Advanced Search')
        self.advancedSearchLabel.grid(column='5', padx='5', pady='5', row='2')

        self.priceLabel = ttk.Label(self)
        self.priceLabel.configure(text='Price')
        self.priceLabel.grid(column='6', padx='5', pady='5', row='2')

        self.colorLabel = ttk.Label(self)
        self.colorLabel.configure(text='Color')
        self.colorLabel.grid(column='6', padx='5', pady='5', row='3')

        self.factoryLabel = ttk.Label(self)
        self.factoryLabel.configure(text='Factory')
        self.factoryLabel.grid(column='6', padx='5', pady='5', row='4')

        self.productionYearLabel = ttk.Label(self)
        self.productionYearLabel.configure(text='Production Year')
        self.productionYearLabel.grid(column='6', padx='5', pady='5', row='5')

        self.powerSupplyLabel = ttk.Label(self)
        self.powerSupplyLabel.configure(text='Power Supply')
        self.powerSupplyLabel.grid(column='6', padx='5', pady='5', row='6')

        self.categoryLabel = ttk.Label(self)
        self.categoryLabel.configure(text='Category')
        self.categoryLabel.grid(column='3', padx='5', pady='5', row='2')

        self.modelLabel = ttk.Label(self)
        self.modelLabel.configure(text='Model')
        self.modelLabel.grid(column='3', padx='5', pady='5', row='3')
        
        ####Item display####
        self.treeFrame= ttk.Frame(self)
        self.treeFrame.configure(height='400', padding='5', relief='ridge', width='300')
        self.treeFrame.grid(column='2', columnspan='6', row='10', rowspan='1')

        cols = ("itemID","Category","Model", "Price", "Color","Factory", "Production Year", "Power Supply")
        
        self.itemTree = ttk.Treeview(self.treeFrame, columns = cols,show='headings')
        self.itemTree.pack(side='left')
        scroll_y = Scrollbar(self.treeFrame, orient = 'vertical', command = self.itemTree.yview)
        scroll_y.pack(side = RIGHT, fill = Y)
        self.itemTree.configure(yscrollcommand = scroll_y.set)

        
        for col in cols:
            self.itemTree.column(col, anchor="center", width=110)
            self.itemTree.heading(col, text=col)


        self.availItems = ttk.Label(self, font=("Arial", 14))
        self.availItems.configure(text='Search Results')
        self.availItems.grid(column='2', columnspan='2', row='9')

         #take inputs from comboboxes and bring to searchResults frame
    def search(self, event):
        self.itemTree.delete(*self.itemTree.get_children())
        mongoSearch = ""
        
        category = self.categoryBox.get()
        model = self.modelBox.get()
        price =  self.priceBox.get()
        color = self.colorBox.get()
        factory = self.factoryBox.get()
        productionYear = self.productionYearBox.get()
        powerSupply = self.powerSupplyBox.get()

        ##special handeling for price
        if price:
            catandmod = self.findModelfromPrice(price)
            if category and category != catandmod[0]:
                category = "no output"
            if model and model != catandmod[1]:
                model = "no output"
            else:
                category = catandmod[0]
                model = catandmod[1]       

        if category:
            mongoSearch += "'Category': " + "'{}'".format(category) + ", "
        if model:
            mongoSearch += "'Model': " + "'{}'".format(model) + ", "
        if color:
            mongoSearch += "'Color': " + "'{}'".format(color) + ", "
        if factory:
            mongoSearch += "'Factory': " + "'{}'".format(factory) + ", "
        if productionYear:
            mongoSearch += "'ProductionYear': " + "'{}'".format(productionYear) + ", "
        if powerSupply:
            mongoSearch += "'PowerSupply': " + "'{}'".format(powerSupply) + ", "
        
        mongoSearch = "{" + mongoSearch + "'PurchaseStatus': 'Unsold'" + "}"

        #uncomment print statement to show output in terminal
        #print(mongoSearch)

        items = db["items"]
        allrecords = items.find(eval(mongoSearch))
        allrecordsList = list(allrecords)
        #uncomment to print records in terminal
        messagebox.showinfo(title="Search Results", message= "{} items available based on your search!".format(len(allrecordsList)))

        if len(allrecordsList) == 0:
            pass
        else:
            for record in allrecordsList:
                result = self.mongoToTree(record)
                self.itemTree.insert("", "end", values=result)
    
    def findModelfromPrice(self, price):
        product = products.find({'Price ($)': int(price)})[0]
        Category = product['Category']
        Model = product['Model']
        return (Category, Model)

    def findPrice(self, category, model):
        product = products.find({'Category': category, 'Model': model})[0]
        price = product['Price ($)']
        return (price)

    def buyItem(self, a):
        curItem = self.itemTree.focus()
        extractID = self.itemTree.item(curItem)['values'][0]
        
        #update mysql database, need to get current customer id
        updateStatement = "UPDATE Item SET PurchaseStatus = 'Sold',dateOfPurchase = %s, customerID = %s  WHERE ItemID = %s"
        val = (date.today().isoformat(),"001", extractID)

        con.ping()  # reconnecting mysql
        with con.cursor() as cursor:         
            cursor.execute(updateStatement, val)
        con.commit()
        con.close()



        #delete item and show purchase success
        self.itemTree.delete(self.itemTree.focus())
        messagebox.showinfo(title="Purchase Successful", message= "Thank you for your purchase!")
        

    def mongoToTree(self, r):
        price = self.findPrice(r["Category"], r["Model"])
        re = (r["ItemID"], r["Category"], r["Model"], price, r["Color"], r["Factory"], r["ProductionYear"], r["PowerSupply"])
        return re