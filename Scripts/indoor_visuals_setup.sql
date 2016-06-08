-- TODO: add foreign keys to the tables

-- select distinct buildingparts
CREATE MATERIALIZED VIEW visualization.bk_bpart_unq AS 
SELECT DISTINCT id, buildingpart
FROM public.buildingparts_bk;

-- !!!
-- see create_bk_movement.sql for creating the required movements table

-- add building part name field to the edge-vertex table
ALTER TABLE visualization.bk_paths_vertices_pgr 
    ADD COLUMN b_part text;

-- match the nodes from the building parts table to the edge-vertex table
UPDATE visualization.bk_paths_vertices_pgr AS a
SET b_part = b.b_part
FROM (SELECT p.id, b.b_part, p.the_geom
        FROM 
            visualization.bk_paths_vertices_pgr AS p, 
            (SELECT b_part, st_buffer(geom, 1.0) AS geom
             FROM visualization.bk_parts) AS b
        WHERE st_within(p.the_geom, b.geom)) AS b
WHERE a.id = b.id;

-- CREATE TABLE TO STORE traffic volume
CREATE TABLE if NOT EXISTS  visualization.bk_traffic(
    edge_id int4,
    cnt int4 DEFAULT 0);

-- fill IN the edge-ids
INSERT INTO visualization.bk_traffic (edge_id, cnt)
SELECT gid AS edge_id, 0
FROM visualization.bk_paths;


