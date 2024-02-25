from botasaurus import *
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

with open("config.json") as f:
    config = json.load(f)

NAME_ID_MAPPING_CRYPTO_MODE = config["NAME_ID_MAPPING_CRYPTO_MODE"]
NAME_ID_MAPPING_USD_MODE = config["NAME_ID_MAPPING_USD_MODE"]

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

        # Initialize the application window with configuration
        self.configure_window()

        # Create the sidebar frame and associated widgets
        self.create_sidebar_frame()

        # Create the textbox and tabview widgets
        self.create_textbox_tabview()

        # Create the scrollable frames within the tabview
        self.create_scrollable_frames()

        # Set default values and configurations
        self.set_defaults()

    # Define a function to get the mappings from the config file
    def get_mappings_from_config(config_file_path, mode):
        with open(config_file_path) as f:
            config = json.load(f)
        return config[mode]

    def configure_window(self):
        """Configures the window title, geometry, and grid layout."""

        # Set the window title
        self.title("Energi Suite")

        # Set the window dimensions
        self.geometry("1100x580")

        # Prevent window resizing
        self.resizable(False, False)

        # Configure grid layout for main application area
        self.grid_columnconfigure(1, weight=1) # Set the second column to expand to fill available space
        self.grid_columnconfigure((2, 3), weight=0) # Set columns 2 and 3 to fixed width
        self.grid_rowconfigure((0, 1, 2), weight=1) # Allow rows 0, 1, and 2 to expand to fill available space

    def create_sidebar_frame(self):
        """Creates the sidebar frame with its widgets."""
        
        # Initialize auto_execute_status
        self.auto_execute_status = False

        # Create the sidebar frame and configure it
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Allow the last row to expand

        # Add the logo label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Energi Suite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10)) # Apply padding

        # Add the running mode label and option menu
        self.running_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Running Mode:", anchor="w")
        self.running_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.running_mode_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["USD Mode", "Crypto Mode"], command=self.running_mode_event)
        self.running_mode_menu.grid(row=7, column=0, padx=20, pady=(10, 10))

        # Add the execute button
        self.sidebar_execute_button = customtkinter.CTkButton(self.sidebar_frame, text="Execute", command=lambda: threading.Thread(target=self.execute, args=(self.running_mode_menu.get(),)).start())
        self.sidebar_execute_button.grid(row=1, column=0, padx=20, pady=10)

        # Add the auto execute button
        self.sidebar_autoexecute_button = customtkinter.CTkButton(self.sidebar_frame, text="Start Auto Execute", command=self.toggle_auto_execute)
        self.sidebar_autoexecute_button.grid(row=2, column=0, padx=20, pady=10)

        # Add the appearance mode label and option menu
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))

        # Add the scaling label and option menu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))

    def create_textbox_tabview(self):
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
        self.USDModeSlider = customtkinter.CTkSlider(self.tabview.tab("USDMode"), from_=0, to=10, number_of_steps=100,command=self.USDModeEvent)
        self.USDModeSlider.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.USDModeVariable = tkinter.StringVar(value="")
        self.USDModeLabel = customtkinter.CTkLabel(self.tabview.tab("USDMode"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.USDModeVariable)
        self.USDModeLabel.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        #second tabview
        self.CryptoModeVariable = tkinter.StringVar(value="")
        self.CryptoModeSlider = customtkinter.CTkSlider(self.tabview.tab("CryptoMode"), from_=0, to=10, number_of_steps=100,button_color="blue",button_hover_color="blue",command=self.CryptoModeEvent)
        self.CryptoModeSlider.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.CryptoModeLabel = customtkinter.CTkLabel(self.tabview.tab("CryptoMode"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.CryptoModeVariable)
        self.CryptoModeLabel.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

        #third tabview
        self.AutoRunVariable = tkinter.StringVar(value="")
        self.AutoRunTimer = customtkinter.CTkSlider(self.tabview.tab("AutoRun Timer"), from_=10, to=60, number_of_steps=50,button_color="red",button_hover_color="red",command=self.AutoRunEvent)
        self.AutoRunTimer.grid(row=3, column=0, padx=(20, 10), pady=(100, 100), sticky="ew")

        self.AutoRunLabel = customtkinter.CTkLabel(self.tabview.tab("AutoRun Timer"),font=customtkinter.CTkFont(size=15),corner_radius=8,text_color="white",textvariable=self.AutoRunVariable)
        self.AutoRunLabel.grid(row=3, column=1, columnspan=1, padx=(5,5), pady=(5,5), sticky="ew")

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

        self.USDModeVariable.set(f"{round(float(self.USDModeSlider.get()), 1)}%")
        self.CryptoModeVariable.set(f"{round(float(self.CryptoModeSlider.get()), 2)}%")
        self.AutoRunVariable.set(f"{round(int(self.AutoRunTimer.get()), 2)}s")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.running_mode_menu.set("Crypto Mode")
        self.running_mode_event("Crypto Mode")

    def running_mode_event(self, mode):
        """Handles the change in running mode (USD or Crypto) and adjusts UI accordingly."""
        
        # Check if mode is USD Mode
        if mode == "USD Mode":
            # Set the tabview to USDMode
            self.tabview.set("USDMode")
            
            # Disable the CryptoModeSlider and enable the USDModeSlider
            self.CryptoModeSlider.configure(state="disabled")
            self.USDModeSlider.configure(state="normal")

            # Disable the switches related to Crypto assets and enable the switches related to USD assets
            for switch in self.scrollable_frame_switches_CG:
                switch.configure(state="disabled")  
            for switch in self.scrollable_frame_switches_USD:
                switch.configure(state="normal") 

        # Check if mode is Crypto Mode
        elif mode == "Crypto Mode":
            # Set the tabview to CryptoMode
            self.tabview.set("CryptoMode")
            
            # Disable the USDModeSlider and enable the CryptoModeSlider
            self.USDModeSlider.configure(state="disabled")
            self.CryptoModeSlider.configure(state="normal")

            # Disable the switches related to USD assets and enable the switches related to Crypto assets
            for switch in self.scrollable_frame_switches_USD:
                switch.configure(state="disabled")
                switch.toggle() # If needed, make sure switches are set to a default state
            for switch in self.scrollable_frame_switches_CG:
                switch.configure(state="normal") 

        else:
            # Handle invalid mode (optional)
            print("Invalid mode:", mode)

    def USDModeEvent(self,value):
        self.USDModeVariable.set(f"{round(float(self.USDModeSlider.get()), 1)}%")

    def CryptoModeEvent(self,value):
        self.CryptoModeVariable.set(f"{round(float(self.CryptoModeSlider.get()), 1)}%")
    
    def AutoRunEvent(self,value):
        self.AutoRunVariable.set(f"{round(int(self.AutoRunTimer.get()), 1)}s")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def toggle_auto_execute(self):
        """Toggle AutoExecute on or off."""
        
        # Check if auto execute is currently on
        if self.auto_execute_status:
            # Stop AutoExecute
            self.auto_execute_status = False

            # Update button text and function
            self.sidebar_autoexecute_button.configure(text="Start Auto Execute", command=self.toggle_auto_execute)

            # Enable the textbox and display message
            self.textbox.configure(state="normal")
            self.textbox.delete(0.0, 'end')
            self.textbox.insert("0.0", "Stopped auto execution.")
            self.textbox.configure(state="disabled")

            # Enable switches for both modes
            for switch in self.scrollable_frame_switches_CG:
                switch.configure(state="normal")  
            for switch in self.scrollable_frame_switches_USD:
                switch.configure(state="normal") 
        else:
            # Start AutoExecute
            self.auto_execute_status = True
            
            # Start the AutoExecute method in a separate thread
            threading.Thread(target=self.AutoExecute, args=(self.running_mode_menu.get(),)).start()
            
            # Update button text and function
            self.sidebar_autoexecute_button.configure(text="Stop Auto Execute", command=self.toggle_auto_execute)

            # Disable switches for both modes
            for switch in self.scrollable_frame_switches_CG:
                switch.configure(state="disabled")  
            for switch in self.scrollable_frame_switches_USD:
                switch.configure(state="disabled")

    def AutoExecute(self, runningMode):
        """AutoExecute method that runs in a loop based on timer value."""
        
        # Get timer value from UI and calculate sleep time
        timer_value = int(self.AutoRunVariable.get().replace("s", ""))
        sleep_time = timer_value - time.time() % timer_value  # Calculate sleep time once
        
        # Loop to execute while auto_execute_status is True
        while self.auto_execute_status:
            # Execute the search and update textbox
            self.execute(runningMode)  
            
            # Enable textbox and update timer value
            self.textbox.configure(state="normal")
            self.textbox.insert("0.0", f"Timer: {timer_value}s\n")
            self.textbox.configure(state="disabled")

            # Sleep for the specified timer interval, minus the time spent in the loop
            if sleep_time > 0:
                time.sleep(sleep_time)
            sleep_time = timer_value  # Update sleep time for the next iteration

    def execute(self, runningMode):
        """Execute method that updates textbox with asset information based on running mode."""
        
        # Enable the textbox for editing
        self.textbox.configure(state="normal")

        # Get assets based on running mode (USD or Crypto)
        assets = self.getAssets(runningMode)
        any_assets_added = False

        # Clear existing content in the textbox
        self.textbox.delete(0.0, 'end')

        # Loop through assets and check if they meet profit criteria
        for asset in assets:
            if (runningMode == "Crypto Mode") and float(self.CryptoModeVariable.get().replace('%', '')) < self.profitPercent(asset.price, asset.cgPrice):
                self.textbox.insert("0.0", asset.symbol + " " + str(self.profitPercent(asset.price, asset.cgPrice)) + "%\n")
                any_assets_added = True
            elif (runningMode == "USD Mode") and float(self.USDModeVariable.get().replace('%', '')) < self.profitPercent(asset.price, asset.cgPrice):
                self.textbox.insert("0.0", asset.symbol + " " + str(self.profitPercent(asset.price, asset.cgPrice)) + "%\n")
                any_assets_added = True

        # If no assets added, show a message
        if not any_assets_added:
            self.textbox.insert("0.0", "Search completed, nothing met minimum profit requirement or no coins enabled.\n")

        # Disable the textbox to prevent editing
        self.textbox.configure(state="disabled")

    def profitPercent(self, energiPrice, cgPrice):
        """Calculate the percentage profit based on Energi price and CoinGecko price."""
        
        # Check if either price is missing
        if cgPrice is None or energiPrice is None:
            return None  

        try:
            # Check if CoinGecko price is 0, to prevent division by zero
            if cgPrice == 0:
                return float('inf') 
            else:
                # Calculate profit percentage
                return (abs(energiPrice-cgPrice))/((energiPrice+cgPrice)/2)*100
        except ZeroDivisionError:
            return None

    def apiRequester(self, url, mode):
        """Request API data based on mode using AntiDetectRequests with Stealth Mode."""
        
        @request(use_stealth=True, output="energi")
        def EnergiRequester(request: AntiDetectRequests, data):
            """Request Energi data."""
            response = request.get(url)
            if response.status_code != 200:
                return "Error"
            return response.text

        @request(use_stealth=True, output="coingecko")
        def CoinGeckoRequester(request: AntiDetectRequests, data):
            """Request CoinGecko data."""
            response = request.get(url)
            if response.status_code != 200:
                return "Error"
            return response.text

        # Check mode to choose the appropriate requester
        if mode == 0:
            return EnergiRequester()
        elif mode == 1:
            return CoinGeckoRequester()
        else:
            return None  # Handle invalid mode (optional)

    def coinGeckoLinkBuilder(self, mapping):
        """Build the CoinGecko API link to request prices for specified cryptocurrencies."""
        
        # Set the base URL for CoinGecko API
        base_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        
        # Append each cryptocurrency ID to the URL
        for k, v in mapping.items():
            # Use the 0th index value (name) for the link
            base_url += v[0] + "%2C"
        
        # Append the desired currency (USD) to the URL
        base_url += "&vs_currencies=usd"
        
        # Return the complete URL
        return base_url

    def getAssets(self, runningMode):
        """Retrieve and process assets data based on the specified running mode."""
        
        # Initialize assets list
        assets = []
        
        try:
            # Get Energi data and load it as JSON
            energiData = json.loads(self.apiRequester("https://api.energiswap.exchange/v1/assets", 0))
        except:
            # Handle API limit hit for EnergiSwap
            self.textbox.configure(state="normal")
            self.textbox.delete(0.0, 'end')
            self.textbox.insert("0.0", "API Limiter hit, please wait 60 seconds for EnergiSwap to unblock.\n")
            self.textbox.configure(state="disabled")
        
        switch_states = {}

        # Check the running mode
        if runningMode == "Crypto Mode":
            # Set the CoinGecko link for Crypto Mode
            cgLink = self.coinGeckoLinkBuilder(NAME_ID_MAPPING_CRYPTO_MODE)
             # Iterate through the switches and add their states to a dictionary
            for switch, name in zip(self.scrollable_frame_switches_CG, NAME_ID_MAPPING_CRYPTO_MODE):
                toggle_value = switch.get()
                switch_states[name] = toggle_value  
            
        else:
            # Set the CoinGecko link for USD Mode
            cgLink = self.coinGeckoLinkBuilder(NAME_ID_MAPPING_USD_MODE)
             # Iterate through the switches and add their states to a dictionary
            for switch, name in zip(self.scrollable_frame_switches_USD, NAME_ID_MAPPING_USD_MODE):
                toggle_value = switch.get()
                switch_states[name] = toggle_value  
        try:
            # Get CoinGecko data and load it as JSON
            coinGeckoData = json.loads(self.apiRequester(cgLink, 1))
        
        except:
            # Handle API limit hit for CoinGecko
            self.textbox.configure(state="normal")
            self.textbox.delete(0.0, 'end')
            self.textbox.insert("0.0", "API Limiter hit, please wait 60 seconds for CoinGecko to unblock.\n")
            self.textbox.configure(state="disabled")

        # Loop through EnergiData and filter out assets that match the running mode
        for key, value in energiData.items():
            if runningMode == "Crypto Mode" and value["name"] in NAME_ID_MAPPING_CRYPTO_MODE:
                cgID = NAME_ID_MAPPING_CRYPTO_MODE.get(value["name"])
            elif runningMode == "USD Mode" and value["name"] in NAME_ID_MAPPING_USD_MODE:  
                cgID = NAME_ID_MAPPING_USD_MODE.get(value["name"])
            else:
                continue  
            
            # Create Asset object and add it to assets list
            asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
            assets.append(asset)
        
        # Loop through assets and update cgPrice based on CoinGecko data
        for asset in assets:
            if asset.cgID[0] in coinGeckoData:  
                asset.cgPrice = coinGeckoData[asset.cgID[0]]["usd"]
        
        # Filter assets based on switch states
        filtered_assets = []
        for asset in assets:
            if switch_states[asset.name] != 0: 
                filtered_assets.append(asset)
        assets = filtered_assets  
        
        # Return the processed assets
        return assets

if __name__ == "__main__":
    app = App()
    app.mainloop()

    