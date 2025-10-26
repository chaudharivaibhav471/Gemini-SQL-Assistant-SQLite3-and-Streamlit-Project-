import sqlite3

#  we connect to our database of employees 
connection = sqlite3.connect("Software_Employee.db")

# we creates a cursor object to insert values into it 

cursor = connection.cursor()

table_info = """
Create Table Employee (employee_name varchar(30),
                        employee_role varchar(30),
                        employee_salary float)"""

cursor.execute(table_info)

# we are insert the date 

cursor.execute('''Insert into Employee values('Vaibhav Chaudhari', 'Data Science', 75000)''')
cursor.execute('''Insert into Employee values('Bhushan Chaudhari', 'Data Engineer', 50000)''')
cursor.execute('''Insert into Employee values('Vinay Barhate', 'Data Analytics', 65000)''')
cursor.execute('''Insert into Employee values('Sahil Kalamkar', 'Data Analysis', 40000)''')
cursor.execute('''Insert into Employee values('Raj Bhagwat', 'Java Developer', 45000)''')
cursor.execute('''Insert into Employee values('Sahil Dabhade', 'Game Developer', 30000)''')
cursor.execute('''Insert into Employee values('Himanshu sangitrao' , 'Data Engineer', 80000)''')
cursor.execute('''Insert into Employee values('Atul Magare', 'App developer', 54000)''')

# we will display all the records
print("The intrested Record are")
data = cursor.execute('''Select * from Employee''')
for row in data:
    print(row)


connection.commit()
connection.close()
