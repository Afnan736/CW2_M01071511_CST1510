import bcrypt



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
  name = input('enter your name:')
  psw = input('enter your password:')
  hash = hash_password(psw)
  with open('user.txt','a') as f :
   f.write(f'{name}, {psw}, {hash}\n')
  print(f'{name}, {psw}, {hash}, register sucessfully\n')


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

