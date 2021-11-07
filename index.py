from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import MySQLdb
import datetime
from datetime import date
from xlsxwriter import *

# -------- Rules ^_^ ----------
# If I Want To Make The Settings Tab Is First Tab Appear When Open Program ===> Put It In Constructor as self.Open_Settings_Tab() , Justt
# Line Edit Take String Data Type Justt,, So Convert The Values To String When setText()

MainUI, _ = loadUiType('main.ui')
import sys


class Main(QMainWindow, MainUI):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.Db_Connect()
        self.Handle_Buttons()
        self.Show_All_Categories()
        self.Show_Branches()
        self.Show_Publisheres()
        self.Show_Authores()
        self.Show_Employee()

        self.Show_aLL_Books()
        self.Show_aLL_Clients()

        self.Show_Daily_Movements()
        # self.Show_All_History()

    def UI_Changes(self):  # UI Changes in Login
        self.tabWidget.tabBar().setVisible(
            False)  # To Make The external Bar Is Hidden,, tabWidget: Basic Tab, tabBar:Bar Which Contain external Tabs

    def Db_Connect(self):  ## Connection between app & DB
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library_')
        self.cur = self.db.cursor()  # As like a means of transport as Query & Database
        print("Connection Accepted ^_^")

    def Handle_Buttons(self):  # Handle Buttons In Our App
        self.pushButton.clicked.connect(self.Open_Daily_Movement_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_4.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_3.clicked.connect(self.Open_Dashboard_Tab)
        self.pushButton_7.clicked.connect(self.Open_History_Tab)
        self.pushButton_5.clicked.connect(self.Open_Reports_Tab)
        self.pushButton_6.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_8.clicked.connect(self.Handle_To_Day_Work)
        self.pushButton_20.clicked.connect(self.Add_Branch)
        self.pushButton_22.clicked.connect(self.Add_Publisher)
        self.pushButton_21.clicked.connect(self.Add_Author)
        self.pushButton_23.clicked.connect(self.Add_Category)

        self.pushButton_27.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_9.clicked.connect(self.Add_New_Client)

        self.pushButton_12.clicked.connect(self.Edit_Book_Search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_16.clicked.connect(self.Edit_Client_Search)
        self.pushButton_17.clicked.connect(self.Edit_Client)

        self.pushButton_13.clicked.connect(self.Delete_Book)
        self.pushButton_18.clicked.connect(self.Delete_Client)

        self.pushButton_14.clicked.connect(self.All_Books_Filter)
        self.pushButton_48.clicked.connect(self.Show_aLL_Books)

        self.pushButton_29.clicked.connect(self.Check_Employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_31.clicked.connect(self.Add_Employee_Permissions)

        self.pushButton_34.clicked.connect(self.Book_Export_Reports)
        self.pushButton_37.clicked.connect(self.Client_Export_Reports)

        self.pushButton_39.clicked.connect(self.User_Login_Permissions)

        self.pushButton_30.clicked.connect(self.Search_Employee)

    def User_Login_Permissions(self):
        username = self.lineEdit_50.text()
        password = self.lineEdit_52.text()
        # ********************** To Add Action To Login ************************
        query = '''SELECT id FROM employee WHERE id = %s'''
        self.cur.execute(query, [(username)])
        data = self.cur.fetchone()
        print("**** id_employee **** ", data[0])
        global employee_id
        employee_id = data[0]
        action = 1
        date = datetime.datetime.now()

        self.cur.execute('''
                INSERT INTO history(employee_id, action, date)
                VALUES (%s, %s, %s)''', (employee_id, action, date))

        self.db.commit()
        # *************************************************************************

        self.cur.execute('''SELECT name, password FROM employee''')
        data = self.cur.fetchall()
        print(data)
        for row in data:
            # print(row)
            if row[0] == username and row[1] == password:
                self.groupBox_14.setEnabled(True)
                self.pushButton.setEnabled(True)
                # ---------- first :Load User Permissions (Return The Permissions For User)
                self.cur.execute('''SELECT * FROM employee_permissions WHERE employee_id = %s''', (username,))
                user_permissions = self.cur.fetchone()
                print(user_permissions)

                self.pushButton_2.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.pushButton_6.setEnabled(True)

                if user_permissions[2] == 1:  # dashboard_tab
                    self.pushButton_3.setEnabled(True)
                if user_permissions[3] == 1:  # history_tab
                    self.pushButton_7.setEnabled(True)
                if user_permissions[4] == 1:  # reports_tab
                    self.pushButton_5.setEnabled(True)

                if user_permissions[5] == 1:  # add_book
                    self.pushButton_10.setEnabled(True)
                if user_permissions[6] == 1:  # edit_book
                    self.pushButton_11.setEnabled(True)
                if user_permissions[7] == 1:  # delete_book
                    self.pushButton_13.setEnabled(True)
                if user_permissions[8] == 1:  # import_book
                    self.pushButton_35.setEnabled(True)
                if user_permissions[9] == 1:  # export_book
                    self.pushButton_34.setEnabled(True)

                if user_permissions[10] == 1:  # add_client
                    self.pushButton_9.setEnabled(True)
                if user_permissions[11] == 1:  # edit_client
                    self.pushButton_17.setEnabled(True)
                if user_permissions[12] == 1:  # delete_client
                    self.pushButton_18.setEnabled(True)
                if user_permissions[13] == 1:  # import_client
                    self.pushButton_36.setEnabled(True)
                if user_permissions[14] == 1:  # export_client
                    self.pushButton_37.setEnabled(True)

                if user_permissions[15] == 1:  # add_branch
                    self.pushButton_20.setEnabled(True)
                if user_permissions[16] == 1:  # add_publisher
                    self.pushButton_22.setEnabled(True)
                if user_permissions[17] == 1:  # add_author
                    self.pushButton_21.setEnabled(True)
                if user_permissions[18] == 1:  # add_category
                    self.pushButton_23.setEnabled(True)
                if user_permissions[19] == 1:  # add_employee
                    self.pushButton_27.setEnabled(True)
                if user_permissions[20] == 1:  # edit_employee
                    self.pushButton_28.setEnabled(True)
                if user_permissions[21] == 1:  # is_admin
                    self.checkBox_23.setEnabled(True)

    def Handle_Login(self):  # Handle With Login Tap
        pass

    def Reset_Passwords(self):  # Handle With Reset Passwords
        pass

    def Handle_To_Day_Work(self):  # Handle Day To Day Operations
        book_title = self.lineEdit.text()  # To Get book_id to Store it In DB From book_title,, To Get The book_title TO Show It I

        sql = '''SELECT id FROM books WHERE title = %s'''
        self.cur.execute(sql, [(book_title)])
        book_id = self.cur.fetchone()[0]
        print("book_id: ", book_id)

        client_national_id = self.lineEdit_4.text()  # To Get Client_id to Store it In DB From Nationa_id,, To Get The Client name TO Show It In Program From National_id
        sql = '''SELECT id FROM clients WHERE national_id = %s'''
        self.cur.execute(sql, [(client_national_id)])
        client_id = self.cur.fetchone()[0]
        print("book_id: ", client_id)

        from_date = str(date.today())
        to_date = self.dateEdit_6.date()
        # to_date_year = self.dateEdit_6.date().year()
        # to_date_month = self.dateEdit_6.date().month()
        # to_date_day = self.dateEdit_6.date().day()
        # print("Year :", to_date_year)
        # print("month :", to_date_month)
        # print("Day :", to_date_day)
        date_ = datetime.datetime.now()
        type = self.comboBox.currentIndex()
        branch = 2
        employee_id = 1

        self.cur.execute('''INSERT INTO daily_movements(book_id, client_id, type, date, branch_id, book_from,
        book_to, employee_id )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (book_id, client_id, type, date_, branch, from_date,
                                                     to_date, employee_id))

        self.db.commit()
        print("Done")
        self.statusBar().showMessage("Action Added successfully")
        self.Show_Daily_Movements()

    def Show_Daily_Movements(self):  # To Retreive The Data For Daily Movements In tableWidget
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.cur.execute('''SELECT book_id, type, client_id, book_from, book_to FROM daily_movements''')
        data = self.cur.fetchall()
        print("Show_Daily_Movements: ", data)
        print("book_id: ", data[0][0])
        print("client_id: ", data[0][2])

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT title FROM books WHERE id = %s'''
                    self.cur.execute(sql, [(data[row][0])])
                    book_title = self.cur.fetchone()
                    print("book_title: ", book_title)
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(book_title[0])))
                elif col == 1:
                    if item == 0:
                        self.tableWidget.setItem(row, col, QTableWidgetItem(str("Rent")))
                    else:
                        self.tableWidget.setItem(row, col, QTableWidgetItem(str("Retrieve")))

                elif col == 2:
                    sql = '''SELECT name FROM clients WHERE id = %s'''
                    self.cur.execute(sql, [(data[row][2])])
                    client_name = self.cur.fetchone()
                    print("client_name: ", client_name)
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(client_name[0])))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    # ============= Books Operations ============

    def Show_aLL_Books(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)  # Specific The Number of Row Which I Want Tto Add Data
        self.cur.execute(
            '''SELECT code, title, category_id, author_id, price FROM books''')  # Specific The Data Which I Want In Table
        data = self.cur.fetchall()
        # print(books)

        # enumerate() : Make Loop On Items With Know Number Of Current Loop
        # row : Number Of Loop (Iteration)
        # form : Item (Data)
        # setItem(x, y, PlaceAdded)
        # QTableWidgetItem() : To add Item To TableWidget
        for row, form in enumerate(data):  # Loop On Rows
            for col, item in enumerate(form):  # Loop On Columns
                if col == 2:
                    sql = '''SELECT category_name FROM category WHERE id=%s'''  #
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))
                    print("category_name:  ", category_name[0])
                elif col == 3:
                    sql = '''SELECT Name FROM author WHERE id=%s'''
                    self.cur.execute(sql, [(item)])
                    author_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                    print("author_name:  ", author_name[0])
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1  # To Pass On Next Column
            row_position = self.tableWidget_2.rowCount()  # To Know The Number of Last Row
            self.tableWidget_2.insertRow(row_position)  # To add New Row After Last Row

    def All_Books_Filter(self):
        book_title = self.lineEdit_14.text()
        category = self.comboBox_11.currentIndex()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        sql = '''SELECT code, title, category_id, author_id, price FROM books WHERE title = %s '''
        self.cur.execute(sql, [(book_title)])
        data = self.cur.fetchall()
        # print(data)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_2.rowCount()  # To Know The Number of Last Row
            self.tableWidget_2.insertRow(row_position)  # To add New Row After Last Row

    # --------------------------------------------------------
    def Add_New_Book(self):
        book_title = self.lineEdit_3.text()
        description = self.textEdit.toPlainText()
        category = self.comboBox_3.currentIndex()
        price = self.lineEdit_5.text()
        code = self.lineEdit_6.text()
        barcode = self.lineEdit_54.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        status = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_7.text()
        date = datetime.datetime.now()  # #  #

        self.cur.execute('''INSERT INTO books (title, description, code, category_id, barcode, part_order, price, 
        publisher_id , author_id, status, date)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                         (
                             book_title, description, code,
                             category, barcode, part_order,
                             price, publisher, author,
                             status, date))

        self.db.commit()
        self.Show_aLL_Books()
        # print("Book Added ^_^")
        self.statusBar().showMessage("Book Added successfully")

        self.lineEdit_3.setText("")
        self.textEdit.setPlainText("")
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_54.setText("")
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.lineEdit_7.setText("")


    # -------------------------------------------------------------------------------------------------------------------

    def Edit_Book_Search(self):
        code_book = self.lineEdit_12.text()
        sql = '''SELECT * FROM books WHERE code = %s'''
        self.cur.execute(sql, [(
            code_book)])  # Mean: Get The Information(Which Return it from sql) Which Special The Book Which Have This Code (code_book)
        # data = self.cur.fetchall()[0]  # Variable Which Contain Information
        data = self.cur.fetchone()
        # print(data)
        self.lineEdit_11.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.comboBox_10.setCurrentIndex(data[3])
        self.lineEdit_10.setText(str(data[7]))
        self.comboBox_7.setCurrentIndex(data[8])
        self.comboBox_9.setCurrentIndex(data[9])
        self.comboBox_8.setCurrentIndex(int(data[11]))
        self.lineEdit_13.setText(str(data[6]))

        # -------- My Way -_- ^_^----------
        # self.cur.execute('''SELECT code, title, description, category_id, publisher_id, author_id, status, part_order, price FROM books''')
        '''books = self.cur.fetchall()
        for book in books:
            print(book[0])
        for book in books:
            if book[0] == code_book:
                self.lineEdit_11.setText(book[1])  # Title
                self.textEdit_2.setPlainText(book[2])  # description
                self.comboBox_10.setCurrentText(str(book[3]))  # category
                self.lineEdit_9.setText(str(book[0]))  # Code
                self.lineEdit_10.setText(str(book[8]))  # price
                self.comboBox_7.setCurrentText(str(book[4]))  # publisher
                self.comboBox_9.setCurrentText(str(book[5]))  # author
                self.comboBox_8.setCurrentText(str(book[6]))  # status
                self.lineEdit_13.setText(str(book[7]))  # part_order'''

    def Edit_Book(self):
        ## Notice : Not Make Edit On Barcde Because Sercuity

        book_title = self.lineEdit_11.text()
        book_description = self.textEdit_2.toPlainText()
        book_category = self.comboBox_10.currentIndex()
        book_price = self.lineEdit_10.text()
        book_code = self.lineEdit_12.text()
        book_publisher = self.comboBox_7.currentIndex()
        book_author = self.comboBox_9.currentIndex()
        book_status = self.comboBox_8.currentIndex()
        book_part_order = self.lineEdit_13.text()

        self.cur.execute('''UPDATE books SET title=%s, description=%s, category_id=%s, price=%s, publisher_id=%s, 
        author_id=%s, status=%s, part_order= %s WHERE code = %s''', (book_title, book_description, book_category,
                                                                     book_price, book_publisher, book_author,
                                                                     book_status, book_part_order, book_code))

        self.db.commit()
        print("Done Update ^_*")
        self.statusBar().showMessage("The book information has been modified successfully")

        self.lineEdit_11.setText("")
        self.textEdit_2.setPlainText("")
        self.comboBox_10.setCurrentIndex(0)
        self.lineEdit_10.setText("")
        self.lineEdit_12.setText("")
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_9.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.lineEdit_13.setText("")

        self.Show_aLL_Books()

    def Delete_Book(self):  # Delete Book From DB

        book_code = self.lineEdit_12.text()
        warning_message = QMessageBox.warning(self, "Delete Book", "Are you sure you want to delete this Book ?!",
                                              QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            sql = '''DELETE FROM books WHERE code = %s'''
            self.cur.execute(sql, [(book_code)])

            self.db.commit()
            self.statusBar().showMessage("Book Removed successfully")
            self.Show_aLL_Books()

            self.lineEdit_11.setText("")
            self.textEdit_2.setPlainText("")
            self.comboBox_10.setCurrentIndex(0)
            self.lineEdit_10.setText("")
            self.lineEdit_12.setText("")
            self.comboBox_7.setCurrentIndex(0)
            self.comboBox_9.setCurrentIndex(0)
            self.comboBox_8.setCurrentIndex(0)
            self.lineEdit_13.setText("")

    # ============= Clients Operations ==============

    def Show_aLL_Clients(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        self.cur.execute('''SELECT name, email, phone, national_id, date FROM clients''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

    def Add_New_Client(self):
        Client_Name = self.lineEdit_2.text()
        client_Email = self.lineEdit_16.text()
        client_Phone = self.lineEdit_18.text()
        client_National_id = self.lineEdit_19.text()
        date = datetime.datetime.now()

        self.cur.execute('''INSERT INTO clients(name, email , phone, date, national_id)
                            VALUES(%s, %s, %s, %s, %s)''',
                         (Client_Name, client_Email, client_Phone, date, client_National_id))
        self.db.commit()
        print("Client Added ^_^")
        self.statusBar().showMessage("Client Added successfully")
        self.Show_aLL_Clients()

        self.lineEdit_2.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")

    def Edit_Client_Search(self):
        data_search = self.lineEdit_17.text()

        if self.comboBox_12.currentIndex() == 0:
            sql = '''SELECT name,email,phone,national_id FROM clients WHERE name = %s'''
            self.cur.execute(sql, [(data_search)])
            data = self.cur.fetchone()
            print("for name: ", data)

        if self.comboBox_12.currentIndex() == 1:
            sql = '''SELECT name,email,phone,national_id FROM clients WHERE email = %s'''
            self.cur.execute(sql, [(data_search)])
            data = self.cur.fetchone()
            print("for email: ", data)

        if self.comboBox_12.currentIndex() == 2:
            sql = '''SELECT name,email,phone,national_id FROM clients WHERE phone = %s'''
            self.cur.execute(sql, [(data_search)])
            data = self.cur.fetchone()
            print("for phone: ", data)

        if self.comboBox_12.currentIndex() == 3:
            sql = '''SELECT name,email,phone,national_id FROM clients WHERE national_id = %s'''
            self.cur.execute(sql, [(data_search)])
            data = self.cur.fetchone()
            print("for national_id: ", data)

        self.lineEdit_20.setText(str(data[0]))  # client name
        self.lineEdit_23.setText(str(data[1]))  # client email
        self.lineEdit_21.setText(str(data[2]))  # client phone
        self.lineEdit_22.setText(str(data[3]))  # client_national_id

    def Edit_Client(self):
        original = self.lineEdit_17.text()
        type_filter = self.comboBox_12.currentIndex()
        client_name = self.lineEdit_20.text()
        client_email = self.lineEdit_23.text()
        client_phone = self.lineEdit_21.text()
        client_Id = self.lineEdit_22.text()

        if type_filter == 0:
            self.cur.execute('''UPDATE clients SET name=%s, email=%s, phone=%s, national_id=%s WHERE name = %s''',
                             (client_name, client_email, client_phone, client_Id, original))
        if type_filter == 1:
            self.cur.execute('''UPDATE clients SET name=%s, email=%s, phone=%s, national_id=%s WHERE email = %s''',
                             (client_name, client_email, client_phone, client_Id, original))
        if type_filter == 2:
            self.cur.execute('''UPDATE clients SET name=%s, email=%s, phone=%s, national_id=%s WHERE phone = %s''',
                             (client_name, client_email, client_phone, client_Id, original))
        if type_filter == 3:
            self.cur.execute(
                '''UPDATE clients SET name=%s, email=%s, phone=%s, national_id=%s WHERE national_id = %s''',
                (client_name, client_email, client_phone, client_Id, original))

        self.db.commit()
        self.statusBar().showMessage("The Client information has been modified successfully")
        self.Show_aLL_Clients()

        self.lineEdit_17.setText("")
        self.comboBox_12.setCurrentIndex(0)
        self.lineEdit_20.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")

    def Delete_Client(self):  # Delete Client From DB
        client_name = self.lineEdit_17.text()
        warning_message = QMessageBox.warning(self, "Delete Client", "Are you sure you want to delete this client ?!",
                                              QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            type_filter = self.comboBox_12.currentIndex()
            if type_filter == 0:
                sql = '''DELETE FROM clients WHERE name = %s'''
            if type_filter == 1:
                sql = '''DELETE FROM clients WHERE email = %s'''
            if type_filter == 2:
                sql = '''DELETE FROM clients WHERE phone = %s'''
            if type_filter == 3:
                sql = '''DELETE FROM clients WHERE national_id = %s'''
            self.cur.execute(sql, [(client_name)])
            self.db.commit()
            self.statusBar().showMessage("Client Removed successfully")
            self.Show_aLL_Clients()

            self.lineEdit_17.setText("")
            self.comboBox_12.setCurrentIndex(0)
            self.lineEdit_20.setText("")
            self.lineEdit_23.setText("")
            self.lineEdit_21.setText("")
            self.lineEdit_22.setText("")

    # ================ History ===================
    def Show_All_History(self):  # Show All History To The Admin
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        self.cur.execute('''SELECT employee_id, action, table, date FROM history''')

        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT name FROM employee WHERE id=%s'''
                    self.cur.execute(sql, [(data[row][0])])
                    employee_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(employee_name[0])))
                if col == 1:
                    action = " "
                    if item == 1:
                        action = "login"
                    if item == 2:
                        action = "logout"
                    if item == 3:
                        action = "Add"
                    if item == 4:
                        action = "Edit"
                    if item == 5:
                        action = "Delete"
                    if item == 6:
                        action = "Search"
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(action)))
                if col == 2:
                    table = " "  #
                    if item == 1:
                        table = "Books"
                    if item == 2:
                        table = "Clients"
                    if item == 3:
                        table = "History"
                    if item == 4:
                        table = "Branch"
                    if item == 5:
                        table = "Category"
                    if item == 6:
                        table = "Daily Movements"
                    if item == 7:
                        table = "Employee"
                    if item == 8:
                        table = "publisher"

                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(table)))
                if col == 4:
                    sql = '''SELECT date FROM history'''  #
                    self.cur.execute(sql, [(data[row][3])])
                    branch_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(branch_name[0])))
                #if col == 4:
                    #sql = '''SELECT name FROM branch WHERE id=%s'''  #
                    #self.cur.execute(sql, [(data[row][3])])
                    #branch_name = self.cur.fetchone()
                    #self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(branch_name[0])))
                col += 1

            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

    # ================ Reports ===================
    # ------- Book Reports Tap-----
    def All_Books_Report(self):
        pass

    def Books_Filter_Report(self):  # Show Report for filtered Books
        pass

    def Book_Export_Reports(self):  # Export Books Data To Exel File
        self.cur.execute(
            '''SELECT code, title, category_id, author_id, price FROM books''')  # Specific The Data Which I Want In Table
        data = self.cur.fetchall()

        excel_file = Workbook("books_report.xlsx")  # Workbook(NameFile)
        sheet1 = excel_file.add_worksheet()  # Create Page In File

        # To Fill in rows and columns (NumberRow, NumberColumn, Information Which Fill it)
        sheet1.write(0, 0, "Book Code")
        sheet1.write(0, 1, "Book Title")
        sheet1.write(0, 2, "Category")
        sheet1.write(0, 3, "Author")
        sheet1.write(0, 4, "Price")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        self.statusBar().showMessage("Report created successfully")

    # ------- Client Reports Tap -----
    def All_Clients_Report(self):
        pass

    def Clients_Filter_Report(self):  # Show Report for filtered Clients
        pass

    def Client_Export_Reports(self):  # Export Clients Data To Exel File
        self.cur.execute('''SELECT name, email, phone, national_id FROM clients''')
        data = self.cur.fetchall()

        excel_file = Workbook("clients_report.xlsx")  # Workbook(NameFile)
        sheet1 = excel_file.add_worksheet()  # Create Page In File

        # To Fill in rows and columns (NumberRow, NumberColumn, Information Which Fill it)
        sheet1.write(0, 0, "Client Name")
        sheet1.write(0, 1, "Client Email")
        sheet1.write(0, 2, "Client Phone")
        sheet1.write(0, 3, "Client National ID")

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        self.statusBar().showMessage("Report created successfully")

    # ------- Monthly Report Tap-----
    def Monthly_Report(self):
        pass

    def Monthly_Report_Export(self):  # Export Monthly Report To Exel File
        pass

    # ================ Settings ===================
    # ------- Add Data Tab -----
    def Add_Branch(self):
        branch_name = self.lineEdit_27.text()
        branch_code = self.lineEdit_28.text()
        branch_location = self.lineEdit_29.text()

        ## self.cur.execute : Mean Execute This Operation On DB
        ## INSERT INTO Name_Table(Names of Columns)
        ## VALUES(Format Types Of Values[ %s, %d, ....etc ])
        ## self.db.commit() : Besaue If Add IN DB ==> Add In Just Ram For Computer System Without DB Itself,, So Use This Statement To Performe Changes From Ram To DB also <== Connection
        self.cur.execute('''
            INSERT INTO branch(name, code, location)  
            VALUES(%s, %s, %s)
                        ''', (branch_name, branch_code, branch_location))
        self.db.commit()
        # QMessageBox.information(self, "Add Finished", "The Branch has been added successfully ^_^")
        self.statusBar().showMessage("The Branch has been added successfully ^_^")

        self.lineEdit_27.setText("")
        self.lineEdit_28.setText("")
        self.lineEdit_29.setText("")

    def Add_Publisher(self):
        publisher_name = self.lineEdit_33.text()
        publisher_location = self.lineEdit_34.text()

        self.cur.execute('''
                    INSERT INTO publisher(name, location)  
                    VALUES(%s, %s)
                                ''', (publisher_name, publisher_location))

        self.db.commit()
        # QMessageBox.information(self, "Add Finished", "The Publisher has been added successfully ^_^")
        self.statusBar().showMessage("The Publisher has been added successfully ^_^")

        self.lineEdit_33.setText("")
        self.lineEdit_34.setText("")

    def Add_Author(self):
        author_name = self.lineEdit_30.text()
        author_location = self.lineEdit_31.text()

        self.cur.execute('''
                            INSERT INTO author(name, location)  
                            VALUES(%s, %s)
                                        ''', (author_name, author_location))

        self.db.commit()
        # QMessageBox.information(self, "Add Finished", "The Author has been added successfully ^_^")
        self.statusBar().showMessage("The Author has been added successfully ^_^")

        self.lineEdit_30.setText("")
        self.lineEdit_31.setText("")

    def Add_Category(self):  # To Add All New Categories In DB
        category_name = self.lineEdit_32.text()
        # parent_category = self.comboBox_13.currentIndex()  # To Select Current Choice(Which I choose It From ComboBbox)
        parent_category_Text = self.comboBox_13.currentText()
        print(parent_category_Text)
        query = '''SELECT id FROM category WHERE category_name = %s'''
        self.cur.execute(query, [(parent_category_Text)])
        # data = self.cur.fetchall()
        data = self.cur.fetchone()
        # print(data)  # Will Print id For Category Which I Choose It
        print(data[0])
        parent_category = data[0]

        self.cur.execute('''
        INSERT INTO category(category_name, parent_category)
        VALUES (%s, %s)''', (category_name,
                             parent_category))  # Put "," After category_name Because The Value Must Be Receive As Tuple Not String

        self.db.commit()

        # self.Show_All_Categories()  # To Add The New Category Directly Without Restart Program
        # QMessageBox.information(self, "Add Finished", "The Category has been added successfully ^_^")
        self.statusBar().showMessage("The Category has been added successfully ^_^")

        self.lineEdit_32.setText("")
        self.comboBox_13.setCurrentIndex(0)

    # ------- Show Data -----
    def Show_All_Categories(
            self):  # To Show All Categories In ComboBox (Which Added In DB) In My Application ,, So We Run This Function In Constructor
        # * : All Items
        # self.cur.execute('''SELECT category_name FROM category''')   # Mean : Recall Just category_name values in the table

        self.comboBox_13.clear()  # To Clear Values In comboBox After Added
        # ======= Ways To Show All Categories IN ComboBox =======
        # ---- Way 1 ----
        self.cur.execute(
            '''SELECT * FROM category''')  # Mean : Recall all values in the table [ Values All Columns(category_name, parent_category) ]

        categories = self.cur.fetchall()
        print(
            categories)  # ((1, , ), (2, , )..etc )  # Will Print All categories In DB [ Because I Recall All Values Not Specific Column Values ] # All Rows In DB as Tuple

        for category in categories:
            print(category[1])
            self.comboBox_13.addItem(category[1])
            self.comboBox_11.addItem(category[1])  # category In "All Books" Tab
            self.comboBox_3.addItem(category[1])  # category In "Add Books" Tab
            self.comboBox_10.addItem(category[1])  # category In "Edit Or Delete Books" Tab

        # ---- Way 2 ----
        # self.cur.execute('''SELECT category_name FROM category''')  # Mean : Recall Just parent_category values in the table
        # category_names = self.cur.fetchall()  # Return Tuple Contain category names
        # for name in category_names:
        # self.comboBox_13.addItem(str(name[0]))  # Because The comboBox_13 Not Take Collection Types Data

    def Show_Branches(self):
        self.cur.execute('''SELECT name FROM branch''')
        branches = self.cur.fetchall()
        # print(branches)
        for branch in branches:
            print(branch[0])
            self.comboBox_22.addItem(branch[0])  # branch in "Add Employee" Tab
            self.comboBox_23.addItem(branch[0])  # branch in "Add Edit Employee Information" Tab
            self.comboBox_16.addItem(branch[0])  # branch in "History" Tab

    def Show_Publisheres(self):
        self.cur.execute('''SELECT name FROM publisher''')
        publisheres = self.cur.fetchall()
        print(publisheres)
        for publishere in publisheres:
            print(publishere[0])
            self.comboBox_4.addItem(publishere[0])
            self.comboBox_7.addItem(publishere[0])

    def Show_Authores(self):
        self.cur.execute('''SELECT name FROM author''')
        authores = self.cur.fetchall()
        # print(authores)
        for author in authores:
            print(author[0])
            self.comboBox_5.addItem(author[0])
            self.comboBox_9.addItem(author[0])

    def Show_Employee(self):
        self.cur.execute('''SELECT name FROM employee''')
        data = self.cur.fetchall()
        for row in data:
            self.comboBox_19.addItem(row[0])

    # ------- Employee Tab -----
    def Add_Employee(self):
        ## --- Get Data From User ---
        employee_name = self.lineEdit_35.text()
        employee_email = self.lineEdit_38.text()
        employee_phone = self.lineEdit_37.text()
        branch = self.comboBox_22.currentIndex()
        national_id = self.lineEdit_36.text()
        date = datetime.datetime.now()
        periority = self.lineEdit_47.text()
        password = self.lineEdit_40.text()
        password2 = self.lineEdit_39.text()

        if password == password2:
            ## --- Add Data To DB ---
            self.cur.execute('''INSERT INTO employee(name, email, phone, national_id, date, periority,password,branch_id)
                                VALUES (%s, %s, %s, %s, %s, %s,%s, %s)
                            ''', (
                employee_name, employee_email, employee_phone, national_id, date, periority, password, branch))
            self.db.commit()
            print("Employee Added ^_^")
            self.statusBar().showMessage("Employee Added ^_^")

            self.lineEdit_35.setText("")
            self.lineEdit_38.setText("")
            self.lineEdit_37.setText("")
            self.comboBox_22.setCurrentIndex(0)
            self.lineEdit_36.setText("")
            self.lineEdit_47.setText("")
            self.lineEdit_40.setText("")
            self.lineEdit_39.setText("")
            self.statusBar().showMessage("The Employee has been added successfully ^_^")
        else:
            print("Wrong Password -_-")

    def Check_Employee(self):
        employee_name = self.lineEdit_41.text()
        employee_password = self.lineEdit_45.text()
        self.cur.execute('''SELECT * FROM employee''')
        data = self.cur.fetchall()
        # print(data)
        for row in data:
            if row[1] == employee_name and row[8] == employee_password:
                # print(row)
                self.groupBox_9.setEnabled(True)
                self.lineEdit_44.setText(row[2])  # email
                self.lineEdit_43.setText(str(row[3]))  # phone
                self.comboBox_23.setCurrentIndex(row[7])  # Branch
                self.lineEdit_42.setText(str(row[5]))  # National_id
                self.lineEdit_48.setText(str(row[6]))  # periority
                self.lineEdit_46.setText(row[8])  # password

    def Edit_Employee_Data(self):
        employee_name = self.lineEdit_41.text()
        password = self.lineEdit_45.text()
        employee_email = self.lineEdit_44.text()
        employee_phone = self.lineEdit_43.text()
        branch = self.comboBox_23.currentIndex()
        national_id = self.lineEdit_42.text()
        periority = self.lineEdit_48.text()
        password2 = self.lineEdit_46.text()

        if password == password2:
            self.cur.execute('''UPDATE employee SET email=%s, phone=%s, national_id=%s, periority=%s, branch_id=%s,
            password=%s WHERE name = %s''',
                             (employee_email, employee_phone, national_id, periority, branch, password2, employee_name))
            self.db.commit()
            self.statusBar().showMessage("The Employee information has been modified successfully")

            self.lineEdit_41.setText("")
            self.lineEdit_45.setText("")
            self.lineEdit_44.setText("")
            self.lineEdit_43.setText("")
            self.lineEdit_48.setText("")
            self.lineEdit_46.setText("")
            self.lineEdit_42.setText("")
            self.comboBox_23.setCurrentIndex(0)

            self.groupBox_9.setEnabled(False)

    def Search_Employee(self):
        employee_name = self.comboBox_19.currentIndex()

        self.cur.execute('''SELECT employee_id FROM employee_permissions''')
        data = self.cur.fetchall()
        print(data)
        try:
            sql = '''SELECT * FROM employee_permissions WHERE employee_id = %s'''
            self.cur.execute(sql, [(employee_name)])
            data = self.cur.fetchone()
            print(data)

            if data[1] == 1:
                self.checkBox_7.setChecked(True)
            if data[2] == 1:
                self.checkBox_10.setChecked(True)
            if data[3] == 1:
                self.checkBox_11.setChecked(True)

            if data[4] == 1:
                self.checkBox.setChecked(True)
            if data[5] == 1:
                self.checkBox_2.setChecked(True)
            if data[6] == 1:
                self.checkBox_4.setChecked(True)
            if data[7] == 1:
                self.checkBox_14.setChecked(True)
            if data[8] == 1:
                self.checkBox_13.setChecked(True)
            if data[9] == 1:
                self.checkBox_6.setChecked(True)
            if data[10] == 1:
                self.checkBox_8.setChecked(True)
            if data[11] == 1:
                self.checkBox_9.setChecked(True)
            if data[12] == 1:
                self.checkBox_15.setChecked(True)
            if data[13] == 1:
                self.checkBox_16.setChecked(True)

            if data[14] == 1:
                self.checkBox_19.setChecked(True)
            if data[15] == 1:
                self.checkBox_18.setChecked(True)
            if data[16] == 1:
                self.checkBox_17.setChecked(True)
            if data[17] == 1:
                self.checkBox_20.setChecked(True)
            if data[18] == 1:
                self.checkBox_21.setChecked(True)
            if data[19] == 1:
                self.checkBox_22.setChecked(True)
        except:
            self.groupBox_10.setEnabled(False)
            self.groupBox_11.setEnabled(False)
            self.groupBox_12.setEnabled(False)
            self.groupBox_13.setEnabled(False)
            warning_message = QMessageBox.warning(self, "warning", "This Employee Hasn't Any Permissions,"
                                                                   "Do you want to add permissions for this employee? ?!",
                                                  QMessageBox.Yes | QMessageBox.No)

            if warning_message == QMessageBox.Yes:
                self.groupBox_10.setEnabled(True)
                self.groupBox_11.setEnabled(True)
                self.groupBox_12.setEnabled(True)
                self.groupBox_13.setEnabled(True)

    # ------- Add User Permissions Tab -----
    def Add_Employee_Permissions(self):
        employee_name = self.comboBox_19.currentIndex()

        if self.checkBox_23.isChecked():
            self.cur.execute('''INSERT INTO employee_permissions (employee_id, books_tab, clients_tab, 
            dashboard_tab, history_tab, reports_tab, settings_tab, add_book, edit_book, delete_book, import_book, 
            export_book, add_client, edit_client, delete_client, import_client, export_client, add_branch, 
            add_publisher, add_author, add_category, add_employee, edit_employee, is_admin) VALUES(%s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
                             , (employee_name, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
            self.db.commit()
            self.statusBar().showMessage("The employee has been set as an admin successfully")
        else:
            dashboard_tab = 0
            history_tab = 0
            reports_tab = 0

            add_book = 0
            edit_book = 0
            delete_book = 0
            import_book = 0
            export_book = 0

            add_client = 0
            edit_client = 0
            delete_client = 0
            import_client = 0
            export_client = 0

            add_branch = 0
            add_publisher = 0
            add_author = 0
            add_category = 0
            add_employee = 0
            edit_employee = 0

            # if [self.checkBox_5.isChecked()] EQUAL [self.checkBox_3.isChecked() == True] ^_*
            if self.checkBox_7.isChecked():
                dashboard_tab = 1
            if self.checkBox_10.isChecked():
                history_tab = 1
            if self.checkBox_11.isChecked():
                reports_tab = 1

            if self.checkBox.isChecked():
                add_book = 1
            if self.checkBox_2.isChecked():
                edit_book = 1
            if self.checkBox_4.isChecked():
                delete_book = 1
            if self.checkBox_14.isChecked():
                import_book = 1
            if self.checkBox_13.isChecked():
                export_book = 1

            if self.checkBox_6.isChecked():
                add_client = 1
            if self.checkBox_8.isChecked():
                edit_client = 1
            if self.checkBox_9.isChecked():
                delete_client = 1
            if self.checkBox_15.isChecked():
                import_client = 1
            if self.checkBox_16.isChecked():
                export_client = 1

            if self.checkBox_19.isChecked():
                add_branch = 1
            if self.checkBox_18.isChecked():
                add_publisher = 1
            if self.checkBox_17.isChecked():
                add_author = 1
            if self.checkBox_20.isChecked():
                add_category = 1
            if self.checkBox_21.isChecked():
                add_employee = 1
            if self.checkBox_22.isChecked():
                edit_employee = 1

            self.cur.execute('''INSERT INTO employee_permissions (employee_id, dashboard_tab,history_tab, reports_tab, 
            add_book, edit_book, delete_book, import_book, export_book, add_client,edit_client, delete_client, 
            import_client, export_client, add_branch, add_publisher, add_author, add_category,add_employee, 
            edit_employee)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                             , (employee_name, dashboard_tab, history_tab,
                                reports_tab, add_book, edit_book, delete_book, import_book,
                                export_book, add_client, edit_client, delete_client, import_client,
                                export_client, add_branch, add_publisher, add_author, add_category,
                                add_employee, edit_employee))
            self.db.commit()
            print("Employee Permissions")
            self.statusBar().showMessage("The Employee Permissions has been modified successfully")

    def Admin_Report(self):
        pass

    # ------- Open Tabs -----
    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)  # Because This Have Index = 0
        print("Login Tab is Opened ^_*")

    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)  # Because This Have Index = 1
        print("Reset Password Tab is Opened ^_*")

    def Open_Daily_Movement_Tab(self):
        self.tabWidget.setCurrentIndex(2)  # Because This Have Index = 2
        print("Daily Movement Tab is Opened ^_^")

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(
            0)  ###!!!!!!!!! Not Work -_- : To Make THe "All Books" Tab Is First To Open When Choose Books Tab
        print("Books Tab is Opened ^_^")

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)
        print("Clients Tab is Opened ^_^")

    def Open_Dashboard_Tab(self):
        self.tabWidget.setCurrentIndex(5)
        print("Dashboard Tab is Opened ^_^")

    def Open_History_Tab(self):
        self.tabWidget.setCurrentIndex(6)
        print("History Tab is Opened ^_^")

    def Open_Reports_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)
        print("Reports Tab is Opened ^_^")

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)
        print("Settings Tab is Opened ^_^")


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
