from botasaurus import *
from mapping import NAME_ID_MAPPING
import json

class Asset:
    def __init__(self, name, symbol, price, cgID=None):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.cgID = cgID

    def __str__(self):
        return f"{self.name} {self.cgID} {self.price}"

@request(use_stealth=True, output="energi")
def EnergiRequester(request: AntiDetectRequests, data):
    response = request.get("https://api.energiswap.exchange/v1/assets")
    if response.status_code != 200:
        return "Error"
    return response.text

def parseEnergiData():
    data = json.loads(EnergiRequester())
    assets = []
    for key, value in data.items():
        cgID = NAME_ID_MAPPING.get(value["name"])
        asset = Asset(value["name"], value["symbol"], value["last_price"], cgID)
        assets.append(asset)
    return assets
    

if __name__ == "__main__":
    energiAssets = parseEnergiData()
    # for energiAsset in energiAssets:
    #     if energiAsset.name in NAME_ID_MAPPING:
    #         print(energiAsset)

