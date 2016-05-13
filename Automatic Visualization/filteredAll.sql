drop table if exists filtered;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into filtered
from wifilog
where apname LIKE '%-%'
order by mac,asstime;

CREATE INDEX i_mac ON filtered (mac);