drop table if exists movements_temp;

select from_bldpart, to_bldpart, start_time, end_time, type 
into movements_temp 
from g2_buildingpartMovements
where from_bldpart != to_bldpart
and ({})
and (start_time+(end_time-start_time)/2)::date in ({})
and type in ({});
