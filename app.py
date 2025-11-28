from flask import Flask, render_template, jsonify, request
from database import db, ExchangeRate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history')
def history():
    currency = request.args.get('currency', 'USD')
    # Get last 30 days of data
    rates = ExchangeRate.query.filter_by(currency_code=currency).order_by(ExchangeRate.pub_date.asc()).all()
    
    data = []
    for r in rates:
        data.append({
            'date': r.pub_date.strftime('%Y-%m-%d'),
            'rate': r.middle_rate or r.buying_rate # Use middle rate if available, else buying
        })
    return jsonify(data)

@app.route('/api/summary')
def summary():
    # Generate summary for all tracked currencies
    currencies = ['USD', 'JPY', 'THB', 'MYR', 'SGD', 'PHP']
    summaries = []
    
    for code in currencies:
        # Get last 2 records
        rates = ExchangeRate.query.filter_by(currency_code=code).order_by(ExchangeRate.pub_date.desc()).limit(2).all()
        
        if len(rates) < 2:
            summaries.append(f"{code}: Not enough data for trend analysis.")
            continue
            
        latest = rates[0]
        previous = rates[1]
        
        current_rate = latest.middle_rate or latest.buying_rate
        prev_rate = previous.middle_rate or previous.buying_rate
        
        if not current_rate or not prev_rate:
             summaries.append(f"{code}: Data incomplete.")
             continue

        diff = current_rate - prev_rate
        percent = (diff / prev_rate) * 100
        
        trend = "up" if diff > 0 else "down"
        arrow = "↑" if diff > 0 else "↓"
        
        # Simple suggestion logic
        suggestion = ""
        if code in ['USD', 'SGD']: # Major currencies
            if percent > 0.5:
                suggestion = "Rate rising significantly. Consider selling if holding."
            elif percent < -0.5:
                suggestion = "Rate dropping. Good time to buy?"
            else:
                suggestion = "Stable."
        else:
             suggestion = "Watch closely."

        summaries.append({
            'currency': code,
            'current': current_rate,
            'change': round(diff, 4),
            'percent': round(percent, 2),
            'trend': trend,
            'suggestion': suggestion
        })
        
    return jsonify(summaries)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
