#!/bin/sh

pg_dump -t visualization.bk_paths -t visualization.bk_paths_vertices_pgr -t visualization.bk_traffic -t visualization.bk_parts -C -h localhost -U bdukai synth_project | psql -h wifitracking.bk.tudelft.nl -U team2 wifi
