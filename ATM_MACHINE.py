
from tkinter import *
from tkinter import messagebox
# Define the bank data file name
bank_data_file = "bank_data.txt"

# Define the function to read the bank data from the file
def read_bank_data():
    # Create an empty dictionary to hold the bank data
    bank = {}
    # Open the bank data file for reading
    with open(bank_data_file, "r") as f:
        # Loop over each line in the file
        for line in f:
        # Split the line into its components (account_number, name, password, balance, and status)
            account_number, name, password, balance, status = line.strip().split(",")
# Add the account's data [ name, password, balance, and status]to the bank dictionary, with the account number as the key
            bank[account_number] = [name, int(password), int(balance), status]
    return bank

# Define the function to write the updated bank database to the file
def write_bank_data():
    # Open the bank data file for writing
    with open(bank_data_file, "w") as f:
        # Loop over each account in the bank dictionary
        for account_number, account_info in bank.items():
            # Write the account data (name, password, balance, and status) to the file.
            #account_info variable holds the list of the account's data
            f.write(f"{account_number},{account_info[0]},{account_info[1]},{account_info[2]},{account_info[3]}\n")


# Read the bank data from the file
bank = read_bank_data()

# Define the GUI window for account number
window = Tk()
window.title("Bank Account Login")
window.geometry("700x400")
window.config(bg='GRAY')

atm_label = Label(window, bg="gray", fg="blue", font=("Ariel", 30), text="ATM MACHINE", padx=8, pady=8, width=100)
atm_label.pack()

# Define the account number input field
account_number_label = Label(window, text="Please Enter Your Account Number:", font=("Ariel", 20), bg="gray")
account_number_label.pack(padx=10, pady=20)

account_number_entry = Entry(window, width=20, font=("Ariel", 20), justify=CENTER)
account_number_entry.pack(padx=10, pady=20)

# Define the login button
def login():
    account_number = account_number_entry.get()

    if account_number in bank:
        if bank[account_number][3] == 'LOCKED':
            messagebox.showerror("Error", "This account is locked. Please visit your branch.")
            return

       
        # remove account number from entry
        account_number_entry.delete(0, END)
        #Hide the window 
        window.withdraw()

        # Create the second window for password
        password_window = Tk()
        password_window.title("Bank Account Login")
        password_window.geometry("700x400")
        password_window.config(bg='gray')  # set gray background

        # Define the account status label
        status_label = Label(password_window, text="", bg="gray")
        status_label.pack()
       # Create a label for the ATM machine title
        atm_label = Label(password_window, bg="gray", fg="blue", font=("Ariel", 30), text="ATM MACHINE", padx=8, pady=8, width=100)
        atm_label.pack()

        # Define the password input field
        password_label = Label(password_window, text="Please Enter Your Password:", font=("Ariel", 20), bg="gray")
        password_label.pack(padx=10, pady=10)

        password_entry = Entry(password_window, show="*", font=("Ariel", 20), justify=CENTER)
        password_entry.pack(padx=10, pady=10)

        # Initialize the number of login attempts to zero
        login_attempts = 0
        # Define a function to check the password
        def check_password():
            nonlocal login_attempts
            password = int(password_entry.get())

            if bank[account_number][1] == password:
                # Successful login
                password_window.destroy()
                # Create the options window
                options_window = Tk()
                atm_label = Label(options_window, bg="gray", fg="blue", font=("Ariel", 30), text=f"ATM MACHINE\nHello, {bank[account_number][0]}\nChoose Your Option", padx=8, pady=8, width=100)                
                atm_label.pack()
                
                options_window.title("Account Options")
                options_window.geometry("700x600")
                options_window.config(bg="gray")
                 #1-# Define a function to handle the 'Withdraw' option
                def withdraw():
                    # hide main options window
                    options_window.withdraw()  
                    # Create a new window for the 'Withdraw' option
                    withdraw_window = Tk()
                    withdraw_window.config(bg="gray")
                    withdraw_window.title("Withdraw")
                    withdraw_window.geometry("700x400")

                    atm_label = Label(withdraw_window, bg="gray", fg="blue", font=("Ariel", 30), text="ATM MACHINE", padx=8, pady=8, width=100)
                    atm_label.pack()

                    amount_label = Label(withdraw_window, text="Enter amount to withdraw:",font=("Ariel", 20),bg="gray")
                    amount_entry = Entry(withdraw_window,font=("Ariel", 20), justify=CENTER)
                    # Define a function to handle the withdrawal process
                    def withdraw_amount():
                        amount = int(amount_entry.get())
                        if amount > 5000:
                            messagebox.showerror("Error", "Maximum withdrawal amount is 5000 EGP.")
                        elif amount > bank[account_number][2]:
                            messagebox.showerror("Error", "Insufficient funds.")
                        elif  amount % 100 != 0:
                            messagebox.showerror("Error", "Invalid withdrawal amount. The amount should be a multiple of 100 EGP.")
                        else:
                            bank[account_number][2] -= amount
                            messagebox.showinfo("Success", f"Withdrawal of {amount} EGP successful.")
                            write_bank_data()
                             # Close the 'Withdraw' window and show the main options window again
                            withdraw_window.destroy()
                            options_window.deiconify()  
                            
                    withdraw_button = Button(withdraw_window, text="Enter", command=withdraw_amount, font=("Ariel",20),  fg="blue") 

                    amount_label.pack(pady=10)
                    amount_entry.pack(pady=10)
                    withdraw_button.pack(pady=10)
                    # Start the 'Withdraw' window loop
                    withdraw_window.mainloop()
                
                withdraw_button = Button(options_window, text="  1-Cash Withdraw  ", command=withdraw, font=("Ariel", 20),fg="blue")
                withdraw_button.pack(pady=10)

                # Define a function to handle the 'Balance Inquiry' option
                def inquiry():
                    messagebox.showinfo("Balance Inquiry", f"Your current balance is {bank[account_number][2]} EGP.")
                inquiry_button = Button(options_window, text="  2-Balance Inquiry  ", command=inquiry,font=("Ariel", 20),fg="blue")
                inquiry_button.pack(pady=10) 

                # Define a function to handle the 'Change password' option
                def change_password():
                    # hide main options window
                    options_window.withdraw()  
                    # Create a new window for the 'Change Password' option
                    change_password_window =Tk()
                    change_password_window.config(bg="gray")
                    change_password_window.title("Change Password")
                    change_password_window.geometry("700x500")

                    atm_label = Label(change_password_window, bg="gray", fg="blue", font=("Ariel", 30), text="ATM MACHINE", padx=8, pady=8, width=100)
                    atm_label.pack()

                    current_password_label = Label(change_password_window, text="Enter Your Current Password:", font=("Ariel", 20), bg="gray")
                    current_password_label.pack(padx=10, pady=10)

                    current_password_entry = Entry(change_password_window, show="*", font=("Ariel", 20), justify=CENTER)
                    current_password_entry.pack(padx=10, pady=10)

                    new_password_label = Label(change_password_window, text="Enter Your New Password:", font=("Ariel", 20), bg="gray")
                    new_password_label.pack(padx=10, pady=10)

                    new_password_entry = Entry(change_password_window, show="*", font=("Ariel", 20), justify=CENTER)
                    new_password_entry.pack(padx=10, pady=10)
                    
                    confirm_password_label = Label(change_password_window, text="Confirm New Password:",bg="gray",font=("Ariel", 20))
                    confirm_password_entry = Entry(change_password_window, show="*",font=("Ariel", 20), justify=CENTER)

                     # Define a function to handle the password change process
                    def change_password_confirm():
                        # Get the current password, new password,
                        # and confirm password entered by the user from the entry fields and convert them to integers
                        current_password = int(current_password_entry.get())
                        new_password = int(new_password_entry.get())
                        confirm_password = int(confirm_password_entry.get())

                        if current_password != bank[account_number][1]:
                            messagebox.showerror("Error", "Incorrect current password.")
                        elif new_password != confirm_password:
                            messagebox.showerror("Error", "New password and confirm password do not match.")
                        elif len(str(new_password)) != 4:
                            messagebox.showerror("Error", "New password must be exactly four digits long.")
                        else:
                            bank[account_number][1] = new_password
                            messagebox.showinfo("Success", "Password changed successfully.")
                            write_bank_data()

                            # Close the 'Change Password' window and show the main options window again
                            change_password_window.destroy()
                            window.deiconify() 

                    confirm_button = Button(change_password_window, text="Confirm", command=change_password_confirm,fg="blue",font=("Ariel",20))
                    
                    current_password_label.pack(pady=10)
                    current_password_entry.pack(pady=10)
                    
                    new_password_label.pack(pady=10)
                    new_password_entry.pack(pady=10)
                    
                    confirm_password_label.pack(pady=10)
                    confirm_password_entry.pack(pady=10)

                    confirm_button.pack(pady=10)
                    # Start the 'Change Password' window loop
                    change_password_window.mainloop()

                change_password_button = Button(options_window, text="3-Change Password", command=change_password,font=("Ariel", 20),fg="blue")
                change_password_button.pack(pady=10)


                # Define a function for the Fawry service option
                def fawry():
                    # hide main options window
                    options_window.withdraw()
                   # Create a new window for the Fawry service option
                    fawry_window = Toplevel()
                    fawry_window.title("Fawry Service")
                    fawry_window.geometry("500x300")
                    fawry_window.config(bg="gray")
                    
                    service_label = Label(fawry_window, text="Choose Fawry service:", font=("Ariel",15),bg="gray")
                    service_var = StringVar(value="Orange Recharge")
                    service_menu = OptionMenu(fawry_window, service_var, "Orange Recharge", "Etisalat Recharge", "Vodafone Recharge", "We Recharge")
                    
                    phone_label = Label(fawry_window, text="Enter Phone Number:",font=("Ariel",15),bg="gray")
                    phone_entry = Entry(fawry_window,font=("Ariel", 15), justify=CENTER)
                    
                    amount_label = Label(fawry_window, text="Enter Amount:",font=("Ariel",15),bg="gray")
                    amount_entry = Entry(fawry_window,font=("Ariel", 15), justify=CENTER)

                    # Define a function to handle the Fawry service confirmation process
                    def confirm_fawry():
                        service = service_var.get()
                        phone_number = phone_entry.get()
                        amount = int(amount_entry.get())
                         # Check if the phone number is 11 digits long and valid for the selected service
                        if len(phone_number) != 11:
                            messagebox.showerror("Error", "Phone number must be 11 digits") 
                        # Check if the service is Orange Recharge and the phone number does not start with "012", 
                        # or if the service is Vodafone Recharge and the phone number does not start with "010", 
                        # or if the service is We Recharge and the phone number does not start with "015", 
                        # or if the service is Etisalat Recharge and the phone number does not start with "011".
                        elif(service == "Orange Recharge" and phone_number[:3] != "012") or \
                            (service == "Vodafone Recharge" and phone_number[:3] != "010") or \
                            (service == "We Recharge" and phone_number[:3] != "015") or \
                            (service == "Etisalat Recharge" and phone_number[:3] != "011"):
                            messagebox.showerror("Error", f"Invalid phone number for {service}")

                        # Check if the user has sufficient balance for the Fawry service transaction
                        elif amount > bank[account_number][2]:
                            messagebox.showerror("Error", " No sufficient balance")
                            # Close the Fawry service window and show the main options window again
                            fawry_window.destroy()
                            options_window.deiconify()  # show main options window
                               
                        else:
                            bank[account_number][2] -= amount
                            messagebox.showinfo("Success", f"{service} recharge of {amount} EGP for {phone_number} successful.")
                            write_bank_data()
                            # Close the Fawry service window and show the main options window again
                            fawry_window.destroy()
                            options_window.deiconify()  # show main options window
                    
                    confirm_button = Button(fawry_window, text="Confirm", command=confirm_fawry, font=("Ariel",15),  fg="blue")
                    service_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                    service_menu.grid(row=0, column=1, padx=10, pady=10, sticky=W)
                    
                    phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
                    phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
                    
                    amount_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                    amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)
                    
                    confirm_button.grid(row=3, column=1, padx=10, pady=10, sticky=E)

                    # Start the Fawry service window loop
                    fawry_window.mainloop()
                
                fawry_button = Button(options_window, text="   4-Fawry Service   ", command=fawry, font=("Ariel", 20),fg="blue")
                fawry_button.pack(pady=10)                
                #exit
                exit_button = Button(options_window, text="          5-Exit            ", command=options_window.destroy,font=("Ariel", 20),fg="blue")
                exit_button.pack(pady=10,padx=10)                
                # Run the options window          
                options_window.mainloop()

           # If the password is incorrect
            else:
                login_attempts += 1
                if login_attempts >= 3:
                    bank[account_number][3] = 'LOCKED'
                    messagebox.showerror("Error", "Invalid password. This account is now locked. Please visit your branch.")
                    write_bank_data()
                    password_window.destroy()
                else:
                    # If there have been fewer than 3 failed login attempts, show a message with the number of attempts remaining.
                    status_label.config(text=f"Invalid password. {3 - login_attempts} attempts remaining.", fg="red",font=("Ariel",15))
                    password_entry.delete(0, END)
        submit_button = Button(password_window, text="Submit", font=("Ariel", 15), command=check_password,fg="blue")
        submit_button.pack(padx=10, pady=10)

        # Start the password window's main loop.
        password_window.mainloop()
    else:
        messagebox.showerror("Error", "Account number not found. Please try again.")
login_button = Button(window, text="Login", font=("Ariel", 15), command=login,fg="blue")
login_button.pack(pady=20)

# Start the main loop of the GUI window.
window.mainloop()  

