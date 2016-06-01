drop table if exists buildingpartStates;

create table buildingpartStates(mac text NOT NULL,buildingpart integer,
	ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL,
    PRIMARY KEY(mac, ts));