from app import app, db, ExchangeRate
from datetime import datetime, timedelta

def add_mock_data():
    with app.app_context():
        yesterday = datetime.now() - timedelta(days=1)
        
        # Mock data: slightly different from today's fetched values
        mock_rates = [
            {'code': 'USD', 'rate': 705.00},
            {'code': 'JPY', 'rate': 4.50},
            {'code': 'THB', 'rate': 20.00}, # scaled for example
            {'code': 'MYR', 'rate': 170.00},
            {'code': 'SGD', 'rate': 540.00},
            {'code': 'PHP', 'rate': 12.00}
        ]
        
        for item in mock_rates:
            rate = ExchangeRate(
                currency_code=item['code'],
                currency_name=item['code'], # Simplified
                buying_rate=item['rate'],
                cash_buying_rate=item['rate'],
                selling_rate=item['rate'],
                cash_selling_rate=item['rate'],
                middle_rate=item['rate'],
                pub_date=yesterday
            )
            db.session.add(rate)
        
        db.session.commit()
        print("Mock data added.")

if __name__ == "__main__":
    add_mock_data()
