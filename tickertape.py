import requests

CHECKLIST_URL = "https://api.tickertape.in/stocks/investmentChecklists/"
STOCKINFO_URL = "https://api.tickertape.in/stocks/info/"
CURRPRICE_URL = "https://quotes-api.tickertape.in/quotes?sids="
HISTPRICE_URL = "https://api.tickertape.in/stocks/charts/inter/"


def checklist_data(symbol):
    checklists_url = f"{CHECKLIST_URL}{symbol}"
    response = requests.get(checklists_url).json()
    titles = []
    description = []

    for k, v in response.items():
        if k == "data":
            for item in v:
                titles.append(item["title"])
                description.append(item["description"])

    return titles, description


def stock_info(symbol):
    stockinfo_url = f"{STOCKINFO_URL}{symbol}"
    response = requests.get(stockinfo_url).json()
    for k, v in response.items():
        if k == "data":
            for key, val in v.items():
                if key == "ratios":
                    return val


def current_price(symbol):
    curr_price_url = f"{CURRPRICE_URL}{symbol}"
    response = requests.get(curr_price_url).json()

    for k, v in response.items():
        if k == "data":
            for item in v:
                return item


def historical_price(symbol):
    hist_price_url = f"{HISTPRICE_URL}{symbol}?duration=1mo"
    response = requests.get(hist_price_url).json()


if __name__ == '__main__':
    print(stock_info("INFY"))
    # need to add further
