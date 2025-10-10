import json 
import os 
DATA_FILE = "bank_data.json" 
 
data = {} 
 
def load_data(): 
    if os.path.exists(DATA_FILE): 
        with open(DATA_FILE, "r") as f: 
            data = json.load(f) 
        return data 
    return {} 
 
def save_data(data): 
    with open(DATA_FILE, "w") as f: 
        json.dump(data, f, indent=4) 
 
def add_account(data): 
    name = input("Enter account holder name: ").strip() 
 
    if name in data: 
        print(f"Account for '{name}' already exists!") 
        return data 
 
    pin = input("Enter 4-digit PIN: ").strip() 
    balance = float(input("Enter initial balance: ")) 
 
    data[name] = { 
        "account_holder": name, 
        "pin": pin, 
        "balance": balance 
    } 
    print(f"\nAccount for {name} added successfully!") 
    return data 
     
data=load_data() 
data=add_account(data)
save_data(data)
print(load_data())