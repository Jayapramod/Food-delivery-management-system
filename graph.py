# ======== Modules ======== #

import matplotlib.pyplot as plt  
import numpy as np
import mysql.connector as mc

#-------------------------------------------------------------------------------------------#
# ======== Connecting with Database ======== #
con = mc.connect(host='localhost', user='root', password='tiger', database='food_delivery')
cursor = con.cursor()

#-------------------------------------------------------------------------------------------#
# ======== Graph of most popular food ======== #

cursor.execute('SELECT food_type, COUNT(food_type) TotalCount FROM orders GROUP BY food_type HAVING COUNT(food_type) > 1')

food_types = cursor.fetchall()

foodType = []
ordered = []

for i in food_types:
    foodType.append(i[0])
    ordered.append(i[1])


plt.bar(foodType, ordered) 
plt.ylim(0, 5) # units of y-axis
plt.ylabel('No. of times ordered') # name of y-axis
plt.xlabel('Food Types') # name of x-axis
plt.title('Popular Food') # graph name 
plt.show()

#-------------------------------------------------------------------------------------------#
# ======== Graph of Employee of the Month ======== #

cursor.execute('SELECT emp_name, orders from employee')
details = cursor.fetchall()

employee = []
order = []

for i in details:
    employee.append(i[0])
    order.append(i[1])
