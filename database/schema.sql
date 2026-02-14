CREATE TABLE zones (
    zone_id INT PRIMARY KEY,
    borough VARCHAR(50),
    zone_name VARCHAR(100),
    service_zone VARCHAR(100)
);

CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance FLOAT,
    total_amount FLOAT,
    duration_minutes FLOAT,
    fare_per_mile FLOAT,
    revenue_per_min FLOAT,
    rush_hour_flag INT,
    pickup_zone_id INT REFERENCES zones(zone_id),
    dropoff_zone_id INT REFERENCES zones(zone_id)
);

CREATE INDEX idx_pickup_time ON trips(pickup_datetime);
CREATE INDEX idx_pickup_zone ON trips(pickup_zone_id);
CREATE INDEX idx_dropoff_zone ON trips(dropoff_zone_id);
