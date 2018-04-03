from Restaurant_gui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow , QApplication , QTableWidgetItem , QHeaderView
from PyQt5.QtGui import QPixmap
import datetime
from mysql.connector import connect
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists as file_exists

from add_detail_menu import add_detail
from data_from_restaurant_sql import get_data_rest_sql
from day_generate import get_day
import smtp_mail

manager_names =Series(("Manas","Shivang","Sagar_beard","Ridima","Sagar"))



t1=get_data_rest_sql()	#getting data from database
l=t1["name"].copy()

l1,l2,l3=add_detail(t1,l) #adding details
l4=list()


data=DataFrame()
try:
	data=DataFrame.from_csv("Data.csv")  #getting data from csv
except FileNotFoundError:
	DataFrame().to_csv("Data.csv")
	

	
customer_id=0
if len(data.index)>0:
	customer_id=data.index.max()

	
	
class MyappGui(QMainWindow,Ui_MainWindow):
	total=0
	total_items=0
	emailid=""
	
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.init_combobox()
		self.init_menu_widget_buttons()
		self.init_data_buttons()
		self.init_date_time()
		self.init_bill_buttons()
		
	def init_menu_widget_buttons(self):
		self.maincourse_pushButton.clicked.connect(self.change_value_Mc)
		self.appetizer_pushButton.clicked.connect(self.change_value_Ap)
		self.beverage_pushButton.clicked.connect(self.change_value_Bv)
		self.add_pushButton.clicked.connect(self.add_dish)
		self.analysis_pushButton.clicked.connect(self.process_analysis)
		self.refresh_pushButton.clicked.connect(self.refresh_page)
		self.delete_pushButton.clicked.connect(self.delete_dish)
		self.bill_pushButton.clicked.connect(self.prepare_bill)
		self.reset_pushButton.clicked.connect(self.reset_page)
		
	
	def reset_page(self):
		self.init_date_time()
		self.amount_spinBox.setValue(1)
		self.amount_spinBox_2.setValue(1)
		self.change_total(0)
		self.delete_comboBox.clear()
		self.change_value_Ap()
		self.init_combobox()
		l4.clear()
		self.tableWidget.clear()
		self.tableWidget.setRowCount(0)
		self.bill_mail_label.clear()
		self.bill_mail_lineEdit.clear()
		self.emailid=""
		
	def process_analysis(self):
		v=DataFrame({"ind":data.index,"day":data["Day"].values})
		if len(v)>0:
			val=v.groupby(["day","ind"]).size().reset_index()
			val["day"].value_counts().plot(kind="bar")
			plt.savefig("Graphs/week_graph.png",format='png')
			plt.clf()
		if file_exists("Graphs/week_graph.png"):
			pixmap=QPixmap("Graphs/week_graph.png")
			self.week_graph.setPixmap(pixmap)
		l=["mon","tue","wed","thu","fri","sat","sun"]
		for i in l:
			d=data["Day"]==i
			t=DataFrame()
			t["type"]=data["Type"][d]
			t["veg"]=data["Veg"][d]
			final=t["veg"][t["type"]!="beverage"]
			path='Graphs/{}.png'.format(i)
			if len(final)>0:
				ax=final.value_counts().plot(kind="pie")
				ax.set_ylabel("")
				plt.savefig(path,format='png')
				plt.clf()
			if file_exists(path):
				pixmap=QPixmap(path)
				if i=="mon":
					self.mon_graph.setPixmap(pixmap)
				elif i=="tue":
					self.tue_graph.setPixmap(pixmap)
				elif i=="wed":
					self.wed_graph.setPixmap(pixmap)
				elif i=="thu":
					self.thu_graph.setPixmap(pixmap)
				elif i=="fri":
					self.fri_graph.setPixmap(pixmap)
				elif i=="sat":
					self.sat_graph.setPixmap(pixmap)
				elif i=="sun":
					self.sun_graph.setPixmap(pixmap)
		self.mov_to_data()
		
	def prepare_bill(self):
		global customer_id
		self.bill_customer_label.setText("Customer id = "+str(customer_id+1))
		date=self.dateEdit.date().toPyDate()
		time=self.timeEdit.time().toPyTime()
		self.bill_date_label.setText("Date = "+str(date))
		self.bill_time_label.setText("Time = "+str(time)[:5])
		self.tableWidget.clear()
		self.tableWidget.setHorizontalHeaderLabels(["Name","Per Price","Amount","Total Price"])
		self.tableWidget.setRowCount(0)
		header = self.tableWidget.horizontalHeader()       
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QHeaderView.Stretch)
		self.mov_to_bill()
		if len(l4)>0:
			l5=np.unique(np.array(l4),return_counts=True)
			self.tableWidget.setRowCount(len(l5[0]))
			for row in range(len(l5[0])):
				i=l5[0][row]
				code=int(i[:i.index(":")])
				for col in range(4):
						if col==0:
							name=t1.loc[code,"name"]
							self.tableWidget.setItem(row,col,QTableWidgetItem(name))
						elif col==1:
							pprice=t1.loc[code,"price"]
							self.tableWidget.setItem(row,col,QTableWidgetItem(str(pprice)))
						elif col==2:
							amt=l5[1][row]
							self.tableWidget.setItem(row,col,QTableWidgetItem(str(amt)))
						else:
							pprice=int(self.tableWidget.item(row,1).text())
							amt=int(self.tableWidget.item(row,2).text())
							self.tableWidget.setItem(row,col,QTableWidgetItem(str(pprice*amt)))
		self.bill_sub_total_label.setText("Sub Total = "+str(self.total))
		self.bill_cgst_total_label.setText("CGST (2.5%) = "+str(round(self.total*2.5/100,2)))
		self.bill_sgst_total_label.setText("SGST (2.5%) = "+str(round(self.total*2.5/100,2)))
		self.bill_total_label.setText("Grand Total = "+str(round(self.total+self.total*5/100,2)))
	
	def setup_mail(self):
		global customer_id
		content=""
		self.bill_mail_label.clear()
		emailid=self.bill_mail_lineEdit.text()
		self.bill_mail_label.setText("Loading...")
		if len(emailid)>0:
			emailid=emailid.lower()
			valid=smtp_mail.check_email(emailid)
			self.bill_mail_label.setText(valid)
			if valid=="VALID":
				self.bill_mail_label.setText("Loading...")
				if len(l4)>0:
					
					id=str(customer_id+1)
					content+="Id : "+id
					content+="\nDate : "+str(self.dateEdit.date().toPyDate()) + "  Time : "+str(self.timeEdit.time().toPyTime())[:5]
					content+="\nManager : "+str(self.manager_names_comboBox.currentText())
					l5=np.unique(np.array(l4),return_counts=True)
					
					for dish in range(len(l5[0])):
						i=l5[0][dish]
						code=int(i[:i.index(":")])
						
						name,amt,pprice=t1.loc[code,"name"],l5[1][dish],t1.loc[code,"price"]
						
						t="Name : "+str(name)+"  X "+str(amt)+", Per Price : "+str(pprice)
						
						content+="\n"+t
					content+="\nSub Total : "+str(self.total)
					content+="\nCGST @2.5% : "+str(round(self.total*2.5/100,2))
					content+="\nSGST @2.5% : "+str(round(self.total*2.5/100,2))
					content+="\nGrand Total : "+str(round(self.total+self.total*5/100,2))
					try:
						smtp_mail.send_mail(emailid,content)	
						self.bill_mail_label.setText("Sent")
					except Exception:
						self.bill_mail_label.setText("Error while sending")

				else:
					self.bill_mail_label.setText("No Items")	
			else:
				self.bill_mail_lineEdit.clear()
		else:
			self.bill_mail_label.setText("Enter Email id")

	def add_to_excel(self):
		global customer_id
		global data
		if len(l4)>0:
			customer_id+=1
			l5=np.unique(np.array(l4),return_counts=True)
			for dish in range(len(l5[0])):
				i=l5[0][dish]
				code=int(i[:i.index(":")])
				
				name,type,amt,date=t1.loc[code,"name"],t1.loc[code,"type"],l5[1][dish],self.dateEdit.date().toPyDate()
				time=str(self.timeEdit.time().toPyTime())[:5]
				manager,day=self.manager_names_comboBox.currentText(),get_day(date)
				veg="Veg" if t1.loc[code,"veg"] ==1 else "NonVeg"
				email=self.bill_mail_lineEdit.text()
				t={"Manager":[manager],"Name":[name],"Amount":[amt],"Date":[date],"Time":[time],"Day":[day],"Amount":[amt],"Veg":[veg],"Type":[type],"Email":[email]}
				
				data=data.append(DataFrame(t,index=[customer_id]))
			
			self.reset_page()
			data.to_csv("Data.csv")
			self.stackedWidget.setCurrentIndex(0)
				
	def init_data_buttons(self):
		self.data_back_pushButton.clicked.connect(self.mov_to_menu)
	
	def init_bill_buttons(self):
		self.bill_back_pushButton.clicked.connect(self.mov_to_menu)
		self.bill_done_pushButton.clicked.connect(self.add_to_excel)
		self.bill_mail_pushButton.clicked.connect(self.setup_mail)
	
	def mov_to_menu(self):
		self.stackedWidget.setCurrentIndex(0)

	def mov_to_data(self):
		self.stackedWidget.setCurrentIndex(1)

	def mov_to_bill(self):
		self.stackedWidget.setCurrentIndex(2)
	
	def change_total(self,*a):
		if len(a)>0:
			self.total_items=a[0]
			self.total=a[0]
		self.total_label.setText("Total Items= "+str(self.total_items))
		temp="Bill"
		if self.total!=0:
			temp+="= "+str(self.total)
		self.bill_pushButton.setText(temp)
		
	def add_dish(self):
		text=self.menu_comboBox.currentText()
		code=int(text[:text.index(":")])
		dish=str(code)+":  "+t1.loc[code,"name"]
		amount=self.amount_spinBox.value()	
		for i in range(amount):
			l4.append(dish)
			self.total+=t1.loc[code,"price"]
			self.total_items+=1
			self.change_total()
		else :
			self.amount_spinBox.setValue(1)
			self.init_delete_comboBox()
			
	def delete_dish(self):
		text=self.delete_comboBox.currentText()
		if len(text)>0:
			code=int(text[:text.index(":")])
			dish1=str(code)+":  "+t1.loc[code,"name"]
			amount2=self.amount_spinBox_2.value()
			for i in range(amount2):
				if dish1 in l4:
					l4.remove(dish1)
					self.total-=t1.loc[code,"price"]
					self.total_items-=1
					self.change_total()
			else :
				self.amount_spinBox_2.setValue(1)
				self.init_delete_comboBox()
				
	def init_delete_comboBox(self):
		self.delete_comboBox.clear()
		if len(l4)>0:
			items=list()
			l5=np.unique(np.array(l4),return_counts=True)
			for i in zip(l5[0],l5[1]):
				items.append(str(i[0])+"  X "+str(i[1]))
			self.delete_comboBox.addItems(items)
	
	def init_combobox(self):
		l=l1
		self.manager_names_comboBox.clear()
		self.manager_names_comboBox.addItems(manager_names)
		self.menu_comboBox.clear()
		self.menu_comboBox.addItems(l)

		
	def refresh_page(self):
		self.amount_spinBox.setValue(1)
		self.amount_spinBox_2.setValue(1)
		self.init_date_time()
	
	def init_date_time(self):
		self.dateEdit.setDate(datetime.date.today())
		self.timeEdit.setTime(datetime.datetime.today().time())
		
	def change_value_Ap(self):
		self.menu_comboBox.clear()
		self.menu_comboBox.addItems(l1)

	def change_value_Mc(self):
		self.menu_comboBox.clear()
		self.menu_comboBox.addItems(l2)
		
	def change_value_Bv(self):
		self.menu_comboBox.clear()
		self.menu_comboBox.addItems(l3)
				
if __name__ =='__main__':
	application=QApplication([]) #Create QApplication object
	Restaurant_gui=MyappGui()
	Restaurant_gui.show()

	application.exec_()