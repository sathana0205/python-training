import streamlit as st

# --- Bank Account Class ---
class BankAccount:
    def _init_(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return f"Deposited ₹{amount}. New Balance: ₹{self.__balance}"
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid withdrawal amount."
        elif amount > self.__balance:
            return "Insufficient funds."
        else:
            self.__balance -= amount
            return f"Withdrawn ₹{amount}. Remaining Balance: ₹{self.__balance}"

    def get_balance(self):
        return self.__balance


# --- Streamlit UI ---
st.title("🏦 OOP BANK DEMO")

# Store account object in session state to persist across actions
if 'account' not in st.session_state:
    st.session_state.account = None

# Create Account
st.subheader("Create New Account")
name = st.text_input("Enter Account Holder Name")
initial_balance = st.number_input("Initial Balance", min_value=0, step=100)

if st.button("Create Account"):
    if name:
        st.session_state.account = BankAccount(name, initial_balance)
        st.success(f"✅ Account created for {name} with balance ₹{initial_balance}")
    else:
        st.warning("Please enter a name to create an account.")

# Deposit
st.subheader("Deposit Money")
deposit_amount = st.number_input("Deposit Amount", min_value=0, step=100, key="deposit")

if st.button("Deposit"):
    if st.session_state.account:
        msg = st.session_state.account.deposit(deposit_amount)
        st.info(msg)
    else:
        st.error("Please create an account first!")

# Withdraw
st.subheader("Withdraw Money")
withdraw_amount = st.number_input("Withdraw Amount", min_value=0, step=100, key="withdraw")

if st.button("Withdraw"):
    if st.session_state.account:
        msg = st.session_state.account.withdraw(withdraw_amount)
        st.info(msg)
    else:
        st.error("Please create an account first!")

# Check Balance
if st.session_state.account:
    st.subheader("💰 Current Balance")
    st.write(f"Account Holder: *{st.session_state.account.account_holder}*")
    st.write(f"Balance: ₹{st.session_state.account.get_balance()}")