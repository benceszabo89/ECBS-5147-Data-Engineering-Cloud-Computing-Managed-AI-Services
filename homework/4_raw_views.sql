CREATE EXTERNAL TABLE raw_views (
    title         STRING,
    views         BIGINT,
    rank          INT,
    date          STRING,
    retrieved_at  STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://szbeni-wikidata/raw-views/';