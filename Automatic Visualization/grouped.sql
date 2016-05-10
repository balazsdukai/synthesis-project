drop table if exists grouped;

create table grouped(mac text NOT NULL,building text NOT NULL,
	ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL,
    ap_start text NOT NULL, ap_end text NOT NULL,
    PRIMARY KEY(mac, ts));