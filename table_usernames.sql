--create a table of the unique usernames or keep the old if already exists
CREATE TABLE IF NOT EXISTS usernames (username text PRIMARY KEY);
INSERT INTO usernames SELECT DISTINCT username FROM wifilog;
CREATE INDEX i_usernames_username ON usernames USING btree (username);

