drop table if exists buildingpartStates;

create table buildingpartStates(mac text NOT NULL,buildingpart integer,
	ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL,
    ap_start text, ap_end text,
    PRIMARY KEY(mac, ts));