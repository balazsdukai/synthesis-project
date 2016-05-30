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
	) as movements
natural join mobility
where from_bld != to_bld 
and mac = mac_next
and start_time < end_time
and end_time - start_time < time '01:00'
order by start_time;

ALTER TABLE buildingMovements ADD PRIMARY KEY (mac,start_time);
CREATE INDEX building_movements_index_frombld ON buildingMovements (from_bld);
CREATE INDEX building_movements_index_tobld ON buildingMovements (to_bld);
CREATE INDEX building_movements_index_starttime ON buildingMovements (start_time);
CREATE INDEX building_movements_index_endtime ON buildingMovements (end_time);