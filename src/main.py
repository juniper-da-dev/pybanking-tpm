#!/usr/bin/env python3

# 1.) Open Account
# 2.) Deposit
# 3.) Withdraw
# 4.) Change Pin
# 5.) Account Information
# 6.) Exit

import getpass
import time
from src.banking import open_account, change_info
from src.banking.accounting import withdraw, deposit
from src.banking.database import store_data, get_data
from src.banking.exceptions import no_acct
from src.core import Clear, Menu, ChangeInfoMenu, InfoMenu
from src.crypto.exceptions import incorrect_pin

finished = False

while not finished:
    try:
        selection = int(Menu())
    except ValueError:
        print("Please enter a valid number.")
        continue
    if selection == 1:  # Open Account
        Clear()
        while not finished:
            print("Whats your name?")
            name = str(input("> "))

            print("\nPin Number?")
            pin = str(getpass.getpass("> "))

            account_number = open_account(name, pin)
            print(f"\nYour account number is {account_number}, please keep it secure.")
            finished = True

    elif selection == 2:  # Deposit
        print("\nWhats your account number?")
        account = str(input("> "))

        print("\nHow much money do you want to deposit?")
        amount = str(input("> "))

        print("\nWhat is your pin number?")
        pin = str(getpass.getpass("> "))

        try:
            new_balance = deposit(amount, account, pin)
        except incorrect_pin:
            print("\nYour pin is incorrect, please try again.")
            time.sleep(3)
            finished = True
            break

        print("\nYour new balance is now {new_balance}.".format(new_balance=new_balance))
        finished = True
        break

    elif selection == 3:  # Withdraw
        print("\nWhats your account number?")
        account = str(input("> "))

        print("\nHow much money do you want to withdraw?")
        amount = str(input("> "))

        print("\nWhat is your pin number?")
        pin = str(getpass.getpass("> "))

        try:
            new_balance = withdraw(amount, account, pin)
        except incorrect_pin:
            print("\nYour pin is incorrect, please try again.")
            time.sleep(3)
            finished = True
            break

        print("\nYour new balance is now {new_balance}.".format(new_balance=new_balance))
        finished = True
        break

    elif selection == 4:  # Change Account Information 5773-7962-0642-8016
        selection = int(ChangeInfoMenu())
        if selection == 1:
            print("\nWhats your account number?")
            account = str(input("> "))

            print("\nWhats your current pin number?")
            old_pin = str(getpass.getpass("> "))

            print("\nYour new pin number?")
            new_pin = str(getpass.getpass("> "))

            try:
                change_info(account, "pin", new_pin, old_pin)
            except incorrect_pin:
                print("\nYour pin number is incorrect, please try again.")
                time.sleep(3)
                finished = True
                break
            except no_acct:
                print("\nSorry, your account number is invalid, please try again.")
                time.sleep(3)
                finished = True
                break

            Clear()
            finished = True
            break

        if selection == 2:
            print("\nWhats your account number?")
            account = str(input("> "))

            print("\nWhats your new name?")
            new_name = str(input("> "))

            print("\nWhat is your pin number?")
            pin = str(getpass.getpass("> "))

            try:
                store_data(account, "name", new_name, pin)
            except incorrect_pin:
                print("\nYour pin number is incorrect, please try again.")
                time.sleep(3)
                finished = True
                break
            except no_acct:
                print("\nSorry, your account number is invalid, please try again.")
                time.sleep(3)
                finished = True
                break

            Clear()
            finished = True
            break

        if selection == 3:
            Clear()
            finished = True
            break

    elif selection == 5:  # Grab Account Info
        selection = int(InfoMenu())
        if selection == 1:
            print("\nWhats your account number?")
            account = str(input("> "))

            print("\nWhat is your pin number?")
            pin = str(getpass.getpass("> "))

            try:
                balance = get_data(account, "balance", pin)
            except incorrect_pin:
                print("\nYour pin number is incorrect, please try again.")
                time.sleep(3)
                finished = True
                break
            except no_acct:
                print("\nSorry, your account number is invalid, please try again.")
                time.sleep(3)
                finished = True
                break

            print(f"\nYour balance is {balance}.")
            finished = True
            break

        if selection == 2:
            print("\nWhats your account number?")
            account = str(input("> "))

            print("\nWhat is your pin number?")
            pin = str(getpass.getpass("> "))

            try:
                name = get_data(account, "name", pin)
            except incorrect_pin:
                print("\nYour pin number is incorrect, please try again.")
                time.sleep(3)
                finished = True
                break
            except no_acct:
                print("\nSorry, your account number is invalid, please try again.")
                time.sleep(3)
                finished = True
                break

            print(f"\nYour name is {name}.")
            finished = True
            break

        if selection == 3:
            Clear()
            finished = True
            break

    elif selection == 6:  # Exit
        Clear()
        break

    else:
        print("Wrong input, please select a valid option.")
        continue
