#!/usr/bin/env python

import boto3, tempfile, os, cli.log

@cli.log.LoggingApp
def s3bury(app):
    bucket = app.params.bucket
    expires_in = app.params.expires_in
    max_keys = app.params.max_keys
    files = app.params.files

    s3_res = boto3.resource("s3")
    s3_client = boto3.client("s3")

    obj = s3_client.list_objects(Bucket=bucket, MaxKeys=max_keys)["Contents"][0] # Just get the first one for now
    _, temp_path = tempfile.mkstemp()

    print("[*] Downloading %s from %s to %s" % (obj["Key"], bucket, temp_path))
    s3_res.Bucket(bucket).download_file(obj["Key"], temp_path)

    for filename in files:
        print("[*] Uploading %s" % filename)
        s3_res.Bucket(bucket).upload_file(filename, obj["Key"])
        obj_meta = s3_client.head_object(Bucket=bucket, Key=obj["Key"])
        version_id = obj_meta["VersionId"]
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            ExpiresIn=expires_in,
            Params={
                "Bucket": bucket,
                "Key": obj["Key"],
                "VersionId": version_id
            }
        )
        print("[*] Buried %s as presigned url %s" % (filename, url))

    print("[*] Restoring original object")
    s3_res.Bucket(bucket).upload_file(temp_path, obj["Key"])
    print("[*] Removing tempory file %s" % temp_path)
    os.remove(temp_path)
    print("[*] Done")

s3bury.add_param("--bucket", "-b", help="Bucket to bury files in", required=True)
s3bury.add_param("--expires-in", help="Presigned URL expiry time in seconds (default: 7 days)", default=60*60*24*7)
s3bury.add_param("--max-keys", help="Maximum number of keys to get from bucket (default: 10)", default=10)
s3bury.add_param("files", help="Files to bury", action="append")

if __name__ == "__main__":
    s3bury.run()
