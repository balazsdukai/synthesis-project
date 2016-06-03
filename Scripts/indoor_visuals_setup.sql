-- TODO: add foreign keys to the tables

-- select distinct buildingparts
CREATE MATERIALIZED VIEW visualization.bk_bpart_unq AS 
SELECT DISTINCT id, buildingpart
FROM public.buildingparts_bk;

-- drop materialized view visualization.bk_movement;

-- view to store the aggergated movement counts
CREATE TABLE visualization.bk_movement AS
SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 and from_bldpart > 0
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id;

CREATE INDEX startp_idx ON visualization.bk_movement (startp);
CREATE INDEX endp_idx ON visualization.bk_movement (endp);
CREATE INDEX cnt_idx ON visualization.bk_movement (cnt);

-- refresh materialized view with: 
-- REFRESH MATERIALIZED VIEW visualization.bk_movement;



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
             FROM bk_parts) AS b
        WHERE st_within(p.the_geom, b.geom)) AS b
WHERE a.id = b.id;

-- CREATE TABLE TO STORE traffic volume
CREATE TABLE visualization.bk_traffic(
    edge_id int4,
    cnt int4 DEFAULT 0);

-- fill IN the edge-ids
INSERT INTO visualization.bk_traffic (edge_id, cnt)
SELECT gid AS edge_id, 0
FROM visualization.bk_paths;


