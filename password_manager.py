import tkinter as tk
from cryptography.fernet import Fernet
import json
import getpass

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        
        # Create encryption key using Fernet from cryptography library
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # Load stored passwords from file (if exists)
        self.passwords = {}
        self.load_passwords()
        
        # Create GUI components using tkinter
        self.label_website = tk.Label(master, text="Website:")
        self.label_username = tk.Label(master, text="Username:")
        self.label_password = tk.Label(master, text="Password:")
        
        self.entry_website = tk.Entry(master)
        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")  # Show asterisks for password

        
        self.button_save = tk.Button(master, text="Save Password", command=self.save_password)
        self.button_get = tk.Button(master, text="Get Password", command=self.get_password)
        
        # Layout components using grid system
        self.label_website.grid(row=0, column=0)
        self.label_username.grid(row=1, column=0)
        self.label_password.grid(row=2, column=0)
        
        self.entry_website.grid(row=0, column=1)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        
        self.button_save.grid(row=3, column=0, columnspan=2)
        self.button_get.grid(row=4, column=0, columnspan=2)
    
    def encrypt_password(self, password):
        """Encrypts a password using Fernet encryption."""
        return self.cipher_suite.encrypt(password.encode())
    
    def decrypt_password(self, encrypted_password):
        """Decrypts an encrypted password using Fernet decryption."""
        return self.cipher_suite.decrypt(encrypted_password).decode()
    
    def save_password(self):
        """Saves a new password entry."""
        website = self.entry_website.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Encrypt password before storing it
        encrypted_password = self.encrypt_password(password)
        
        # Store password information in the passwords dictionary
        self.passwords[website] = {
            "username": username,
            "encrypted_password": encrypted_password.decode()  # Convert bytes to string
        }
        
        self.save_passwords()  # Save passwords to a file
        
        # Clear entry fields after saving
        self.entry_website.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
    
    def get_password(self):
        """Retrieves and displays a stored password."""
        website = self.entry_website.get()
        
        if website in self.passwords:
            password_info = self.passwords[website]
            username = password_info["username"]
            encrypted_password = password_info["encrypted_password"].encode()  # Convert string to bytes
            password = self.decrypt_password(encrypted_password)
            
            # Update entry fields with retrieved data
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_username.insert(0, username)
            self.entry_password.insert(0, password)
        else:
            # Display a message if website is not found
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.entry_username.insert(0, "Website not found")
    # Loading the passwords.json file 
    def load_passwords(self):
        """Loads stored passwords from a file if it exists."""
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
                self.passwords = data
        except FileNotFoundError:
            pass
    
    def save_passwords(self):
        """Saves the passwords dictionary to a file."""
        with open("passwords.json", "w") as file:
            json.dump(self.passwords, file)

def main():
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
