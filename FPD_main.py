#region Inports
import os
import subprocess
import sys
import copy

import FPD_installation_manager
#External Packages
required_packages = ["tabulate", "colorama"]
FPD_installation_manager.install_package_list(required_packages)

from colorama import init, Fore, Style, Back
from tabulate import tabulate

#Other Scripts
import FPD_file_finder

#endregion Inports


#region Variables
file_count_total: int = 0


#Current Status tracks our relevant menu variables to display them dynamically. The label is used
# as a display lable, the value alongside it. If it is none, it hides the value and just shows text
# The state is used for the total ready check. If all members are true the program will allow you to run it
# if not, it shows which have not completed the ready check.
current_status: dict = {
    "directory": {
        "label": "Target Directory",
        "value": "", #Could consider making 'os.getcwd()' the default
        "state": False,
        "function_call": "target_directory_manager",
    },
    "depth": {
        "label": "Folder Depth",
        "value": "All",
        "state": True,
        "function_call": "folder_depth_manager",
    },
    "extensions": {
        "label": "File Extension Rules",
        "value": "",
        "state": True,
        "function_call": "extension_manager",
    },
    "display": {
        "label": "Display Rules",
        "value": "Reduced",
        "state": True,
        "function_call": "display_manager"
    },
    "file_units":{
        "label": "File Size Units",
        "value": "GB",
        "state": True,
        "function_call": "file_unit_manager"
    },
    "size_rounding":{
        "label": "File Size Rounding",
        "value": "3",
        "state": True,
        "function_call": "file_rounding_manager"
    },
    "uninstall": {
        "label": "Uninstall Program",
        "value": "",
        "state": True,
        "function_call": "uninstall_manager"
    }
}

#TODO create a file_unit_manger
#TODO create a file_rounding_manage 


#Default extension and category pairs
default_extension_categories: dict = {
    "Video": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3"],
    "Image": [".png", ".jpg", ".jpeg"],
    "Executable": [".exe"],
}
#Used to store the temporary extension category
current_extension_categories: dict = copy.deepcopy(default_extension_categories)

#endregion Variables


#region Menu Functions
    # Called by the user to change and manage the target directory
def target_directory_manager():
    new_directory = input("Please enter a new directory:\n")
    if user_interrupt(new_directory) == True:
        main()
    elif not os.path.isdir(new_directory):
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + new_directory + Style.RESET_ALL + " is not a valid directory.\n" + "Please enter a valid directory." + "\n")
        return(target_directory_manager())
    else:
        current_status["directory"]["value"] = new_directory
        current_status["directory"]["state"] = True


    # Called by the user to change folder depth
def folder_depth_manager():
    new_depth = input("Please enter a new folder depth (type all for maximum depth):\n")
    if new_depth.isdigit():
        current_status["depth"]["value"] = new_depth
        current_status["depth"]["state"] = True
    elif new_depth.lower() == "all":
        current_status["depth"]["value"] = "All"
        current_status["depth"]["state"] = True
    elif user_interrupt(new_depth) == True:
        main()
    else:
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + new_depth + Style.RESET_ALL + " is not a valid depth.\n" + "Please enter a valid depth." + "\n")
        return(folder_depth_manager())


    #Allows the user to expand or contract the display
def display_manager():
    choice = input("Would you like to have the final file menu reduced? Y/N):\n")
    choice = str(choice).lower()
    if choice == 'y':
        current_status["display"]["value"] = "Reduced"
    elif choice == 'n':
        current_status["display"]["value"] = "Expanded"
    else:
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + choice + Style.RESET_ALL + " is not a valid depth.\n" + "Please enter a valid answser." + "\n")
        return(folder_depth_manager())


    #Allows for the user to uninstall the program
def uninstall_manager():
    choice = input("Are you certain, this would uninstall all installed packages, you have to delete the python files yourself though. Y/N):\n")
    choice = str(choice).lower()
    if choice == 'y':
        FPD_installation_manager.uninstall_package_list(required_packages)
        os._exit(0)
    elif choice == 'n':
        return(folder_depth_manager())
    else:
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + choice + Style.RESET_ALL + " is not a valid depth.\n" + "Please enter a valid answser." + "\n")
        return(folder_depth_manager())


    #Called by the user to manage extenion rules
    #NOTE The dictionary is passed in and handled in the form Category -> Extension, but when it is  processed
    #the dictionary is flipped at the start to allow for faster lookup times
def extension_manager():
    global current_extension_categories
    while True:
        os.system('cls')
        print(tabulate(current_extension_categories, headers="keys", tablefmt="github"))
        menu = [["0)", "Return to Main Menu"],["1)", "Add Category"],["2)", "Remove Category"],["3)", "Add Extension"],["4)", "Remove Extension"]]
        print("\n" + tabulate(menu))
        user_input = input("\nPlease select an option:\n ")
        match user_input:
            case "1":
                extension_add_category()
            case "2":
                extension_remove_category()
            case "3":
                extension_add_extension()
            case "4":
                extension_remove_extension()
            case value if user_interrupt(value) == True or value == "0":
                return #Goes back to main()
            case _:
                os.system('cls')
                print(Back.RED + user_input + " is an invalid choice, please try again " + Style.RESET_ALL + "\n")
                input("Press enter to continue...")


#region Extension Manager Helper Functions
    #Adds a category to the current_extension_categories dicionary
def extension_add_category():
    global current_extension_categories
    while True:
        user_input = input("\nPlease type a category name:\n")
        user_input = str(user_input).title()
        if user_interrupt(user_input) == True:
            return #Goes back extension_manager()
        elif user_input in current_extension_categories:
            print("\n"+ user_input + " - is already present")
            input("Press enter to continue...")
            return
        elif user_input == "Other":
            print("\n"+ user_input + " - is an invalid name")
            input("Press enter to continue...")
            return
        else:
            current_extension_categories.update({user_input : []})
            print("\n"+ user_input + " - added")
            input("Press enter to continue...")
            return


    #Removes a category from the current_extension_categories dictionary
def extension_remove_category():
    global current_extension_categories
    while True:
        user_input = input("\nPlease type a category name:\n")
        user_input = user_input.title()
        if user_input in current_extension_categories:
            current_extension_categories.pop(user_input)
            print("\n" + user_input + " - removed")
            input("Press enter to continue...")
            return
        elif user_interrupt(user_input) == True:
            return #Goes back extension_manager()
        else:
            print("\n" + Back.RED + user_input + " is an invalid choice, please try again " + Style.RESET_ALL + "\n")
            input("Press enter to continue...")
            return
        

    #Adds an extension to the current_extension_categories dictionary
def extension_add_extension():
    global current_extension_categories
    while True:
        user_input = input("\nPlease type a category name:\n")
        user_input = user_input.title()
        if user_interrupt(user_input) == True:
            return #Goes back extension_manager()
        elif user_input in current_extension_categories:
            extension_input = input ("\nPlease enter extension name:\n")
            if extension_input in current_extension_categories[user_input]:
                print("\n" + extension_input + " - alreayd in " + user_input + " Please try again")
                input("Press enter to continue...")
                return
            elif extension_input.startswith("."):
                current_extension_categories[user_input].append(extension_input)
                print("\n" + extension_input + " - was added to " + user_input)
                input("Press enter to continue...")
                return
            else:
                print("\n" + Back.RED + extension_input + " is an not a valid extension name, please try again " + Style.RESET_ALL + "\n")
                input("Press enter to continue...")
                return
        else:
            print("\n" + Back.RED + user_input + " is an not a valid category name, please try again " + Style.RESET_ALL + "\n")
            input("Press enter to continue...")
            return


    #Removes an extension to the current_extension_categories dictionary
def extension_remove_extension():
    global current_extension_categories
    while True:
        user_input = input("\nPlease type a category name:\n")
        user_input = user_input.title()
        if user_interrupt(user_input) == True:
            return #Goes back extension_manager()
        elif user_input in current_extension_categories:
            extension_input = input ("\nPlease enter extension name:\n")
            if extension_input in current_extension_categories[user_input]:
                current_extension_categories[user_input].remove(extension_input)
                print("\n" + extension_input + " - was removed from " + user_input)
                input("Press enter to continue...")
                return
            else:
                print("\n" + Back.RED + extension_input + " is an not a valid extension name, please try again " + Style.RESET_ALL + "\n")
                input("Press enter to continue...")
                return
        else:
            print("\n" + Back.RED + user_input + " is an not a valid category name, please try again " + Style.RESET_ALL + "\n")
            input("Press enter to continue...")
            return
        

    #Used to change the units to measure the file size with
def file_unit_manager():
    new_unit = input("Please enter a unit size (Bytes, KB, MB, GB, or TB):\n")
    if new_unit.lower() in ("bytes", "kb", "mb", "gb", "tb"):
        current_status["file_units"]["value"] = new_unit.capitalize()
        current_status["file_units"]["value"] = new_unit.capitalize()
    else:
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + new_unit + Style.RESET_ALL + " is not a valid size.\n" + "Please enter a valid size." + "\n")
        return(folder_depth_manager())


    #Used to change the rounding value
def file_rounding_manager():
    new_rounding = input("Please enter a new rounding value:\n")
    if new_rounding.isdigit():
        current_status["size_rounding"]["value"] = new_rounding
        current_status["size_rounding"]["state"] = True
    elif user_interrupt(new_rounding) == True:
        main()
    else:
        os.system('cls')
        print("\n" + Back.RED + Fore.WHITE + new_rounding + Style.RESET_ALL + " is not a valid number.\n" + "Please enter a valid number." + "\n")
        return(folder_depth_manager())




# def file_size_converter(file_size: int, unit_size: str) -> float:
#     match(unit_size):
#         case "Bytes":
#             return file_size
#         case "KB":
#             return file_size * 0.001
#         case "MB":
#             return file_size * 0.000001
#         case "GB":
#             return file_size * 0.000000001
#         case "TB":
#             return file_size * 0.000000000001
#         case _:
#             return 0

#endregion Extension Manager and Helper Functions


#region Helper Functions
    #Called to check to see if the user types in quit or exit
def user_interrupt(input: str) -> bool:
    if input.lower() == "quit" or input.lower() == "exit":
        return True
    else:
        return False
#endregion Helper Functions


#region Main Loop
def main():
    #Prints the current_status dictionary for the user menu
    os.system('cls')
    while True:
        #Display Current Status
        count: int = 0
        menu: list = []
        for category in current_status:
            #Menu Variables
            label = current_status[category]["label"]
            value = current_status[category]["value"]
            state = current_status[category]["state"]
            state_text: str
            if state == True:
                state_text = Back.GREEN + "   Ready   " + Style.RESET_ALL
            else:
                state_text = Back.RED + " Not Ready " + Style.RESET_ALL
            function_call = current_status[category]["function_call"]
            
            menu.append([str(count) + ") ", label, value, state_text, function_call])
            count += 1

        #Table Creation (The last colum is sliced off using a for loop)   
        print(tabulate(
            [row[:-1] for row in menu], 
            headers=["#", "Name", "Value", "Status"],
            tablefmt="github")
            )
        
        #User Input Managment    
        user_input = input("\nSelect an Option or type 'run' to run the program:\n ")
        if user_input.isdigit() and int(user_input) <= count:
            user_choice = menu[int(user_input)][-1]
            os.system('cls')
            try:
                globals()[user_choice]()
            except:
                print(Back.RED + "Function label error" + Style.RESET_ALL + "\n")        
                input("Press enter to continue...")
            os.system('cls')
        elif user_input.lower() == "run":
            run_status = True
            for category in current_status:
                if (current_status[category]["state"] != True):
                    run_status = False
                    continue
            if (run_status == True):
                os.system('cls')
                FPD_file_finder.file_counter(current_status, current_extension_categories)
            else:
                os.system('cls')
                print(Back.RED + " Ready check failed " + Style.RESET_ALL + "\n")
        elif user_interrupt(user_input) == True:
            sys.exit()
        else:
            os.system('cls')
            print(Back.RED + user_input + " is an invalid choice, please try again " + Style.RESET_ALL + "\n")
#endregion Main Loop

main()