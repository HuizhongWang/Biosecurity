use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now varchar(8) not null,
address varchar(500) not null,
email varchar(300) not null,
phone varchar(11) not null,
date_joined date not null
);


CREATE TABLE IF NOT EXISTS staff
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30),
family_name varchar(30) not null,
status_now varchar(8) not null,
email varchar(300) not null,
phone varchar(11) not null,
hire_date date not null,
staff_position varchar(100) not null,
department varchar(100) not null
);

CREATE TABLE IF NOT EXISTS admini
(
admin_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30),
family_name varchar(30) not null,
status_now varchar(8) not null,
email varchar(300) not null,
phone varchar(11) not null,
hire_date date not null,
admin_position varchar(100) not null,
department varchar(100) not null
);

CREATE TABLE IF NOT EXISTS forestry
(
forestry_id INT auto_increment PRIMARY KEY NOT NULL,
forestry_type  varchar(7) not null ,
present_in_nz varchar(3) not null,
common_name varchar(320) not null,
scientific_name varchar(100) not null ,
key_characteristics text,
biology text,
symptoms text,
image_num int
);

CREATE TABLE IF NOT EXISTS images
(
image_num INT auto_increment PRIMARY KEY NOT NULL,
forestry_id INT NOT NULL,
images mediumblob,
FOREIGN KEY (forestry_id) REFERENCES forestry(forestry_id)
on update cascade
);

