drop table if exists filtered;

select 
	mac,
	maploc,
	asstime as start_time,
	asstime + sesdur as end_time,
	apname 
into filtered
from wifilog
where ((asstime+sesdur-time'03:00')::date in ({}) or (asstime-time'05:00')::date in ({}))
and (substring(maploc,17,1) between '0' and '9' or  substring(maploc,17,1) = 'V')
order by mac,asstime;

CREATE INDEX i_mac ON filtered (mac);