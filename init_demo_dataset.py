import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME", "bonus")
print(mongo_uri)

client = MongoClient(mongo_uri)
db = client[mongo_db_name]

rules_collection = db["rules"]
strategies_collection = db["strategies"]
holidays_collection = db["holidays"]

rules_collection.delete_many({})
strategies_collection.delete_many({})
holidays_collection.delete_many({})

base_rate_rule = {
    "code": "base_rate",
    "name": "Базовое начисление",
    "description": "1 бонус за каждые $10",
    "type": "base",
    "conditions": [],
    "formula": {
        "type": "fixed_per_amount",
        "config": {
            "per_amount": 10,
            "bonus": 1
        }
    }
}
base_rate_id = rules_collection.insert_one(base_rate_rule).inserted_id

weekend_holiday_bonus_rule = {
    "code": "holiday_weekend",
    "name": "x2 бонусов в выходные и праздники",
    "description": "В выходные и праздники начисляется x2 бонусов",
    "type": "modifier",
    "conditions": [
        {
            "type": "holiday_weekend",
            "items": [
                {"type": "is_weekend"}
            ]
        }
    ],
    "formula": {
        "type": "multiplier",
        "config": {
            "multiplier": 2.0
        }
    }
}
holiday_bonus_id = rules_collection.insert_one(weekend_holiday_bonus_rule).inserted_id

vip_bonus_rule = {
    "code": "vip_boost",
    "name": "VIP +40%",
    "description": "VIP-клиенты получают +40%",
    "type": "modifier",
    "conditions": [
        {
            "type": "customer_status",
            "config": {"value": "vip"}
        }
    ],
    "formula": {
        "type": "percent",
        "config": {
            "percent": 40
        }
    }
}
vip_boost_id = rules_collection.insert_one(vip_bonus_rule).inserted_id

holidays_collection.insert_one({
    "date": datetime(2025, 3, 8),
    "name": "Международный женский день"
})

strategy = {
    "name": "Default Strategy",
    "description": "Стандартная схема начисления бонусов",
    "enabled": True,
    "is_default": True,
    "rules": [
        {"rule_id": base_rate_id, "order": 1, "enabled": True},
        {"rule_id": holiday_bonus_id, "order": 2, "enabled": True},
        {"rule_id": vip_boost_id, "order": 3, "enabled": True}
    ]
}

strategies_collection.insert_one(strategy)
