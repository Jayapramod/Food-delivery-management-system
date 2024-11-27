# ======== Modules ======== #

import mysql.connector as mc
from random import choice

#-------------------------------------------------------------------------------------------#
# ======== Connecting with Database ======== #

con = mc.connect(host='localhost', user='root', password='tiger', database='food_delivery')
cursor = con.cursor()

#-------------------------------------------------------------------------------------------#
# ======== EMPLOYEE TABLE ======== #

def add_emp(): # Add employee
    name = input('Enter the name of the new employee: ')
    cursor.execute('SELECT COUNT(*) FROM employee')
    emp_id = cursor.fetchone()
    emp_id = int(emp_id[0]) + 1
    sql = "INSERT INTO employee(emp_id, emp_name, orders) VALUES(%s, %s, %s)"
    data = (emp_id, name, 0)
    cursor.execute(sql, data)
    con.commit()
    print(f'{name} successfully added as employee! Your employee id is {emp_id}')

def remove_emp(): # Delete employee
    id = int(input('Enter the employee ID you want to remove: '))
    cursor.execute('SELECT emp_id FROM employee') # check if employee ID is valid
    ids = cursor.fetchall()
    ids = [i[0] for i in ids]
    if id not in ids:
        print('Invalid ID...')
        return

    while True:
        option = input('Are you sure you want to remove this employee(y/n): ')
        if option.lower() == 'y':
            sql = f"DELETE FROM employee WHERE emp_id = {id}"
            cursor.execute(sql)
            print(f'Employee {id} removed!')
            cursor.execute('SELECT emp_name FROM employee')
            delivery_agents = cursor.fetchall()
            delivery_agents = [i[0] for i in delivery_agents] 
            delivery_agent = choice(delivery_agents)
            sql = f'UPDATE orders SET delivery_agent = "{delivery_agent}"'
            cursor.execute(sql)
            con.commit()
            break
        elif option.lower() == 'n':
            return
        else:
            print('Invalid input, enter either y for yes or n for no')

#-------------------------------------------------------------------------------------------#
# ======== ORDERS TABLE ======== #

prices = {'north indian': 500, 'south indian': 600, 'chinese': 300, 'fast food': 100}
cursor.execute('SELECT emp_name FROM employee')
delivery_agents = cursor.fetchall()
delivery_agents = [i[0] for i in delivery_agents] 
delivery_agent = choice(delivery_agents) # choose a random delivery_agent

def add_order(): # Add a new order
    food_type = input('What type of food do you want to order (north indian/south indian/chinese/fast food): ')
    if food_type.lower() not in prices.keys():
        print('Invalid food type, enter again...')

    price = prices[food_type]
    cursor.execute('SELECT COUNT(*) FROM orders')
    order_id = cursor.fetchone()
    order_id = int(order_id[0]) + 1

    sql = "INSERT INTO orders(order_id, food_type, cost, delivery_agent) VALUES(%s, %s, %s, %s)"
    data = (order_id, food_type, price, delivery_agent)
    cursor.execute(sql, data)
    sql = f'UPDATE employee SET orders = orders + 1 WHERE emp_name = "{delivery_agent}"'
    cursor.execute(sql)
    con.commit()
    print(f'Order {order_id} of {food_type} successfully registered!')


def edit_order(): # Edit order
    id = int(input('Enter your order ID: '))
    cursor.execute('SELECT order_id FROM orders') # check if employee ID is valid
    ids = cursor.fetchall()
    ids = [i[0] for i in ids]
    if id not in ids:
        print('Invalid ID...')
        return

    food_type = input('Enter the new food type you want (north indian/south indian/chinese/fast food): ')
    if food_type.lower() not in prices.keys():
        print('Invalid food type, enter again...')
        return

    price = prices[food_type]
    sql = "UPDATE orders SET food_type = %s, cost = %s WHERE order_id = %s"
    data = (food_type, price, id)
    cursor.execute(sql, data)
    #cursor.execute('UPDATE orders SET food_type = ?, cost = ? WHERE order_id = ?', (food_type, price, id))
    con.commit()
    print(f'Your order of ID {id} has been successfully changed to {food_type}.')

def delete_order(): # Delete order
    id = int(input("Enter your order ID: "))
    cursor.execute('SELECT order_id FROM orders') # check if employee ID is valid
    ids = cursor.fetchall()
    ids = [i[0] for i in ids]
    if id not in ids:
        print('Invalid ID...')
        return
    cursor.execute(f'SELECT orders FROM employee WHERE emp_name = "{delivery_agent}"')
    orders = cursor.fetchone()
    orders = int(orders[0]) + 1
    while True:
        option = input(f'Are you sure you want to cancel the order of id {id}? (y/n): ')
        if option.lower() == 'y':
            sql = f"DELETE FROM orders WHERE order_id = {id}"
            cursor.execute(sql)
            if orders > 1:
                sql = f'UPDATE employee SET orders = orders - 1 WHERE emp_name = "{delivery_agent}"'
                cursor.execute(sql)
            con.commit()
            print(f"Order {id} cancelled successfully!")
            break
        elif option.lower() == 'n':
            return
        else:
            print('Invalid input, enter either y for yes or n for no')

def report():
    cursor.execute('SELECT delivery_agent, COUNT(delivery_agent) as empMonth FROM orders GROUP BY delivery_agent ORDER BY empMonth DESC;')
    #SELECT emp_name, MAX(orders) FROM employee
    employee_m = cursor.fetchall()
    employee_m = employee_m[0]
    cursor.execute('SELECT food_type, COUNT(food_type) as popFood FROM orders GROUP BY food_type ORDER BY popFood DESC')
    food_m = cursor.fetchone() 

    print('REPORT')
    print("=====================================")
    print('The employee of the month is', employee_m[0],'as they have successfully delivered the highest amount of orders, which is', employee_m[1])
    print('The most popular type of food ordered is', food_m[0],'& the numbers of times it has been ordered is', food_m[1])
    print("=====================================")

#-------------------------------------------------------------------------------------------#
# ======== MAIN ======== #

print('FOOD DELIVERY MANAGEMENT SYSTEM')
print('====================================')
print('1 -- Add employee')
print('2 -- Remove employee')
print('3 -- Make order')
print('4 -- Change your order')
print('5 -- Delete your order')
print('6 -- Report')
print('q -- Quit')
print('=====================================')

while True:
    option = input('Select an option(1/6): ')
    if option == '1':
        add_emp()
    elif option == '2':
        remove_emp()
    elif option == '3':
        add_order()
    elif option == '4':
        edit_order()
    elif option == '5':
        delete_order()
    elif option == '6':
        report()
    elif option.lower() == 'q':
        con.close()
        break
    else:
        print('Invalid option, select a number from 1 to 6 or q...')


