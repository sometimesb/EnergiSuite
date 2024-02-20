from botasaurus import *

@request(use_stealth=True)
def scrape_heading_task(request: AntiDetectRequests, data):
    response = request.get('http://api.energiswap.exchange/v1/assets')
    print(response.status_code)
    return response.text

def handleRequest(data):
    pass

if __name__ == "__main__":
    apiReturn = scrape_heading_task()
    print(apiReturn)





    