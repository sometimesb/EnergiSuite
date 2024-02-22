from botasaurus import *
from user import NAME_ID_MAPPING
import customtkinter
import json
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import ttk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class Asset:
    def __init__(self, name, symbol, price, cgID=None,cgPrice=None):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.cgID = cgID
        self.cgPrice = cgPrice

    def __str__(self):
        return f"{self.name} {self.cgID} {self.price} {self.cgPrice}"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Energi Suite")
        self.geometry(f"{1100}x{580}")
        self.minsize(1100,580)
        self.maxsize(1100,580)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Energi Suite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Execute", command=self.execute)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Author Info", command=self.execute)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Execute to populate data.")
        self.textbox.configure(state="disabled")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=5, number_of_steps=100)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # self.user_profit_label = customtkinter.CTkLabel(self.slider_progressbar_frame, text="User Profit",font=customtkinter.CTkFont(size=15, weight="bold"),text_color="green", anchor="w")
        # self.user_profit_label.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="w")  # Position above the slider


        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Enable & Disable Coins")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def execute(self):
        self.textbox.configure(state="normal")
        self.textbox.delete(0.0, 'end')
        assets = getAssets()
        for asset in assets:
            print(asset)
            self.textbox.insert("0.0",asset)

def apiRequester(url,mode):
    @request(use_stealth=True, output="energi")
    def EnergiRequester(request: AntiDetectRequests, data):
        response = request.get(url)
        if response.status_code != 200:
            return "Error"
        return response.text
    
    @request(use_stealth=True, output="coingecko")
    def CoinGeckoRequester(request: AntiDetectRequests, data):
        response = request.get(url)
        if response.status_code != 200:
            return "Error"
        return response.text

    if mode == 0:
        return EnergiRequester()
    elif mode == 1:
        return CoinGeckoRequester()

def parseCoinGeckoData():
    data = json.loads(apiRequester("https://api.coingecko.com/api/v3/simple/price?ids=energi%2Cenergi-dollar%2Cdai%2Cethereum%2Cbitcoin%2Cusd-coin&vs_currencies=usd",1))
    print(data)

def coinGeckoLinkBuilder(mapping):
    base_url = "https://api.coingecko.com/api/v3/simple/price?ids="
    for k, v in mapping.items():
        base_url += v + "%2C"
    base_url+= "&vs_currencies=usd"
    return base_url

def getAssets():
    energiData = json.loads(apiRequester("https://api.energiswap.exchange/v1/assets",0))
    cgLink = coinGeckoLinkBuilder(NAME_ID_MAPPING)
    coinGeckoData = json.loads(apiRequester("https://api.coingecko.com/api/v3/simple/price?ids=energi%2Cenergi-dollar%2Cdai%2Cethereum%2Cbitcoin%2Cusd-coin&vs_currencies=usd",1))

    assets = []
    for key, value in energiData.items():
        if value["name"] in NAME_ID_MAPPING:
            cgID = NAME_ID_MAPPING.get(value["name"])
            asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
            assets.append(asset)
    
    for asset in assets:
        if asset.cgID in coinGeckoData:
            asset.cgPrice = coinGeckoData[asset.cgID]["usd"]
    
    return assets

if __name__ == "__main__":
    app = App()
    app.mainloop()