from flask import Flask, render_template, request, jsonify
import requests
from api import API_KEY
from openai_queries import get_openai_response_startup_investments



app = Flask(__name__, static_folder="static", template_folder="templates")

# API Keys
GEMINI_API_KEY = "AIzaSyB4MQ_qUVx0_em6HJtabbm6rA4WiejjM3w"
SERPAPI_KEY = "fd31d498753a28932a6e379d6d824a2b2b65a2c2c9e8a82a3ecdb4643011f11c"
CRUNCHBASE_API_KEY = "388d92eb580be80dd6e1422e8a48fe48"

# -------------------- FLASK ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market-analysis')
def market_analysis_page():
    return render_template('market-analysis.html')

@app.route('/ww')
def cofounder_page():
    return render_template('ww.html')

def get_prices(product):
    """Simulating fetching prices (Replace with real API calls or scraping)."""
    prices = {
        "Amazon": 9999 + len(product) * 10,
        "Flipkart": 9499 + len(product) * 8,
        "Snapdeal": 9700 + len(product) * 5
    }
    return prices

@app.route('/analyze-market', methods=['POST'])
def analyze_market():
    data = request.get_json()
    business_idea = data.get('idea', '')

    if not business_idea:
        return jsonify({"error": "No business idea provided"}), 400

    # Call OpenAI API to get market analysis
    analysis = get_openai_response_startup_investments(business_idea)

    return jsonify({"analysis": analysis})


@app.route('/market_access', methods=['GET', 'POST'])
def market_access():
    if request.method == 'POST':
        product = request.form.get('product')  

        # Ensure product is not empty
        if not product:
            return render_template('market_access.html', product=None, prices=None, error="Please enter a product name.")

        prices = get_prices(product)  # Fetch prices from platforms
        lowest_price_site = min(prices, key=prices.get)  # Find the lowest price

        return render_template('market_access.html', product=product, prices=prices, lowest_price_site=lowest_price_site)

    return render_template('market_access.html', product=None, prices=None)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data['message']

    # Send request to Google Gemini AI
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        ai_reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't understand.")
    else:
        ai_reply = "Error: Unable to reach AI service."

    return jsonify(reply=ai_reply)

'''@app.route('/google-finance-data', methods=['POST'])
def google_finance_data():
    data = request.get_json()
    business_idea = data['idea']

    serpapi_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_finance_markets",
        "trend": "most-active",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(serpapi_url, params=params)
    if response.status_code == 200:
        market_data = response.json()
        most_active_stocks = market_data.get("markets", {}).get("us", [])
        return jsonify(most_active_stocks)
    else:
        return jsonify({"error": "Could not fetch data"})'''

@app.route('/funding-data', methods=['POST'])
def funding_data():
    data = request.get_json()
    business_idea = data['idea']

    # Query Google Finance Markets API via SerpApi
    serpapi_url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_finance_markets",
        "trend": "most-active",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(serpapi_url, params=params)
    
    if response.status_code == 200:
        market_data = response.json()
        most_active_stocks = market_data.get("markets", {}).get("us", [])

        if most_active_stocks:
            top_stock = most_active_stocks[0]  # Get the first result
            stock_name = top_stock.get("name", "N/A")
            stock_price = top_stock.get("price", "N/A")
            stock_movement = top_stock.get("price_movement", {}).get("movement", "N/A")
            stock_change = top_stock.get("price_movement", {}).get("value", "N/A")
            stock_link = top_stock.get("link", "#")
        else:
            stock_name, stock_price, stock_movement, stock_change, stock_link = "N/A", "N/A", "N/A", "N/A", "#"
    else:
        stock_name, stock_price, stock_movement, stock_change, stock_link = "Error fetching data", "N/A", "N/A", "N/A", "#"

    return jsonify({
        "top_stock": stock_name,
        "stock_price": stock_price,
        "stock_movement": stock_movement,
        "stock_change": stock_change,
        "stock_link": stock_link
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
