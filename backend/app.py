from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import pandas as pd
from config import DATABASE_URL

app = Flask(__name__)
CORS(app)
engine = create_engine(DATABASE_URL)

@app.route("/total-trips")
def total_trips():
    query = text("SELECT COUNT(*) FROM trips")
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    return jsonify({"total_trips": result[0]})

@app.route("/avg-fare")
def avg_fare():
    query = text("SELECT AVG(total_amount) FROM trips")
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    return jsonify({"average_fare": float(result[0])})

@app.route("/trips-by-borough")
def trips_by_borough():
    query = """
        SELECT z.borough, COUNT(*) as trip_count
        FROM trips t
        JOIN zones z ON t.pickup_zone_id = z.zone_id
        GROUP BY z.borough
        ORDER BY trip_count DESC
    """
    try:
        df = pd.read_sql(query, engine)

        df = df.fillna("Unknown") 
        
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/debug-columns")
def debug_columns():
    with engine.connect() as conn:
        # Check 'trips' table columns
        trips_cols = conn.execute(text("SELECT * FROM trips LIMIT 0")).keys()
        # Check 'zones' table columns
        zones_cols = conn.execute(text("SELECT * FROM zones LIMIT 0")).keys()
    return jsonify({
        "trips_columns": list(trips_cols),
        "zones_columns": list(zones_cols)
    })

if __name__ == "__main__":
    app.run(debug=True)

