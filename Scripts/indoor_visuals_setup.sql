-- TODO: add foreign keys to the tables

-- table to store the aggergated movement counts
CREATE TABLE bk_movement (
    id serial PRIMARY KEY,
    startp text,
    endp text,
    cnt int4);

-- insert dummy data
INSERT INTO bk_movement (startp, endp, cnt) VALUES ('OTB', 'Urbanism', 10);
INSERT INTO bk_movement (startp, endp, cnt) VALUES ('Urbanism', 'Bouwpub', 30);
INSERT INTO bk_movement (startp, endp, cnt) VALUES ('Orange hall', 'Restaurant', 50);
INSERT INTO bk_movement (startp, endp, cnt) VALUES ('Restaurant', 'East wing', 40);

-- add building part name field to the edge-vertex table
ALTER TABLE bk_paths_vertices_pgr 
    ADD COLUMN b_part text;

-- match the nodes from the building parts table to the edge-vertex table
UPDATE bk_paths_vertices_pgr AS a
SET b_part = b.b_part
FROM (SELECT p.id, b.b_part, p.the_geom
        FROM 
            bk_paths_vertices_pgr AS p, 
            (SELECT b_part, st_buffer(geom, 1.0) AS geom
             FROM bk_parts) AS b
        WHERE st_within(p.the_geom, b.geom)) AS b
WHERE a.id = b.id;

-- CREATE TABLE TO STORE traffic volume
CREATE TABLE bk_traffic(
    edge_id int4,
    cnt int4 DEFAULT 0);

-- fill IN the edge-ids
INSERT INTO bk_traffic (edge_id, cnt)
SELECT gid AS edge_id, 0
FROM bk_paths;


