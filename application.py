import bcrypt
import string

def hash_password(password):
    binary_pass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(binary_pass, salt)
    return hashed_password.decode('utf-8')

def validate_hash(password, stored_hash):
    hash_bytes = stored_hash.encode('utf-8')
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)

def register_user():
    while True:
        fname = input('Enter your first name: ').strip()
        if not fname:
            print("First name cannot be empty.")
            continue
        if len(fname) < 2 or len(fname) > 25:
            print("First name must be between 2 and 25 characters.")
            continue
        break
    
    while True:
        lname = input('Enter your last name: ').strip()
        if not lname:
            print("Last name cannot be empty.")
            continue
        if len(lname) < 2 or len(lname) > 25:
            print("Last name must be between 2 and 25 characters.")
            continue
        break
        
    # Check if name already exists
    while True:
        try:
            name_exists = False
            with open(r'C:\Users\afnan\Desktop\CW2_M01071511_CST1510\user.txt', 'r') as f:
                for line in f:
                    existing_fname, existing_lname, _, _ = line.strip().split(',')
                    
                    if existing_fname == fname and existing_lname == lname:
                        name_exists = True
                        break
            
            if name_exists:
                print("Name already exists. Please use a different first name or last name.")
                fname = input('Enter your first name: ')
                lname = input('Enter your last name: ')
                continue
            else:
                break  
                    
        except FileNotFoundError:
            break  

    # Password validation
    while True:
        psw = input('Enter your password: ')
        if not psw:
            print("Password cannot be empty.")
            continue
            
        upper = lower = digit = special = space = False
        
        for char in psw:
            if char.isupper(): upper = True
            if char.islower(): lower = True
            if char.isdigit(): digit = True
            if char in string.punctuation: special = True
            if char == ' ': space = True
        
        # Check each requirement and show specific errors
        if len(psw) >= 8 and upper and lower and digit and special and not space:
            break
        else:
            print("Password missing requirements:")
            if len(psw) < 8:
                print(" At least 8 characters")
            if not upper:
                print(" At least one uppercase letter (A-Z)")
            if not lower:
                print(" At least one lowercase letter (a-z)")
            if not digit:
                print(" At least one number (0-9)")
            if not special:
                print(" At least one special character")
            if space:
                print(" No spaces allowed")
            continue
    
    hash_val = hash_password(psw)

    with open(r'C:\Users\afnan\Desktop\CW2_M01071511_CST1510\user.txt', 'a') as f:
        f.write(f'{fname},{lname},{psw},{hash_val}\n')   
    print("Registered successfully!")


    

def log_in():

    while True:
        full_name = input('Enter your full name both first and last name: ').strip()
        password = input('Enter your password: ')

        nospace = full_name.replace(' ', '')

        try:
            with open(r'C:\Users\afnan\Desktop\CW2_M01071511_CST1510\user.txt', 'r') as f:
                users = f.readlines()

            user_found = False
            for user in users:
                fname, lname, psw, hash_val = user.strip().split(',')
                stored_name = fname + lname
                
                if stored_name == nospace:
                    user_found = True
                    if validate_hash(password, hash_val):
                        print("Login successful!")
                        return True
                    else:
                        print("Wrong password. Try again.")
                        break
            
            
            if not user_found:
                print('Name not found. Try again.')
                return False
                
        except FileNotFoundError:
            print("No users found. Please register first.")
            return False