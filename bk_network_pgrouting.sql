ALTER TABLE bk_bg_paths
    ADD COLUMN source integer,
    ADD COLUMN target integer,
    ADD COLUMN cost_len double precision,
    ADD COLUMN cost_time double precision,
    ADD COLUMN rcost_len double precision,
    ADD COLUMN rcost_time double precision,
    ADD COLUMN x1 double precision,
    ADD COLUMN y1 double precision,
    ADD COLUMN x2 double precision,
    ADD COLUMN y2 double precision,
    ADD COLUMN to_cost double precision,
    ADD COLUMN rule text,
    ADD COLUMN isolated integer;
    
SELECT pgr_createTopology('bk_bg_paths', 0.0, 'geom', 'gid');

SELECT pgr_analyzegraph('bk_bg_paths', 0.0, 'geom', 'gid');

/*
 * Check if there the multi-geometries are real multi-geometries, and correct them if they are
 * Reference: http://gis.stackexchange.com/questions/116414/take-from-multilinestring-the-start-end-points/116444#116444
 */
SELECT COUNT(
        CASE WHEN ST_NumGeometries(geom) > 1 THEN 1 END
    ) AS multi, COUNT(geom) AS total 
FROM bk_bg_paths;

ALTER TABLE bk_bg_paths
    ALTER COLUMN geom TYPE geometry(LineString, 4326) 
    USING ST_GeometryN(geom, 1);

SELECT pgr_nodeNetwork('bk_bg_paths', 0.0, 'gid', 'geom');

SELECT pgr_createTopology('bk_bg_paths_noded', 0.0, 'geom', 'id');
