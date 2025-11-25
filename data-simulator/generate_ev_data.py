#!/usr/bin/env python3
# generate_and_publish_ev_data.py
# pip install google-cloud-pubsub

import time, json, random
from datetime import datetime, timezone
from google.cloud import pubsub_v1
import os

# service_account_path = r'c:\Users\vinay\Downloads\boxwood-axon-470816-b1-a21b5542b2c6.json'
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path


PROJECT = "boxwood-axon-470816-b1"                   
TOPIC = f"projects/{PROJECT}/topics/ev-telemetry-topic"
NUM_VEHICLES = 10
SEND_INTERVAL = 5   # seconds between each round of events

vehicles = []
models = ["I-PACE","Range-Rover-EV","Defender-EV","Discovery-EV"]

def init_vehicles(n):
    for i in range(1, n+1):
        vehicles.append({
            "vin": f"JLR-EV-{i:03}",
            "model": random.choice(models),
            "soc": random.uniform(60, 100),     # state of charge
            "soh": random.uniform(90, 99),      # state of health
            "odometer": random.uniform(2000, 40000),
            "lat": 18.5204 + random.uniform(-0.2,0.2),
            "lon": 73.8567 + random.uniform(-0.2,0.2),
            "motor_temp": random.uniform(30, 50)
        })

def step_state(v):
    # simulate driving/charging behavior
    speed = max(0, random.gauss(50, 18))
    is_charging = random.random() < 0.05   # 5% chance to be charging
    if is_charging:
        charging_power = random.choice([7.2, 11, 50])
        v["soc"] = min(100.0, v["soc"] + random.uniform(0.2, 2.0) * (charging_power/10.0))
    else:
        v["soc"] = max(0.0, v["soc"] - (speed/100.0) * random.uniform(0.01, 0.03))
    # update other fields
    v["motor_temp"] += (speed/200.0) * random.uniform(0.0, 1.5)
    # small gps random walk
    v["lat"] += random.uniform(-0.001, 0.001) * (speed/50.0)
    v["lon"] += random.uniform(-0.001, 0.001) * (speed/50.0)
    v["odometer"] += speed * (SEND_INTERVAL / 3600.0)
    # occasional fault
    fault = None
    if random.random() < 0.002:
        fault = random.choice(["BMS_001","TEMP_002","COMM_003"])
    return {
        "speed_kmph": round(speed,2),
        "charging": is_charging,
        "charging_power_kw": charging_power if is_charging else 0.0,
        "fault_code": fault
    }

def make_event(vstate, dynamics):
    return {
        "vin": vstate["vin"],
        "vehicle_model": vstate["model"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gps_lat": round(vstate["lat"],6),
        "gps_lon": round(vstate["lon"],6),
        "speed_kmph": dynamics["speed_kmph"],
        "odometer_km": round(vstate["odometer"],2),
        "state_of_charge_percent": round(vstate["soc"],2),
        "state_of_health_percent": round(vstate["soh"],2),
        "motor_temp_c": round(vstate["motor_temp"],2),
        "charging_state": "CHARGING" if dynamics["charging"] else "NOT_CHARGING",
        "charging_power_kw": round(dynamics["charging_power_kw"],2),
        "fault_code": dynamics["fault_code"]
    }

def publish_loop():
    publisher = pubsub_v1.PublisherClient()
    init_vehicles(NUM_VEHICLES)
    print(f"Publishing events for {NUM_VEHICLES} vehicles to {TOPIC} every {SEND_INTERVAL}s")
    try:
        while True:
            for v in vehicles:
                dyn = step_state(v)
                evt = make_event(v, dyn)
                payload = json.dumps(evt).encode("utf-8")
                # publish with attribute vin for easier filtering
                future = publisher.publish(TOPIC, payload, vin=v["vin"])
            print(f"Published {len(vehicles)} events @ {datetime.now(timezone.utc).isoformat()}")
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        print("Stopped simulator")

if __name__ == "__main__":
    publish_loop()
