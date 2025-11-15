import bcrypt
import string


def hash_password(password):
 binary_pass = password.encode('utf-8')
 salt = bcrypt.gensalt()
 hash_password = bcrypt.hashpw(binary_pass, salt)
 return hash_password.decode ('utf-8')


def validate_hash(password, hash ):
 hash_password = hash.encode('utf-8')
 bin_pssword = password.encode('utf-8')
 return bcrypt.checkpw(bin_pssword, hash_password)



def register_user():
    # Name validation - separate loops for each field
    while True:
        fname = input('Enter your first name: ').strip()
        if not fname:
            print("First name cannot be empty.")
            continue
        if len(fname) < 2 or len(fname) > 50:
            print("First name must be between 2 and 50 characters.")
            continue
        if not fname.isalpha():
            print("First name cannot contain numbers, spaces, or special characters.")
            continue
        break
    
    while True:
        lname = input('Enter your last name: ').strip()
        if not lname:
            print("Last name cannot be empty.")
            continue
        if len(lname) < 2 or len(lname) > 50:
            print("Last name must be between 2 and 50 characters.")
            continue
        if not lname.isalpha():
            print("Last name cannot contain numbers, spaces, or special characters.")
            continue
        
        # Check if name already exists
        try:
            name_exists = False
            with open('user.txt', 'r') as f:
                for line in f:
                    existing_fname, existing_lname, _, _ = line.strip().split(',')
                    if existing_fname.lower() == fname.lower() and existing_lname.lower() == lname.lower():
                        name_exists = True
                        break
            
            if name_exists:
                print("Name already exists. Please use a different last name.")
                continue
            else:
                break
                
        except FileNotFoundError:
            break  # File doesn't exist, so no duplicates
    
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
                print("- At least 8 characters")
            if not upper:
                print("- At least one uppercase letter (A-Z)")
            if not lower:
                print("- At least one lowercase letter (a-z)")
            if not digit:
                print("- At least one number (0-9)")
            if not special:
                print("- At least one special character (!@#$% etc.)")
            if space:
                print("- No spaces allowed")
            continue
    
    hash_val = hash_password(psw)

    with open('user.txt', 'a') as f:
        f.write(f'{fname},{lname},{psw},{hash_val}\n')   
    print("User registered successfully!")





def log_in():
    name = input('enter your name: ')
    password = input('enter your password: ')
    
    with open('user.txt', 'r') as f:
        users = f.readlines()
    
    for user in users:
        name_ , hash = user.strip().split(', ')
        
        if name_ == name:
            return validate_hash(password, hash)
    
    return False

