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
