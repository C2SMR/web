create table CITY
(
    NAME             varchar(200) not null
        primary key,
    mail             varchar(200) null,
    password         varchar(220) null,
    latitude         float null,
    longitude        float null,
    color_flag       int null,
    actual_picture   varchar(200) null,
    number_beach     int null,
    number_sea       int null,
    picture          longtext null,
    ip               varchar(200) null,
    name_ip          varchar(200) null,
    password_ip      varchar(200) null,
    run_detection    tinyint(1) null,
    type_detection   json null,
    blur             tinyint(1) null,
    detector_id      int null,
    launch_detection int null,
    stop_detection   int null
);

CREATE TABLE DATA
(
    ID             INTEGER PRIMARY KEY,
    CITY           VARCHAR(200) REFERENCES CITY (NAME),
    nb_beach       INTEGER,
    nb_sea         INTEGER,
    time           VARCHAR(200),
    precipitation  INTEGER,
    temp_beach     INTEGER,
    cloud_cover    INTEGER,
    wind           INTEGER,
    visibility     INTEGER,
    cam_visibility INTEGER
);

CREATE TABLE WARNINGS
(
    ID          INTEGER PRIMARY KEY,
    CITY        VARCHAR(200) REFERENCES CITY (NAME),
    color       INTEGER,
    information VARCHAR(220),
    picture     VARCHAR(220),
    notif       INTEGER
);

create table line
(
    ID    int auto_increment primary key,
    ville VARCHAR(200) not null,
    type  int          not null,
    x1    int,
    x2    int,
    y1    int,
    y2    int
);


/*---INSERT INIT DATA---*/

INSERT INTO DATA(ID)
VALUES (0);
INSERT INTO WARNINGS(ID)
VALUES (0);
