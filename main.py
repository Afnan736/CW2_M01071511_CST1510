from application import register_user, log_in

def menu():
    print('*' * 20)
    print('*** Welcome to my system ***')
    print('Choose from the following options:')
    print('1. Register')
    print('2. Login')
    print('3. Exit!!')
    print('*' * 20)

def main():
    while True:
        menu()
        choice = input('> ')

        if choice == '1':
            register_user()
        elif choice == '2':
            result = log_in()
            if result:
                print('You are logged in!')
            else:
                print('Returning to main menu...')
        elif choice == '3':
            print('Good bye!!')
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()