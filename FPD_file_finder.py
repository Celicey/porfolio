# Description: Called by main to search a directory and grab needed information
import os
import pathlib

#Counts the files and prints the results
def file_counter(current_status: dict, current_extension_categories: dict):
    target_directory = current_status["directory"]["value"]
    converted_extension_categories = convert_extension_dictionary(current_extension_categories)
    #Tracked Variables
    file_count_total: int = 0
    folder_count_total: int = 0
    file_size_total: float = 0

    for root, dirs, files in os.walk(target_directory):
        for file in files:
            file_count_total += 1
            file_extension = pathlib.Path(str(file)).suffix            
            checker = False

            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_size_total += file_size

            for category in converted_extension_categories:            
                if (str(file_extension) in converted_extension_categories[category]):
                    stats = converted_extension_categories[category][file_extension]
                    stats["count"] += 1
                    stats["size"] += file_size 
                    checker = True 
                    continue
            
            if (checker == False):
                if ("Other" not in converted_extension_categories):
                    converted_extension_categories["Other"] = {}
                #Checks to see if the display is reduced or expanded
                if (current_status["display"]["value"] == "Reduced"):
                    if ("file" not in converted_extension_categories["Other"]):
                        converted_extension_categories["Other"]["file"] = {"count": 0, "size": 0}
                    converted_extension_categories["Other"]["file"]["count"] += 1
                    converted_extension_categories["Other"]["file"]["size"] += file_size
                else:
                    if(str(file_extension) not in converted_extension_categories["Other"]):
                        converted_extension_categories["Other"][str(file_extension)] = {"count": 0, "size": 0}
                    converted_extension_categories["Other"][str(file_extension)]["count"] += 1
                    converted_extension_categories["Other"][str(file_extension)]["size"] += file_size

        for dir in dirs:
            folder_count_total += 1
        #Limits the depth of the search
        if (str(current_status["depth"]["value"]).lower() != "all"):
            directory = target_directory.rstrip(os.path.sep)
            dicrectory_depth = directory.count(os.path.sep)
            current_dicrectory_depth = root.count(os.path.sep)
            if dicrectory_depth + int(current_status["depth"]["value"]) <= current_dicrectory_depth:
                del dirs[:]


    rounded_converted_total_size = str(round(file_size_converter(file_size_total, current_status["file_units"]["value"]), int(current_status["size_rounding"]["value"])))
    print("File Count Total: " + str(file_count_total) + 
          "\nFile Size Total: " + rounded_converted_total_size + " " + current_status["file_units"]["value"] + 
          "\nFolder Count Total: " + str(folder_count_total) + "\n\n")
    #Displays the file category tree along with file count
    round_file_size(converted_extension_categories, current_status["size_rounding"]["value"], current_status["file_units"]["value"])
    # converted_dictionary: dict, longest_extension: int, longest_count: int, longest_size: int, file_units: str = "GB"
    longest_extension = find_longest_extension(converted_extension_categories)
    longest_count = find_longest_count(converted_extension_categories)
    longest_size = find_longest_size(converted_extension_categories)
    file_units = current_status["file_units"]["value"]
    display_extension_dictionary(converted_extension_categories, longest_extension, longest_count, longest_size, file_units)
    input("\n\nPress enter to run again...")


#region Helper Functions
    #Used to convert a dictionary into one that tracks the number of occurences
def convert_extension_dictionary(dictionary: dict) -> dict:
    new_dictionary = {}
    for category, extension_list in dictionary.items():
        extension_sub_dictionary = {}
        for extension in extension_list:
            extension_sub_dictionary[extension] = {"count": 0, "size": 0}
        new_dictionary[category] = extension_sub_dictionary
    return new_dictionary


    #Finds the length of the longest extension
def find_longest_extension(converted_dictionary: dict) -> int:
    longest_extension: int = 0

    for category in converted_dictionary.keys():
        for extension in converted_dictionary[category]:
            new_length = len(str(extension))
            if (new_length > longest_extension):
                longest_extension = new_length
    return longest_extension


def find_longest_count(converted_dictionary: dict) -> int:
    longest_count = 0

    for category in converted_dictionary.keys():
        for extension in converted_dictionary[category]:
            new_length = len(str(converted_dictionary[category][extension]["count"]))
            if (new_length > longest_count):
                longest_count = new_length
    return longest_count


#Finds the longest size for formatting purposes
def find_longest_size(converted_dictionary: dict) -> int:
    longest_size = 0

    for category in converted_dictionary.keys():
        for extension in converted_dictionary[category]:
            new_length = len(str(converted_dictionary[category][extension]["size"]))
            if (new_length > longest_size):
                longest_size = new_length
    return longest_size


#Rounds the file sizes down to the user defined level
def round_file_size(converted_dictionary: dict, rounding:str = "3", file_units: str = "GB"):
    for category in converted_dictionary.keys():
        for extension in converted_dictionary[category]:
            size_value = int(converted_dictionary[category][extension]["size"])
            size_value = file_size_converter(size_value, file_units)
            size_value = str(round(size_value, int(rounding)))
            converted_dictionary[category][extension]["size"] = size_value
    return


#Takes in a file and a size unit and returns the files size in that unit
def file_size_converter(file_size: int, unit_size: str) -> float:
    match(unit_size):
        case "Bytes":
            return file_size
        case "KB":
            return file_size / 1024
        case "MB":
            return file_size / 1048576
        case "GB":
            return file_size / 1073741824
        case "TB":
            return file_size / 1099511627776
        case _:
            return 0


    #Displays the converted dictionary as a tree graph
def display_extension_dictionary(converted_dictionary: dict, longest_extension: int, longest_count: int, longest_size: int, file_units: str = "GB"):
    elbow = "└──"
    tee = "├──"
    pipe = "│  "
    blank = "   "

    #Prints the tree 
    for category in converted_dictionary.keys():
        end: bool = False
        if (list(converted_dictionary).index(category) == len(converted_dictionary)-1):
            print(elbow + category)
            end = True
        else:
            print(tee + category)

        for extension in converted_dictionary[category]:
            section = ""
            
            count_value = str(converted_dictionary[category][extension]["count"])
            
            size_value = str(converted_dictionary[category][extension]["size"])

            #as stands for alignment spaces
            as_extension_name = " " * (longest_extension - len(extension))
            as_count = " " * (longest_count - len(str(count_value)))
            as_size = " " * (longest_size - len(str(size_value)))

            if (list(converted_dictionary[category]).index(extension) == len(converted_dictionary[category]) - 1):
                section = elbow + extension + as_extension_name + " - " + "Count: " + count_value + as_count + "  |  " + "Size: " + size_value + as_size + "  " + file_units
                           
            else:
                section = tee + extension + as_extension_name +  " - " + "Count: " + count_value + as_count + "  |  " + "Size: " + size_value + as_size + "  " + file_units
                           
            
            if(end == False):
                print (pipe + section)
            else:
                print(blank + section)
#endregion Helper Functions