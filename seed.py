"""
Database seeder for Supply Chain AI Platform.
Run: python seed.py
"""
import sys
import os
import random
from datetime import date, timedelta, datetime

sys.path.insert(0, os.path.dirname(__file__))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.database import SessionLocal, engine
from app import models
from app.utils.auth import get_password_hash

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_users():
    users_data = [
        {"name": "Admin User", "email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"name": "Supply Manager", "email": "manager@example.com", "password": "manager123", "role": "manager"},
        {"name": "Data Analyst", "email": "analyst@example.com", "password": "analyst123", "role": "analyst"},
    ]
    for ud in users_data:
        if not db.query(models.User).filter(models.User.email == ud["email"]).first():
            db.add(models.User(
                name=ud["name"],
                email=ud["email"],
                password_hash=get_password_hash(ud["password"]),
                role=ud["role"],
            ))
    db.commit()
    print("✅ Users seeded")

def seed_suppliers():
    suppliers_data = [
        {"supplier_name": "TechParts India Ltd", "location": "Chennai", "delivery_time": 5.0, "cost": 1200.0, "reliability_score": 92.0},
        {"supplier_name": "Bharat Electronics Pvt Ltd", "location": "Bangalore", "delivery_time": 7.0, "cost": 850.0, "reliability_score": 85.0},
        {"supplier_name": "Mumbai Industrial Supply", "location": "Mumbai", "delivery_time": 4.0, "cost": 1500.0, "reliability_score": 78.0},
        {"supplier_name": "Delhi Precision Components", "location": "Delhi", "delivery_time": 10.0, "cost": 650.0, "reliability_score": 70.0},
        {"supplier_name": "Hyderabad Auto Parts", "location": "Hyderabad", "delivery_time": 6.0, "cost": 980.0, "reliability_score": 88.0},
        {"supplier_name": "Coimbatore Textiles Co", "location": "Coimbatore", "delivery_time": 8.0, "cost": 420.0, "reliability_score": 82.0},
        {"supplier_name": "Pune Machining Works", "location": "Pune", "delivery_time": 5.5, "cost": 1100.0, "reliability_score": 90.0},
        {"supplier_name": "Ahmedabad Chemical Corp", "location": "Ahmedabad", "delivery_time": 12.0, "cost": 320.0, "reliability_score": 65.0},
        {"supplier_name": "Kolkata Steel Traders", "location": "Kolkata", "delivery_time": 9.0, "cost": 780.0, "reliability_score": 74.0},
        {"supplier_name": "Jaipur Handicrafts House", "location": "Jaipur", "delivery_time": 14.0, "cost": 250.0, "reliability_score": 60.0},
    ]
    for sd in suppliers_data:
        if not db.query(models.Supplier).filter(models.Supplier.supplier_name == sd["supplier_name"]).first():
            db.add(models.Supplier(**sd))
    db.commit()
    print("✅ Suppliers seeded")

def seed_products():
    products_data = [
        {"product_name": "Microcontroller Unit MCU-8051", "category": "Electronics", "unit_cost": 450.0},
        {"product_name": "Industrial Bearings 6205", "category": "Mechanical", "unit_cost": 180.0},
        {"product_name": "Hydraulic Pump HP-200", "category": "Hydraulics", "unit_cost": 8500.0},
        {"product_name": "Copper Wire 2.5mm Roll", "category": "Electrical", "unit_cost": 3200.0},
        {"product_name": "Polypropylene Granules", "category": "Raw Material", "unit_cost": 95.0},
        {"product_name": "Stainless Steel Sheet 4mm", "category": "Metal", "unit_cost": 2800.0},
        {"product_name": "Pneumatic Cylinder PC-40", "category": "Pneumatics", "unit_cost": 4200.0},
        {"product_name": "Industrial Lubricant 20L", "category": "Chemical", "unit_cost": 1800.0},
        {"product_name": "PVC Pipe 1 inch 6m", "category": "Plumbing", "unit_cost": 320.0},
        {"product_name": "Circuit Breaker 32A", "category": "Electrical", "unit_cost": 650.0},
        {"product_name": "Textile Cotton Yarn 100kg", "category": "Textile", "unit_cost": 7500.0},
        {"product_name": "Aluminium Extrusion T-Slot", "category": "Metal", "unit_cost": 1400.0},
        {"product_name": "Servo Motor 1.5kW", "category": "Electronics", "unit_cost": 12000.0},
        {"product_name": "Industrial Filter Element", "category": "Filtration", "unit_cost": 890.0},
        {"product_name": "Conveyor Belt 500mm", "category": "Mechanical", "unit_cost": 6500.0},
        {"product_name": "Safety Gloves Nitrile Box", "category": "Safety", "unit_cost": 450.0},
        {"product_name": "Epoxy Resin 5kg Kit", "category": "Chemical", "unit_cost": 2200.0},
        {"product_name": "LED Strip Light 5m", "category": "Electrical", "unit_cost": 380.0},
        {"product_name": "Packaging Bubble Wrap Roll", "category": "Packaging", "unit_cost": 280.0},
        {"product_name": "Welding Electrode 3.15mm 5kg", "category": "Welding", "unit_cost": 560.0},
    ]
    for pd in products_data:
        if not db.query(models.Product).filter(models.Product.product_name == pd["product_name"]).first():
            db.add(models.Product(**pd))
    db.commit()
    print("✅ Products seeded")

def seed_inventory():
    products = db.query(models.Product).all()
    for p in products:
        existing = db.query(models.Inventory).filter(models.Inventory.product_id == p.id).first()
        if not existing:
            min_stock = random.randint(20, 100)
            max_stock = min_stock * random.randint(5, 15)
            # Vary availability: some critical, some low, some healthy, some overstocked
            rand = random.random()
            if rand < 0.15:
                qty = random.uniform(0, min_stock * 0.5)  # Critical
            elif rand < 0.30:
                qty = random.uniform(min_stock * 0.5, min_stock)  # Low
            elif rand < 0.85:
                qty = random.uniform(min_stock, max_stock)  # Healthy
            else:
                qty = random.uniform(max_stock, max_stock * 1.3)  # Overstocked
            db.add(models.Inventory(
                product_id=p.id,
                available_quantity=round(qty, 0),
                minimum_stock=float(min_stock),
                maximum_stock=float(max_stock),
            ))
    db.commit()
    print("✅ Inventory seeded")

def seed_orders():
    suppliers = db.query(models.Supplier).all()
    products = db.query(models.Product).all()
    customers = [
        "Reliance Industries", "Tata Motors", "Infosys Ltd", "Mahindra & Mahindra",
        "Larsen & Toubro", "Wipro Technologies", "HDFC Bank", "Asian Paints",
        "Bajaj Auto", "Sun Pharma", "Hindustan Unilever", "ONGC",
        "Maruti Suzuki", "HCL Technologies", "Titan Company",
    ]
    statuses = ["Pending", "Processing", "Shipped", "Delivered", "Delivered", "Delivered", "Delayed", "Cancelled"]
    existing_count = db.query(models.Order).count()
    if existing_count >= 200:
        print("✅ Orders already seeded")
        return
    for i in range(250):
        sup = random.choice(suppliers)
        prod = random.choice(products)
        order_date = date.today() - timedelta(days=random.randint(1, 365))
        delivery_days = int(sup.delivery_time) + random.randint(0, 7)
        expected = order_date + timedelta(days=delivery_days)
        status = random.choice(statuses)
        actual = None
        if status == "Delivered":
            delay = random.randint(-2, 5)
            actual = expected + timedelta(days=delay)
        elif status == "Delayed":
            actual = None
        qty = random.randint(10, 500)
        cost = round(qty * prod.unit_cost * (1 + random.uniform(-0.1, 0.15)), 2)
        db.add(models.Order(
            supplier_id=sup.id,
            product_id=prod.id,
            customer=random.choice(customers),
            quantity=float(qty),
            order_date=order_date,
            expected_delivery_date=expected,
            actual_delivery_date=actual,
            order_status=status,
            total_cost=cost,
        ))
    db.commit()
    print("✅ Orders seeded")

def seed_transport():
    orders = db.query(models.Order).filter(
        models.Order.order_status.in_(["Shipped", "Delivered", "Delayed"])
    ).all()
    vehicles = ["Tata Ace", "Ashok Leyland 3516", "Mahindra Bolero Pickup", "Eicher 10.90", "Bharat Benz 1217"]
    drivers = [
        "Ramesh Kumar", "Suresh Patel", "Anil Sharma", "Vijay Singh",
        "Mohan Das", "Ravi Verma", "Santosh Nair", "Pradeep Yadav",
    ]
    routes = [
        "Chennai → Bangalore", "Mumbai → Pune", "Delhi → Jaipur",
        "Hyderabad → Chennai", "Bangalore → Mumbai", "Pune → Hyderabad",
        "Coimbatore → Chennai", "Kolkata → Delhi", "Ahmedabad → Mumbai",
        "Jaipur → Delhi",
    ]
    for o in orders:
        if not db.query(models.Transport).filter(models.Transport.order_id == o.id).first():
            fuel = round(random.uniform(800, 8000), 2)
            t_status_map = {
                "Shipped": "In Transit",
                "Delivered": "Delivered",
                "Delayed": "Delayed",
            }
            db.add(models.Transport(
                order_id=o.id,
                vehicle=random.choice(vehicles),
                driver=random.choice(drivers),
                fuel_cost=fuel,
                route=random.choice(routes),
                transport_status=t_status_map.get(o.order_status, "Scheduled"),
            ))
    db.commit()
    print("✅ Transport seeded")

def seed_demand_history():
    products = db.query(models.Product).all()
    existing = db.query(models.DemandHistory).count()
    if existing >= 500:
        print("✅ Demand history already seeded")
        return
    for p in products:
        base_demand = random.uniform(50, 500)
        for day_offset in range(365, 0, -1):
            d = date.today() - timedelta(days=day_offset)
            # Seasonal pattern: higher in Oct-Dec, lower in Jan-Feb
            seasonal = 1.0 + 0.3 * (1 if d.month in [10, 11, 12] else -0.2 if d.month in [1, 2] else 0)
            trend = 1.0 + (365 - day_offset) / 365 * 0.2  # gradual uptrend
            noise = random.gauss(0, base_demand * 0.15)
            qty = max(0, base_demand * seasonal * trend + noise)
            db.add(models.DemandHistory(
                product_id=p.id,
                demand_date=d,
                quantity=round(qty, 2),
            ))
    db.commit()
    print("✅ Demand history seeded (365 days × 20 products)")

def seed_risk_history():
    from app.services.risk_service import calculate_risk_score, save_risk_to_db
    from app.services.recommendation_service import generate_recommendations
    suppliers = db.query(models.Supplier).all()
    if db.query(models.RiskHistory).count() > 30:
        print("✅ Risk history already seeded")
        return
    weather_scores = [5.0, 15.0, 40.0, 60.0, 85.0]
    for sup in suppliers:
        for _ in range(5):
            delay = random.uniform(0, 80)
            inv = random.uniform(0, 100)
            fuel = random.uniform(20, 90)
            weather = random.choice(weather_scores)
            demand = random.uniform(20, 90)
            risk_data = calculate_risk_score(
                supplier_delay=delay,
                inventory_shortage=inv,
                fuel_price_index=fuel,
                weather_impact=weather,
                demand_factor=demand,
                reliability_score=sup.reliability_score,
            )
            risk = save_risk_to_db(db, sup.id, None, risk_data)
            generate_recommendations(db, risk)
    print("✅ Risk history seeded")

def main():
    print("🌱 Starting database seed...")
    seed_users()
    seed_suppliers()
    seed_products()
    seed_inventory()
    seed_orders()
    seed_transport()
    seed_demand_history()
    seed_risk_history()
    db.close()
    print("\n🎉 Database seeding complete!")
    print("\nDemo credentials:")
    print("  Admin:   admin@example.com   / admin123")
    print("  Manager: manager@example.com / manager123")
    print("  Analyst: analyst@example.com / analyst123")

if __name__ == "__main__":
    main()
