import os, boto3
s3=boto3.client('s3', region_name=os.environ['AWS_REGION']); bucket=os.environ['S3_BUCKET_PARQUET']; base=os.environ['PREFIX']
it=(o for p in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=base) for o in p.get('Contents',[]) if o['Key'].lower().endswith('.parquet'))
latest=max(it, key=lambda o:o['LastModified']); key=latest['Key']; day_prefix=key.rsplit('/',1)[0]+'/'
print("latest_key:", key); print("latest_day_prefix:", day_prefix)