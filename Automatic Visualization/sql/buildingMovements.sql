drop table if exists buildingmovements_temp;

select from_bld, to_bld, start_time, end_time, type 
into buildingmovements_temp 
from g2_buildingMovements
where from_bld != to_bld
and ({})
and (start_time+(end_time-start_time)/2)::date in ({})
and type in ({});
