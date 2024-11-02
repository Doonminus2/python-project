from select_order import select_order, ReportOrderDaily, ReportAll


def main():
    while True:
    # ตัวเลือกของผู้ใช้
        print("=" * 100)
        print("\t\t\t\t\tsomchai cafe")
        print("=" * 100)
        choice = input("Choose an action (A for order, B for Report All time, C for Report Daily , exit): ").upper()

        if choice == "A":
            select_order()
        elif choice == "B":
            ReportAll()  # แสดงรายงานยอดขายทั้งหมด
        elif choice == "C":
            ReportOrderDaily()  # แสดงรายงานยอดขายรายวัน
        elif choice == "EXIT":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")



if __name__ == '__main__':
    main()

