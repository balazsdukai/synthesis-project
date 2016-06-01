#!/bin/sh

shp2pgsql -s 3857 -S '/var/nobackup/Google_Drive/TU-Delft_GEO1101_Group-2/data/bk_map/paths_bg.shp' public.bk_bg_paths | psql -h localhost -d geo1006_hw1 -U bdukai