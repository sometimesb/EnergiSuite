from botasaurus import *
from mapping import NAME_ID_MAPPING
import json

class Asset:
    def __init__(self, name, symbol, price, cgID=None,cgPrice=None):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.cgID = cgID
        self.cgPrice = cgPrice

    def __str__(self):
        return f"{self.name} {self.cgID} {self.price}"

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

def parseEnergiData():
    data = json.loads(apiRequester("https://api.energiswap.exchange/v1/assets",0))
    assets = []
    for key, value in data.items():
        cgID = NAME_ID_MAPPING.get(value["name"])
        asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
        if  asset.name in NAME_ID_MAPPING:
            assets.append(asset)
    return assets

if __name__ == "__main__":
    energiAssets = parseEnergiData()
    coinGeckoAssets = parseCoinGeckoData()
    for energiAsset in energiAssets:
        print(energiAsset)

