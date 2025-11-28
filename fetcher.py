import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import db, ExchangeRate
from app import app

# Mapping of Chinese names to Currency Codes
CURRENCY_MAP = {
    "美元": "USD",
    "日元": "JPY",
    "泰铢": "THB",
    "林吉特": "MYR",
    "新加坡元": "SGD",
    "菲律宾比索": "PHP"
}

def fetch_rates():
    url = "https://www.boc.cn/sourcedb/whpj/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'align': 'left'})
        
        if not table:
            print("Could not find the rates table")
            return

        rows = table.find_all('tr')
        # Skip header row
        
        rates_to_save = []
        
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) < 8:
                continue
                
            currency_name = cols[0].text.strip()
            
            if currency_name in CURRENCY_MAP:
                code = CURRENCY_MAP[currency_name]
                
                # Parse values, handle empty or '-'
                def parse_float(val):
                    try:
                        return float(val)
                    except ValueError:
                        return None

                buying_rate = parse_float(cols[1].text.strip())
                cash_buying_rate = parse_float(cols[2].text.strip())
                selling_rate = parse_float(cols[3].text.strip())
                cash_selling_rate = parse_float(cols[4].text.strip())
                middle_rate = parse_float(cols[5].text.strip())
                pub_date_str = cols[6].text.strip() + " " + cols[7].text.strip()
                
                try:
                    pub_date = datetime.strptime(pub_date_str, '%Y.%m.%d %H:%M:%S')
                except ValueError:
                    pub_date = datetime.now()

                rate_entry = ExchangeRate(
                    currency_code=code,
                    currency_name=currency_name,
                    buying_rate=buying_rate,
                    cash_buying_rate=cash_buying_rate,
                    selling_rate=selling_rate,
                    cash_selling_rate=cash_selling_rate,
                    middle_rate=middle_rate,
                    pub_date=pub_date
                )
                rates_to_save.append(rate_entry)
                print(f"Fetched {code}: {middle_rate}")

        # Save to DB
        with app.app_context():
            # Optional: Check if data for this timestamp already exists to avoid duplicates
            # For simplicity, we just add. In production, we should check.
            for rate in rates_to_save:
                # Simple check to avoid exact duplicate for same currency and time
                exists = ExchangeRate.query.filter_by(
                    currency_code=rate.currency_code, 
                    pub_date=rate.pub_date
                ).first()
                
                if not exists:
                    db.session.add(rate)
            
            db.session.commit()
            print(f"Saved {len(rates_to_save)} records to database.")

    except Exception as e:
        print(f"Error fetching rates: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    fetch_rates()
