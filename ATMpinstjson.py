import streamlit as st 
 
# ---------- BankAccount Class ---------- 
class BankAccount: 
    def _init_(self, account_holder, pin, balance=0): 
        self.account_holder = account_holder 
        self.__pin = pin 
        self.__balance = balance 
 
    def verify_pin(self, pin): 
        return self.__pin == pin 
 
    def deposit(self, amount): 
        if amount > 0: 
            self.__balance += amount 
            return f"Deposited ₹{amount}. New balance: ₹{self.__balance}" 
        else: 
            return "Invalid deposit amount." 
 
    def withdraw(self, amount): 
        if amount <= 0: 
            return "Invalid withdrawal amount." 
        elif amount > self.__balance: 
            return "Insufficient funds." 
        else: 
            self.__balance -= amount 
            return f"Withdrew ₹{amount}. Remaining balance: ₹{self.__balance}" 
 
    def get_balance(self): 
        return self.__balance 
 
# ---------- Streamlit UI ---------- 
st.set_page_config(page_title="ATM System", page_icon="&&&") 
st.title("ATM System") 
 
# Initialize session state 
if "account" not in st.session_state: 
    st.session_state.account = None 
if "logged_in" not in st.session_state: 
    st.session_state.logged_in = False 
 
# Navigation 
menu = st.sidebar.radio("Menu", ["Create Account", "Login", "ATM Operations"]) 
 
# ---------- CREATE ACCOUNT ---------- 
if menu == "Create Account": 
    st.header("Step 1: Create Account") 
    name = st.text_input("Enter account holder name:") 
    pin = st.text_input("Set 4-digit PIN", type="password", max_chars=4) 
    initial_balance = st.number_input("Initial Deposit", min_value=0, step=100) 
 
    if st.button("Create Account"): 
        if not name.strip(): 
            st.warning("Enter a valid name.") 
        elif not pin.isdigit() or len(pin) != 4: 
            st.warning("PIN must be a 4-digit number.") 
        else: 
            st.session_state.account = BankAccount(name.strip(), pin, initial_balance) 
            print(st.session_state.account) 
            st.success(f"Account created for {name} with ₹{initial_balance}") 
            st.info("Go to 'Login' page from the sidebar to access ATM services.") 
 
# ---------- LOGIN PAGE ---------- 
elif menu == "Login": 
    st.header("Step 2: Login to Your Account") 
 
    if st.session_state.account is None: 
        st.warning("No account found. Please create one first.") 
    else: 
        entered_pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4) 
 
        if st.button("Login"): 
            if st.session_state.account.verify_pin(entered_pin): 
                st.session_state.logged_in = True 
                st.success(f"Welcome {st.session_state.account.account_holder}! Login successful.") 
                st.info("Go to 'ATM Operations' page to perform transactions.") 
            else: 
                st.error("Incorrect PIN. Try again.") 
 
# ---------- ATM OPERATIONS ---------- 
elif menu == "ATM Operations": 
    st.header("Step 3: ATM Operations") 
 
    if not st.session_state.logged_in: 
        st.warning("Please log in first from the 'Login' page.") 
    elif st.session_state.account is None: 
        st.warning("No active account. Please create one.") 
    else: 
        action = st.radio("Choose an action", ["Deposit", "Withdraw", "Check Balance"]) 
 
        if action == "Deposit": 
            amount = st.number_input("Enter deposit amount", min_value=0, step=100, key="dep") 
            if st.button("Deposit"): 
                st.info(st.session_state.account.deposit(amount)) 
 
        elif action == "Withdraw": 
            amount = st.number_input("Enter withdrawal amount", min_value=0, step=100, key="with") 
            if st.button("Withdraw"): 
                st.info(st.session_state.account.withdraw(amount)) 
 
        elif action == "Check Balance": 
            st.success(f"Your current balance is ₹{st.session_state.account.get_balance()}") 
 
        if st.button("Logout"): 
            st.session_state.logged_in = False 
st.success("Logged out successfully.")
import json
import os

DATA_FILE = "bank_data.json"


# --- Data Handling ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- Streamlit App ---
st.set_page_config(page_title="Bank Account Manager", page_icon="🏦", layout="centered")
st.title("Bank Account Manager")

data = load_data()

menu = st.sidebar.selectbox("Menu", ["Add Account", "Update Account", "Delete Account", "View Accounts"])

# --- Add Account ---
if menu == "Add Account":
    st.subheader("Add New Account")

    name = st.text_input("Account Holder Name").strip()
    pin = st.text_input("4-digit PIN", type="password").strip()
    balance = st.number_input("Initial Balance", min_value=0.0, step=0.01)

    if st.button("Add Account"):
        if name in data:
            st.error(f"⚠ Account for '{name}' already exists!")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("⚠ PIN must be exactly 4 digits.")
        else:
            data[name] = {
                "account_holder": name,
                "pin": pin,
                "balance": balance,
            }
            save_data(data)
            st.success(f"Account for '{name}' added successfully!")


# --- Update Account ---
elif menu == "Update Account":
    st.subheader("Update Account")

    if data:
        name = st.selectbox("Select account to update", list(data.keys()))

        if name:
            new_balance = st.number_input(
                "New Balance", min_value=0.0, step=0.01, value=data[name]["balance"]
            )
            new_pin = st.text_input("New 4-digit PIN (optional)", type="password")

            if st.button("Update"):
                if new_pin and (len(new_pin) != 4 or not new_pin.isdigit()):
                    st.error("⚠ PIN must be 4 digits if provided.")
                else:
                    if new_pin:
                        data[name]["pin"] = new_pin
                    data[name]["balance"] = new_balance
                    save_data(data)
                    st.success(f"Account '{name}' updated successfully!")
    else:
        st.info("No accounts found to update.")


# --- Delete Account ---
elif menu == "Delete Account":
    st.subheader("Delete Account")

    if data:
        name = st.selectbox("Select account to delete", list(data.keys()))

        if st.button("Delete Account"):
            del data[name]
            save_data(data)
            st.warning(f"🗑 Account '{name}' deleted successfully!")
    else:
        st.info("No accounts available to delete.")


# --- View Accounts ---
elif menu == "View Accounts":
    st.subheader("View All Accounts")

    if data:
        for name, details in data.items():
            st.write(f"Account Holder: {details['account_holder']}")
            st.write(f"Balance: ${details['balance']:.2f}")
            st.write("---")
    else:
        st.info("No accounts available.")


st.sidebar.info("Data is stored locally in 'bank_data.json'")