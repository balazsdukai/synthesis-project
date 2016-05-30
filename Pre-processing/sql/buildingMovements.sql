drop table if exists buildingMovements;

select mac,from_bld,to_bld,start_time,end_time,(case when mobilityratio < 0.27 then 'static' else 'mobile' end) as type 
into buildingMovements
from (
	select 
		mac, 
		LEAD(mac) OVER (ORDER BY mac,ts) mac_next,
		building as from_bld, 
		LEAD(building) OVER (ORDER BY mac,ts) to_bld, 
		te - (time '00:05') as start_time,
		LEAD(ts) OVER (ORDER BY mac,ts) end_time
	from buildingStates
	order by mac,start_time asc
	) as movements
natural join mobility
where from_bld != to_bld 
and mac = mac_next
and end_time - start_time < time '01:00'
order by start_time