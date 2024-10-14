from select_order import select_order

def main():
    while True:
        action = input('choose an action: ')
        if action == 'none':
            break
        elif action == 'order':
            select_order()

if __name__ == '__main__':
    main()

