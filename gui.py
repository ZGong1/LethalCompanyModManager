################################################
#                    TODO:                     #
#       Delete mod button                      #
#       Update mod button                      # 
#       include version somehow                #
#       Add useful error messages              #
#                                              #         
################################################



import os
import tkinter as tk
from tkinter import filedialog
import requests
import zipfile


# Initialization
folder_path = r"C:\Program Files (x86)\Steam\steamapps\common\Lethal Company\BepInEx\plugins\\"
enabledList = []
disabledList = []
# Split enabled (.dll) mods and disabled (.disabled) 
try:
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
except:
    folder_path = filedialog.askdirectory()+"\\"
    print(folder_path)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

for file in files:
    if ".dll" in file:
        enabledList.append(file[:-4])
    if ".disabled" in file:
        disabledList.append(file[:-9])





#Download file function
def download(url):
    response = requests.get(url)
    file_name_split = url.split("/")
    file_name = file_name_split[6] + "_" + file_name_split[7] + ".zip"

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"File {file_name} downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

    return file_name


#update listbox for enabled mods
def display_enabled():
    listbox1.delete(0, tk.END)  # Clear the existing items
    for item in enabledList:
        listbox1.insert(tk.END, item)


#update listbox for disabled mods
def display_disabled():
    listbox2.delete(0, tk.END)
    for item in disabledList:
        listbox2.insert(tk.END, item)

#Disables the mod selected
def disableMod():
    selected_item = listbox1.get(tk.ACTIVE)
    if selected_item:
        disabledMod = selected_item
        os.rename(folder_path + disabledMod + ".dll", folder_path + disabledMod + ".disabled")
        enabledList.remove(disabledMod)
        disabledList.append(disabledMod)
        display_enabled()
        display_disabled()

#Enables the mod selected
def enableMod():
    selected_item = listbox2.get(tk.ACTIVE)
    if selected_item:
        enabledMod = selected_item
        os.rename(folder_path + enabledMod + ".disabled", folder_path + enabledMod + ".dll")
        disabledList.remove(enabledMod)
        enabledList.append(enabledMod)
        display_enabled()
        display_disabled()

#installs new mod
def installNew():
    print(f"downloading {entry.get()}")
    fileLoc = download(entry.get())
    targetDLL = None

    #unzip dll file only
    with zipfile.ZipFile(fileLoc, 'r') as zip_ref:
        for item in zip_ref.namelist():
            if ".dll" in item:
                targetDLL = item
        zip_ref.extract(targetDLL, folder_path)
    enabledList.append(targetDLL.split(".")[0])
    display_enabled()
    os.remove(fileLoc)






# Create the main window
root = tk.Tk()
root.title("Mod Manager")

# Create a Listbox to display the enabled mods
listbox1 = tk.Listbox(root, width=40, height=10)
listbox1.grid(row=1, column=0, padx=10, pady=10)

# Create a Button to disable a mod
disable_button = tk.Button(root, text="Disable Mod", command=disableMod)
disable_button.grid(row=2, column=0, padx=10, pady=5)

# Create a Listbox to display the disabled mods
listbox2 = tk.Listbox(root, width=40, height=10)
listbox2.grid(row=1, column=1, padx=10, pady=10)

# Create a Button to enable a mod
enable_button = tk.Button(root, text="Enable Mod", command=enableMod)
enable_button.grid(row=2, column=1, padx=10, pady=5)

# Create a Button to install new mods
install_button = tk.Button(root, text="Install new mod", command=installNew)
install_button.grid(row = 0, column=0)

# To install link entry
entry = tk.Entry(root, width=30)
entry.grid(row = 0, column = 1)


# Display the initial list of enabled mods
display_enabled()
display_disabled()

# Run the Tkinter main loop
root.mainloop()
