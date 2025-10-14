import streamlit as st
import json
import os

DATA_FILE = "bank_data.json"

# ---------- Save data to JSON ----------
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Load existing data ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                st.warning("JSON file was empty or corrupted. Starting fresh.")
                return {}
    else:
        return {}

# ---------- Create account ----------
def create_account(data):
    st.subheader("Create New Account")
    name = st.text_input("Account Holder Name").strip()
    pin = st.text_input("4-digit PIN", type="password").strip()
    balance = st.number_input("Initial Balance", min_value=0.0)

    if st.button("Create Account"):
        if name in data:
            st.error(f"Account for '{name}' already exists!")
        else:
            data[name] = {"account_holder": name, "pin": pin, "balance": balance}
            save_data(data)
            st.success(f"Account for {name} added successfully!")
    return data

# ---------- Display accounts ----------
def display_accounts(data):
    st.subheader("All Bank Accounts")
    if not data:
        st.info("No accounts found.")
    else:
        for account in data.values():
            st.write(f"**Name:** {account['account_holder']} | **PIN:** {account['pin']} | **Balance:** ₹{account['balance']}")

# ---------- Update account ----------
def update_account(data):
    st.subheader("Update Account")
    name = st.text_input("Enter Account Holder Name to Update").strip()
    if name in data:
        option = st.radio("What would you like to update?", ["PIN", "Balance"])
        if option == "PIN":
            new_pin = st.text_input("Enter New 4-digit PIN", type="password").strip()
            if st.button("Update PIN"):
                data[name]['pin'] = new_pin
                save_data(data)
                st.success(f"PIN updated for {name}")
        elif option == "Balance":
            new_balance = st.number_input("Enter New Balance", min_value=0.0)
            if st.button("Update Balance"):
                data[name]['balance'] = new_balance
                save_data(data)
                st.success(f"Balance updated for {name}")
    elif name:
        st.error(f"Account for '{name}' does not exist!")
    return data

# ---------- Delete account ----------
def delete_account(data):
    st.subheader("Delete Account")
    name = st.text_input("Enter Account Holder Name to Delete").strip()
    if name in data:
        if st.button(f"Delete '{name}'"):
            del data[name]
            save_data(data)
            st.success(f"Account '{name}' deleted successfully!")
    elif name:
        st.error(f"Account for '{name}' does not exist!")
    return data

# ---------- Main Streamlit App ----------
def main():
    st.title("🏦 Bank Account Manager")
    menu = ["Create Account", "Display Accounts", "Update Account", "Delete Account"]
    choice = st.sidebar.selectbox("Menu", menu)

    data = load_data()

    if choice == "Create Account":
        data = create_account(data)
    elif choice == "Display Accounts":
        display_accounts(data)
    elif choice == "Update Account":
        data = update_account(data)
    elif choice == "Delete Account":
        data = delete_account(data)

if __name__ == "__main__":
    main()