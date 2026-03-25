from colorama import init, Fore, Style, Back
import os
import sys



#TODO - Can't handle trailing _ need to adjust that later
#TODO - cannot currently handle folders, just has the option to turn it on
#TODO - add an option for getting rid of trailing numbers and then numbering them accordingly
#TODO - Add an option to replace all _ or - or both _ and _ with " "
#TODO - Make personal documentation talking about what you need to remember to make changes in the future




#region Variables

ready_status = [Back.RED + "NOT READY" + Style.RESET_ALL, Back.GREEN + "READY" + Style.RESET_ALL]
current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
options_file_types = [Back.RED + "Not Implemented" + Style.RESET_ALL]
options_folder_processing = ["No", "Yes"]
options_capitalization = ["Capitalize The First Letter of Every Word", "No Capital Letters"]
options_spacing = ["Spaces Before Numbers", "No Spaces Before Numbers", "Underscore Instead of Space", "No Spaces"]
options_underscore_settings = ["Replace Underscores With Spaces", "Replace Spaces With Underscores"]
options_numbering = ["Gallery DL Numbering Scheme","Number Sequentially", "No Added Numbers"]

current_settings = {
    "directory": current_directory,
    "file_types": options_file_types[0],
    "folder_processing": options_folder_processing[0],
    "capitalization": options_capitalization[0],
    "spacing": options_spacing[0],
    "underscore_settings": options_underscore_settings[0],
    "numbering": options_numbering[0],
    "run_status": ready_status[1],
}


current_settings_display = []


#region Update Functions

def function_update_current_settings():
    global current_settings_display
    current_settings_display = [
        ["Run Status", current_settings["run_status"]], #0
        ["Current Directory ", current_settings["directory"]], #1
        ["Enabled File Types ", current_settings["file_types"]], #2
        ["Rename and Process Folders ", current_settings["folder_processing"]], #3
        ["Capitialization ", current_settings["capitalization"]], #4
        ["Spacing ", current_settings["spacing"]], #5
        ["Underscore Settings ", current_settings["underscore_settings"]], #6
        ["Number Settings", current_settings["numbering"]] #7
                                ]
    
#endregion Update Functions



#region Startup Functions

## Opening spiel for the user
def function_opening_prompt():
    print(Fore.CYAN + "\n\nHello and thank you for running my program. This program is meant to rename all of the files inside of a given directory. "
    "\nYou can type quit at any point to quit the program or ctrl+c to stop it at any time. Here are your current settings:\n\n" + Style.RESET_ALL)
    function_main_menu()


## The main menu where the user can select what settings to change or just run it
def function_main_menu():
    function_update_current_settings()
    option_selection(current_settings, "\n\nPlease select the setting you wish to change: ")

#endregion Startup Functions



#region Option Functions

#Handles Option selection
def option_selection(option_index, msg: str):
    while True:
        print(Fore.YELLOW + msg + ":\n" + Style.RESET_ALL)
        if option_index is current_settings:
            for index, (name, option) in enumerate(current_settings_display):
                print(f"{index}) {name:<30}: {option}")
        else:        
            for index, item in enumerate(option_index):
                print(str(index) + ") " + item)
        #Choice selection
        input_selection = input(Fore.GREEN + "\nSelect a Number: " + Style.RESET_ALL)
        if input_selection.isdigit():
            selected_index = int(input_selection)
        
            if 0 <= selected_index <= len(option_index)-1:
                break
                                        
            else:
                print("\n" + Back.RED + Fore.WHITE + "Error: Index invalid, please try again." + Style.RESET_ALL + "\n")
        
        elif input_selection.lower() == "quit":
            quit()

        else:
            print("\n" + Back.RED + Fore.WHITE + "Error: Please enter a number." + Style.RESET_ALL + "\n")

    if option_index is current_settings:
        match int(input_selection):
            #Directory Settings
            case 0:
                run_file_processing()
            case 1:
                current_settings["directory"] = function_directory_change()                
                function_main_menu()
            #File Type Settings
            case 2:
                print("\n" + Fore.GREEN + "Sorry, but this feature is not implimented yet." + Style.RESET_ALL + "\n")
                function_main_menu()
            #Folder Processing Setting
            case 3:
                current_settings["folder_processing"] = options_folder_processing[function_configuration_folders()]
                function_main_menu()
            #Capitalization Processing
            case 4:
                current_settings["capitalization"] = options_capitalization[function_configuration_capitalization()]
                function_main_menu()
            #Spacing Processing
            case 5:
                current_settings["spacing"] = options_spacing[function_configuration_spaces()]
                function_main_menu()
            case 6:
                current_settings["underscore_settings"] = options_underscore_settings[function_underscore_replacement_processing()]
                function_main_menu()
            case 7:
                current_settings["numbering"] = options_numbering[function_configuration_numbering()]
                function_main_menu()
            case _:
                print("\n" + Back.RED + Fore.WHITE + "Error: Non-implemented Case" + Style.RESET_ALL + "\n")
    else:
        return int(input_selection)


#Allows the user to change the current directory
def function_directory_change():
    new_directory = input("Please enter the path to the directory you want to execute on:\n> ")
    if new_directory == "quit":
        quit()
    elif not os.path.isdir(new_directory):
        print("\n" + Back.RED + Fore.WHITE + "Error: Please enter a valid directory." + Style.RESET_ALL + "\n")
        return(function_directory_change())
    else:
        os.chdir(new_directory)
        return new_directory


#Captures the configurations that user can do
def function_configuration_capitalization():
    return option_selection(options_capitalization, "How would you like your files capitalized")
       

#User input regarding spaces
def function_configuration_spaces():
    return option_selection(options_spacing, "How would you like to handle spacing")


def function_configuration_folders():
    return option_selection(options_folder_processing, "Would you like to rename folders")

def function_configuration_numbering():
    return option_selection(options_folder_processing, "Would you like to handle tailing numbers")

#endregion Option Functions



#region Processing Functions

#Folder and File Exclusion function
def function_file_processing(option: str):
    path = current_settings["directory"]
    dir_list = os.listdir(path)
    match option:
        #All files and folders
        case "Yes":
            return(dir_list)
        #All files no folders
        case "No":
            files = [
                f for f in dir_list 
                if os.path.isfile(os.path.join(path, f))
            ]
            return files


#Capitalization Function
def function_capitalization_processing(option, file_name):
    match option:
        case "Capitalize The First Letter of Every Word":
            #First Letter of every word
            return file_name.title()
        case "No Capital Letters":
            #All lower case
            return file_name.lower()


#Spacing Function
def function_spacing_processing(option, file_name):
    length = len(file_name)

    while length > 0 and file_name[length - 1].isdigit():
        length -= 1

    #No numbers
    if length == len(file_name):
        return file_name
    
    i = length
    while length > 0 and file_name[length - 1] == " ":
        length -= 1
    
    front_half = file_name[:length]
    back_half = file_name[i:]

    match option:
        case "Spaces Before Numbers":
            return f"{front_half.rstrip("_ ")} {back_half}"
        
        case "No Spaces Before Numbers":
            return f"{front_half.rstrip("_")}{back_half}"
        
        case "Underscore Instead of Space":
            return f"{front_half.rstrip("_")}_{back_half}"
        
        case "No Spaces":
            return f"{front_half.rstrip("_").replace(' ', '')}{back_half}"
        
        case _:
            return file_name


#Underscore and Spacing Replacement
def function_underscore_replacement_processing(option, file_name):
    match option:
        case "Replace Underscores With Spaces":
            return file_name.replace('_', ' ')
        
        case "Replace Spaces With Underscores":
            return file_name.replace(' ', '_')
        
        case _:
            return file_name


#Processes tailing numbers
def function_tailing_number_processing(option, file):
    
    match option:
        case "Gallery DL Numbering Scheme":
            length = len(file)
            #Itterate past the file numbers
            while file[length-1].isdigit() and length > 0:
                length = length - 1
            #Remove the GalleryDL Idenetity numbers
            length = length - 1
            while file[length-1].isdigit() and length > 0:
                file = file[:length]+file[length+1:]
                length = length - 1
            file = file[:length]+file[length+1:]
            return file
        case _:
            return



#Runs all of the file processing code and renames the files.
def run_file_processing():
    files = function_file_processing(current_settings["folder_processing"])
    for file in files:
        name, ext = os.path.splitext(file)
        new_name = function_capitalization_processing(current_settings["capitalization"], name)
        new_name = function_spacing_processing(current_settings["spacing"], new_name)
        new_name = function_underscore_replacement_processing(current_settings["underscore_settings"], new_name)
        new_name = function_tailing_number_processing(current_settings["numbering"], new_name)
        new_name = new_name + ext


        old_path = os.path.join(current_settings["directory"], file)
        new_path = os.path.join(current_settings["directory"], new_name)
        if old_path == new_path:
              print(Fore.YELLOW + f"Skipping {file}. old_path == new_path" + Style.RESET_ALL)
        if old_path != new_path:
            if os.path.exists(new_path):
                print(f"\n{Back.RED + Fore.WHITE}Error: file {new_path} already exists, abandoning work on {old_path}{Style.RESET_ALL}\n")
            else:
                os.rename(old_path, new_path)
                print(Fore.CYAN + "File renamed from:\n" + Style.RESET_ALL + old_path + Fore.GREEN + "\nto the new name:\n" + Style.RESET_ALL + new_path)    
    #Final Check to remove 0s from single files and keep them on series
    processed_files = function_file_processing(current_settings["folder_processing"])
    for file in processed_files:
        name, ext = os.path.splitext(file)
        length = len(name)
        if name[length-1] == "0" and not name[length-2].isdigit():
            new_name = name.rstrip("_0 ")
            one_name = new_name + " 1" + ext
            new_name = new_name + ext

            old_path = os.path.join(current_settings["directory"], file)
            new_path = os.path.join(current_settings["directory"], new_name)
            one_file_path = os.path.join(current_settings["directory"], one_name)
            if not os.path.exists(one_file_path):
                if os.path.exists(new_path):
                    print(f"\n{Back.RED + Fore.WHITE}Error: file {new_path} already exists in 0 strip, abandoning work on {old_path}{Style.RESET_ALL}\n")
                else:
                    os.rename(old_path, new_path)
    print(Back.GREEN + "Finished Job" + Style.RESET_ALL)
    function_main_menu()
#endregion Processing Functions



#Initial Start
function_opening_prompt()
