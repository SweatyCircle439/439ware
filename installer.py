import customtkinter
import tkinter
import requests
import markdown2
import webbrowser
import os

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
    
def display_md(content):
        html_content = markdown2.markdown(content)
        with open('temp.html', 'w', encoding='utf-8') as temp_file:
            temp_file.write(html_content)
        webbrowser.open('temp.html')
        os.remove('temp.html')



customtkinter.set_ctk_parent_class(tkinter.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("install ware")

def button_callback():
    print("Button click", combobox_1.get())


def slider_callback(value):
    progressbar_1.set(value)


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text="install ware")
label_1.pack(pady=10, padx=10)

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback)
button_1.pack(pady=10, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
slider_1.pack(pady=10, padx=10)
slider_1.set(0.5)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
entry_1.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
optionmenu_1.pack(pady=10, padx=10)
optionmenu_1.set("CTkOptionMenu")

combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
combobox_1.pack(pady=10, padx=10)
combobox_1.set("CTkComboBox")

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
checkbox_1.pack(pady=10, padx=10)

radiobutton_var = customtkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
radiobutton_1.pack(pady=10, padx=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
radiobutton_2.pack(pady=10, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1)
switch_1.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "CTkTextbox\n\n\n\n")

segmented_button_1 = customtkinter.CTkSegmentedButton(master=frame_1, values=["CTkSegmentedButton", "Value 2"])
segmented_button_1.pack(pady=10, padx=10)

tabview_1 = customtkinter.CTkTabview(master=frame_1, width=300)
tabview_1.pack(pady=10, padx=10)
tabview_1.add("CTkTabview")
tabview_1.add("Tab 2")

app.mainloop()