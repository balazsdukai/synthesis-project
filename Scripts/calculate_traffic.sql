-- function to match the traffic count to the path network in BK
-- table and field names are hardcoded, it requires the data model as it is set up by 'indoor_visuals_setup.sql'
-- uses pgrouting 2.1.0 pgr_dijkstra() function
-- Example use:
-- SELECT calculate_traffic();

CREATE OR REPLACE FUNCTION calculate_traffic()
    RETURNS text
AS $$
rv = plpy.execute("select * from visualization.bk_movement");
a = "Succes";
for i in rv:
    startp = i['startp']
    endp = i['endp']
    cnt = i['cnt']
    query = "select id::int4 from visualization.bk_paths_vertices_pgr where b_part = '{}'".format(startp)
    x = plpy.execute(query)
    sp = x[0]['id']
    query = "select id from visualization.bk_paths_vertices_pgr where b_part = '{}'".format(endp)
    y = plpy.execute(query)
    ep = y[0]['id']
    query = "SELECT seq, id1 as node, id2 as edge FROM pgr_dijkstra('SELECT gid as id, source::int4, target::int4, cost_len::float8 as cost FROM visualization.bk_paths', {}, {}, false, false);".format(sp,ep)
    s_path = plpy.execute(query)
    for e in s_path:
		edge_id = e['edge']
		if edge_id >= 0:
			query = "update visualization.bk_traffic set cnt = cnt + {} where edge_id = {};".format(cnt, edge_id)
			plpy.execute(query)
return a
$$ LANGUAGE plpythonu;

