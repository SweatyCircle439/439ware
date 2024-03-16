import os
import shutil
import ctypes
import sys

def create_and_move_folder_to_program_files(folder_name, files_and_folders=[]):
    try:
        # Create a temporary directory to hold the files
        temp_dir = os.path.join(os.environ['TEMP'], folder_name)
        os.makedirs(temp_dir, exist_ok=True)

        # Recursively create files and subfolders
        def create_files_and_folders(base_path, items):
            for item in items:
                item_path = os.path.join(base_path, item['name'])
                if 'content' in item:  # File
                    with open(item_path, 'w') as f:
                        f.write(item['content'])
                elif 'items' in item:  # Subfolder
                    os.makedirs(item_path, exist_ok=True)
                    create_files_and_folders(item_path, item['items'])

        create_files_and_folders(temp_dir, files_and_folders)

        # Move the entire folder to Program Files
        program_files_path = os.environ['ProgramFiles']
        dest_dir = os.path.join(program_files_path, folder_name)
        shutil.move(temp_dir, dest_dir)

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
                        with open(item_path, 'w') as f:
                            f.write(item['content'])
                    elif 'items' in item:  # Subfolder
                        os.makedirs(item_path, exist_ok=True)
                        create_files_and_folders_elevated(item_path, item['items'])

            create_files_and_folders_elevated(temp_dir, files_and_folders)

            # Move the entire folder to Program Files
            program_files_path = os.environ['ProgramFiles']
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

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Usage
folder_name = "MyNewFolder"
files_and_folders = [
    {
        "name": "file1.txt",
        "content": "Content of file1"
    },
    {
        "name": "subfolder1",
        "items": [
            {
                "name": "file2.txt",
                "content": "Content of file2"
            },
            {
                "name": "file3.txt",
                "content": "Content of file3"
            },
            {
                "name": "subfolder2",
                "items": [
                    {
                        "name": "file4.txt",
                        "content": "Content of file4"
                    },
                    {
                        "name": "file5.txt",
                        "content": "Content of file5"
                    }
                ]
            }
        ]
    }
]
create_and_move_folder_to_program_files(folder_name, files_and_folders)
