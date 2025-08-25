#!/usr/bin/env python3
import os, sys, io, re, json
import boto3, pandas as pd

AWS_REGION        = os.getenv('AWS_REGION')
S3_BUCKET_PARQUET = os.getenv('S3_BUCKET_PARQUET')
PREFIX            = (os.getenv('PREFIX') or '').lstrip('/')

if not (AWS_REGION and S3_BUCKET_PARQUET and PREFIX):
    sys.exit("Set AWS_REGION, S3_BUCKET_PARQUET, PREFIX env vars.")

GNSS_PREFIX = os.getenv('GNSS_PREFIX')
if not GNSS_PREFIX:
    GNSS_PREFIX = PREFIX.replace("CAN1_Analog1To4", "CAN9_GnssPos").rstrip('/') + '/'

s3 = boto3.client('s3', region_name=AWS_REGION)

def newest_parquet(bucket, prefix):
    pages = s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix)
    objs  = [o for p in pages for o in p.get('Contents', []) if o['Key'].lower().endswith('.parquet')]
    return max(objs, key=lambda o: o['LastModified']) if objs else None

def col_like(df, pattern, numeric=False):
    rx = re.compile(pattern, re.I)
    cols = [c for c in df.columns if rx.search(c)]
    if numeric:
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    return cols[0] if cols else None

def to_iso(dtval):
    try:
        return pd.to_datetime(dtval, errors='coerce', utc=True).isoformat()
    except Exception:
        return None

analog_obj = newest_parquet(S3_BUCKET_PARQUET, PREFIX)
if not analog_obj:
    sys.exit(f"No parquet under s3://{S3_BUCKET_PARQUET}/{PREFIX}")
analog_key = analog_obj["Key"]
blob = s3.get_object(Bucket=S3_BUCKET_PARQUET, Key=analog_key)['Body'].read()
adf = pd.read_parquet(io.BytesIO(blob))

ts_col  = col_like(adf, r'(^t$)|(time|timestamp|datetime|ts)')
lvl_col = col_like(adf, r'(lit(re|er)s?|level|volume|tank|depth|analog\d+)', numeric=True)

if ts_col:
    ts = pd.to_datetime(adf[ts_col], errors='coerce', utc=True)
    aidx = ts.idxmax() if ts.notna().any() else adf.index[-1]
else:
    aidx = adf.index[-1]
arow = adf.loc[aidx]
analog_iso = to_iso(arow[ts_col]) if ts_col else None

def fenv_float(name, default=None):
    v = os.getenv(name)
    return float(v) if v not in (None, "") else default

A1E = fenv_float("A1_EMPTY")              # raw Analog1 at empty (optional)
A1F = fenv_float("A1_FULL")               # raw Analog1 at full (optional)
LE  = fenv_float("LITRES_EMPTY", 0.0)
LF  = fenv_float("LITRES_FULL",  600.0)

litres = None
if "Analog1" in adf.columns and pd.notna(arow["Analog1"]) and A1E is not None and A1F is not None and A1F != A1E:
    litres = LE + (LF - LE) * ((float(arow["Analog1"]) - A1E) / (A1F - A1E))
    litres = max(min(litres, max(LE, LF)), min(LE, LF))
elif lvl_col and pd.notna(arow[lvl_col]):
    try:
        litres = float(arow[lvl_col])
    except Exception:
        litres = None

gps_current = None
breadcrumbs = []

gnss_obj = newest_parquet(S3_BUCKET_PARQUET, GNSS_PREFIX)
gnss_key = gnss_obj["Key"] if gnss_obj else None
if gnss_obj:
    gblob = s3.get_object(Bucket=S3_BUCKET_PARQUET, Key=gnss_key)['Body'].read()
    gdf = pd.read_parquet(io.BytesIO(gblob))
    # Note: lat = latitude, lng = longitude (correct order)
    g_ts  = col_like(gdf, r'(^t$)|(time|timestamp|datetime|ts)')
    g_lat = col_like(gdf, r'\b(lat|latitude)\b',  numeric=True)
    g_lon = col_like(gdf, r'\b(lon|lng|longitude)\b', numeric=True)
    if g_lat and g_lon:
        if g_ts:
            gdf = gdf.assign(_ts=pd.to_datetime(gdf[g_ts], errors='coerce', utc=True)).sort_values('_ts')
        last = gdf.tail(1).iloc[0]
        try:
            gps_current = {
                "lat": float(last[g_lat]),   # latitude
                "lng": float(last[g_lon]),   # longitude
                "timestamp": (to_iso(last[g_ts]) if g_ts else None)
            }
        except Exception:
            gps_current = None
        tail = gdf.tail(6)
        for _, r in tail.iterrows():
            try:
                breadcrumbs.append({
                    "lat": float(r[g_lat]),
                    "lng": float(r[g_lon]),
                    "timestamp": (to_iso(r[g_ts]) if g_ts else None)
                })
            except Exception:
                pass

payload = {
    "litres": round(litres, 1) if isinstance(litres, (int, float)) else None,
    "timestamp": analog_iso,
    "lat": (gps_current or {}).get("lat"),
    "lng": (gps_current or {}).get("lng"),
    "gps_current": gps_current,
    "breadcrumbs": breadcrumbs,
    "s3_key": analog_key,
    "gnss_key": gnss_key,
    # ← added calibration fields so the UI can display them
    "A1_EMPTY": A1E,
    "A1_FULL": A1F,
    "LITRES_EMPTY": LE,
    "LITRES_FULL": LF
}

with open("latest.json", "w") as f:
    json.dump(payload, f, indent=2)
print("latest.json:", json.dumps(payload, ensure_ascii=False))
