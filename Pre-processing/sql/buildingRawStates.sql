drop table if exists buildingRawStates;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into buildingRawStates
from wifilog
where apname LIKE '%-%'
order by mac,asstime;

CREATE INDEX building_raw_states_index_mac ON buildingRawStates (mac);