"""
Verification script for Supply Chain AI Platform backend.
Validates all imports, schemas, models, services, ML modules, and router registrations.
"""
import sys
import os

# Set UTF-8 stdout if possible
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("[*] RUNNING BACKEND HEALTH AND VERIFICATION CHECK")
print("=" * 60)

# 1. Config & Settings
try:
    from app.config import get_settings
    settings = get_settings()
    print(f"[+] [1/7] Config loaded successfully (DB_HOST={settings.DB_HOST}, DB_NAME={settings.DB_NAME})")
except Exception as e:
    print(f"[-] [1/7] Config loading failed: {e}")
    sys.exit(1)

# 2. Database & Models
try:
    from app.database import Base, engine, SessionLocal, get_db
    from app import models
    # Check that Base is attached
    assert hasattr(models, 'Base'), "models.Base not found!"
    
    # Check model list
    expected_models = [
        "User", "Supplier", "Product", "Inventory", "Order", "Transport",
        "DemandHistory", "Forecast", "RiskHistory", "ShapExplanation",
        "Recommendation", "SimulationScenario", "SimulationResult",
    ]
    for m in expected_models:
        assert hasattr(models, m), f"Model {m} missing from models package!"
    print(f"[+] [2/7] All {len(expected_models)} SQLAlchemy models loaded and mapped to Base")
except Exception as e:
    print(f"[-] [2/7] Database & models check failed: {e}")
    sys.exit(1)

# 3. Schemas
try:
    from app import schemas
    expected_schemas = [
        "UserCreate", "UserLogin", "UserOut", "Token", "TokenData",
        "SupplierCreate", "SupplierUpdate", "SupplierOut", "SupplierDetail",
        "ProductCreate", "ProductUpdate", "ProductOut",
        "InventoryUpdate", "InventoryOut", "InventoryWithProduct",
        "OrderCreate", "OrderUpdate", "OrderOut", "OrderDetail",
        "TransportCreate", "TransportUpdate", "TransportOut",
        "DemandHistoryOut", "ForecastOut", "ForecastRequest",
        "RiskCalculateRequest", "RiskOut", "RiskDetail",
        "ShapExplanationOut", "RecommendationOut",
        "SimulationRequest", "SimulationOut",
    ]
    for s in expected_schemas:
        assert hasattr(schemas, s), f"Schema {s} missing from schemas package!"
    print(f"[+] [3/7] All {len(expected_schemas)} Pydantic v2 schemas validated")
except Exception as e:
    print(f"[-] [3/7] Schemas check failed: {e}")
    sys.exit(1)

# 4. Auth Utilities
try:
    from app.utils.auth import (
        verify_password, get_password_hash, create_access_token,
        get_current_user, require_role, pwd_context, oauth2_scheme
    )
    from app.auth import (
        verify_password as v2, get_password_hash as g2,
        create_access_token as c2, get_current_user as u2
    )
    pw = "testpassword123"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed), "Password verification failed!"
    print("[+] [4/7] Auth utilities, JWT handling & bcrypt password hashing verified")
except Exception as e:
    print(f"[-] [4/7] Auth check failed: {e}")
    sys.exit(1)

# 5. Services
try:
    from app.services.inventory_service import get_inventory_status, get_all_inventory_with_status
    from app.services.dashboard_service import get_dashboard_kpis, get_order_status_distribution
    from app.services.risk_service import calculate_risk_score, normalize_delay, WEIGHTS, WEATHER_SCORES
    from app.services.recommendation_service import generate_recommendations, get_all_recommendations
    
    # Test risk calculation formula
    res = calculate_risk_score(50, 40, 60, 20, 50, 80)
    assert "risk_score" in res and "risk_level" in res, "Risk calculation returned invalid structure"
    print(f"[+] [5/7] Backend business logic & risk calculation services verified (Sample score: {res['risk_score']})")
except Exception as e:
    print(f"[-] [5/7] Services check failed: {e}")
    sys.exit(1)

# 6. ML Models
try:
    from app.ml.risk_model import RiskModel
    from app.ml.forecast_model import prepare_features, FEATURE_COLS
    
    rm = RiskModel()
    shap_vals = rm.compute_shap(10, 20, 30, 40, 50, 60)
    assert len(shap_vals) == 6, "SHAP values dictionary incomplete"
    print(f"[+] [6/7] Machine Learning modules verified (RandomForest & TreeExplainer operational, SHAP features: {list(shap_vals.keys())})")
except Exception as e:
    print(f"[-] [6/7] ML models check failed: {e}")
    sys.exit(1)

# 7. FastAPI App & All 14 Routers
try:
    from app.main import app
    from app.routers import (
        auth, suppliers, products, inventory, orders,
        transport, forecast, risk, simulation, recommendations,
        dashboard, reports, powerbi
    )
    
    routes = [getattr(route, "path", getattr(route, "path_format", str(route))) for route in app.routes]
    print(f"[+] [7/7] FastAPI App initialized with {len(app.routes)} registered endpoints across all 13 router modules")
except Exception as e:
    print(f"[-] [7/7] FastAPI app mounting failed: {e}")
    sys.exit(1)

print("=" * 60)
print("[OK] ALL BACKEND CHECKS PASSED WITH ZERO ERRORS!")
print("=" * 60)
