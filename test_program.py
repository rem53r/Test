import keyboard, time, wmi, requests, customtkinter, threading, json, os, uuid, re

config_path = "C:\\BhopConfig\\config.json"
programm_exit_bool = False
config_status: bool = True
config_bind = 'end'
config_delay = 1
config_divider = 50

def save_config() -> None:
    config_data = {
        "bind": bind_box.get(),
        "delay": int(delay_slider.get()),
        "divider": int(divider_slider.get()),
        "status": config_status
    }
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file)

def load_config() -> None:
    global config_bind, config_divider, config_delay, config_status
    try:
        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            config_bind = config_data.get("bind", 'end')
            config_delay = config_data.get("delay", 1)
            config_divider = config_data.get("divider", 50)
            config_status = config_data.get("status", True)
    except FileNotFoundError:
        pass

def change_status() -> None:
    global config_status
    config_status = not config_status

def bhop_method() -> None:
    global config_status
    while True:
        time.sleep(float(int(config_delay) / int(config_divider)))
        if programm_exit_bool:
            exit()
        if not config_status:
            continue
        if keyboard.is_pressed('space'):
            keyboard.press_and_release('space')

def on_programm_exit() -> None:
    global programm_exit_bool
    if not os.path.exists("C:\\BhopConfig"):
        os.makedirs("C:\\BhopConfig")
    save_config()
    programm_exit_bool = True
    programm.destroy()

def update_text() -> None:
    button_status_info.set("Status: " + ("On" if config_status else "Off"))
    sliders_delay_info.set('Delay: ' + str(int(delay_slider.get())) + ' / ' + str(int(divider_slider.get())))
    programm.after(500, update_text)

load_config()

programm = customtkinter.CTk()
programm.protocol("WM_DELETE_WINDOW", on_programm_exit)

programm.title('t.me/remula222')
programm.resizable(False, False)
programm.geometry('255x205')

button_status_info = customtkinter.StringVar()
sliders_delay_info = customtkinter.StringVar()
button_status_info.set("Status: " + ("On" if config_status else "Off"))

logo_text = customtkinter.CTkLabel(master=programm, text='bunnyhop.im')
logo_text.pack(pady=5, padx=5)

programm_frame = customtkinter.CTkFrame(master=programm)
programm_frame.pack(pady=5, padx=5, fill="both", expand=True)

status_button = customtkinter.CTkButton(master=programm_frame, textvariable=button_status_info, width=210, command=change_status)
status_button.pack(pady=5, padx=5)

bind_box = customtkinter.CTkEntry(master=programm_frame, placeholder_text='Bind', width=210)
bind_box.pack(pady=5, padx=5)
bind_box.insert('insert', config_bind)

delay_slider = customtkinter.CTkSlider(master=programm_frame, from_=1, to=20, width=210)
delay_slider.pack(pady=5, padx=5)
delay_slider.set(config_delay)

divider_slider = customtkinter.CTkSlider(master=programm_frame, from_=1, to=100, width=210)
divider_slider.pack(pady=5, padx=5)
divider_slider.set(config_divider)

sliders_delay_info.set('Delay: ' + str(int(delay_slider.get())) + ' / ' + str(int(divider_slider.get())))

sliders_delay_text = customtkinter.CTkLabel(master=programm_frame, textvariable=sliders_delay_info)
sliders_delay_text.pack(pady=5, padx=5)

if __name__ == '__main__':
    keyboard.add_hotkey(config_bind, change_status)
    threading.Thread(target=bhop_method).start()
    update_text()
    programm.mainloop()

