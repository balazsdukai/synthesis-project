drop table if exists buildingpartMovements;

select mac,from_bldpart,to_bldpart,start_time,end_time,(case when mobilityratio < 0.27 then 'static' else 'mobile' end) as type 
into buildingpartMovements
from (
	select 
		mac, 
		LEAD(mac) OVER (ORDER BY mac,ts) mac_next,
		buildingpart as from_bldpart, 
		LEAD(buildingpart) OVER (ORDER BY mac,ts) to_bldpart, 
		te - (time '00:05') as start_time,
		LEAD(ts) OVER (ORDER BY mac,ts) end_time
	from buildingpartStates
	) as movements
natural join mobility
where from_bldpart != to_bldpart 
and mac = mac_next
and start_time < end_time
and end_time - start_time < time '01:00'
order by start_time;

ALTER TABLE buildingpartMovements ADD PRIMARY KEY (mac,start_time);
CREATE INDEX buildingpart_movements_index_frombldpart ON buildingpartMovements (from_bldpart);
CREATE INDEX buildingpart_movements_index_tobldpart ON buildingpartMovements (to_bldpart);
CREATE INDEX buildingpart_movements_index_starttime ON buildingpartMovements (start_time);
CREATE INDEX buildingpart_movements_index_endtime ON buildingpartMovements (end_time);