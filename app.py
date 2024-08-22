# app.py

from flask import Flask, request, jsonify
from financial_manager import FinancialManager

app = Flask(__name__)
manager = FinancialManager()

@app.route('/convert_currency', methods=['GET'])
def convert_currency():
    amount = float(request.args.get('amount'))
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')
    converted_amount = manager.convert_currency(amount, from_currency, to_currency)
    if converted_amount is not None:
        return jsonify({'converted_amount': converted_amount}), 200
    else:
        return jsonify({'error': 'Conversion error'}), 500

@app.route('/get_crypto_price', methods=['GET'])
def get_crypto_price():
    crypto_symbol = request.args.get('crypto_symbol')
    currency = request.args.get('currency', 'USD')
    price = manager.get_crypto_price(crypto_symbol, currency)
    if price is not None:
        return jsonify({'price': price}), 200
    else:
        return jsonify({'error': 'Price retrieval error'}), 500

@app.route('/convert_crypto', methods=['GET'])
def convert_crypto():
    amount = float(request.args.get('amount'))
    crypto_symbol = request.args.get('crypto_symbol')
    to_currency = request.args.get('to_currency', 'USD')
    converted_amount = manager.convert_crypto(amount, crypto_symbol, to_currency)
    if converted_amount is not None:
        return jsonify({'converted_amount': converted_amount}), 200
    else:
        return jsonify({'error': 'Conversion error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
