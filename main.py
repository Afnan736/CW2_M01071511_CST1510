# Import authentication functions from the application module
from application import register_user, log_in, change_username_menu, change_password_menu, delete_account_menu

def main_menu():
    """Main menu with all authentication options"""
    
    # Loop continues until user chooses to exit
    while True:
        # Display menu header
        print("\n" + "="*40)
        print("1. Register New User")
        print("2. Change Username")
        print("3. Change Password")
        print("4. Delete Account")
        print("5. Login")
        print("6. Exit")
        
        # Get user choice
        choice = input("\nSelect option (1-6): ").strip()
        
        # Process user selection
        if choice == '1':
            register_user()  # Register a new user
        elif choice == '2':
            change_username_menu()  # Change username for existing user
        elif choice == '3':
            change_password_menu()  # Change password for existing user
        elif choice == '4':
            delete_account_menu()  # Delete user account
        elif choice == '5':
            log_in()  # User login
        elif choice == '6':
            print("Goodbye!")  # Exit message
            break  # Exit the loop and program
        else:
            print("Invalid choice. Please enter 1-6.")  # Handle invalid input

# Entry point of the program
if __name__ == "__main__":
    main_menu()  # Start the main menu