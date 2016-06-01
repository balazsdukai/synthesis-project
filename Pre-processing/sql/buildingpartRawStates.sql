drop table if exists buildingpartRawStates;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into buildingpartRawStates
from wifilog
where apname LIKE 'A-08%'
order by mac,asstime;

CREATE INDEX buildingpart_raw_states_index_mac ON buildingpartRawStates (mac);