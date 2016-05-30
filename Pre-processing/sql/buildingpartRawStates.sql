drop table if exists buildingpartRawStates;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into buildingpartRawStates
from wifilogSmall
where maploc LIKE '%BK%'
order by mac,asstime;

CREATE INDEX buildingpart_raw_states_index_mac ON buildingpartRawStates (mac);