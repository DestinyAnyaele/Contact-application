# Developed by Anyaele Destiny Chinaemerem
# initialisating Owner of Script
print('welcome to Contact by Anyaele Destiny Chinaemerem')
print('\n')

# importing  required modules
import colorama,time,smtplib,datetime,hashlib,asyncio,json,getpass,socket,string,sys
time.sleep(4)

# initializing colourama for colours
colorama.init(autoreset = True) 


# Timer function for countdown during lock-out
def Timer() :
    hrs,mins,secs = 24,0,0
    print('wait 24hrs to continue registration')
    print('\n')
    while True :
        if (hrs == 0) and(mins == 0) and (secs == 0) :
            print('Registration can continue')
            time.sleep(1)
            print ('\n')
            break
        print (f'Hour : {hrs} Minute : {mins} Second : {secs}')
        time.sleep(1)
        if secs == 0 :
            secs = 59
            if mins == 0 :
                mins = 59
                hrs -= 1
            else :
                 mins -= 1
        else :
            secs -= 1
    Register()
        
            
 # inintializing Registration process
def Register() :
    global OTP,user_phone_number,gmail

    # user phone number  is taken
    user_phone_number = input('Enter your phone number : ')
    
    
    # Necessary information given to user
    print('Registering helps to save contacts if Phone gets replaced')
    time.sleep(2)
    print('\n')
    
    # User input (Gmail) is taken for verification
    gmail = input('Enter your Gmail address : ')


    # Generating OTP for Verification
    import random
    Time_generated = datetime.datetime.today()
    if Time_generated.hour == 23 :
        Hour = 0
    else :
        Hour = Time_generated.hour + 1
    expired_date = datetime.datetime(Time_generated.year,Time_generated.month,Time_generated.day,Hour,Time_generated.minute,Time_generated.second)
    print()
    time.sleep(2)
    print(f'This is a one-hour OTP so will expire on {expired_date}')
    print()
    OTP = random.randint(1000,9999)
    for tries in range(5) :
      try :
        asyncio.run(email_sender(gmail))
      except socket.gaierror : # can't connect to the internet at all
        print('Please turn on wifi or sim network')
      except smtplib.SMTPConnectError : # Data is on but can't connect to host
        print("You don't have internet connection,buy date plans")
      except smtplib.SMTPRecipientsRefused : # Emsil given doesn't exit
        print(colorama.Fore.RED + 'invalid email address')
        print()
        gmail = input('Enter a valid Email_address : ')  
      else :
        print('A verification code has been sent to',gmail)
        break
    else :
       print('Closing terminal')
       sys.exit()
     
     
    
    # User is given tries to input correct OTP
    i = 1
    while i <= 5 :
        try :
            user_input = int(input('Enter the OTP sent to ' + gmail + ' : '))
            if len(str(user_input)) != 4 :
                raise Exception (colorama.Fore.RED + colorama.Style.BRIGHT + 'OTP IS 4 DIGITS')
        except ValueError :
            print ('Integers are accepted only')
            print ('\n')
            continue
        except Exception as error_name :
            print (error_name)
            print ('\n')
        else :
            if user_input == OTP :
                if datetime.datetime.today() > expired_date :
                    print(colorama.Fore.MAGENTA + 'OTP is expired')
                    print ('Re-Registering')
                    print('\n')
                    Register ()
                else :
                    print(colorama.Fore.GREEN + 'successfully verified')
                    print('\n')
                    Password()
                    break
            else :
                print (colorama.Fore.RED + colorama.Style.BRIGHT + 'Wrong OTP')
                print (f'you have {5 - i} trie(s)')
                print ('\n')
                i += 1
    if i == 5 :
      Timer()
      Register()
    
    
# A function to check for digits if present in a string
def Digit(String):
  for char in String :
    if char in '0123456789' :
      return True
  else :
    return False
    
    
# creating a password function
def Password() :
    global contacts
    print('create your password')
    print()
    print('password should contain digits, alphabets only and must be greater than 10 characters but less than 20 characters')
    print('\n')
    password = getpass.getpass('Enter your password : ')
    conformity = getpass.getpass('confirm your password : ')
    if password != conformity :
      print(colorama.Fore.RED + 'Password do not correspond')
      print('\n')
      Password()
    elif len(password) < 4 :
      print(colorama.Fore.RED + 'password is less than 10 characters')
      print('\n')
      Password()
    elif len(password) > 20 :
      print(colorama.Fore.RED + 'password is greater than 20 characters')
      print('\n')
      Password()
    elif password.isalnum() == False :
      print(colorama.Fore.RED + 'Password cointains special characters')
      print('\n')
      Password()
    elif Digit(password) == False :
      print(colorama.Fore.RED + 'password do not have numeric character')
      print('\n')
      Password()
    else :
      print(colorama.Fore.GREEN + 'password Accepted')
      print('\n')
      
      
      # Reading data in json file
      with open('Server/Data.json','r') as password_file :
        Password_dict = json.load(password_file)
        
        
      # adding new data
      Password_dict.update({f'{gmail.title()}' : [user_phone_number, password,{}]})
      contacts = Password_dict[gmail][2]
      
      # overwrite new data to old one
      with open('Server/Data.json','w') as password_file :
        json.dump(Password_dict, password_file,ensure_ascii = False)
      



# function to send Email address
async def email_sender(email_address) :
    ''' Multithreading is not necessary but i used it so the 
    terminal won't be blank while sending the Message
        
    This email needs synchronious programming,Email verification 
    needs to be done first but while it is going through i wouldn't like the screen to be blank
    so i used asyncio to print a message saying The email is trying to send '''
        
    task = asyncio.create_task(keep_screen_on())
    message = f"Your OTP is {OTP} .\n if this OTP was not requested for please ignore"
    title = 'OTP request for Contact Registration by Anyaele Destiny Chinaemerem'
    # I do not need to create a Main function that encompasses Task and i/o tasks because the side Task(keep_screen_on) do not need to be awaited to finish because it is an infinite loop
    
    
    # Sender address which is mine
    sender_address = 'unknownpython81@gmail.com'
    
    
    # sender password
    # if password is not supported by app go to Google and create an app password for the ide
    sender_password = 'bitxdnrrlbgxfbor'
    
    
    # setup MIMEMultipart for email
    from email.mime.multipart import MIMEMultipart
    
    
    # setup MIMEText
    from email.mime.text import MIMEText
    
    mail = MIMEMultipart()
    mail['From'] = sender_address
    mail['To'] = email_address
    mail['Subject'] = title
    mail.attach(MIMEText(message,'plain'))
    
    
    # creating smtplib session
    session = smtplib.SMTP_SSL('smtp.gmail.com',465) # i am using port 465 which is Google
    
    
    session.login(sender_address,sender_password)
    mail = mail.as_string()
    session.sendmail(sender_address,email_address,mail)
    
    
    # end session
    session.quit()
    
    
# print message for when Email is tring to send
async def keep_screen_on() :
    while True :
        print(colorama.Fore.YELLOW + 'Email is trying to send')
        await asyncio.sleep(2)
        

# login function        
def Login() :
    global contacts,Data
    while True :
        print("Enter 'Q' if you don't have an account and would like to register")
        print('\n')
        gmail = input("Enter your email_address or 'Q' to register : ").title()
        if gmail == 'Q' :
          time.sleep(1)
          Register()
          break
        print('\n')
        Password = getpass.getpass('Enter your password : ')
        
        # reading passwords in server
        with open('Server/Data.json','r') as data :
          Data = json.load(data)
        data = Data.get(gmail,'Not Found')
        if data[1] ==  Password :
          print(colorama.Fore.GREEN + 'login successfully')
          
          
          # Getting contacts for user
          contacts = Data[gmail][2]
          break
        else :
          print(colorama.Fore.RED + 'user_email or password is invalid')
          print('\n')
        
# Contacts     
def Contact() :
  # possible Functions for user
  Functions = [
                       'Getting all phone_contacts','Editing a Contact','Calling a contact',
                      'Getting a particular contact number by Name','Creating a new contact',
                      'Deleting a contact','Logout'
                     ]
  while True :
      print()
      print('select what you want to do ')
      print()
      for index,function in enumerate(Functions) :
        print(index,' : ', function)
        time.sleep(1)
        print()
      try :
        Task = int(input('Enter the number of the what you want to do : '))
        if (Task > 6) or (Task < 0) :
          raise Exception('number is not available')
      except ValueError:
        time.sleep(1)
        print('Enter numbers only')
        print('\n')
      except Exception as message :
        time.sleep(1)
        print(message)
        print('\n')
      else :
        if Task == 0 :
          if len(contacts) == 0 :
            print('You have no contacts,\n try 4 to create a new contact')
          for Name,Phone_number in contacts.items() :
            print(Name,' : ',Phone_number)
            time.sleep(1)
          time.sleep(4)
        elif Task == 1 :
          print()
          Edit = input('Select the contact name you would like to edit : ')
          Edit_phone_number = contacts.get(Edit,'contact not found')
          print(Edit_phone_number)
          if Edit_phone_number == 'contact not found' :
            print('Try 0 to get all contacts name')
          else :
            while True :
              var = input("Would you like to edit the 'name' or 'phone number' : ")
              print('\n')
              if 'NAME' == var.upper() :
                del contacts[Edit]
                contacts[input(f'Enter the new name of {Edit} : ')] = Edit_phone_number
                print()
                print(colorama.Fore.GREEN + 'contact edited successfully')
                break
              elif 'PHONE NUMBER' == var.upper() :
                foo = input(f'Enter the the new phone number of {Edit} : ')
                contact[Edit] = foo
                print()
                print(colorama.Fore.GREEN + 'contact edited successfully')
                break
              else :
                print(colorama.Fore.RED + f"Enter 'name' if you would like to edit a {Edit}`s name or 'phone number' if you would like to edit {Edit}'s phone number")
                print('\n')
          time.sleep(4)
        elif Task == 2 :
            print()
            calling = input('Enter the person you would like to call : ')
            calling = contacts.get(calling)
            if calling == None :
              print('contact not found')
              print('Try 0 to get all contacts name')
            else :
              while True :
                print(colorama.Fore.YELLOW + f'trying to call {calling}')
                time.sleep(1)
                var = input("Enter 'Q' if you would like to stop call : ")
                if var == 'Q' :
                  break
            time.sleep(4)
        elif Task == 3 :
          print()
          name = input('Select the contact name you would like to View : ')
          number = contacts.get(name,'contact not found')
          time.sleep(2)
          print(colorama.Fore.GREEN + f'{name} --> {number}')
          if number == 'contact not found' :
            print('Try 0 to get all contacts name')
          time.sleep(4)
        elif Task == 4 :
          First_name = input('Enter the contact first name : ')
          Last_name = input('Enter the contact second name : ')
          New_contact = First_name + ' ' + Last_name
          time.sleep(2)
          print('\n')
          print(New_contact)
          time.sleep(1)
          contact_number = input('Enter his phone number : ')
          contacts[New_contact] = contact_number
          time.sleep(4)
          print(colorama.Fore.GREEN + 'contact created successfully')
        elif Task == 5 :
          print()
          value = input('Enter the Contact you would like to delete : ')
          try :
            del contacts[value]
          except KeyError:
            print('contact not found')
            print('\n')     
          time.sleep(4)
        elif Task == 6 :
          time.sleep(4)
          break
  with open('Server/Data.json','w') as File :
      json.dump(Data,File,ensure_ascii = False)
      
      
# General main function
def Main() : 
  while True :
    Login()
    Contact()
if __name__ == '__main__' :
 Main()
 