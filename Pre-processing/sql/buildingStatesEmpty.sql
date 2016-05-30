drop table if exists buildingStates;

create table buildingStates(mac text NOT NULL,building integer,
	ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL,
    PRIMARY KEY(mac, ts));