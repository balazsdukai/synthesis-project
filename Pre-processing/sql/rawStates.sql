drop table if exists rawStates;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into rawStates
from wifilogSmall
where apname LIKE '%-%'
order by mac,asstime;

CREATE INDEX raw_states_index_mac ON rawStates (mac);