from flask import Flask, render_template, request, jsonify
import requests

TOKEN = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhbmdlbCIsImV4cCI6MTc0MDU2MzQwNCwiaWF0IjoxNzA4NTgzMDIzLCJ1c2Vy"
         "RGF0YSI6eyJjb3VudHJ5X2NvZGUiOiIiLCJtb2Jfbm8iOiI3OTgzNTI5MDAzIiwidXNlcl9pZCI6Ikg1MTMxMzcwNiIsInNvdXJjZSI6I"
         "lNQQVJLIiwiYXBwX2lkIjoiNjUzMmVjYmQtYmMxMC01MjlkLWE4NWItYmVmZDFlYTA0OTM1IiwiY3JlYXRlZF9hdCI6IjIwMjQtMDItMj"
         "JUMTE6NTM6NDMuMTg3MjQ2MzQ2KzA1OjMwIiwiZGF0YUNlbnRlciI6IiJ9LCJ1c2VyX3R5cGUiOiJjbGllbnQiLCJ0b2tlbl90eXBlIjoi"
         "bm9uX3RyYWRlX2d1ZXN0X3Rva2VuIiwic291cmNlIjoiU1BBUksiLCJkZXZpY2VfaWQiOiI2NTMyZWNiZC1iYzEwLTUyOWQtYTg1Yi1i"
         "ZWZkMWVhMDQ5MzUiLCJhY3QiOnt9fQ.DIR5qs4WwiVVD9UP2MebzdaLfCjqylSP6hbxwXgQeNY")
keys_to_keep = [
    "category",
    "entry_low_price",
    "entry_high_price",
    "target_price",
    "stop_loss_price",
    "rrr",
    "close_price",
    "exit_at",
    "state",
    "call_type",
    "company_name",
    "security_description",
    "isin",
    "symbol",
    "call_percentage_change",
    "percentage_returns_one_month"
]


from llm import process_msg

app = Flask(__name__)

supported_stocks_list = ["INFY", "TATA"]


# Route to serve the chatbot UI
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle button click
@app.route('/process_message', methods=['POST'])
def process_message():
    # Get user input from the request
    user_message = request.json.get('message')
    reply = process_msg(user_message)
    return jsonify({"response": reply})

# getAdvisoryStockData API fetches all the advisory stocks in EQ segment and calls
# getFinancialMatrix api to get the financial matrix api
@app.route('/getAdvisoryStockData', methods=['GET'])
def get_filtered_calls():
    # API URL and Authorization Token
    url = "https://advisory-service-prod.angelone.in/ssa/v1/ssa_calls"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        # Fetch data from API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()  # Parse JSON response

        # Filter condition: segment == "cash" (equity)
        equity_calls = [
            call for call in data.get("data", {}).get("calls", [])
            if call.get("segment") == "cash"
        ]

        # Filter only specified keys
        filtered_calls = [
            {key: call[key] for key in keys_to_keep if key in call}  # Extract only the specified keys
            for call in equity_calls
        ]

        # Return the filtered results as JSON
        return jsonify(filtered_calls)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


# get getFinancialMatrix api fetches sid from tickertape stocklist api and based
# on sid fetches financial matrix using another info api.
@app.route('/getFinancialMatrix/<ticker>', methods=['GET'])
def get_(ticker):
    # Fetch the list of stocks
    url = "https://api.tickertape.in/stocks/List"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching stock list: {str(e)}"}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON response from stock list API"}), 500

    # Search for the stock with the given ticker
    stock_info = next((stock for stock in data.get("data", []) if stock["ticker"] == ticker), None)

    if not stock_info:
        return jsonify({"error": "Stock not found"}), 404

    # Fetch detailed stock data using the SID
    stock_data_url = f"https://api.tickertape.in/stocks/info/{stock_info['sid']}"
    try:
        response = requests.get(stock_data_url)
        response.raise_for_status()  # Raise an error for HTTP issues
        detailed_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching stock details: {str(e)}"}), 500
    except ValueError:
        return jsonify({"error": "Invalid JSON response from stock details API"}), 500

    # Return the detailed stock data
    return jsonify(detailed_data)


if __name__ == '__main__':
    app.run(debug=True)
