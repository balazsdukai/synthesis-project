-- table of movement counts (total time)
CREATE TABLE visualization.bk_movement AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 and from_bldpart > 0
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);

CREATE INDEX startp_idx ON visualization.bk_movement (startp);
CREATE INDEX endp_idx ON visualization.bk_movement (endp);
CREATE INDEX cnt_idx ON visualization.bk_movement (cnt);

-- table of static movement counts (total time)
CREATE TABLE visualization.bk_mov_static AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 
            AND from_bldpart > 0 
            AND "type" LIKE 'static'
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);

-- table of mobile movement counts (total time)
CREATE TABLE visualization.bk_mov_mobile AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 
            AND from_bldpart > 0 
            AND "type" LIKE 'mobile'
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);

-- table of mobile movement counts (weekdays)
CREATE TABLE visualization.bk_mov_weekday AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 
            AND from_bldpart > 0 
            AND "type" LIKE 'mobile'
            AND (start_time+(end_time-start_time)/2)::date in ('2016-04-18','2016-04-19','2016-04-20','2016-04-21','2016-04-22','2016-04-25','2016-04-26','2016-04-28','2016-04-29','2016-05-02','2016-05-03','2016-05-04','2016-05-09','2016-05-10','2016-05-11','2016-05-12','2016-05-13','2016-05-17','2016-05-18','2016-05-19','2016-05-20','2016-05-23','2016-05-24','2016-05-25','2016-05-26','2016-05-27')
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);

-- table of mobile movement counts (weekends)
CREATE TABLE visualization.bk_mov_weekend AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart > 0 
            AND from_bldpart > 0 
            AND "type" LIKE 'mobile'
            AND  (start_time+(end_time-start_time)/2)::date in ('2016-04-02','2016-04-03','2016-04-09','2016-04-10','2016-04-16','2016-04-17','2016-04-23','2016-04-24','2016-04-30','2016-05-01','2016-05-07','2016-05-08','2016-05-14','2016-05-15','2016-05-21','2016-05-22')
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);

-- table of mobile movement counts to Bouwpub (weekdays)
CREATE TABLE visualization.bk_mov_bouwpub AS
(SELECT 
    startp,
    ep.buildingpart AS endp,
    cnt
FROM (
    SELECT 
        sp.buildingpart AS startp,
        a.to_bldpart,
        a.cnt
    FROM 
        (SELECT 
            from_bldpart,
            to_bldpart,
            count(*) AS cnt
        FROM public.g2_buildingpartmovements
        WHERE to_bldpart = 10 
            AND from_bldpart > 0 
            AND "type" LIKE 'mobile'
            AND (start_time+(end_time-start_time)/2)::date in ('2016-04-18','2016-04-19','2016-04-20','2016-04-21','2016-04-22','2016-04-25','2016-04-26','2016-04-28','2016-04-29','2016-05-02','2016-05-03','2016-05-04','2016-05-09','2016-05-10','2016-05-11','2016-05-12','2016-05-13','2016-05-17','2016-05-18','2016-05-19','2016-05-20','2016-05-23','2016-05-24','2016-05-25','2016-05-26','2016-05-27')
        GROUP BY from_bldpart, to_bldpart) AS a
    INNER JOIN visualization.bk_bpart_unq AS sp
        ON a.from_bldpart = sp.id
    ) b
INNER JOIN visualization.bk_bpart_unq AS ep
    ON b.to_bldpart = ep.id
);