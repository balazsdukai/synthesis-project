ALTER TABLE visualization.bk_paths
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

SELECT pgr_createTopology('visualization.bk_paths', 0.5, 'geom', 'gid');
SELECT pgr_analyzegraph('visualization.bk_paths', 0.5, 'geom', 'gid');

-- assign costs to the edges
UPDATE visualization.bk_paths as a
SET cost_len = b.len
FROM (SELECT gid, st_length(geom) as len
FROM visualization.bk_paths
WHERE name != 'staris') b
WHERE a.gid = b.gid;

UPDATE visualization.bk_paths as a
SET cost_len = 20
WHERE name LIKE 'stairs';

-- test query
SELECT seq, id1 as node, id2 as edge 
FROM pgr_dijkstra(
	'SELECT gid as id, source::int4, target::int4, cost_len::float8 as cost FROM visualization.bk_paths',
	 15, 		-- start vertex id
	  3,		-- end vertex id
	 false,		-- directed graph is used
	 false		-- route has reverse costs
);	 

