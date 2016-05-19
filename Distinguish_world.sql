-- Total movement
select count(*)
from trajectories
where (from_bld != 0 or to_bld != 0) and extract(hour from end_time-(end_time-start_time)/2) = 8;

-- Between buildings
select count(*)
from trajectories
where from_bld != 0 and to_bld != 0 and extract(hour from end_time-(end_time-start_time)/2) = 8;

-- Between world and buildings
select count(*)
from trajectories
where (from_bld = 0 or to_bld = 0) and extract(hour from end_time-(end_time-start_time)/2) = 8;

