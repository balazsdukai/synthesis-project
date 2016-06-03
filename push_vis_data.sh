#!/bin/sh

pg_dump -t visualization.bk_paths -t visualization.bk_paths_vertices_pgr -t visualization.bk_traffic -C -h localhost -U bdukai synth_project | psql -n visualization -h wifitracking.bk.tudelft.nl -U team2 wifi
