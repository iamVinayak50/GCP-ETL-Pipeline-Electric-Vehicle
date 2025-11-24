import json
import argparse
import apache_beam as beam
from datetime import datetime
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions


# ------------------------
# DQ + Error Handler
# ------------------------
def validate_and_clean(record):
    """Returns (valid_record, None) or (None, error_record)"""
    try:
        # Mandatory fields check
        if not record.get("vehicle_id"):
            raise ValueError("Missing vehicle_id")
        if not record.get("timestamp"):
            raise ValueError("Missing timestamp")

        # Type validation
        record["speed"] = float(record.get("speed", 0))
        record["battery_level"] = float(record.get("battery_level", 0))

        # Range validation
        if record["battery_level"] < 0 or record["battery_level"] > 100:
            raise ValueError("battery_level out of range")

        # Add ingestion time
        record["ingestion_time"] = datetime.utcnow().isoformat()

        return (record, None)

    except Exception as e:
        # Send error record to DLQ
        error_rec = {
            "raw_data": str(record),
            "error_message": str(e),
            "error_time": datetime.utcnow().isoformat()
        }
        return (None, error_rec)


# ------------------------
# Main Pipeline
# ------------------------
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--pubsub_topic", required=True)
    parser.add_argument("--bq_valid_table", required=True)
    parser.add_argument("--bq_error_table", required=True)
    args, beam_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(
        beam_args,
        streaming=True,
        save_main_session=True
    )

    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:

        decoded = (
            p
            | "ReadFromPubSub" >> beam.io.ReadFromPubSub(topic=args.pubsub_topic)
            | "Decode" >> beam.Map(lambda x: json.loads(x.decode("utf-8")))
        )

        # Apply validation logic
        validated = decoded | "Validate" >> beam.Map(validate_and_clean)

        valid = validated | "GetValid" >> beam.Filter(lambda x: x[0] is not None) \
                          | beam.Map(lambda x: x[0])

        errors = validated | "GetErrors" >> beam.Filter(lambda x: x[1] is not None) \
                           | beam.Map(lambda x: x[1])

        # Write valid records
        valid | "WriteValidToBQ" >> beam.io.WriteToBigQuery(
            table=args.bq_valid_table,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )

        # Write bad records
        errors | "WriteErrorsToBQ" >> beam.io.WriteToBigQuery(
            table=args.bq_error_table,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )


if __name__ == "__main__":
    run()
