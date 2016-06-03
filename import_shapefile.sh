#!/bin/sh

shp2pgsql -s 3857 -S '/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/Graphs, BuildingParts & Nodes/merged_graphs' visualization.bk_paths | psql -h localhost -U bdukai synth_project

shp2pgsql -s 3857 -S '/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/Graphs, BuildingParts & Nodes/merged_nodes' visualization.bk_parts | psql -h localhost -U bdukai synth_project

