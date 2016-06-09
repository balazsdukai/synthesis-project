#!/bin/sh

#pg_dump -t visualization.bk_movement -C -h wifitracking.bk.tudelft.nl -U team2 wifi | psql -h localhost -U bdukai synth_project

pg_dump -t visualization.bk_mov_bouwpub -t visualization.bk_mov_canteen -C -h wifitracking.bk.tudelft.nl -U team2 wifi | psql -h localhost -U bdukai synth_project
