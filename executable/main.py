from botasaurus import *
from user import NAME_ID_MAPPING_CRYPTO_MODE
import customtkinter
import json
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import ttk
import colorama

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
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Energi Suite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Execute", command=self.execute)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.running_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Running Mode:", anchor="w")
        self.running_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.running_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["USD Mode", "Crypto Mode"],command=self.running_mode_event)
        self.running_mode_menu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Execute to populate data.")
        self.textbox.configure(state="disabled")

        #tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("USDMode Parameters")
        self.tabview.tab("USDMode Parameters").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.add("CryptoMode Parameters")
        self.tabview.tab("CryptoMode Parameters").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        #first tabview
        self.slider_1 = customtkinter.CTkSlider(self.tabview.tab("USDMode Parameters"), from_=0, to=10, number_of_steps=100,command=self.slider_event_1)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.text_var_r_1 = tkinter.StringVar(value="")
        self.entry_1 = customtkinter.CTkLabel(self.tabview.tab("USDMode Parameters"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.text_var_r_1)
        self.entry_1.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        #second tabview
        self.text_var_r_2 = tkinter.StringVar(value="")
        self.slider_2 = customtkinter.CTkSlider(self.tabview.tab("CryptoMode Parameters"), from_=0, to=10, number_of_steps=100,button_color="blue",command=self.slider_event_2)
        self.slider_2.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.entry_2 = customtkinter.CTkLabel(self.tabview.tab("CryptoMode Parameters"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.text_var_r_2)
        self.entry_2.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        # create scrollable frame
        self.scrollable_frame_USD = customtkinter.CTkScrollableFrame(self, label_text="USD Coin Selection")
        self.scrollable_frame_USD.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_USD.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_USD = []

        # Create switches with specific values
        self.switch_values = ["DAI", "USDC", "USDE"]
        for value in self.switch_values:
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame_USD, text=value)
            switch.grid(row=len(self.scrollable_frame_switches_USD), column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches_USD.append(switch)

        self.scrollable_frame_CG = customtkinter.CTkScrollableFrame(self, label_text="Crypto Coin Selection")
        self.scrollable_frame_CG.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_CG.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_CG = []

        # Access key values from dictionary
        coin_names = list(NAME_ID_MAPPING_CRYPTO_MODE.keys())

        for name in coin_names:
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame_CG, text=name)
            switch.grid(row=len(self.scrollable_frame_switches_CG), column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches_CG.append(switch)

        #set defaults
        self.text_var_r_1.set(f"{round(float(self.slider_1.get()), 1)}%")
        self.text_var_r_2.set(f"{round(float(self.slider_2.get()), 2)}%")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.running_mode_menu.set("Crypto Mode")
        self.running_mode_event("Crypto Mode")
    
    def running_mode_event(self, mode):
        if mode == "USD Mode":
            self.tabview.set("USDMode Parameters")
            self.slider_2.configure(state="disabled")
            self.slider_1.configure(state="normal")
            for self.switch in self.scrollable_frame_switches_CG:
                self.switch.configure(state="disabled")  
            for self.switch in self.scrollable_frame_switches_USD:
                self.switch.configure(state="normal") 

        elif mode == "Crypto Mode":
            self.slider_1.configure(state="disabled")
            self.slider_2.configure(state="normal")

            self.tabview.set("CryptoMode Parameters")
            for self.switch in self.scrollable_frame_switches_USD:
                self.switch.configure(state="disabled")
                self.switch.toggle()
            for self.switch in self.scrollable_frame_switches_CG:
                self.switch.configure(state="normal") 

        else:
            # Handle invalid mode (optional)
            print("Invalid mode:", mode)

    def slider_event_1(self,value):
        self.text_var_r_1.set(f"{round(float(self.slider_1.get()), 1)}%")

    def slider_event_2(self,value):
        self.text_var_r_2.set(f"{round(float(self.slider_2.get()), 1)}%")

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
            self.textbox.insert("0.0","\n")

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
    cgLink = coinGeckoLinkBuilder(NAME_ID_MAPPING_CRYPTO_MODE)
    coinGeckoData = json.loads(apiRequester("https://api.coingecko.com/api/v3/simple/price?ids=energi%2Cenergi-dollar%2Cdai%2Cethereum%2Cbitcoin%2Cusd-coin&vs_currencies=usd",1))

    assets = []
    for key, value in energiData.items():
        if value["name"] in NAME_ID_MAPPING_CRYPTO_MODE:
            cgID = NAME_ID_MAPPING_CRYPTO_MODE.get(value["name"])
            asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
            assets.append(asset)
    
    for asset in assets:
        if asset.cgID in coinGeckoData:
            asset.cgPrice = coinGeckoData[asset.cgID]["usd"]
    
    return assets

if __name__ == "__main__":
    app = App()
    app.mainloop()

    