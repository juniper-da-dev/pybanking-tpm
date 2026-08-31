import os
import platform

def Menu():
    Clear()
    print("=================")
    print("1.) Open Account")
    print("2.) Deposit")
    print("3.) Withdraw")
    print("4.) Change Account Information")
    print("5.) Grab Account Information")
    print("6.) Exit")
    print("=================")

    selection = input("\n> ")
    return selection


def InfoMenu():
    Clear()
    print("=================")
    print("1.) Balance Inquiry")
    print("2.) Name")
    print("3.) Exit")
    print("=================")

    selection = input("\n> ")
    return selection


def Clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def ChangeInfoMenu():
    Clear()
    print("=================")
    print("1.) Pin")
    print("2.) Name")
    print("3.) Exit")
    print("=================")

    selection = input("\n> ")
    return selection