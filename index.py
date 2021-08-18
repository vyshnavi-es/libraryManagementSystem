from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb

from PyQt5.uic import  loadUiType

ui,_=loadUiType('library.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_changes()
        self.handle_buttons()

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()
        
    def show_themes(self):
        self.groupBox_3.show()
    
    def hiding_themes(self):
        self.groupBox_3.hide()
    
    def handle_ui_changes(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.show_themes)
        self.pushButton.clicked.connect(self.open_today_tab)
        self.pushButton_2.clicked.connect(self.open_books_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)
        self.pushButton_15.clicked.connect(self.hiding_themes)
        self.pushButton_7.clicked.connect(self.add_new_book)

        self.pushButton_8.clicked.connect(self.add_category)
        self.pushButton_9.clicked.connect(self.add_author)
        self.pushButton_10.clicked.connect(self.add_publisher)

        self.pushButton_26.clicked.connect(self.search_book)
        self.pushButton_23.clicked.connect(self.edit_book)
        self.pushButton_27.clicked.connect(self.delete_book)

        self.pushButton_31.clicked.connect(self.add_new_user)
        self.pushButton_33.clicked.connect(self.login)
        self.pushButton_34.clicked.connect(self.edit_user)

    """ opening tabs"""

    def open_today_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)
    
    """ books """

    def add_new_book(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()
        
        book_title=self.lineEdit_3.text()
        book_desc=self.textEdit.toPlainText()
        book_code=self.lineEdit_5.text()
        book_price=self.lineEdit_4.text()
        book_category=self.comboBox_2.currentIndex()
        book_author=self.comboBox_5.currentIndex()
        book_publisher=self.comboBox_6.currentIndex()


        self.cur.execute('''
            INSERT INTO book (book_name,book_desc,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_title, book_desc, book_code, book_category, book_author, book_publisher, book_price))
        
        self.db.commit()
        self.statusBar().showMessage("New Book Added")

        self.lineEdit_3.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_5.setText('')
        self.lineEdit_4.setText('')
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)

    def search_book(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()

        book_title=self.lineEdit_75.text()

        sql=''' SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql , [(book_title)])

        data = self.cur.fetchone()
        
        print(data)
        self.lineEdit_67.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_69.setText(data[3])
        self.comboBox_52.setCurrentIndex(data[4])
        self.comboBox_53.setCurrentIndex(data[5])
        self.comboBox_54.setCurrentIndex(data[6])
        self.lineEdit_68.setText(str(data[7]))


    def delete_book(self):
       self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
       self.cur=self.db.cursor()

       book_title=self.lineEdit_75.text()

       warning=QMessageBox.warning(self, 'Delete Book', "Are you sure you wanna delete this book?", QMessageBox.Yes|QMessageBox.No)
       if warning == QMessageBox.Yes:
           sql=''' DELETE FROM book WHERE book_name=%s'''
           self.cur.execute(sql , [(book_title)])
           self.db.commit()
           self.statusBar().showMessage("Book Deleted")


    def edit_book(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()

        book_title=self.lineEdit_67.text()
        book_desc=self.textEdit_2.toPlainText()
        book_code=self.lineEdit_69.text()
        book_price=self.lineEdit_68.text()
        book_category=self.comboBox_52.currentIndex()
        book_author=self.comboBox_53.currentIndex()
        book_publisher=self.comboBox_54.currentIndex()

        search_book_title=self.lineEdit_75.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_desc=%s ,book_code=%s ,book_category= %s ,book_author= %s, book_publisher= %s, book_price= %s WHERE book_name=%s
        ''', (book_title, book_desc, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.db.commit()
        self.statusBar().showMessage("Book Updated")

    """users"""

    def add_new_user(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()
        
        username=self.lineEdit_2.text()
        email=self.lineEdit_80.text()
        password=self.lineEdit_81.text()
        password_again=self.lineEdit_81.text()

        if password == password_again :
            self.cur.execute('''
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (%s,%s,%s)
            ''',(username,email,password))

            self.db.commit()
            self.statusBar().showMessage('New User Added.')

        else:
            self.label_13.setText("please enter a valid password twice.")

    def login(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()

        username = self.lineEdit_88.text()
        password = self.lineEdit_87.text()

        sql = '''SELECT * FROM users'''

        self.cur.execute(sql)
        data=self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print("user match")
                self.statusBar().showMessage("Valid Username And Password")
                self.groupBox_4.setEnabled(True)

                self.lineEdit_92.setText(row[1])
                self.lineEdit_93.setText(row[2])
                self.lineEdit_94.setText(row[3])




    def edit_user(self):

        username=self.lineEdit_92.text()
        email=self.lineEdit_93.text()
        password=self.lineEdit_94.text()
        password_again=self.lineEdit_89.text()

        original_name=self.lineEdit_88.text()

        if password == password_again:
            self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
            self.cur=self.db.cursor()

            self.cur.execute('''
            UPDATE users SET user_name= %s, user_email=%s ,user_password = %s WHERE user_name =%s
            ''',(username , email , password, original_name ))


            self.db.commit()
            self.statusBar().showMessage("user data updated successfully")
        else:
            print("make sure you enterted password correctly.")
    """ settings """

    def add_category(self):
        self.db = MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur = self.db.cursor()
        
        category_name = self.lineEdit_6.text()
        print(category_name)
        self.cur.execute('''insert into category (category_name) values (%s)''',[category_name])
        self.db.commit()
        self.statusBar().showMessage("New Category Added")
        self.lineEdit_6.setText('')

        self.show_category()
        self.show_category_combobox()



    def show_category(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()
        
        self.cur.execute('''SELECT category_name FROM category''')
        data=self.cur.fetchall()
        

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column,item in enumerate(form):
                     self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(item)))
                     column+=1
                    

                row_position=self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

        
    def add_author(self):
        self.db = MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur = self.db.cursor()
        
        author_name = self.lineEdit_7.text()
        self.cur.execute('''INSERT INTO authors(author_name) VALUES (%s)''',(author_name,))
        self.db.commit()
        self.statusBar().showMessage("New Author Added")
        self.lineEdit_7.setText('')

        self.show_author()
        self.show_author_combobox()

    def show_author(self):
        self.db = MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        author_data=self.cur.fetchall()
        

        if author_data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(author_data):
                for column,item in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
                    column+=1


                row_position=self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
    



        
     
    def add_publisher(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()
        
        publisher_name=self.lineEdit_8.text()
        self.cur.execute('''INSERT INTO publisher(publisher_name) VALUES (%s)''',(publisher_name,))
        self.db.commit()
        self.statusBar().showMessage("New Publisher Added")
        self.lineEdit_8.setText('')

        self.show_publisher()
        self.show_publisher_combobox()
    



    def show_publisher(self):
       self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
       self.cur=self.db.cursor()

       self.cur.execute(''' SELECT publisher_name FROM publisher ''')
       publisher_data=self.cur.fetchall()


       if(publisher_data):
           self.tableWidget_4.setRowCount(0)
           self.tableWidget_4.insertRow(0)
           for row, form in enumerate(publisher_data):
               for column, item in enumerate(form):
                   self.tableWidget_4.setItem(row,column,QTableWidgetItem(str(item)))
                   column+=1

               row_position=self.tableWidget_4.rowCount()
               self.tableWidget_4.insertRow(row_position)


    """ show settings in UI"""
    def show_category_combobox(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()
        
        self.cur.execute('''SELECT category_name FROM category''')
        data=self.cur.fetchall()

        self.comboBox_2.clear()

        for category in data:
            self.comboBox_2.addItem(category[0])
            self.comboBox_52.addItem(category[0])



    def show_author_combobox(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        author_data=self.cur.fetchall()

        self.comboBox_5.clear()

        for author in author_data:
            self.comboBox_5.addItem(author[0])
            self.comboBox_53.addItem(author[0])
        


    def show_publisher_combobox(self):
        self.db=MySQLdb.connect(host='localhost' ,user='root' , password='vyshnavies_13' ,db ='library')
        self.cur=self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        publisher_data=self.cur.fetchall()

        self.comboBox_6.clear()

        for publisher in publisher_data:
            self.comboBox_6.addItem(publisher[0])
            self.comboBox_54.addItem(publisher[0])



def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()