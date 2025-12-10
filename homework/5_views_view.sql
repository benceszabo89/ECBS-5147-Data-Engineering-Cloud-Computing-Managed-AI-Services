CREATE VIEW szbeni.views AS
    SELECT
        title,
        views,
        rank,
        date,
        retrieved_at,
        cast(from_iso8601_timestamp(retrieved_at) AS TIMESTAMP) as retrieved_at
    FROM szbeni.raw-views
    ORDER BY
    date ASC,
    rank ASC;