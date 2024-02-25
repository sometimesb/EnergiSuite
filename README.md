# 🌐 Energi Suite
A third iteration of the energi reaper bot that I built. Second version used to much RAM because it used selenium. Can now be run on a server and even headless.

## 📝 Introduction
This Python script functions as a cryptocurrency monitoring bot, leveraging various libraries and APIs to perform comprehensive analyses. It operates in two distinct modes: CoinGecko and USD. In CoinGecko mode, the bot compares cryptocurrency prices between EnergiSwap and CoinGecko. Conversely, in USD mode, it focuses on analyzing price differentials among selected stablecoins.

I put a lot of work into this bot and it made me 40x my initial investment at its peak :)

This uses _EnergiSwap_ (a fork of UniSwap).

## 🔧 Technologies Used
* Python - Main driver of the script
* Batch - executes script for the user

*No more* Selenium!

## 📙 Libraries and Versions Used
* python             3.11.4
* botasaurus         3.2.24
* customtkiner       5.2.2
* pillow             10.2.0

## 🤔 Why is this the third version of the same core code?
It actually isn't the same core code! The first version was spaghetti code, the second uses functions + selenium for webscraping. This new version removes selenium entirely.
Requests library cannot be used as the energiswap API uses cloudflare and blocks robot requests...as an API. 

Yes, I know. So you must use botasaurus in stealth mode.

*Memory usage factor is rough approximation of watching total memory usage across the programs*

|  | Memory Usage Factor | Speed |
| --------------- | --------------- | --------------- |
| Version 1 | 3 | 60s |
| EnergiReaperReborn | 3 | 3s |
| EnergiSuite | 1 | 0.25s |


## 🚀 Functionality
The UI boasts an easy to use screen. Immediately, you can decide what mode you want to run in.
1. USD Mode -> USDC, DAI, USDE, etc.
   ![image](https://github.com/sometimesb/EnergiReaperReborn/assets/77695101/9bb7a931-71d6-4022-87ab-4ad46b314976)
   
2. Crypto Mode -> BTC, ETH, etc.
   ![image](https://github.com/sometimesb/EnergiReaperReborn/assets/77695101/59f7a81e-3f8a-4dc2-9eea-99b7e7ad54fe)
  
3. Allows you to set custom search parameters, what kind of profit % do we need to search for? This is used as a minimum, anything below the minimum will not be shown in the textbox.
   ![image](https://github.com/sometimesb/EnergiReaperReborn/assets/77695101/82f7bcc2-b851-4e7d-a3e9-a0173f75e618)
 
4. API Limiter detection. Tells you when coingecko OR energiswap API blocks you.
   ![image](https://github.com/sometimesb/EnergiReaperReborn/assets/77695101/1b7ec14c-3224-47ff-9bef-6ca34d68d602)

5. Modular JSON file that allows you to add and remove cryptocurrencies as you desire.
```JSON
{
  "NAME_ID_MAPPING_CRYPTO_MODE": {
    "Ether": ["ethereum","ETH"],
    "Bitcoin": ["bitcoin","BTC"]
  },
  "NAME_ID_MAPPING_USD_MODE": {
    "Energi Dollar": ["energi-dollar","USDE"],
    "Dai Stablecoin": ["dai","DAI"]
  }
}
```
## 📄 Full rundown & Installation:
1) Must install libraries with specific versions above. Special emphasis on the discord version, or it will not work.
2) Head to config.json, you must follow this specific format.
```
"Crypto Name": ["ID in coingecko", "Symbol"]
```
3. Run Main.py, UI will automatically open.
4. Profit


Made with ♥️ by Bilal Zakaria.



