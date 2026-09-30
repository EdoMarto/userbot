-- Maps each source-channel message to its copy in the target channel.
CREATE TABLE IF NOT EXISTS tradingpost (
    send_id    BIGINT NOT NULL PRIMARY KEY,
    receive_id BIGINT NOT NULL
);
