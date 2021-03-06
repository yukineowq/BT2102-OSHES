from datetime import date
import tkinter as tk
import tkinter.ttk as ttk
import pymysql
import os
import json

from pymysql.connections import MySQLResult

class SQLDatabase():
    def __init__(self):
        try:
            self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
            self.c = self.connection.cursor()
        except:
            print("Oshes Database does not exist. Creating now")
            tempconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", autocommit=True)
            tempcursor = tempconnection.cursor()
            tempcursor.execute("CREATE DATABASE oshes;")
            tempconnection.commit()

            tempcursor.close()
            tempconnection.close()

            self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
            self.c = self.connection.cursor()


    # remaining : where to add the create tables codes 

    # TODO: Consider initializing the connection as None and invoke this function to connect
    def connect(self, dbname = "oshes"):
        self.connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes", autocommit=True)
        self.c = self.connection.cursor()

    def createDB(self):
        print("createDB: Oshes Database does not exist. Creating now")
        tempconnection = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", autocommit=True)
        tempcursor = tempconnection.cursor()
        tempcursor.execute("CREATE DATABASE oshes;")
        tempconnection.commit()
        tempcursor.close()
        tempconnection.close()


    # Create Customer - DONE
    def createCustomer(self, custInfo):
        addCust = ("INSERT INTO customer "
               "(customerID, name, email, password, address, phoneNumber, gender) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        try:   
            self.c.execute(addCust, custInfo)
            self.connection.commit()
        except Exception as e:
            return e

    # DISABLED
    def createAdmin(self, adminInfo): 
        addAdmin = ("INSERT INTO admin "
               "(adminID, name, password, gender, phoneNumber)"
               "VALUES (%s, %s, %s, %s, %s)")  
        # self.c.execute(addAdmin, adminInfo)
        # self.connection.commit()
        try:   
            self.c.execute(addAdmin, adminInfo)
            self.connection.commit()
        except Exception as e:
            return e

    # get Login
    def getCustomerLogin(self, customerID, password):
        getCustomerLogin = ("SELECT * FROM customer WHERE customerID = %s AND password=%s")
        
        self.c.execute(getCustomerLogin, (customerID,password))
        details = self.c.fetchone()
        if details:
            return details
        else:
            getCustomerLogin = ("SELECT * FROM customer WHERE customerID = %s")
            self.c.execute(getCustomerLogin, (customerID))
            details = self.c.fetchone()

            if details:
                return ("Incorrect Password")
            else:
                return ("User doesn't exist")
        

    def getAdminLogin(self, adminID, password):
        getAdminLogin = ("SELECT * FROM admin WHERE adminID = %s AND password=%s")
        
        self.c.execute(getAdminLogin, (adminID,password))
        details = self.c.fetchone()
        if details:
            return details
        else:
            getAdminLogin = ("SELECT * FROM admin WHERE adminID = %s")
            self.c.execute(getAdminLogin, (adminID))
            details = self.c.fetchone()

            if details:
                return ("Incorrect Password")
            else:
                return ("Admin User doesn't exist")

    # DONE: Changed to send to mysql
    def changePassword(self, newPassword, userID, domain):
        if domain == "Administrator":
            changeAdminPass = ("UPDATE admin SET password = %s WHERE adminID = %s")
            self.c.execute(changeAdminPass, (newPassword, userID))
            self.connection.commit()
        elif domain == "Customer":
            changeCustPass = ("UPDATE customer SET password = %s WHERE customerID = %s")
            self.c.execute(changeCustPass, (newPassword, userID))
            self.connection.commit()
        else:
            raise Exception("Check domain in changePassword")

    def dropTables(self):
        tables = ["Service","ServiceRequest","items","products","Customer","admin"]
        for table in tables:
            print("executing: Drop table "+table)
            sql = "DROP TABLE IF EXISTS {}"
            self.c.execute(sql.format(table))

    # Reset the whole database with the sql scripts in db_scripts/
    def resetMySQLState(self):
        # import inspect
        # print("Printed:",inspect.stack()[1].function)
        # dropDatabase()
        # self.createDB()
        rootdir = "./db_scripts"
        # Just in case someone cd into this dir and run the script
        # TODO: Specify the order of scripts to be executed
        try:
            files = os.listdir("./db_scripts")
        except:
            files = os.listdir("../db_scripts")
            rootdir = "../db_scripts"
        
        # Drop Tables
        tables = ["Service","ServiceRequest","items","products","Customer","admin"]
        for table in tables:
            print("executing: Drop table "+table)
            sql = "DROP TABLE IF EXISTS {}"
            self.c.execute(sql.format(table))

        dropEvent = "DROP EVENT IF EXISTS paymentOverdue"
        self.c.execute(dropEvent)

        #table.sql creates admin, customer, product and item table while customer and admin sqls create new users
        files = ["table.sql", "customer.sql", "admin.sql"]

        for file in files:
            with open(os.path.join(rootdir, file)) as f:
                allCmd = f.read().split(';')
                allCmd.pop()

                for idx, sql_request in enumerate(allCmd):
                    self.c.execute(sql_request + ';')
                    print("Executing:", sql_request)
        self.connection.commit()

    def loadMongo(self, items, products):
        productStr  = 'INSERT INTO products VALUES (%s, %s,%s, %s,%s, %s);'
        itemStr = 'INSERT INTO items VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s);'
        for product in products:
            print("Executing:", product)
            self.c.execute(productStr, product)
            self.connection.commit()

        for item in items:
            print("Executing:", item)
            self.c.execute(itemStr, item)
            self.connection.commit()

        # reqcreate = ("INSERT INTO ServiceRequest (serviceFee, requestStatus, dateOfRequest, itemID, dateOfPayment) VALUES (%s,%s,%s,%s,%s)")
        # self.c.execute(reqcreate, ("30", "Submitted and Waiting for Payment", "2021-01-01", "1001", "2021-01-09"))
        # self.connection.commit()
       

        # reqcreate1 = ("INSERT INTO ServiceRequest (serviceFee, requestStatus, dateOfRequest, itemID, dateOfPayment) VALUES (%s,%s,%s,%s,%s)")
        # self.c.execute(reqcreate1, ("40", "Submitted", "2021-01-01", "1002", "2021-01-09"))
        # self.connection.commit()
       

        # servicecreate = ("INSERT INTO Service (serviceStatus, itemID, requestID, adminID) VALUES (%s,%s,%s,%s)")
        # self.c.execute(servicecreate, ("Waiting for Approval", "1001", "1", "admin1"))
        # self.connection.commit()


        # servicecreate1 = ("INSERT INTO Service (serviceStatus, itemID, requestID, adminID) VALUES (%s,%s,%s,%s)")
        # self.c.execute(servicecreate1, ("In Progress", "1002", "2", "admin1"))
        # self.connection.commit()


        # upd = ("UPDATE Items SET customerID = 'customer1' WHERE itemID = %s")
        # self.c.execute(upd, ("1001"))
        # self.connection.commit()


        # upd = ("UPDATE Items SET customerID = 'customer1' WHERE itemID = %s")
        # self.c.execute(upd, ("1002"))
        # self.connection.commit()


    def retrieveRequestsForApproval(self):
        retrieveRequestsForApproval = ("SELECT r.requestID, s.serviceID, s.itemID, r.dateOfRequest, r.serviceFee, r.requestStatus, s.serviceStatus FROM ServiceRequest r, Service s WHERE s.requestID = r.requestID AND (r.requestStatus='Submitted' OR r.requestStatus='In progress') AND s.serviceStatus = 'Waiting for Approval' ORDER BY requestID")
        self.c.execute(retrieveRequestsForApproval, ())
        results = self.c.fetchall()
        return results

    def approveRequests(self, requestIDs, serviceIDs, adminID):
        approveRequests = ("UPDATE ServiceRequest SET requestStatus = 'Approved' WHERE requestID = %s")
        result = self.c.executemany(approveRequests, requestIDs)
        if result != len(requestIDs):
            self.connection.rollback()
            return result
        queryString1 = ("UPDATE Service SET serviceStatus = 'In Progress', adminID = ")
        queryString2 = (" WHERE serviceID = %s")
        serviceItems = queryString1 + "'" + adminID + "'" + queryString2
        result = self.c.executemany(serviceItems, serviceIDs)
        if result != len(serviceIDs):
            self.connection.rollback()
            return result
        self.connection.commit()
        return result

    def retrieveServicesToComplete(self, adminID):
        retrieveServicesToComplete = ("SELECT r.requestID, s.serviceID, s.itemID, r.dateOfRequest, r.requestStatus, s.serviceStatus FROM ServiceRequest r, Service s WHERE s.requestID = r.requestID AND s.serviceStatus = 'In Progress' AND r.requestStatus = 'Approved' AND s.adminID = %s ORDER BY r.requestID")
        self.c.execute(retrieveServicesToComplete, (adminID))
        results = self.c.fetchall()
        return results

    def completeService(self, requestIDs, serviceIDs):
        completeService = ("UPDATE Service SET serviceStatus = 'Completed' WHERE serviceID = %s")
        result = self.c.executemany(completeService, serviceIDs)
        if result != len(serviceIDs):
            self.connection.rollback()
            return result
        completeRequest = ("UPDATE ServiceRequest SET requestStatus = 'Completed' WHERE requestID = %s")
        result = self.c.executemany(completeRequest, requestIDs)
        if result != len(requestIDs):
            self.connection.rollback()
            return result
        self.connection.commit()
        return result

    def itemUnderService(self):
        # itemsList = ("SELECT i.itemID, p.category, p.model, s.serviceStatus, (SELECT name FROM admin a WHERE a.adminID = s.adminID) as adminAssigned FROM Items i, Products p, Service s WHERE i.productID = p.productID AND s.itemID = i.itemID ORDER BY itemID")
        # self.c.execute(itemsList)
        itemsList = ("SELECT i.itemID, p.category, p.model, s.serviceStatus, (SELECT name FROM admin a WHERE a.adminID = s.adminID) as adminAssigned FROM Items i, Products p, Service s WHERE i.productID = p.productID AND s.itemID = i.itemID AND (s.serviceStatus = %s OR s.serviceStatus = %s) ORDER BY itemID")
        self.c.execute(itemsList, ("Waiting for Approval", "In Progress"))
        results = self.c.fetchall()
        return results
    
    def custWithUnpaidFees(self):
        custList  =  ("SELECT customerID, name, email, requestID, serviceFee, (DATEDIFF(r.dateOfRequest, CURDATE())+ 10) as daysLeft FROM Customer c, ServiceRequest r WHERE requestStatus = %s ORDER BY customerID")
        self.c.execute(custList, ("Submitted and Waiting for payment"))
        results = self.c.fetchall()
        return results
    

    def retrieveRequests(self, customerID):
        # requestsList = ("SELECT r.requestID, i.itemID, r.requestStatus, r.dateOfRequest, ADDDATE(r.dateOfRequest, 10) as dueDate, r.serviceFee FROM Items i, ServiceRequest r WHERE i.itemID = r.itemID AND i.customerID = %s ORDER BY r.requestID")
        requestsList = ("SELECT r.requestID, i.itemID, r.requestStatus, r.dateOfRequest, ADDDATE(r.dateOfRequest, 10) as dueDate, r.serviceFee, s.serviceStatus FROM Items i, ServiceRequest r, Service s WHERE i.itemID = r.itemID AND i.customerID = %s AND s.requestID = r.requestID ORDER BY r.requestID")
        self.c.execute(requestsList, customerID)
        results = self.c.fetchall()
        return results

    def payRequest(self, requestID):
        cancelReq = ("UPDATE ServiceRequest SET requestStatus = %s, dateOfPayment = CURDATE() WHERE requestID = %s")
        self.c.execute(cancelReq, ("In Progress", requestID))
        self.connection.commit()

    def cancelRequest(self, requestID):
        cancelReq = ("UPDATE ServiceRequest SET requestStatus = %s WHERE requestID = %s")
        self.c.execute(cancelReq, ("Canceled", requestID))
        
        cancelService = ("UPDATE Service SET serviceStatus = %s WHERE requestID = %s")
        self.c.execute(cancelService, ("Completed", requestID))
        self.connection.commit()

    def retrieveInventoryLevel(self):
        retrieveInventoryLevel = "SELECT i.productID, p.category, p.model, sum(case when purchaseStatus='sold' then 1 else 0 end) AS 'Sold', sum(case when purchaseStatus='unsold' then 1 else 0 end) AS 'Unsold' FROM items i, products p WHERE i.productID = p.productID GROUP BY productID;"
        self.c.execute(retrieveInventoryLevel, ())
        results = self.c.fetchall()
        return results

    def loadPurchases(self, userID):
        # purchasesList = ("SELECT i.itemID, category, model, price, dateOfPurchase, warranty, serviceStatus FROM (items i JOIN products p ON i.productID = p.productID) LEFT JOIN service s ON i.itemID = s.serviceID WHERE customerID = %s")

        purchasesList = ("SELECT itemID, category, model, cost, price, dateOfPurchase, warranty FROM items i, products p WHERE i.productID = p.productID AND customerID = %s")
        self.c.execute(purchasesList, (userID,))
        results = self.c.fetchall()
        return results

    def findExistingServices(self, itemID):
        findServices = ("SELECT * FROM service WHERE itemID = %s AND (serviceStatus = 'Waiting for Approval' OR serviceStatus = 'In Progress')")
        self.c.execute(findServices, (itemID))
        results = self.c.fetchall()
        return results

    def createServiceRequest(self, reqInfo):
        # createReq = ("INSERT INTO servicerequest (serviceFee, requestStatus, dateOfRequest, itemID) VALUES (%s, 'Submitted and Waiting for payment', %s, %s);")
        # print(reqInfo[0])
        # print(reqInfo[1])
        # print(reqInfo[2])
        # print(reqInfo[3])
        createReq = ("INSERT INTO servicerequest (serviceFee, requestStatus, dateOfRequest, itemID) VALUES (%s, %s, %s, %s);")

        try:   
            self.c.execute(createReq, reqInfo)
            self.connection.commit()
            requestID = self.c.lastrowid
            print(requestID)
            self.createService([reqInfo[3], requestID])
        except Exception as e:
            return e

    # def retrieveRequestID(self, reqInfo):
    #     reqID  =  ("SELECT requestID FROM servicerequest WHERE dateOfRequest = %s AND itemID = %s")
    #     self.c.execute(reqID, reqInfo)
    #     results = self.c.fetchone()
    #     return results

    def createService(self, serviceInfo):
        createService = ("INSERT INTO service (serviceStatus, itemID, requestID) VALUES ('Waiting for Approval', %s, %s)")
        try:   
            self.c.execute(createService, serviceInfo)
            self.connection.commit()
            print("created Service")
        except Exception as e:
            return e


    def getConnection(self):
        return self.connection

# # this methods will be callable without any requirements for the database
# class DBOps():
#     def dropDatabase(self):
#         print("Dropping Databases")
#         try:
#             tempc = pymysql.connect(host="localhost", port=3306, user="root", passwd="password")
#             cur = tempc.cursor()
#             print("check1")
#             cur.execute("CREATE DATABASE oshes;")
#             tempc.commit()

#             tempc.select_db("oshes")

#             cur.execute("DROP DATABASE oshes;")
#             tempc.commit()
#             print("check2")
            
#         except:
#             raise Exception("DB oshes does not exist")


# # Exists outside of the class. Drops the oshes database if it exists
# def dropDatabase():
#     print("Dropping Databases")
#     try:
#         tempc = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", database="oshes")
#         cur = tempc.cursor()
#         # print("check1")
#         cur.execute("DROP DATABASE oshes;")
#         tempc.commit()
#         # print("check2")
        
#     except:
#         print("DB oshes does not exist")


if __name__ == "__main__":
    db = SQLDatabase()
    # db.changePassword('aa', 'bb', "Customer")
    # print(db.getCustomerLogin('aa','aa'))
    db.resetMySQLState()


    # db.resetMySQLState()
    # Testing Functions

    # # Create customer
    # db.createCustomer(["brenda3","Brenda3","brenda3@gmail.com","password","1 Street", "4444", "F"])
    # db.createAdmin(["admin2","Admin2","password", "F", "5555" ])


    # login
    # email = 'brenda2@gmail.com'
    # print(db.getCustomerLogin(email,"password")) # correct
    # print(db.getCustomerLogin(email,"Aassword")) # incoreect password
    # print(db.getCustomerLogin("a"+email,"password")) # user doesnt exist
