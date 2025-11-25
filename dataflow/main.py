import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
import json

# -----------------------------
# Pipeline Options
# -----------------------------
options = PipelineOptions(
    project='boxwood-axon-470816-b1',
    region='us-central1',
    temp_location='gs://ev-raw/temp',
    streaming=True,
    runner='DataflowRunner',
    job_name='pubsub-to-bq-simple'
)
options.view_as(StandardOptions).streaming = True

# -----------------------------
# Simple validation function
# -----------------------------
def validate_message(msg):
    try:
        msg = json.loads(msg.decode('utf-8'))
        required_fields = [
            "vin", "vehicle_model", "timestamp", "gps_lat", "gps_lon",
            "speed_kmph", "odometer_km", "state_of_charge_percent",
            "state_of_health_percent", "motor_temp_c",
            "charging_state", "charging_power_kw"
        ]
        for field in required_fields:
            if field not in msg:
                return None
        # Convert numeric fields
        for field in ["gps_lat","gps_lon","speed_kmph","odometer_km",
                      "state_of_charge_percent","state_of_health_percent",
                      "motor_temp_c","charging_power_kw"]:
            msg[field] = float(msg[field])
        return msg
    except Exception:
        return None

# -----------------------------
# Pipeline
# -----------------------------
with beam.Pipeline(options=options) as p:
    (
        p
        | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(
            subscription='projects/boxwood-axon-470816-b1/subscriptions/ev-telemetry-topic-sub'
        )
        | 'Validate' >> beam.Map(validate_message)
        | 'FilterValid' >> beam.Filter(lambda x: x is not None)
        | 'WriteToBigQuery' >> WriteToBigQuery(
            table='boxwood-axon-470816-b1.bronze.bronze_ev_telemetry',
            schema=(
                'vin:STRING, vehicle_model:STRING, timestamp:STRING, '
                'gps_lat:FLOAT, gps_lon:FLOAT, speed_kmph:FLOAT, odometer_km:FLOAT, '
                'state_of_charge_percent:FLOAT, state_of_health_percent:FLOAT, '
                'motor_temp_c:FLOAT, charging_state:STRING, charging_power_kw:FLOAT'
            ),
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
    )
