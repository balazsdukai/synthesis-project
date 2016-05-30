select mac,mobilityRatio
into mobility
from (
	select 
		mac,
		count(*) as total_scans,
		sum(case when sesdur < time '00:06:00' then 1 else 0 end)/cast(count(*) as numeric(5,0)) as mobilityRatio
	from wifilog
	group by mac
	) as AZZ
where total_scans>100
order by mobilityRatio
