from menu import menu_list
from order import order_list
from employee import employee_list

def select_order():
    employee = input("Enter employee name: ")
    while True:

        for item, price in menu_list.items(): # print เมนูทั้งหมด
            print(f'{item}: {price}')

        selected_order = str.lower(input("\nSelect your order (or type 'none' to finish): "))

        if selected_order == "none":  # ออกจากการสั่ง
            print(order_list)
            break

        elif selected_order in menu_list:
            if not(selected_order in order_list): # เช็คว่าเมนูที่สั่งมามีอยู่ใน order_list ไหมถ้าไม่จะนำเมนูที่สี่งเข้าไปใน order_list
                order_list.update({selected_order: 1})
            elif selected_order in order_list: # ถ้ามีอยู่แล้วให้ + เพิ่มไป
                order_list[selected_order] += 1
    employee_list[employee] = order_list # เอา order ที่สั่งเก็บเป็น value ของชื่อพนักงาน