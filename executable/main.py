from botasaurus import *
from user import NAME_ID_MAPPING_CRYPTO_MODE,NAME_ID_MAPPING_USD_MODE
import customtkinter
import json
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import ttk
import threading
import time

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
        self.configure_window()
        self.create_sidebar_frame()
        self.create_textbox()
        self.create_scrollable_frames()
        self.set_defaults()

    def configure_window(self):
        """Configures the window title, geometry, and grid layout."""

        self.title("Energi Suite")
        self.geometry(f"{1100}x{580}")
        self.minsize(1100, 580)
        self.maxsize(1100, 580)

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_sidebar_frame(self):
        """Creates the sidebar frame with its widgets."""
        self.auto_execute_status = False  # Initialize auto_execute_status

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Energi Suite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.running_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Running Mode:", anchor="w")
        self.running_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.running_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["USD Mode", "Crypto Mode"], command=self.running_mode_event)
        self.running_mode_menu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Execute", command=lambda: threading.Thread(target=self.execute, args=(self.running_mode_menu.get(),)).start())
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Start Auto Execute", command=self.toggle_auto_execute)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

    def create_textbox(self):
        """Creates the textbox with its initial text and disabled state."""

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Execute to populate data.")
        self.textbox.configure(state="disabled")

        #tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("USDMode")
        self.tabview.tab("USDMode").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.add("CryptoMode")
        self.tabview.tab("CryptoMode").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.add("AutoRun Timer")
        self.tabview.tab("AutoRun Timer").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        #first tabview
        self.slider_1 = customtkinter.CTkSlider(self.tabview.tab("USDMode"), from_=0, to=10, number_of_steps=100,command=self.slider_event_1)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.text_var_r_1 = tkinter.StringVar(value="")
        self.entry_1 = customtkinter.CTkLabel(self.tabview.tab("USDMode"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.text_var_r_1)
        self.entry_1.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        #second tabview
        self.text_var_r_2 = tkinter.StringVar(value="")
        self.slider_2 = customtkinter.CTkSlider(self.tabview.tab("CryptoMode"), from_=0, to=10, number_of_steps=100,button_color="blue",button_hover_color="blue",command=self.slider_event_2)
        self.slider_2.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.entry_2 = customtkinter.CTkLabel(self.tabview.tab("CryptoMode"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.text_var_r_2)
        self.entry_2.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        #third tabview
        self.text_var_r_3 = tkinter.StringVar(value="")
        self.slider_3 = customtkinter.CTkSlider(self.tabview.tab("AutoRun Timer"), from_=10, to=60, number_of_steps=50,button_color="red",button_hover_color="red",command=self.slider_event_3)
        self.slider_3.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.entry_3 = customtkinter.CTkLabel(self.tabview.tab("AutoRun Timer"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.text_var_r_3)
        self.entry_3.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

    def create_scrollable_frames(self):
        """Creates scrollable frames for USD and Crypto coin selections with switches."""

        # Define a common function for creating switches
        def create_switches(frame, mapping, switch_list):
            for symbol in [value[1] for key, value in mapping.items()]:
                switch = customtkinter.CTkSwitch(master=frame, text=symbol)
                switch.grid(row=len(switch_list), column=0, padx=10, pady=(0, 20))
                switch_list.append(switch)

        # Create USD Coin Selection frame
        self.scrollable_frame_USD = customtkinter.CTkScrollableFrame(self, label_text="USD Coin Selection")
        self.scrollable_frame_USD.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_USD.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_USD = []
        create_switches(self.scrollable_frame_USD, NAME_ID_MAPPING_USD_MODE, self.scrollable_frame_switches_USD)

        # Create Crypto Coin Selection frame
        self.scrollable_frame_CG = customtkinter.CTkScrollableFrame(self, label_text="Crypto Coin Selection")
        self.scrollable_frame_CG.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_CG.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches_CG = []
        create_switches(self.scrollable_frame_CG, NAME_ID_MAPPING_CRYPTO_MODE, self.scrollable_frame_switches_CG)

    def set_defaults(self):
        """Sets default values for text variables, option menus, and triggers an event."""

        self.text_var_r_1.set(f"{round(float(self.slider_1.get()), 1)}%")
        self.text_var_r_2.set(f"{round(float(self.slider_2.get()), 2)}%")
        self.text_var_r_3.set(f"{round(int(self.slider_3.get()), 2)}s")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.running_mode_menu.set("Crypto Mode")
        self.running_mode_event("Crypto Mode")

    def running_mode_event(self, mode):
        if mode == "USD Mode":
            self.tabview.set("USDMode")
            self.slider_2.configure(state="disabled")
            self.slider_1.configure(state="normal")
            for self.switch in self.scrollable_frame_switches_CG:
                self.switch.configure(state="disabled")  
            for self.switch in self.scrollable_frame_switches_USD:
                self.switch.configure(state="normal") 

        elif mode == "Crypto Mode":
            self.slider_1.configure(state="disabled")
            self.slider_2.configure(state="normal")

            self.tabview.set("CryptoMode")
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
    
    def slider_event_3(self,value):
        self.text_var_r_3.set(f"{round(int(self.slider_3.get()), 1)}s")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def toggle_auto_execute(self):
        """Toggle AutoExecute on or off."""
        if self.auto_execute_status:
            # Stop AutoExecute
            self.auto_execute_status = False
            self.sidebar_button_2.configure(text="Start Auto Execute", command=self.toggle_auto_execute)
            self.textbox.configure(state="normal")
            self.textbox.delete(0.0, 'end')
            self.textbox.insert("0.0", "Stopped auto execution.")
            self.textbox.configure(state="disabled")
            for self.switch in self.scrollable_frame_switches_CG:
                self.switch.configure(state="normal")  
            for self.switch in self.scrollable_frame_switches_USD:
                self.switch.configure(state="normal") 
        else:
            # Start AutoExecute
            self.auto_execute_status = True
            threading.Thread(target=self.AutoExecute, args=(self.running_mode_menu.get(),)).start()
            self.sidebar_button_2.configure(text="Stop Auto Execute", command=self.toggle_auto_execute)
    
    def AutoExecute(self, runningMode):
        timer_value = int(self.text_var_r_3.get().replace("s", ""))
        sleep_time = timer_value - time.time() % timer_value  # Calculate sleep time once
        
        while self.auto_execute_status:

            for self.switch in self.scrollable_frame_switches_CG:
                self.switch.configure(state="disabled")  
            for self.switch in self.scrollable_frame_switches_USD:
                self.switch.configure(state="disabled") 

            self.execute(runningMode)  # Execute the search and update textbox
            # Update timer and text in the textbox
            self.textbox.configure(state="normal")
            self.textbox.insert("0.0", f"Timer: {timer_value}s\n")
            self.textbox.configure(state="disabled")

            # Sleep for the specified timer interval, minus the time spent in the loop
            if sleep_time > 0:
                time.sleep(sleep_time)
            sleep_time = timer_value  # Update sleep time for the next iteration

    def execute(self, runningMode):
        self.textbox.configure(state="normal")

        assets = self.getAssets(runningMode)
        any_assets_added = False
        self.textbox.delete(0.0, 'end')

        for asset in assets:
            if (runningMode == "Crypto Mode") and float(self.text_var_r_2.get().replace('%', '')) < self.profitPercent(asset.price, asset.cgPrice):
                self.textbox.insert("0.0", asset.symbol + " " + str(self.profitPercent(asset.price, asset.cgPrice)) + "%\n")
                any_assets_added = True
            elif (runningMode == "USD Mode") and float(self.text_var_r_1.get().replace('%', '')) < self.profitPercent(asset.price, asset.cgPrice):
                self.textbox.insert("0.0", asset.symbol + " " + str(self.profitPercent(asset.price, asset.cgPrice)) + "%\n")
                any_assets_added = True

        if not any_assets_added:
            self.textbox.insert("0.0", "Search completed, nothing met minimum profit requirement or no coins enabled.\n")

        self.textbox.configure(state="disabled")

    def profitPercent(self, energiPrice, cgPrice):
        if cgPrice is None or energiPrice is None:
            return None  
        try:
            if cgPrice == 0:
                return float('inf') 
            else:
                return (abs(energiPrice-cgPrice))/((energiPrice+cgPrice)/2)*100
        except ZeroDivisionError:
            return None

    def apiRequester(self,url,mode):
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

    def coinGeckoLinkBuilder(self,mapping):
        base_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        for k, v in mapping.items():
            # Use the 0th index value (name) for the link
            base_url += v[0] + "%2C"
        base_url += "&vs_currencies=usd"
        return base_url

    def getAssets(self,runningMode):
        try:
            energiData = json.loads(self.apiRequester("https://api.energiswap.exchange/v1/assets", 0))
        except:
            self.textbox.configure(state="normal")
            self.textbox.delete(0.0, 'end')
            self.textbox.insert("0.0", "API Limiter hit, please wait 60 seconds for EnergiSwap to unblock.\n")
            self.textbox.configure(state="disabled")

        switch_states = {}
                
        if runningMode == "Crypto Mode":
            cgLink = self.coinGeckoLinkBuilder(NAME_ID_MAPPING_CRYPTO_MODE)
            try:
                coinGeckoData = json.loads(self.apiRequester(cgLink, 1))
                print(coinGeckoData)
                for switch, name in zip(self.scrollable_frame_switches_CG, NAME_ID_MAPPING_CRYPTO_MODE):
                    toggle_value = switch.get()
                    switch_states[name] = toggle_value  
            except:
                self.textbox.configure(state="normal")
                self.textbox.delete(0.0, 'end')
                self.textbox.insert("0.0", "API Limiter hit, please wait 60 seconds for CoinGecko to unblock.\n")
                self.textbox.configure(state="disabled")

        else:
            try:
                cgLink = self.coinGeckoLinkBuilder(NAME_ID_MAPPING_USD_MODE)
                coinGeckoData = json.loads(self.apiRequester(cgLink, 1)) 
                for switch, name in zip(self.scrollable_frame_switches_USD, NAME_ID_MAPPING_USD_MODE):
                    toggle_value = switch.get()
                    switch_states[name] = toggle_value  
            except:
                self.textbox.configure(state="normal")
                self.textbox.delete(0.0, 'end')
                self.textbox.insert("0.0", "API Limiter hit, please wait 60 seconds for CoinGecko to unblock.\n")
                self.textbox.configure(state="disabled")


        assets = []
        for key, value in energiData.items():
            if runningMode == "Crypto Mode" and value["name"] in NAME_ID_MAPPING_CRYPTO_MODE:
                cgID = NAME_ID_MAPPING_CRYPTO_MODE.get(value["name"])
            elif runningMode == "USD Mode" and value["name"] in NAME_ID_MAPPING_USD_MODE:  
                cgID = NAME_ID_MAPPING_USD_MODE.get(value["name"])
            else:
                continue  
            asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
            assets.append(asset)
        for asset in assets:
            if asset.cgID[0] in coinGeckoData:  
                asset.cgPrice = coinGeckoData[asset.cgID[0]]["usd"]
        filtered_assets = []
        for asset in assets:
            if switch_states[asset.name] != 0: 
                filtered_assets.append(asset)
        assets = filtered_assets  
        return assets
    
if __name__ == "__main__":
    app = App()
    app.mainloop()

    