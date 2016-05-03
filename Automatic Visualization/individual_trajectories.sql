CREATE VIEW individual_trajectories AS 
(select bld_nr,next_bld_nr,start_time,end_time
from (
	select 
		username, 
		mac, 
		LEAD(mac) OVER (ORDER BY mac,asstime) mac_next,
		SUBSTRING(SUBSTRING(maploc,position('> ' in maploc),char_length(maploc)),3, position(' >' in SUBSTRING(maploc,position('> ' in maploc),char_length(maploc)))-3) as bld_nr, 
		LEAD(SUBSTRING(SUBSTRING(maploc,position('> ' in maploc),char_length(maploc)),3, position(' >' in SUBSTRING(maploc,position('> ' in maploc),char_length(maploc)))-3)) OVER (ORDER BY mac,asstime) next_bld_nr, 
		asstime + sesdur - (time '00:05') as start_time,
		LEAD(asstime) OVER (ORDER BY mac,asstime) end_time
	from (
		select *
		from wifilog
		where substring(maploc,17,1) between '0' and '9' or  substring(maploc,17,1) = 'V'
		) as filtered
	where extract(day from (asstime - time '04:00')) = 11
	order by mac,asstime asc
	) as trajectories
where bld_nr != next_bld_nr 
and mac = mac_next
and end_time - start_time < time '01:00'
order by start_time)