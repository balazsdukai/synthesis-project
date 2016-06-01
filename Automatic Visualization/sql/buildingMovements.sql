drop table if exists buildingmovements_temp;
create table buildingmovements_temp 
	(
	from_bld integer,
  	to_bld integer,
  	start_time timestamp without time zone,
  	end_time timestamp without time zone,
  	type text
);

insert into buildingmovements_temp
select from_bld, to_bld, start_time, end_time, type  
from g2_buildingMovements
where from_bld != to_bld
and from_bld in ({})
and to_bld in ({})
and (start_time+(end_time-start_time)/2)::date in ({})
and type in ({});
