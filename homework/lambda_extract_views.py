import datetime
import json

import boto3
import requests

S3_WIKI_BUCKET = "szbeni-wikidata"


def lambda_handler(event, context):
    date_str = event.get("date")
    if date_str:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=21)

    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{date.strftime('%Y/%m/%d')}"
    response = requests.get(url, headers={"User-Agent": "curl/7.68.0"})

    if response.status_code != 200:
        raise Exception(f"Wikipedia API error: {response.status_code} - {response.text}")

    most_viewed = response.json()["items"][0]["articles"]

    current_time = datetime.datetime.now(datetime.timezone.utc)
    retrieved_at = current_time.replace(tzinfo=None).isoformat()

    json_lines = ""
    for page in most_viewed:
        record = {
            "title": page["article"],
            "views": page["views"],
            "rank": page["rank"],
            "date": date.strftime("%Y-%m-%d"),
            "retrieved_at": retrieved_at,
        }
        json_lines += json.dumps(record) + "\n"

    s3 = boto3.client("s3")
    s3_key = f"raw-views/raw-views-{date.strftime('%Y-%m-%d')}.json"
    s3.put_object(Bucket=S3_WIKI_BUCKET, Key=s3_key, Body=json_lines.encode("utf-8"))

    return {
        "statusCode": 200,
        "body": f"Uploaded {len(most_viewed)} records to s3://{S3_WIKI_BUCKET}/{s3_key}",
    }