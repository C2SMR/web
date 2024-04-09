CREATE TABLE CITY(
    NAME VARCHAR(200) PRIMARY KEY ,
    mail VARCHAR(200),
    password VARCHAR(220),
    latitude FLOAT,
    longitude FLOAT,
    color_flag INTEGER,
    actual_picture VARCHAR(200),
    number_beach INTEGER,
    number_sea INTEGER,
    picture longtext,
    ip VARCHAR(200),
    name_ip VARCHAR(200),
    password_ip VARCHAR(200),
    run_detection BOOLEAN,
    type_detection JSON,
    blur BOOLEAN,
    detector_id INTEGER,
    stop_detection datetime,
    start_detection datetime,
);

CREATE TABLE DATA(
    ID INTEGER PRIMARY KEY ,
    CITY VARCHAR(200) REFERENCES CITY(NAME),
    nb_beach INTEGER,
    nb_sea INTEGER,
    time VARCHAR(200),
    precipitation INTEGER,
    temp_beach INTEGER,
    cloud_cover INTEGER,
    wind INTEGER,
    visibility INTEGER,
    cam_visibility INTEGER
);

CREATE TABLE WARNINGS(
    ID INTEGER PRIMARY KEY ,
    CITY VARCHAR(200) REFERENCES CITY(NAME),
    color INTEGER,
    information VARCHAR(220),
    picture VARCHAR(220),
    notif INTEGER
);

create table line (
    ID int auto_increment primary key ,
    ville VARCHAR(200) not null ,
    type int not null ,
    x1 int,
    x2 int,
    y1 int,
    y2 int
);


/*---INSERT INIT DATA---*/

INSERT INTO DATA(ID) VALUES(0);
INSERT INTO WARNINGS(ID) VALUES (0);
