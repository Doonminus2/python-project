import datetime  # เอามาใช้ระบุวันที่คิดorderของพลักงาน
from menu import menu_list  
from order import order_list  
from employee import calculate_commission  # นำเข้าฟังก์ชันคำนวณคอมมิชชั่นจากไฟล์ employee.py

def select_order():
    employee = input("Enter employee name: ")  # รับชื่อพนักงานจากผู้ใช้งาน
    order_list.clear()  # ล้างรายการสั่งซื้อเก่าใน order_list

    while True:
        # แสดงรายการเมนูในรูปแบบตาราง
        print("\n" + "=" * 60)  # แสดงเส้นขีด = สำหรับแบ่งส่วนหัวของตาราง
        print(f"{'Item':<40} | {'Price (THB)':<15}")  # แสดงชื่อคอลัมน์ Item และ Price (THB)
        print("=" * 60)  # แสดงเส้นขีด = หลังส่วนหัวของตาราง
        for item, price in menu_list.items():  # วนซ้ำแสดงเมนูและราคา
            print(f"{item:<40} | {price:<15.2f}")  # แสดงชื่อสินค้าและราคาในรูปแบบจัดเรียง
        print("=" * 60)  # แสดงเส้นขีด = ปิดท้ายตารางเมนู

        # รับออเดอร์จากผู้ใช้
        selected_order = input("\nSelect your order (or type 'done' to finish): ").lower()  # รับชื่อสินค้า
        if selected_order == "done":  # ตรวจสอบว่าผู้ใช้ต้องการเสร็จสิ้นการสั่งซื้อหรือไม่
            save_sales(employee, order_list)  # บันทึกรายการสั่งซื้อของพนักงาน
            print("Order saved!")  # แจ้งข้อความว่าการสั่งซื้อถูกบันทึก
            break  # ออกจากลูป
        elif selected_order in menu_list:  # ตรวจสอบว่าสินค้ามีในเมนูหรือไม่
            order_list[selected_order] = order_list.get(selected_order, 0) + 1  # เพิ่มจำนวนสั่งซื้อของสินค้านั้น
            print("Add your order complete\n")  # แจ้งว่าการเพิ่มออเดอร์เสร็จสมบูรณ์
        else:
            print("Item not in menu.")  # แจ้งว่าสินค้าไม่มีในเมนู

def read_menu(filename='menu.txt'):
    menu = {}  # สร้าง dictionary สำหรับเก็บเมนูสินค้าและราคา
    try:
        with open(filename, 'r') as file:  # เปิดไฟล์เมนูสำหรับอ่านข้อมูล
            for line in file:  # วนซ้ำแต่ละบรรทัดในไฟล์
                try:
                    item, price = line.strip().split(',')  # แยกชื่อสินค้าและราคาจากไฟล์
                    menu[item] = int(price)  # เก็บข้อมูลสินค้าและราคาใน dictionary
                except ValueError:
                    print(f"Skipping malformed line in menu: {line.strip()}")  # แจ้งเตือนหากบรรทัดนั้นไม่ถูกต้อง
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")  # แจ้งเตือนหากไฟล์ไม่พบ
    except Exception as e:
        print(f"An unexpected error occurred while reading menu: {e}")  # แจ้งเตือนหากมีข้อผิดพลาดอื่น ๆ
    return menu  # ส่งคืนข้อมูลเมนู

def read_sales(filename='sales.txt'):
    sales = {}  # สร้าง dictionary สำหรับเก็บข้อมูลการขาย
    try:
        with open(filename, 'r') as file:  # เปิดไฟล์การขายสำหรับอ่านข้อมูล
            for line in file:  # วนซ้ำแต่ละบรรทัดในไฟล์
                data = line.strip().split(',')  # แยกข้อมูลด้วยเครื่องหมาย comma
                
                # ตรวจสอบว่าเป็นข้อมูลที่มี 4 ส่วน (วันที่, พนักงาน, สินค้า, จำนวน)
                if len(data) == 4:
                    date, employee, item, quantity = data  # แยกข้อมูลออกเป็น วันที่ พนักงาน สินค้า จำนวน
                elif len(data) == 3:
                    # กรณีข้อมูลมีเพียง 3 ส่วน ให้เติมวันที่ปัจจุบันเข้าไป
                    employee, item, quantity = data  # แยกข้อมูลออกเป็น พนักงาน สินค้า จำนวน
                    date = datetime.date.today().isoformat()  # กำหนดวันที่เป็นวันที่ปัจจุบัน
                else:
                    print(f"Skipping malformed line in sales: {line.strip()}")  # แจ้งเตือนหากข้อมูลไม่ครบถ้วน
                    continue

                # เพิ่มข้อมูลยอดขายลงใน dictionary
                quantity = int(quantity)  # แปลงจำนวนสินค้าให้เป็นจำนวนเต็ม
                if employee not in sales:  # ตรวจสอบว่าพนักงานยังไม่มีใน dictionary
                    sales[employee] = {}  # เพิ่มพนักงานใหม่ใน dictionary
                sales[employee][item] = sales[employee].get(item, 0) + quantity  # เพิ่มยอดขายของสินค้าสำหรับพนักงาน

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")  # แจ้งเตือนหากไฟล์ไม่พบ
    except Exception as e:
        print(f"An unexpected error occurred while reading sales: {e}")  # แจ้งเตือนหากมีข้อผิดพลาดอื่น ๆ
    return sales  # ส่งคืนข้อมูลยอดขาย

def save_sales(employee, order, filename='sales.txt'):
    today = datetime.date.today().isoformat()  # กำหนดวันที่ปัจจุบัน
    try:
        with open(filename, 'a') as file:  # เปิดไฟล์การขายสำหรับเขียนข้อมูลเพิ่ม
            for item, quantity in order.items():  # วนซ้ำสินค้าและจำนวนที่สั่ง
                file.write(f"{today},{employee},{item},{quantity}\n")  # เขียนข้อมูลการขายลงไฟล์
    except Exception as e:
        print(f"Error saving sales: {e}")  # แจ้งเตือนหากมีข้อผิดพลาดขณะบันทึกข้อมูลการขาย

def read_daily_sales(filename='sales.txt'):
    daily_sales = {}  # สร้าง dictionary สำหรับเก็บข้อมูลการขายของวันนี้
    today = datetime.date.today().isoformat()  # กำหนดวันที่ปัจจุบัน
    
    try:
        with open(filename, 'r') as file:  # เปิดไฟล์การขายสำหรับอ่านข้อมูล
            for line in file:  # วนซ้ำแต่ละบรรทัดในไฟล์
                data = line.strip().split(',')  # แยกข้อมูลด้วย comma
                
                if len(data) == 4:
                    date, employee, item, quantity = data  # แยกข้อมูลเป็นวันที่ พนักงาน สินค้า จำนวน
                    quantity = int(quantity)  # แปลงจำนวนสินค้าให้เป็นจำนวนเต็ม
                    
                    # ตรวจสอบว่าเป็นยอดขายของวันนี้หรือไม่
                    if date == today:
                        if employee not in daily_sales:  # ตรวจสอบว่าพนักงานยังไม่มีใน dictionary
                            daily_sales[employee] = {}  # เพิ่มพนักงานใหม่ใน dictionary
                        daily_sales[employee][item] = daily_sales[employee].get(item, 0) + quantity  # เพิ่มยอดขายของสินค้าสำหรับพนักงาน
                else:
                    print(f"Skipping malformed line in daily sales: {line.strip()}")  # แจ้งเตือนหากข้อมูลไม่ครบถ้วน
    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")  # แจ้งเตือนหากไฟล์ไม่พบ
    except Exception as e:
        print(f"An unexpected error occurred while reading daily sales: {e}")  # แจ้งเตือนหากมีข้อผิดพลาดอื่น ๆ
    
    return daily_sales  # ส่งคืนข้อมูลยอดขายของวันนี้

def ReportOrderDaily():
    """รายงานยอดขายเฉพาะของวันนี้"""
    menu_data = read_menu()  # อ่านข้อมูลเมนู
    daily_sales_data = read_daily_sales()  # อ่านข้อมูลยอดขายของวันนี้
    print()
    print(f"{'Employee':<30} | {'Item':<30} | {'Quantity':<30} | {'Total Price (THB)':<30} | {'Commission (THB)':<30}")  # หัวตาราง
    print("=" * 150)  # เส้นแบ่ง

    daily_total_quantity = 0  # ตัวแปรเก็บยอดขายรวมของวันนี้
    daily_total_price = 0.0  # ตัวแปรเก็บยอดเงินรวมของวันนี้

    for employee, orders in daily_sales_data.items():  # วนซ้ำแต่ละพนักงานในยอดขายของวันนี้
        employee_total_quantity = 0  # ตัวแปรเก็บจำนวนรวมของแต่ละพนักงาน
        employee_total_price = 0.0  # ตัวแปรเก็บยอดเงินรวมของแต่ละพนักงาน

        for item, quantity in orders.items():  # วนซ้ำแต่ละสินค้าในยอดขายของพนักงาน
            total_price = menu_data[item] * quantity  # คำนวณยอดเงินของสินค้านั้น
            commission = calculate_commission(total_price)  # คำนวณคอมมิชชั่น

            print(f"{employee:<30} | {item:<30} | {quantity:<30} | {total_price:<30.2f} | {commission:<30.2f}")  # แสดงข้อมูลพนักงาน สินค้า จำนวน ราคา คอมมิชชั่น

            employee_total_quantity += quantity  # เพิ่มจำนวนสินค้ารวมของพนักงาน
            employee_total_price += total_price  # เพิ่มยอดเงินรวมของพนักงาน

        daily_total_quantity += employee_total_quantity  # เพิ่มจำนวนรวมของวันนี้
        daily_total_price += employee_total_price  # เพิ่มยอดเงินรวมของวันนี้
        employee_commission = calculate_commission(employee_total_price)  # คำนวณคอมมิชชั่นของพนักงาน

        print(f"{'Total for ' + employee:<30} | {'':<30} | {employee_total_quantity:<30} | {employee_total_price:<30.2f} | {employee_commission:<30.2f}")  # แสดงผลรวมของพนักงานแต่ละคน
        print("-" * 150)  # เส้นแบ่ง

    print(f"{'Total Sales for Today:':<30} | {'':<30} | {daily_total_quantity:<30} | {daily_total_price:<30.2f} | {'0.00':<30}")  # แสดงผลรวมของวันนี้
    print("=" * 150)  # เส้นแบ่ง

def ReportAll():
    """รายงานยอดขายทั้งหมดในระบบ"""
    menu_data = read_menu()  # อ่านข้อมูลเมนู
    sales_data = read_sales()  # อ่านข้อมูลยอดขายทั้งหมด
    
    print()
    print(f"{'Employee':<30} | {'Item':<30} | {'Total Quantity':<30} | {'Total Price (THB)':<30} | {'Commission (THB)':<30}")  # หัวตาราง
    print("=" * 150)  # เส้นแบ่ง

    overall_total_quantity = 0  # ตัวแปรเก็บจำนวนรวมทั้งหมด
    overall_total_price = 0.0  # ตัวแปรเก็บยอดเงินรวมทั้งหมด

    for employee, orders in sales_data.items():  # วนซ้ำแต่ละพนักงานในยอดขายทั้งหมด
        employee_total_quantity = 0  # ตัวแปรเก็บจำนวนรวมของแต่ละพนักงาน
        employee_total_price = 0.0  # ตัวแปรเก็บยอดเงินรวมของแต่ละพนักงาน

        for item, quantity in orders.items():  # วนซ้ำแต่ละสินค้าในยอดขายของพนักงาน
            total_price = menu_data[item] * quantity  # คำนวณยอดเงินของสินค้านั้น
            commission = calculate_commission(total_price)  # คำนวณคอมมิชชั่น

            print(f"{employee:<30} | {item:<30} | {quantity:<30} | {total_price:<30.2f} | {commission:<30.2f}")  # แสดงข้อมูลพนักงาน สินค้า จำนวน ราคา คอมมิชชั่น

            employee_total_quantity += quantity  # เพิ่มจำนวนสินค้ารวมของพนักงาน
            employee_total_price += total_price  # เพิ่มยอดเงินรวมของพนักงาน

        overall_total_quantity += employee_total_quantity  # เพิ่มจำนวนรวมทั้งหมด
        overall_total_price += employee_total_price  # เพิ่มยอดเงินรวมทั้งหมด
        employee_commission = calculate_commission(employee_total_price)  # คำนวณคอมมิชชั่นของพนักงาน

        print(f"{'Total for ' + employee:<30} | {'':<30} | {employee_total_quantity:<30} | {employee_total_price:<30.2f} | {employee_commission:<30.2f}")  # แสดงผลรวมของพนักงานแต่ละคน
        print("-" * 150)  # เส้นแบ่ง

    print(f"{'Total Sales Overall:':<30} | {'':<30} | {overall_total_quantity:<30} | {overall_total_price:<30.2f} | {'0.00':<30}")  # แสดงผลรวมทั้งหมด
    print("=" * 150)  # เส้นแบ่ง
