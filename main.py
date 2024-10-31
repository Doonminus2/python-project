from select_order import select_order, display_sales_summary

def main():
    while True:
        action = input("Choose an action (order, display, exit): ")
        if action == 'exit':
            break
        elif action == 'order':
            select_order()
        elif action == 'display':
            display_sales_summary()  # เรียกใช้ฟังก์ชันแสดงผล

if __name__ == '__main__':
    main()

