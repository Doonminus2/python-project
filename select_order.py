import datetime
from menu import menu_list
from order import order_list
from employee import calculate_commission

def select_order():
    employee = input("Enter employee name: ")
    order_list.clear()

    while True:
        print("Menu List")
        for item, price in menu_list.items():
            print("=" * 60)
            print(f'{item}: {price} THB')
            print("-" * 60)
        selected_order = input("\nSelect your order (or type 'done' to finish): ").lower()
        if selected_order == "done":
            save_sales(employee, order_list)
            print("Order saved!")
            break
        elif selected_order in menu_list:
            order_list[selected_order] = order_list.get(selected_order, 0) + 1
            print("Add your order complete\n")
        else:
            print("Item not in menu.")

def read_menu(filename='menu.txt'):
    menu = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    item, price = line.strip().split(',')
                    menu[item] = int(price)
                except ValueError:
                    print(f"Skipping malformed line in menu: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading menu: {e}")
    return menu

def read_sales(filename='sales.txt'):
    sales = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                
                # ตรวจสอบว่าเป็นข้อมูลที่มี 4 ส่วน (วันที่, พนักงาน, สินค้า, จำนวน)
                if len(data) == 4:
                    date, employee, item, quantity = data
                elif len(data) == 3:
                    # กรณีข้อมูลมีเพียง 3 ส่วน ให้เติมวันที่ปัจจุบันเข้าไป
                    employee, item, quantity = data
                    date = datetime.date.today().isoformat()
                else:
                    print(f"Skipping malformed line in sales: {line.strip()}")
                    continue

                # เพิ่มข้อมูลยอดขายลงใน dictionary
                quantity = int(quantity)
                if employee not in sales:
                    sales[employee] = {}
                sales[employee][item] = sales[employee].get(item, 0) + quantity

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading sales: {e}")
    return sales

def save_sales(employee, order, filename='sales.txt'):
    today = datetime.date.today().isoformat()
    try:
        with open(filename, 'a') as file:
            for item, quantity in order.items():
                file.write(f"{today},{employee},{item},{quantity}\n")
    except Exception as e:
        print(f"Error saving sales: {e}")
def read_daily_sales(filename='sales.txt'):
    daily_sales = {}
    today = datetime.date.today().isoformat()  # กำหนดวันที่ปัจจุบัน
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                
                if len(data) == 4:
                    date, employee, item, quantity = data
                    quantity = int(quantity)
                    
                    # ตรวจสอบว่าเป็นยอดขายของวันนี้หรือไม่
                    if date == today:
                        if employee not in daily_sales:
                            daily_sales[employee] = {}
                        daily_sales[employee][item] = daily_sales[employee].get(item, 0) + quantity
                else:
                    print(f"Skipping malformed line in daily sales: {line.strip()}")
    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading daily sales: {e}")
    
    return daily_sales

def ReportOrderDaily():
    """รายงานยอดขายเฉพาะของวันนี้"""
    menu_data = read_menu()
    daily_sales_data = read_daily_sales()
    print()
    print(f"{'Employee':<30} | {'Item':<30} | {'Quantity':<15} | {'Total Price (THB)':<30} | {'Commission (THB)':<30}")
    print("=" * 150)

    daily_total_quantity = 0
    daily_total_price = 0.0

    for employee, orders in daily_sales_data.items():
        employee_total_quantity = 0
        employee_total_price = 0.0

        for item, quantity in orders.items():
            total_price = menu_data[item] * quantity
            commission = calculate_commission(total_price)

            print(f"{employee:<30} | {item:<30} | {quantity:<30} | {total_price:<30.2f} | {commission:<30.2f}")

            employee_total_quantity += quantity
            employee_total_price += total_price

        daily_total_quantity += employee_total_quantity
        daily_total_price += employee_total_price
        employee_commission = calculate_commission(employee_total_price)

        print(f"{'Total for ' + employee:<30} | {'':<30} | {employee_total_quantity:<30} | {employee_total_price:<30.2f} | {employee_commission:<30.2f}")
        print("-" * 150)

    print(f"{'Total Sales for Today:':<30} | {'':<30} | {daily_total_quantity:<30} | {daily_total_price:<30.2f} | {'0.00':<30}")
    print("=" * 150)

def ReportAll():
    """รายงานยอดขายทั้งหมดในระบบ"""
    menu_data = read_menu()
    sales_data = read_sales()
    print()
    print(f"{'Employee':<30} | {'Item':<30} | {'Total Quantity':<30} | {'Total Price (THB)':<30} | {'Commission (THB)':<30}")
    print("=" * 150)

    overall_total_quantity = 0
    overall_total_price = 0.0

    for employee, orders in sales_data.items():
        employee_total_quantity = 0
        employee_total_price = 0.0

        for item, quantity in orders.items():
            total_price = menu_data[item] * quantity
            commission = calculate_commission(total_price)

            print(f"{employee:<30} | {item:<30} | {quantity:<30} | {total_price:<30.2f} | {commission:<30.2f}")

            employee_total_quantity += quantity
            employee_total_price += total_price

        overall_total_quantity += employee_total_quantity
        overall_total_price += employee_total_price
        employee_commission = calculate_commission(employee_total_price)

        print(f"{'Total for ' + employee:<30} | {'':<30} | {employee_total_quantity:<30} | {employee_total_price:<30.2f} | {employee_commission:<30.2f}")
        print("-" * 150)

    print(f"{'Total Sales Overall:':<30} | {'':<30} | {overall_total_quantity:<30} | {overall_total_price:<30.2f} | {'0.00':<30}")
    print("=" * 150)
