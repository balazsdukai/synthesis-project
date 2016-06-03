#!/bin/sh

pg_dump -t visualization.bk_movement -t visualization.bk_paths -t visualization.bk_parts -C -h wifitracking.bk.tudelft.nl -U team2 wifi | psql -h localhost -U bdukai synth_project
