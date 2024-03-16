import customtkinter
import tkinter
import requests
import markdown2
from pathlib import Path
import os
import ctypes
import sys
import tkhtmlview
import shutil
import subprocess
import winshell
import time

app = customtkinter.CTk()
app.geometry("400x600")
app.maxsize(width=400, height=600) 
app.minsize(width=400, height=600)
app.resizable(0,0)
app.title("install ware console")
app.iconbitmap("logo.ico")

def create_shortcut(source_path, target_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs")):
    # Create a shortcut to the source file
    winshell.CreateShortcut(
        Path=os.path.join(target_folder, "ware.lnk"),
        Target=source_path,
        Description="ware",
        Icon=(os.path.join(source_path.replace(source_path.split("\\")[-1], ""), "logo.ico"), 0),
    )

def remove_shortcut(source_path, target_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs")):
    os.remove(os.path.join(target_folder, "ware.lnk"))

customtkinter.set_ctk_parent_class(tkinter.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
def create_and_move_folder_to_program_files(folder_name, files_and_folders=[],
        program_files_dir=os.environ['ProgramFiles']):
    try:
        # Create a temporary directory to hold the files
        temp_dir = os.path.join(os.environ['TEMP'], folder_name)
        os.makedirs(temp_dir, exist_ok=True)

        # Recursively create files and subfolders
        def create_files_and_folders(base_path, items):
            for item in items:
                item_path = os.path.join(base_path, item['name'])
                if 'content' in item:  # File
                    with open(item_path, 'wb') as f:
                        f.write(item['content'])
                elif 'items' in item:  # Subfolder
                    if not os.path.exists(item_path):
                        os.makedirs(item_path, exist_ok=True)
                        print(f"Created folder: {item_path}")
                    create_files_and_folders(item_path, item['items'])

        create_files_and_folders(temp_dir, files_and_folders)

        # Move the entire folder to Program Files
        program_files_path = program_files_dir
        dest_dir = os.path.join(program_files_path, folder_name)
        if os.path.exists(dest_dir):
            for file in os.listdir(temp_dir):
                shutil.move(os.path.join(temp_dir, file), dest_dir)
        else:
            shutil.move(temp_dir, dest_dir)
        time.sleep(1)
        for file in os.listdir(os.path.join(dest_dir, "439ware")):
            if file == "ware.exe":
                create_shortcut(os.path.join(os.path.join(dest_dir, "439ware"), file))

    except PermissionError:
        try:
            # Define ShellExecuteInfo structure
            class ShellExecuteInfo(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("fMask", ctypes.c_ulong),
                    ("hwnd", ctypes.c_void_p),
                    ("lpVerb", ctypes.c_wchar_p),
                    ("lpFile", ctypes.c_wchar_p),
                    ("lpParameters", ctypes.c_wchar_p),
                    ("lpDirectory", ctypes.c_wchar_p),
                    ("nShow", ctypes.c_int),
                    ("hInstApp", ctypes.c_void_p),
                    ("lpIDList", ctypes.c_void_p),
                    ("lpClass", ctypes.c_wchar_p),
                    ("hkeyClass", ctypes.c_void_p),
                    ("dwHotKey", ctypes.c_ulong),
                    ("hIconOrMonitor", ctypes.c_void_p),
                    ("hProcess", ctypes.c_void_p)
                ]

            # Create the temporary directory if it doesn't exist
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Recursively create files and subfolders
            def create_files_and_folders_elevated(base_path, items):
                for item in items:
                    item_path = os.path.join(base_path, item['name'])
                    if 'content' in item:  # File
                        with open(item_path, 'wb') as f:
                            f.write(item['content'])
                    elif 'items' in item:  # Subfolder
                        if not os.path.exists(item_path):
                            os.makedirs(item_path, exist_ok=True)
                        create_files_and_folders_elevated(item_path, item['items'])

            create_files_and_folders_elevated(temp_dir, files_and_folders)

            # Move the entire folder to Program Files
            program_files_path = program_files_dir
            dest_dir = os.path.join(program_files_path, folder_name)

            # Set up ShellExecuteInfo
            sei = ShellExecuteInfo()
            sei.cbSize = ctypes.sizeof(sei)
            sei.lpVerb = "runas"  # Run with elevated permissions
            sei.lpFile = "cmd.exe"  # Command to execute
            sei.lpParameters = f"/c move \"{temp_dir}\" \"{dest_dir}\""  # Command parameters
            sei.nShow = 0  # SW_HIDE (do not display the window)

            # Call ShellExecuteEx
            if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
                raise ctypes.WinError()
            time.sleep(1)
            for file in os.listdir(os.path.join(dest_dir, "439ware")):
                if file == "ware.exe":
                    create_shortcut(os.path.join(os.path.join(dest_dir, "439ware"), file))
        except Exception as e:
            print(f"Error: {e}")
            if "exists" in str(e):
                errorwindow = customtkinter.CTk()
                errorwindow.geometry("250x150")
                def repair():
                    try:
                        subprocess.run(['cmd', '/c', 'rmdir', '/S', '/Q', dest_dir], check=True, shell=True)
                        print(f"Directory '{dest_dir}' deleted successfully.")
                        errorwindow.destroy()
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to delete directory '{dest_dir}': {e}")
                    remove_shortcut(os.path.join(os.path.join(dest_dir, "439ware"), file))
                    create_and_move_folder_to_program_files(folder_name, files_and_folders, program_files_dir)
                def delete():
                    try:
                        subprocess.run(['cmd', '/c', 'rmdir', '/S', '/Q', dest_dir], check=True, shell=True)
                        print(f"Directory '{dest_dir}' deleted successfully.")
                    except subprocess.CalledProcessError as e:
                        print(f"Failed to delete directory '{dest_dir}': {e}")
                    remove_shortcut(os.path.join(os.path.join(dest_dir, "439ware"), file))
                    os._exit(0)
                customtkinter.CTkLabel(errorwindow, text=f"you already have 439ware installed").pack(pady=20, padx=20)
                customtkinter.CTkButton(errorwindow, command=repair, text="repair").pack(pady=5, padx=20)
                customtkinter.CTkButton(errorwindow, command=delete, text="delete").pack(pady=5, padx=20)
                errorwindow.mainloop()
            else:
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if "exists" in str(e):
            errorwindow = customtkinter.CTk()
            errorwindow.geometry("250x150")
            def repair():
                try:
                    subprocess.run(['cmd', '/c', 'rmdir', '/S', '/Q', dest_dir], check=True, shell=True)
                    print(f"Directory '{dest_dir}' deleted successfully.")
                    errorwindow.destroy()
                except subprocess.CalledProcessError as e:
                    print(f"Failed to delete directory '{dest_dir}': {e}")

                create_and_move_folder_to_program_files(folder_name, files_and_folders, program_files_dir)
            def delete():
                try:
                    subprocess.run(['cmd', '/c', 'rmdir', '/S', '/Q', dest_dir], check=True, shell=True)
                    print(f"Directory '{dest_dir}' deleted successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to delete directory '{dest_dir}': {e}")
                os._exit(0)
            customtkinter.CTkLabel(errorwindow, text=f"you already have 439ware installed").pack(pady=20, padx=20)
            customtkinter.CTkButton(errorwindow, command=repair, text="repair").pack(pady=5, padx=20)
            customtkinter.CTkButton(errorwindow, command=delete, text="delete").pack(pady=5, padx=20)
            errorwindow.mainloop()
        else:
            sys.exit(1)

def download_file_from_github(file_url, local_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        return False
    
def read_file_from_github(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.content
    else:
        return False
    
def display_md(content, window):
    html_content = markdown2.markdown(content)
    # Create a Text widget to display the Markdown content
    text_widget = tkhtmlview.HTMLLabel(window, html=html_content)
    text_widget.pack(expand=True, fill="both", padx=20, pady=20)

title = customtkinter.CTkLabel(app, justify=customtkinter.LEFT, text="install 439ware console", font=('tuple', 15, 'bold'))
title.pack(pady=0, padx=0)
disclaimerwindow = customtkinter.CTkFrame(app)
licensewindow = customtkinter.CTkFrame(app)
licensewindow.pack(pady=20, padx=20, fill="both", expand=True)
disclaimerwindow.pack(pady=20, padx=20, fill="both", expand=True)
disclaimerwindow.configure(width=10, height=0.1)

optionswindow = customtkinter.CTkFrame(master=app)
optionswindow.pack(pady=20, padx=20, fill="both", expand=True)
optionswindow.configure(width=10, height=0.1)

def startwindow():
    
    def button_callback():
        print("Button click", combobox_1.get())
        
    def slider_callback(value):
        progressbar_1.set(value)

    label_1 = customtkinter.CTkLabel(master=optionswindow, justify=customtkinter.LEFT, text="install ware")
    label_1.pack(pady=10, padx=10)

    progressbar_1 = customtkinter.CTkProgressBar(master=optionswindow)
    progressbar_1.pack(pady=10, padx=10)

    button_1 = customtkinter.CTkButton(master=optionswindow, command=button_callback)
    button_1.pack(pady=10, padx=10)

    slider_1 = customtkinter.CTkSlider(master=optionswindow, command=slider_callback, from_=0, to=1)
    slider_1.pack(pady=10, padx=10)
    slider_1.set(0.5)

    entry_1 = customtkinter.CTkEntry(master=optionswindow, placeholder_text="CTkEntry")
    entry_1.pack(pady=10, padx=10)

    optionmenu_1 = customtkinter.CTkOptionMenu(optionswindow, values=["Option 1", "Option 2", "Option 42 long long long..."])
    optionmenu_1.pack(pady=10, padx=10)
    optionmenu_1.set("CTkOptionMenu")

    combobox_1 = customtkinter.CTkComboBox(optionswindow, values=["Option 1", "Option 2", "Option 42 long long long..."])
    combobox_1.pack(pady=10, padx=10)
    combobox_1.set("CTkComboBox")

    checkbox_1 = customtkinter.CTkCheckBox(master=optionswindow)
    checkbox_1.pack(pady=10, padx=10)

    radiobutton_var = customtkinter.IntVar(value=1)

    radiobutton_1 = customtkinter.CTkRadioButton(master=optionswindow, variable=radiobutton_var, value=1)
    radiobutton_1.pack(pady=10, padx=10)

    radiobutton_2 = customtkinter.CTkRadioButton(master=optionswindow, variable=radiobutton_var, value=2)
    radiobutton_2.pack(pady=10, padx=10)

    switch_1 = customtkinter.CTkSwitch(master=optionswindow)
    switch_1.pack(pady=10, padx=10)

    text_1 = customtkinter.CTkTextbox(master=optionswindow, width=200, height=70)
    text_1.pack(pady=10, padx=10)
    text_1.insert("0.0", "CTkTextbox\n\n\n\n")

    segmented_button_1 = customtkinter.CTkSegmentedButton(master=optionswindow, values=["CTkSegmentedButton", "Value 2"])
    segmented_button_1.pack(pady=10, padx=10)

    tabview_1 = customtkinter.CTkTabview(master=optionswindow, width=300)
    tabview_1.pack(pady=10, padx=10)
    tabview_1.add("CTkTabview")
    tabview_1.add("Tab 2")

def options():
    global optionswindow
    customtkinter.CTkLabel(optionswindow, justify=customtkinter.LEFT, text="select directory", font=('tuple', 13, 'bold')).pack(pady=5, padx=10)
    dir = customtkinter.CTkComboBox(optionswindow, values=[
        str(os.getcwd().split("\\")[0] + "\\program files"),
        str(str(Path.home()))
    ])
    dir.pack(pady=10, padx=10)
    dir.set(str(os.getcwd().split("\\")[0] + "\\program files"))
    dir.configure(width=300)
    customtkinter.CTkLabel(optionswindow, justify=customtkinter.LEFT, text="packages", font=('tuple', 13, 'bold')).pack(pady=5, padx=10)
    ware = tkinter.BooleanVar(optionswindow, value=False)
    wareswitch = customtkinter.CTkSwitch(optionswindow, text="ware", variable=ware)
    wareswitch.pack(pady=5, padx=10)
    antiware = tkinter.BooleanVar(optionswindow, value=False)
    antiwareswitch = customtkinter.CTkSwitch(optionswindow, text="antiware", variable=antiware)
    antiwareswitch.pack(pady=5, padx=10)
    def start():
        newpath = dir.get()
        wareexecontent = read_file_from_github("https://raw.githubusercontent.com/SweatyCircle439/439ware/main/ware.exe")
        logoicocontent = read_file_from_github("https://raw.githubusercontent.com/SweatyCircle439/439ware/main/logo.ico")
        if ware.get():
            warepyconent = read_file_from_github("https://raw.githubusercontent.com/SweatyCircle439/439ware/main/RES/ware.py")
        if antiware.get():
            antiwarepyconent = read_file_from_github("https://raw.githubusercontent.com/SweatyCircle439/439ware/main/RES/antiware.py")
        folder_name = "SweatyCircle439"
        files_and_folders = [
            {
                "name": "439ware",
                "items": [
                    {
                        "name": "ware.exe",
                        "content": wareexecontent
                    },
                    {
                        "name": "logo.ico",
                        "content": logoicocontent
                    },
                    {
                        "name": "packages",
                        "items": []
                    }
                ]
            }
        ]
        if ware.get():
            for item in files_and_folders[0]["items"]:
                if item["name"] == "packages":
                    item["items"].append({
                        "name": "ware.py",
                        "content": warepyconent
                    })
        if antiware.get():
            for item in files_and_folders[0]["items"]:
                if item["name"] == "packages":
                    item["items"].append({
                        "name": "antiware.py",
                        "content": antiwarepyconent
                    })
        create_and_move_folder_to_program_files(folder_name, files_and_folders, newpath)
    startbutton = customtkinter.CTkButton(optionswindow, text="install", command=start)
    startbutton.pack(pady=10, padx=10)

def display_disclaimer():
    global disclaimerwindow

    customtkinter.CTkLabel(disclaimerwindow, justify=customtkinter.LEFT, text="Disclaimer").pack(pady=10, padx=10)
    display_md(
        read_file_from_github(
            "https://raw.githubusercontent.com/SweatyCircle439/439ware/main/installer/install.md"
        ), disclaimerwindow
    )
    def start():
        print("start")
        options()
        disclaimerwindow.destroy()

    def stop():
        os._exit(0)

    customtkinter.CTkButton(disclaimerwindow, text="accept", command=start).pack(pady=20, padx=10)
    customtkinter.CTkButton(disclaimerwindow, text="don't accept", command=stop).pack(pady=5, padx=10)

def display_license():
    global licensewindow
    customtkinter.CTkLabel(licensewindow, justify=customtkinter.LEFT, text="GNU GENERAL PUBLIC LICENSE").pack(pady=10, padx=10)
    display_md(
        read_file_from_github(
            "https://raw.githubusercontent.com/SweatyCircle439/439ware/main/LICENSE"
        ), licensewindow
    )
    def disclaim():
        display_disclaimer()
        licensewindow.destroy()

    def stop():
        os._exit(0)

    customtkinter.CTkButton(licensewindow, text="accept", command=disclaim).pack(pady=20, padx=10)
    customtkinter.CTkButton(licensewindow, text="don't accept", command=stop).pack(pady=5, padx=10)

display_license()

app.mainloop()