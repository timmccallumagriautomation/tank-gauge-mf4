# Tank Gauge 

Monitor tank level via on-board CANedge2 and sensors.

# Dashboard

This is just a prototype to research options for how to read the information coming from the CANedge2 and sensors. Alternatives include Grafana "[gauge](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/gauge/)" and Grafana "[geomap](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/geomap/)". The following uses HTML. Bootstrap, Apache Visualisation (in the meantime).

<img width="1813" height="1034" alt="Screenshot from 2025-08-25 20-18-35" src="https://github.com/user-attachments/assets/800d4203-d363-4c98-844b-b7892a222b1a" />

# AWS Bucket interoperability

# Secrets

Use the repositories secret variables "Settings"->"Security"->"Secrets and Variables"->"Actions"->"New Repository Secret".

# Test Access To Latest File

```bash
export AWS_ACCESS_KEY_ID="" AWS_SECRET_ACCESS_KEY="..." AWS_REGION="" S3_BUCKET_PARQUET="" S3_BUCKET_MDF="" PREFIX=""
```

# GitHub Actions

Calibrate the sensor using GitHub Environment Variables:







