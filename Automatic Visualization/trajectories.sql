drop table if exists trajectories;

select building,next_building,start_time,end_time into trajectories
from (
	select 
		mac, 
		LEAD(mac) OVER (ORDER BY mac,ts) mac_next,
		building, 
		LEAD(building) OVER (ORDER BY mac,ts) next_building, 
		te - (time '00:05') as start_time,
		LEAD(ts) OVER (ORDER BY mac,ts) end_time
	from (
		select *
		from {}
		where ((ts-time'01:00')::date in ({}) or (te+time'01:00')::date in ({}))
		) as filtered
	order by mac,start_time asc
	) as trajectories
where building != next_building 
and mac = mac_next
and end_time - start_time < time '01:00'
and (start_time+(end_time-start_time)/2)::date in ({})
and building in ({})
and next_building in ({})
order by start_time