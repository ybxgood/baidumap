CREATE TABLE baidumap.address (
id INTEGER PRIMARY KEY auto_increment,
uid VARCHAR ( 24 ) NOT NULL,
aname VARCHAR ( 100 ) NOT NULL,
lng FLOAT8 NOT NULL,
lat FLOAT8 NOT NULL,
address VARCHAR ( 200 ) NOT NULL,
telephone VARCHAR ( 20 ) NOT NULL,
keyword VARCHAR ( 200 )
);
