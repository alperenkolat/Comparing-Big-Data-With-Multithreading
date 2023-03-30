
from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit,QCheckBox
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem,QDialog
from PyQt5.QtCore import QDate,QDateTime,Qt,QSortFilterProxyModel
from PyQt5 import QtGui,QtCore,QtWidgets
import sys
import multiprocessing,threading
import psutil
import Similarity_calculator1 as Similarity_calculator
required_col=["Product","Issue","Company","State","ZIP code","Complaint ID"]
import numpy as np
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yazlab1.2")
        self.create_menu()
        self.setMinimumSize(1350,750)
        self.open=Window()
        self.setCentralWidget(self.open) 
        self.show()


    def create_menu(self):
        menubar = self.menuBar()
        
        user_interface = menubar.addMenu("Sorgu")
        query_screen = QAction("Sorgu",self)
        user_interface.addAction(query_screen)
        user_interface.triggered.connect(self.response)



    def response(self,action):
        if action.text() == "Sorgu":
            tabtitle = action.text()
            self.open.new_tab(user_interface(),tabtitle)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tabwidget=QTabWidget()
        self.tabwidget.addTab(user_interface(),"Sorgu")
        self.tabwidget.setTabsClosable(True)
        h_box=QHBoxLayout()
        h_box.addWidget(self.tabwidget)
        self.setLayout(h_box)
        self.tabwidget.tabCloseRequested.connect(self.close_function)
        self.show()

    def close_function(self,index):
        self.tabwidget.removeTab(index)

    def new_tab(self,w_name,tabtitle):
        self.tabwidget.addTab(w_name,tabtitle)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class user_interface(QWidget):
    def __init__(self):
        super().__init__()
        f_box = QFormLayout()
        h_box = QHBoxLayout()
        h_box2 = QHBoxLayout()
        h_box3 = QHBoxLayout()



        self.table = QtWidgets.QTableView()
        # self.table1 = QtWidgets.QTableView()
        # self.table2 = QtWidgets.QTableView()
        self.filter_label = QLabel(" Filtre: ")

        self.filter_product = QCheckBox("Product")
        self.filter_issue = QCheckBox("Issue")
        self.filter_company = QCheckBox("Company")
        self.filter_state = QCheckBox("State")
        self.filter_zip_code = QCheckBox("ZIP Code")
        self.filter_complaint_id = QCheckBox("Complaint ID")



        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # self.table1.horizontalHeader().setStretchLastSection(True) 
        # self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table2.horizontalHeader().setStretchLastSection(True) 
        # self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        raw_data=pd.read_csv(r"out.csv")


        self.columns = QComboBox(self)
        for i in required_col:
            self.columns.addItem(i)

        
        self.same_columns = QComboBox(self)
        self.same_columns.addItem("None")
        for i in required_col:
            self.same_columns.addItem(i)
        

        
        self.model = TableModel(raw_data)

        self.table.setModel(self.model)


        self.thread_amount = QLabel(" Thread Sayısı ")
        self.thread_amount_i = QLineEdit()
        
        
        self.similarity_ratio = QLabel("Benzerlik Oranı ")
        self.similarity_ratio_i = QLineEdit()
      

        self.data_1 = QLabel(" Aranacak Sorgu ")
        self.data_1_i = QLineEdit()


        self.search_button = QPushButton("Ara")

        self.product = QCheckBox("Product")
        self.issue = QCheckBox("Issue")
        self.company = QCheckBox("Company")
        self.state = QCheckBox("State")
        self.zip_code = QCheckBox("ZIP Code")
        self.complaint_id = QCheckBox("Complaint ID")


        h_box3.addWidget(self.filter_product)
        h_box3.addWidget(self.filter_issue)
        h_box3.addWidget(self.filter_company)
        h_box3.addWidget(self.filter_state)
        h_box3.addWidget(self.filter_zip_code)
        h_box3.addWidget(self.filter_complaint_id)
        h_box3.addWidget(self.same_columns)


        h_box2.addWidget(self.product)
        h_box2.addWidget(self.issue)
        h_box2.addWidget(self.company)
        h_box2.addWidget(self.state)
        h_box2.addWidget(self.zip_code)
        h_box2.addWidget(self.complaint_id)
        h_box2.addWidget(self.columns)
        h_box2.addWidget(self.data_1)
        h_box2.addWidget(self.data_1_i)

        #h_box2.addStretch(2)

        h_box.addWidget(self.similarity_ratio)
        h_box.addWidget(self.similarity_ratio_i)
        h_box.addWidget(self.thread_amount)
        h_box.addWidget(self.thread_amount_i)


 

        self.search_button.clicked.connect(self.search) 
        h_box.addWidget(self.search_button)
        f_box.addItem(h_box3)
        f_box.addWidget(self.table)
        f_box.addItem(h_box2)
        f_box.addItem(h_box)
        self.setLayout(f_box)


    def search(self):
        try:
            self.msgbox = QMessageBox()
            self.msgbox.setIcon(QMessageBox.Information)
            self.msgbox.setEnabled(False)
                
            self.msgbox.setWindowTitle("Arama Başlatıldı")
            self.msgbox.setText("Hesaplama bittiğinde otomatik kapanacaktır.")
        
            self.table1 = QtWidgets.QTableView()
            self.table2 = QtWidgets.QTableView()
            self.table1.horizontalHeader().setStretchLastSection(True) 
            self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table2.horizontalHeader().setStretchLastSection(True) 
            self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            f = open("time.txt", "w")
            f.close()

            f = open("demofile2.csv", "w")
            f.close()

            thread_amount = self.thread_amount_i.text()
            similarity_ratio= self.similarity_ratio_i.text()
            filter_colon_number= [None,None,None,None,None,None]
            column_to_compare = -1
            specific_filter = self.data_1_i.text()
            same_column = self.same_columns.currentIndex()
            
            specific_filter_column=self.columns.currentIndex()
            self.new_window= SubWindow()
            self.new_window_csv= SubWindow_csv()
            f_box = QFormLayout()
            h_box = QHBoxLayout()

        
            #Gösterilecek kolon
            if(self.filter_product.isChecked()):
                filter_colon_number[0] = True
            if(self.filter_issue.isChecked()):
                filter_colon_number[1] =True
            if(self.filter_company.isChecked()):
                filter_colon_number [2]= True
            if(self.filter_state.isChecked()):
                filter_colon_number [3]= True
            if(self.filter_zip_code.isChecked()):
                filter_colon_number [4]= True
            if(self.filter_complaint_id.isChecked()):
                filter_colon_number [5]= True
            
            #Kolon tespiti
            if(self.product.isChecked()):
                column_to_compare = 0
            elif(self.issue.isChecked()):
                column_to_compare = 1
            elif(self.company.isChecked()):
                column_to_compare = 2
            elif(self.state.isChecked()):
                column_to_compare = 3
            elif(self.zip_code.isChecked()):
                column_to_compare = 4
            elif(self.complaint_id.isChecked()):
                column_to_compare = 5

            #3. senaryo
            if(len(specific_filter) != 0):
                
                self.msgbox.show()
                print(thread_amount,similarity_ratio,column_to_compare,filter_colon_number,specific_filter_column,specific_filter)
                Similarity_calculator.man2(int(thread_amount),int(similarity_ratio),int(column_to_compare),filter_colon_number,int(specific_filter_column),specific_filter)

            
            #2. senaryo
            elif(same_column != 0):

                self.msgbox.show()
                print(thread_amount,similarity_ratio,column_to_compare,filter_colon_number,same_column)
                Similarity_calculator.man3(int(thread_amount),int(similarity_ratio),int(column_to_compare),filter_colon_number,int(same_column)-1)
   
            
            #1 ve 4
            else:
        
                self.msgbox.show()
                print(thread_amount,similarity_ratio,column_to_compare,filter_colon_number)
                Similarity_calculator.man(int(thread_amount),int(similarity_ratio),int(column_to_compare),filter_colon_number)
            self.msgbox.close()
          
            data_time=Similarity_calculator.timer()

            self.model2 = TableModel(data_time)
            self.table2.setModel(self.model2)
            f_box.addWidget(self.table2)
    

            self.new_window.setLayout(f_box)
            self.new_window.show()

        


            self.new_window_csv= SubWindow_csv()
            f_box1= QFormLayout()
            print("***")
            f = open("demofile2.csv", "r")
            size_col=f.readline().count(",")+1
            f.close()
            list_col=[0,1,2,3,4,5,6,7,8,9,10,11,12]
            print(list_col[:size_col])
            raw_data1=pd.read_csv(r"demofile2.csv",usecols=list_col[:size_col],encoding="utf-8")
            print("***")
            self.model1 = TableModel(raw_data1)
            self.table1.setModel(self.model1)
            f_box1.addWidget(self.table1)
            self.new_window_csv.setLayout(f_box1)
            self.new_window_csv.show()
            

        except ValueError:

            QMessageBox.about(self,"Thread Sayısı Hatalı","Lütfen çalışacak thread sayısını giriniz.")






class SubWindow(QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Thread Manager")
        self.setMinimumSize(1280, 720)


class SubWindow_csv(QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Result")
        self.setMinimumSize(1280, 720)

def start_app():
    app = QApplication(sys.argv)

    Win = MainWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':

  if multiprocessing.current_process().name=='MainProcess':
    start_app()
