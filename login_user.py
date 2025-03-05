import pandas
import getpass
from encdyc import TextSecurity

##### Load the Data File ######
try:
   user_info = pandas.read_csv("Login_encrypted.csv")
except FileNotFoundError:
   print("The Login file was not found. Please ensure the file is in the right location")
except Exception as e:
   print(f"An error found: {e}")

cipher = TextSecurity(5)
    
##### Class LoginUser #####
class LoginUser:
    """ This class validate if the user is valid or not """
    def __init__(self, email_id = None, password = None):
        self.email_id = email_id
        self.password = password
    
    def login(self):
        """ Check login detail """
        if self.email_id in user_info["User_id"].to_list(): # Check if user ID exists 
            user_row = user_info[user_info["User_id"] == self.email_id]
            stored_encrypted_password = user_row["Password"].values[0] # Get stored encrypted password
            decrypted_password = cipher.decrypt(stored_encrypted_password) # Decrypt the password
            if decrypted_password == self.password:
                print("Login successful!")
                return True, user_row["Role"].values[0]
            else:
                print("Incorrect password.")
                return False, None
        else:
            print("Email ID not found.")
            return False, None
    
    def logout(self):
        """ Logged out from the system """
        return "loggedout"

    def change_password(self):
        """ Change password """
        while True:
            new_password = getpass.getpass("Please enter your new password: ").strip()
            check_new_password = getpass.getpass("Please enter your new password again: ").strip()
            if new_password == check_new_password:
                user_info.loc[user_info.User_id == self.email_id, "Password"] = cipher.encrypt(new_password)
                user_info.csv("Login_encrypted.csv", index = False) # save to CSV file
                print("Changing password successfully!") 
                return True
            else:
                print("Inconsistent passwords, please re-enter your new password.")
    
