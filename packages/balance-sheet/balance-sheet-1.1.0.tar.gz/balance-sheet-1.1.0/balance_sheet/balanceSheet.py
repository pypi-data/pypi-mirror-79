""" The balance sheet object.

    Backend in SQL, persists in memory with Pandas.
"""
import os
from pathlib import Path
import pandas as pd 
import sqlite3


class BalanceSheet:
    "The balance sheet class"
    def __init__(self):
        self.sql_connection()       # opens the connection to the database
        self.sql_table()            # creates the tables if they have not been created
        self.get_date()             # get the date of the last balance sheet
        self.get_table_id()         # get the current table id

    def __len__(self):
        return len(self.data)

    def sql_connection(self):
        "opens a connection to the local sql database"
        # get the location of the home directory
        home = Path.home()
        # check if there is a .balance_sheet directory
        if not '.balance_sheet' in os.listdir(home):
            # create one if it does not exist
            os.mkdir(os.path.join(home, '.balance_sheet'))
        # open the connection to the database
        try:
            self.con = sqlite3.connect(os.path.join(home, ".balance_sheet/balancesheet.db"))
        except sqlite3.Error:
            print(sqlite3.Error)

    def sql_table(self):
        "makes a new empty balance sheet"
        # the cursor object
        cursorObj = self.con.cursor()
        # the balance sheet table
        cursorObj.execute("CREATE TABLE IF NOT EXISTS balancesheet(item_id INTEGER PRIMARY KEY AUTOINCREMENT, table_id INTEGER, type TEXT, name TEXT, value REAL, description TEXT)")
        # a table to keep track of when the tables were updates
        cursorObj.execute("CREATE TABLE IF NOT EXISTS lastupdated(table_id INTEGER PRIMARY KEY, date TEXT)")
        # a table for stats on our progress
        cursorObj.execute("CREATE TABLE IF NOT EXISTS stats(table_id INTEGER PRIMARY KEY, date TEXT, assets REAL, liabilities REAL, net_worth REAL)")
        self.con.commit()

    def read(self):
        "Reads the current balance sheet"
        # the cursor object
        cursorObj = self.con.cursor()
        # selecting from the balance sheet table
        cursorObj.execute("SELECT type, name, value, description FROM balancesheet")
        rows = cursorObj.fetchall()
        # create dataframe of results
        self.data = pd.DataFrame(rows, columns = ["Type", "Name", "Value", "Description"])
        # separate into assets and liabilities
        self.data = self.data.set_index("Type").sort_index()

    def get_date(self):
        "Gets the most recent balance sheet"
        # the cursor object
        cursorObj = self.con.cursor()
        cursorObj = cursorObj.execute("SELECT date FROM lastupdated ORDER BY table_id DESC LIMIT 1")
        try:
            self.last_date = cursorObj.fetchone()[0]
        except TypeError:
            self.last_date = None

    def get_table_id(self):
        "get the id number of the new table"
        # the cursor object
        cursorObj = self.con.cursor()
        cursorObj = cursorObj.execute("SELECT MAX(table_id) FROM lastupdated")
        self.table_id = cursorObj.fetchone()[0]

    def insert_date(self, date):
        "inserts a date for a new table"
        # the cursor object
        cursorObj = self.con.cursor()
        cursorObj = cursorObj.execute("INSERT INTO lastupdated(table_id, date) VALUES(?, ?)", (self.table_id, date))
        self.con.commit()

    def update_date(self, today):
        "updates the date of the current balancesheet"
        # the cursor object
        cursorObj = self.con.cursor()
        cursorObj = cursorObj.execute(f"UPDATE lastupdated SET date = {today} WHERE table_id = {self.table_id}")
        self.con.commit()

    def insert(self, item):
        "inserts an asset or liability"
        # the cursor object
        cursorObj = self.con.cursor()
        x = [self.table_id] + item
        cursorObj.execute('INSERT INTO balancesheet(table_id, type, name, value, description) VALUES(?, ?, ?, ?, ?)', x)
        self.con.commit()

    def move_forward(self):
        "copies the current balance sheet and increments the table_id"
        cursorObj = self.con.cursor()
        cursorObj.execute(f"INSERT INTO balancesheet(table_id, type, name, value, description) SELECT {self.table_id+1}, type, name, value, description FROM balancesheet WHERE table_id={self.table_id}")
        self.con.commit()

    def modify(self, type_sec, item, field, value):
        "modifies value of the field of the type of item"
        # the cursor object
        cursorObj = self.con.cursor()
        # the type of security we are modifying
        if type_sec == "Asset":
            # update the assets dataframe
            self.ass.at[item, field] = value 
        elif type_sec == "Liability":
            # update the liabilities dataframe
            self.liab.at[item, field] = value
        # typecast the value
        if field == "value":
            cursorObj = cursorObj.execute(f"UPDATE balancesheet SET {field} = {value} WHERE type = '{type_sec}' AND table_id = {self.table_id}")
        else:
            cursorObj = cursorObj.execute(f"UPDATE balancesheet SET {field} = '{value}' WHERE type = '{type_sec}' AND table_id = {self.table_id}")
        self.con.commit()

    def delete(self, type_sec, item):
        "dete an item on assets or liabilities"
        # the cursor object
        cursorObj = self.con.cursor()
        # the type of security we are deleting
        if type_sec == "Asset":
            (name, value, description) = self.ass.iloc[item]
            self.ass.drop(item, inplace=True)
        elif type_sec == "Liability":
            (name, value, description) = self.liab.iloc[item]
            self.liab.drop(item, inplace=True)
        # update the SQL table
        cursorObj = cursorObj.execute(f"DELETE FROM balancesheet WHERE table_id = {self.table_id} AND name = '{name}' AND value = {value}")
        self.con.commit()

    def eval(self):
        "Evaluates the value of the balance sheet"
        # assets
        try:
            self.ass = self.data.loc['Asset'].reset_index(drop=True)
            self.tot_ass = self.ass.Value.sum()
        # if there are no assets
        except KeyError:
            self.tot_ass = 0
        # if there is only one asset
        except AttributeError:
            self.tot_ass = self.ass.iloc[1]
        # liabilities
        try:
            self.liab = self.data.loc['Liability'].reset_index(drop=True)
            self.tot_liab = self.liab.Value.sum()
        # if there are no liabilities
        except KeyError:
            self.tot_liab = 0
        # if there is only one liability
        except AttributeError:
            self.tot_liab = self.liab.iloc[1]
        # net worth
        self.net_worth = self.tot_ass - self.tot_liab

    def display(self):
        "Displays the current state of the balance sheet"
        # read from the sql table
        self.read()
        # eval
        self.eval()
        # assets
        if self.tot_ass == 0:
            print("No Assets")
        else:
            print(f"\nAssets:\n{self.ass}")
            print(f"Total Assets: {self.tot_ass}")
        # liabilities
        if self.tot_liab == 0:
            print("No Liabilities")
        else:
            print(f"\nLiabilities:\n{self.liab}")
            print(f"Total Liabilities: {self.tot_liab}")
        # net worth
        print(f"\nNet worth: {self.net_worth}")
