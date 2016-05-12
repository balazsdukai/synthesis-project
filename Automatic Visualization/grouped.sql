drop table if exists grouped;

create table grouped(mac text NOT NULL,building text,
	ts timestamp without time zone NOT NULL,te timestamp without time zone NOT NULL,
    ap_start text, ap_end text,
    PRIMARY KEY(mac, ts));