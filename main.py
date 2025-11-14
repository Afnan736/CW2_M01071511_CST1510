from application import register_user, log_in


def menu():
  print('*' * 20)
  print('*** Welcome to my ststem***')
  print('choose from the following option:')
  print('1. Register')
  print('2. login')
  print('3. Exit!!')
  print('*' * 20)


def main():
  while True :
    menu ()
    choice = input('> ')

    if choice  =='1':
      register_user()
      print('User registered!!')
    elif choice == '2':
      log_in()
      print('you are login')
    elif choice == '3' :
      print('good bye!!')
      break 
main()