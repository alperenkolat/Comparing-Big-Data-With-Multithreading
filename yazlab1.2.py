
from PyQt5.QtWidgets import QTabWidget,QWidget,QApplication,QHBoxLayout,QMainWindow,QAction,QFormLayout,QDateEdit,QDateTimeEdit,QHeaderView,QDateTimeEdit,QCheckBox
from PyQt5.QtWidgets import QLabel,QLineEdit,QRadioButton,QPushButton,QMessageBox,QSpinBox,QVBoxLayout,QComboBox,QSpinBox,QTableWidget,QTableWidgetItem,QDialog
from PyQt5.QtCore import QDate,QDateTime,Qt,QSortFilterProxyModel
from PyQt5 import QtGui,QtCore,QtWidgets
import sys

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



        self.table = QtWidgets.QTableView()


        self.product = QCheckBox("Product")
        self.issue = QCheckBox("Issue")
        self.company = QCheckBox("Company")
        self.state = QCheckBox("State")
        self.zip_code = QCheckBox("ZIP Code")
        self.complaint_id = QCheckBox("Complaint ID")

        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        raw_data=pd.read_csv(r"test.csv")


        self.columns = QComboBox(self)
        for i in raw_data.columns:
            self.columns.addItem(i)

        
        self.model = TableModel(raw_data)

        self.table.setModel(self.model)


        self.thread_amount = QLabel(" Thread Sayısı ")
        self.thread_amount_i = QLineEdit()
        
        
        self.similarity_ratio = QLabel("Benzerlik Oranı ")
        self.similarity_ratio_i = QLineEdit()
      

        self.data_1 = QLabel(" Aranacak Sorgu ")
        self.data_1_i = QLineEdit()


        self.search_button = QPushButton("Ara")

        f_box.addWidget(self.table)

       
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

        f_box.addItem(h_box2)
        f_box.addItem(h_box)
        self.setLayout(f_box)

    def search(self):
        try:
            thread_amount = self.thread_amount_i.text()
            similarity_ratio= self.similarity_ratio_i.text()

            self.new_window= SubWindow()
            f_box = QFormLayout()
            h_box = QHBoxLayout()

            for i in range(0,int(thread_amount)):
            
                self.thread_no = QLabel("Thread ID: "+str(i+1))
                self.thread_amount = QLabel("Time: 2.0sn")
                
                h_box.addWidget(self.thread_no)
                h_box.addWidget(self.thread_amount)

            
                if((i%2==1)):
                    f_box.addItem(h_box)
                    h_box = QHBoxLayout()
                elif((i%2==0)and(int(thread_amount)-1!=i)):
                    self.slender = QLabel(" / ")
                    h_box.addWidget(self.slender)
        
            f_box.addItem(h_box)
            h_box = QHBoxLayout()      
            self.total_thread=QLabel("Total Thread:"+str(thread_amount))
            self.total_time=QLabel("Total Time:"+str(thread_amount))
            h_box.addWidget(self.total_thread)
            h_box.addWidget(self.total_time)
            f_box.addItem(h_box)
            self.new_window.setLayout(f_box)
            self.new_window.show()

        except ValueError:
            QMessageBox.about(self,"Thred Sayısı Hatalı","Lütfen çalışacak thread sayısını giriniz.")





class SubWindow(QWidget):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Thread Manager")
        self.setMinimumSize(1280, 720)




if __name__ == '__main__':

    app = QApplication(sys.argv)

    Win = MainWindow()
    sys.exit(app.exec_())