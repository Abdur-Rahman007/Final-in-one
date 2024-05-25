import random
from abc import ABC

class User(ABC):
    def __init__(self, name, email, adress) -> None:
        self.name = name
        self.email = email
        self.adress = adress

class Customer(User):
    def __init__(self, name, email, adress, accountType) -> None:
        super().__init__(name, email, adress)
        self.accountType = accountType
        self.balance = 0
        self. transaction_history = []
        self.account_number = random.randint(1,112)+99

    def history(self):
        print("------Transaction_History------")
        for info in self.transaction_history:
            for key, val in info.items():
                print(f'{key} : {val}')
        print()

    def deposit(self, amount, bank):
        bank.bank_balance += amount
        self.balance += amount
        self.transaction_history.append(
                {"Operation": "Deposit", 
                "Amount" : amount}
            )
        print(f'Deposit {amount} tk Successfully')


    def withdraw(self, amount, bank):
        if bank.bankrpt == False:
            if self.balance > amount:
                self.balance -= amount
                bank.bank_balance -= amount
                self.transaction_history.append(
                    {"Operation": "Withdraw", 
                    "Amount" : amount}
                )
                print(f'Whithdraw {amount} tk Successfully')
            else: 
                print(f'Wihdrawal amount exceeded')
        else:
            print("Bankrupt no transaction is possible.")


    def check_balance(self):
        print(f'your current balance is {self.balance}')

    def take_loan(self, amount, bank):
        loan_count = 2
        if loan_count > 0:
            if bank.bank_balance > amount:
                if bank.loan:
                    if bank.bankrpt == False:
                        bank.total_loan += amount
                        self.balance += amount
                        loan_count -= 1
                        self.transaction_history.append(
                            {"Operation": "loan", 
                            "Amount" : amount}
                            )
                        print(f'You took {amount} tk loan from bank.')
                    else:
                        print("Bankrupt no transaction is possible.")
                else:
                    print("Sorry currently loan status is off.")
            else:
                print("Invalid request!!!")
        else:
            print("You have already used your max loan attempt.")

    def send_money(self, to_email, amount, bank):
        bank.transfer_balance(self.email, to_email, amount)

class Admin(User):
    def __init__(self, name, email, adress) -> None:
        super().__init__(name, email, adress)

    def create_admin(self, admin_info, bank):
        bank.create_admin_account(admin_info)

    def view_customer_list(self, bank):
        bank.user_list()

    def view_admin_list(self, bank):
        bank.admin_list()

    def remove_user(self, user_email, bank):
        bank.delete_account(user_email)

    def check_bank_balances(self, bank):
        bank.bank_balances()

    def check_total_bank_loan(self, bank):
        bank.loan_balance()

    def set_loan_status(self, status, bank):
        bank.loan_status(status)

    def set_bankrupt_status(self, status, bank):
        bank.bankrpt_status(status)


                    #########   BANK   #########

class Bank:
    def __init__(self, name) -> None:
        self.name = name
        self.custo_account_list = []
        self.admin_account_list = []
        self.bank_balance = 0
        self.total_loan = 0
        self.loan = False
        self.bankrpt = False

    def find_customer(self, email): #no duplicate email is possible
        for acc in self.custo_account_list:
            if email == acc.email:
                return acc
        return None
    
    def find_admin(self, email):
        for acc in self.admin_account_list:
            if email == acc.email:
                return acc
        return None
    
    def transfer_balance(self, sender_email, to_email, amount):
        sender = self.find_customer(sender_email)
        reciever = self.find_customer(to_email)
        if sender is not None and reciever is not None:
            if self.bankrpt == False:
                if sender.balance > amount:
                    reciever.balance += amount
                    sender.balance -= amount
                    print(f'From {sender_email} to {to_email} total {amount} Tk transfered successfully')
                    sender.transaction_history.append(
                        {"Operation": "Send money", 
                        "Amount" : amount}
                        )
                    reciever.transaction_history.append(
                        {"Operation": "Recive money", 
                        "Amount" : amount}
                        )
                else:
                    print("Limit exited")
            else:
                print("Bankrupt no transaction is possible")
        else:
            print("Invalid User")

    def create_user_account(self, customer):
        self.custo_account_list.append(customer)
        print("Account created successfully.") 
    
    def create_admin_account(self, admin):
        self.admin_account_list.append(admin)
        print("Account created successfully.") 

    def delete_account(self, email):
        for acc in self.custo_account_list:
            if email == acc.email:
                self.custo_account_list.remove(acc)
                print("Account deleted successfully.")
            else:
                print("User not found")
    
    def user_list(self):
        for acc in self.custo_account_list:
            print(f'User name: {acc.name}\tUser Email: {acc.email}\tAccount Name: {acc.accountType}')

    def admin_list(self):
        for acc in self.admin_account_list:
            print(f'User name: {acc.name}\tUser Email: {acc.email}')

    def bank_balances(self):
        print(self.bank_balance)
    
    def loan_balance(self):
        print(self.total_loan)

    def loan_status(self, status):
        if status.lower() == "on":
            self.loan = True
            print(f'Loan Status On')
        elif status.lower()=="off":
            self.loan = False
            print(f'Loan Status Off')

    def bankrpt_status(self, status):
        if status.lower() == "on":
            self.bankrpt = True
            print(f'Loan Status On')
        elif status.lower()=="off":
            self.bankrpt = False
            print(f'Loan Status Off')

    
##################################   MAIN   ##################################

is_bank = Bank("Islami Bank")
Manager = Admin("Alam", "alam@gmail.com", "Dhaka")
Manager.create_admin(Manager, is_bank)


def admin_menu():

    while True:
        print(f"Welcome To Admin Dashboard")
        print("1 : Create New Admin")
        print("2 : Remove User")
        print("3 : View Admins")
        print("4 : View User")
        print("5 : Bank Stock")
        print("6 : Loan Balance")
        print("7 : Set Loan Status")
        print("8 : Set Bankrpt Status")
        print("9 : Exit")

        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            adminName = input("Type Name : ")
            adminEmail = input("Type Email : ").lower()
            adminAddress = input("Type Address : ")
            if is_bank.find_admin(adminEmail):
                print("Sorry This Email Allready Exist")
            else:
                newAdmin = Admin(adminName, adminEmail, adminAddress)
                Manager.create_admin(newAdmin, is_bank)

        elif choice == 2:
            userEmail = input("Type User Email ")
            Manager.remove_user(userEmail, is_bank)
        elif choice == 3:
            Manager.view_admin_list(is_bank)
        elif choice == 4:
            Manager.view_customer_list(is_bank)
        elif choice == 5:
            Manager.check_bank_balances(is_bank)
        elif choice == 6:
            Manager.check_total_bank_loan(is_bank)
        elif choice == 7:
            print(f"Loan Status : ")
            status = input("type on or off : ").lower()
            Manager.set_loan_status(status, is_bank)
        elif choice == 8:
            print(f"Bankrupt Status : ")
            status = input("type on or off : ").lower()
            Manager.set_bankrupt_status(status, is_bank)
        elif choice == 9:
            break
        else:
            print("Invalid Input")


def user_menu(customer):

    while True:
        print(f"Welcome To User Dashboard")
        print("1 : Deposite")
        print("2 : Withdraw")
        print("3 : Check Balance")
        print("4 : Take Loan")
        print("5 : Send Money")
        print("6 : History")
        print("7 : Exit")

        choice = int(input("Enter your choice : "))
        if choice == 1:
            amount = int(input("Enter Your Amount For Deposite = "))
            customer.deposit(amount, is_bank)
        elif choice == 2:
            amount = int(input("Enter Your Amount For Withdraw = "))
            customer.withdraw(amount, is_bank)
        elif choice == 3:
            customer.check_balance()
        elif choice == 4:
            amount = int(input("Enter Your Amount For Take Loan = "))
            customer.take_loan(amount, is_bank)
        elif choice == 5:
            re_email = input("Reciever Email : ")
            amount = int(input("Amount = "))
            customer.send_money(re_email, amount, is_bank)
        elif choice == 6:
            customer.history()
        elif choice == 7:
            break
        else:
            print("Invalid Input")


def admin_login():
    while True:
        print(f"Login First")
        email = input("Enter Your Email : ")
        if is_bank.find_admin(email):
            admin_menu()
            break
        else:
            print("Admin Does Not Exist")
            return


def customer_login():
    while True:
        print("1 : Login")
        print("2 : Sign Up")
        print("3 : Exit")

        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            email = input("Enter Your Email ")
            if is_bank.find_customer(email) is not None:
                user_menu(is_bank.find_customer(email))
            else:
                print("User Does Not Exist")
        elif choice == 2:
            userName = input("Name : ").lower()
            userEmail = input("User Email : ").lower()
            userAddress = input("User Address : ").lower()
            print("Account Type : Savings/Current")
            accountType = input("Account type : ").lower()
            if is_bank.find_customer(userEmail) is not None:
                print(f"Sorry {userEmail} Already Exist")
            else:
                customer = Customer(userName, userEmail, userAddress, accountType)
                is_bank.create_user_account(customer)
                user_menu(customer)
        elif choice == 3:
            break
        else:
            print("Invalid Input !!")


while True:
    print(f"Wellcome To {is_bank.name}")
    print("1 : Admin")
    print("2 : User")
    print("3 : Exit")
    choice = int(input("Enter Your Choice : "))

    if choice == 1:
        admin_login()
    elif choice == 2:
        customer_login()
    elif choice == 3:
        break
    else:
        print("Invalid Input")

