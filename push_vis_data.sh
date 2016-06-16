#!/bin/sh

#pg_dump -t visualization.bk_paths -t visualization.bk_paths_vertices_pgr -t visualization.bk_traffic -t visualization.bk_parts -C -h localhost -U bdukai synth_project | psql -h wifitracking.bk.tudelft.nl -U team2 wifi

#pg_dump -t visualization.bk_traf_bouwpub -t visualization.bk_traf_canteen -C -h localhost -U bdukai synth_project | psql -h wifitracking.bk.tudelft.nl -U team2 wifi

pg_dump -t visualization.bk_traf_bkbeats -C -h localhost -U bdukai synth_project | psql -h wifitracking.bk.tudelft.nl -U team2 wifi
