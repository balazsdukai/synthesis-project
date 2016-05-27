CREATE OR REPLACE VIEW bk_test AS (
    SELECT username, asstime, to_char(asstime, 'day') weekday, sesdur, building_part
    FROM wifilogsmall, building_part_bk
    WHERE building_part_bk.apname = wifilogsmall.apname
);

SELECT * 
FROM bk_test
WHERE username = 'ytlQ36A0Sg7kt1FLYnVmTguf19NeO/JLDu6g6R08mpw='
AND sesdur > INTERVAL '10 minutes'
ORDER BY asstime;
