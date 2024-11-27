import mysql.connector as mc

con = mc.connect(host='localhost', user='root', password='tiger', database='food_delivery')
cursor = con.cursor()

print('created database successfully!')

cursor.execute('CREATE TABLE employee(emp_id INT NOT NULL, emp_name VARCHAR(20) NOT NULL, orders INT NOT NULL, PRIMARY KEY(emp_id))')
cursor.execute('CREATE TABLE orders(order_id INT NOT NULL, food_type VARCHAR(20) NOT NULL, cost INT, delivery_agent VARCHAR(20) NOT NULL , PRIMARY KEY(order_id))')
print('tables created successfully!')
