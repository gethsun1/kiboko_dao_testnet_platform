from flask import Flask, render_template, jsonify, request
from solana.rpc.api import Client
import requests

app = Flask(__name__)

# Solana RPC client setup
SOLANA_DEVNET = "https://api.devnet.solana.com"
client = Client(SOLANA_DEVNET)

# Fixed exchange rate for demonstration purposes
EXCHANGE_RATE = 0.00001  # 1 MLINK = 0.00001 SOL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wallet/<address>', methods=['GET'])
def get_wallet_balance(address):
    result = client.get_balance(address)
    return jsonify({
        "wallet": address,
        "balance": result['result']['value']
    })

@app.route('/swap', methods=['POST'])
def swap_tokens():
    data = request.json
    from_token = data.get('from_token')
    to_token = data.get('to_token')
    amount = float(data.get('amount'))  # Convert to float
    wallet_address = data.get('wallet_address')

    if from_token == 'MLNK' and to_token == 'SOL':
        # Calculate the amount of SOL received
        amount_received = amount * EXCHANGE_RATE

        # For this demo, we'll assume the swap is always successful
        return jsonify({
            "success": True,
            "message": f"Swapped {amount} MLNK for {amount_received:.10f} SOL",
            "amount_received": amount_received
        })
    
    return jsonify({"success": False, "message": "Invalid swap request!"})

@app.route('/transaction-history/<address>', methods=['GET'])
def get_transaction_history(address):
    # Solana Explorer API to fetch transaction history
    response = requests.get(f'https://public-api.solscan.io/account/tokens?account={address}')
    transactions = response.json()
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
