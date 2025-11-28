from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(10), nullable=False)
    currency_name = db.Column(db.String(50), nullable=False)
    buying_rate = db.Column(db.Float) # 现汇买入价
    cash_buying_rate = db.Column(db.Float) # 现钞买入价
    selling_rate = db.Column(db.Float) # 现汇卖出价
    cash_selling_rate = db.Column(db.Float) # 现钞卖出价
    middle_rate = db.Column(db.Float) # 中行折算价
    pub_date = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'currency_code': self.currency_code,
            'currency_name': self.currency_name,
            'buying_rate': self.buying_rate,
            'cash_buying_rate': self.cash_buying_rate,
            'selling_rate': self.selling_rate,
            'cash_selling_rate': self.cash_selling_rate,
            'middle_rate': self.middle_rate,
            'pub_date': self.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
