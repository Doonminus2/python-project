from menu import menu_list
from order import order_list
from employee import employee_list, calculate_commission

def select_order():
    employee = input("Enter employee name: ")
    order_list.clear()

    while True:
        for item, price in menu_list.items():
            print(f'{item}: {price} THB')
        selected_order = input("\nSelect your order (or type 'done' to finish): ").lower()
        if selected_order == "done":
            save_sales(employee, order_list)  # บันทึกข้อมูลการขายลงไฟล์ sales.txt
            print("Order saved!")
            break
        elif selected_order in menu_list:
            order_list[selected_order] = order_list.get(selected_order, 0) + 1
        else:
            print("Item not in menu.")

def read_menu(filename='menu.txt'):
    menu = {}
    with open(filename, 'r') as file:
        for line in file:
            item, price = line.strip().split(',')
            menu[item] = int(price)
    return menu

def read_sales(filename='sales.txt'):
    sales = {}
    with open(filename, 'r') as file:
        for line in file:
            employee, item, quantity = line.strip().split(',')
            quantity = int(quantity)
            if employee not in sales:
                sales[employee] = {}
            sales[employee][item] = sales[employee].get(item, 0) + quantity
    return sales

def save_sales(employee, order, filename='sales.txt'):
    with open(filename, 'a') as file:
        for item, quantity in order.items():
            file.write(f"{employee},{item},{quantity}\n")

def display_sales_summary():
    menu_data = read_menu()  # อ่านจาก menu.txt
    sales_data = read_sales()  # อ่านจาก sales.txt

    # แสดงหัวตาราง
    print()
    print(f"{'Employee':<20} | {'Item':<25} | {'Quantity':<10} | {'Total Price (THB)':<25} | {'Commission (THB)':<25} |")
    print("=" * 120)  # แสดงเส้นแบ่ง
    print("-" * 120)  # เส้นแบ่งก่อนเริ่มข้อมูล

    overall_total = 0  # สำหรับยอดรวมรวม

    for employee, orders in sales_data.items():
        employee_total = 0
        for item, quantity in orders.items():
            total_price = menu_data[item] * quantity
            employee_total += total_price
            commission = calculate_commission(total_price)  # คำนวณค่าคอมมิชชั่น

            # แสดงข้อมูลในตาราง
            print(f"{employee:<20} | {item:<25} | {quantity:<10} | {total_price:<25} | {commission:<25} |")

        # แสดงยอดรวมสำหรับพนักงาน
        overall_total += employee_total  # รวมยอดทั้งหมด
        print(f"{'Total for ' + employee:<20} | {'':<25} | {'':<10} | {employee_total:<25} | {calculate_commission(employee_total):<25} |")
        print("-" * 120)  # แสดงเส้นแบ่งระหว่างพนักงาน

    # แสดงยอดรวมรวมทั้งหมด
    print(f"{'Total Sales Overall:':<20} | {'':<25} | {'':<10} | {overall_total:<25} | {'':<25} |")
    print()

# ใช้ฟังก์ชัน select_order() และ display_sales_summary() ที่อื่นในโปรแกรม
