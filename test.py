import json
import os

DATABASE_FILE = "database.json"


# =========================
# Database Handling
# =========================

def load_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            json.dump({"users": {}}, f)
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


def save_database(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# Authentication System
# =========================

def sign_up():
    data = load_database()
    username = input("Enter username: ")

    if username in data["users"]:
        print("❌ Username already exists!")
        return

    password = input("Enter password: ")
    try:
        balance = float(input("Enter initial balance: "))
    except ValueError:
        print("❌ Invalid balance!")
        return

    data["users"][username] = {
        "password": password,
        "balance": balance
    }

    save_database(data)
    print("✅ Account created successfully!")


def log_in():
    data = load_database()
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in data["users"] and data["users"][username]["password"] == password:
        print("✅ Login successful!")
        return username
    else:
        print("❌ Invalid username or password!")
        return None


# =========================
# Financial Operations
# =========================

def deposit(username):
    data = load_database()
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            return
    except ValueError:
        print("❌ Invalid amount!")
        return

    data["users"][username]["balance"] += amount
    save_database(data)
    print("✅ Deposit successful!")


def withdraw(username):
    data = load_database()
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            return
    except ValueError:
        print("❌ Invalid amount!")
        return

    if data["users"][username]["balance"] >= amount:
        data["users"][username]["balance"] -= amount
        save_database(data)
        print("✅ Withdrawal successful!")
    else:
        print("❌ Insufficient balance!")


def transfer(username):
    data = load_database()
    receiver = input("Enter receiver username: ")

    if receiver not in data["users"]:
        print("❌ Receiver not found!")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            return
    except ValueError:
        print("❌ Invalid amount!")
        return

    if data["users"][username]["balance"] >= amount:
        data["users"][username]["balance"] -= amount
        data["users"][receiver]["balance"] += amount
        save_database(data)
        print("✅ Transfer successful!")
    else:
        print("❌ Insufficient balance!")


# =========================
# Dashboard
# =========================

def dashboard(username):
    while True:
        data = load_database()
        print("\n===== DASHBOARD =====")
        print(f"Username: {username}")
        print(f"Balance: {data['users'][username]['balance']}")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            deposit(username)
        elif choice == "2":
            withdraw(username)
        elif choice == "3":
            transfer(username)
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice!")


# =========================
# Main Menu
# =========================

def main():
    while True:
        print("\n===== DIGITAL WALLET =====")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            user = log_in()
            if user:
                dashboard(user)
        elif choice == "3":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()