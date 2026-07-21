#The package_manager is meant to check to check whether
# packages are installed or not and allow for the removal
# and instilation of packages. 

import subprocess
import sys
import urllib.request

#region Functions
    #Checks for a connection to the python servers
def connect(host="https://pypi.org"):
    try:
        urllib.request.urlopen(host, timeout=5)
        return True
    except:
        return False

    #Installs passed in packages
def install_package(package_name: str, connection: bool):
    if connection == False:
        print("No internet connection detected")
        print("This program requires the instilation of some packages to function")
        print("Please connect to the internet and try again")
        sys.exit()
    else:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(package_name + " was installed successfully")
        else:
            print(package_name + " failed to install")
            print("Error: " + result.stderr)
            print("Exiting FPD")
            sys.exit()

    #Uninstalls packages from a passed in list.
def uninstall_package_list(package_list: list):
    for package in package_list:
        try:
            __import__(package)
            print("Uninstalling: " + package)
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            print("Succsessfully removed: " + package)
        except ImportError:
            print(package + "is already uninstalled/not found")
print("\nPackage list uninstalled")

    #Calls install_package for each package passed in
def install_package_list(package_list: list):
    internet: bool
    if not connect():
        print("Internet connection is not available")
        internet = False
    else:
        internet = True

    for package in package_list:
        try:
            __import__(package)
            print(package + " is already installed")
        except ImportError as e:
            print("Error: ", e, "\nAttepting instilation...")
            install_package(package, internet)


#endregion Functions