drop table if exists filtered;

select 
	mac,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname
into filtered
from wifilog
where ((asstime+sesdur-time'03:00')::date in ('2016-05-03') or (asstime-time'05:00')::date in ('2016-05-03'))
and apname LIKE '%-%'
order by mac,asstime;

CREATE INDEX i_mac ON filtered (mac);