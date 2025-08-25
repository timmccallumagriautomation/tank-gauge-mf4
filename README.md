# Tank Gauge 

Monitor tank level via on-board CANedge2 and sensors.

# Dashboard

This is just a prototype to research options of how to read the information coming from the CANedge2 and sensors. Alternatives include Grafana "[gauge](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/gauge/)" and Grafana "[geomap](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/geomap/)". The following uses HTML. Bootstrap, Google Visualisation (in the meantime).

<img width="1341" height="963" alt="Screenshot from 2025-08-18 15-05-35" src="https://github.com/user-attachments/assets/7121a718-7426-4648-9a4e-7bb4ad8eecaf" />

# Roadmap

- [] Add AWS S3 bucket interoperability
- [] Add GitHub Action Secrets/Configuration
- [] Write `.mf4`/`latest.json` file parser
- [] Add issues and requests as the sensor nodes start to come online (look at what the CANedge2 is pushing into S3 storage)

# AWS Bucket interoperability

# Secrets

Use the repositories secret variables "Settings"->"Security"->"Secrets and Variables"->"Actions"->"New Repository Secret".

# Test Access To Latest File

```bash
export AWS_ACCESS_KEY_ID="" AWS_SECRET_ACCESS_KEY="..." AWS_REGION="" S3_BUCKET_PARQUET="" S3_BUCKET_MDF="" PREFIX=""
```

```bash
python3.12 test_tank_latest_data.py 
```

Will output something line this:

```bash
latest_key: C4DF4028/CAN1_Analog1To4/2025/08/25/00000018_00000075.parquet
latest_day_prefix: C4DF4028/CAN1_Analog1To4/2025/08/25/
```

# Test GitHub Action Logic

You can also set local environment variables and test access to buckets and more. First set the env vars:

```bash
export AWS_ACCESS_KEY_ID="" AWS_SECRET_ACCESS_KEY="..." AWS_REGION="" S3_BUCKET_PARQUET="" S3_BUCKET_MDF="" PREFIX=""
```

Set up a Python VENV:

```bash
python3.12 -m venv myenv
python3 -m venv myenv
source myenv/bin/activate
```
Install `boto3` and `pandas`:

```bash
python3.12 -m pip install --upgrade pip setuptools wheel
pip3 install boto3 pandas
pip install "pyarrow"
```

```bash
python3.12 test_tank_data_source.py 
```

The above script will output something like this:

```json
{
    "litres": 1755,
    "timestamp": "2025-08-25T01:49:59.413300+00:00",
    "lat": -35.12943,
    "lng": 139.129435,
    "gps_current": {
        "lat": -35.12943,
        "lng": 139.129435,
        "timestamp": "2025-08-25T01:49:59.863602+00:00"
    },
    "breadcrumbs": [
        {
            "lat": -35.12943,
            "lng": 139.12943,
            "timestamp": "2025-08-25T01:49:58.675652+00:00"
        },
        {
            "lat": -35.12943,
            "lng": 139.129431,
            "timestamp": "2025-08-25T01:49:59.071602+00:00"
        },
        {
            "lat": -35.12943,
            "lng": 139.129432,
            "timestamp": "2025-08-25T01:49:59.269602+00:00"
        },
        {
            "lat": -35.12943,
            "lng": 139.129433,
            "timestamp": "2025-08-25T01:49:59.467652+00:00"
        },
        {
            "lat": -35.12943,
            "lng": 139.129434,
            "timestamp": "2025-08-25T01:49:59.665852+00:00"
        },
        {
            "lat": -35.12943,
            "lng": 139.129435,
            "timestamp": "2025-08-25T01:49:59.863602+00:00"
        }
    ],
    "s3_key": "C4DF4028/CAN1_Analog1To4/2025/08/25/00000018_00000103.parquet",
    "gnss_key": "C4DF4028/CAN9_GnssPos/2025/08/25/00000018_00000103.parquet"
}
```

# GitHub Actions

Calibrate the sensor using GitHub Environment Variables:







