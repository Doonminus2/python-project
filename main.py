from select_order import select_order, ReportOrderDaily, ReportALL

def main():
    while True:
        action = input("Choose an action (A for order, B for Report All time, C for Report Daily  , exit): ")
        if action == 'exit':
            break
        elif action == 'A':
            select_order()
        elif action == 'B':
            ReportALL()  # เรียกใช้ฟังก์ชันแสดงผล
        elif action == 'C':
            ReportOrderDaily()

if __name__ == '__main__':
    main()

