use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30),
family_name varchar(30) not null,
status_now varchar(8) not null,
address varchar(500) not null,
email varchar(300) not null,
phone INT not null
);


CREATE TABLE IF NOT EXISTS staff
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30),
family_name varchar(30) not null,
email varchar(300) not null,
phone INT not null,
hire_date date not null,
staff_position varchar(100) not null,
department varchar(100) not null
);

CREATE TABLE IF NOT EXISTS admini
(
admin_id INT auto_increment PRIMARY KEY NOT NULL,
first_name varchar(30),
family_name varchar(30) not null,
email varchar(300) not null,
phone INT not null,
hire_date date not null,
admin_position varchar(100) not null,
department varchar(100) not null
);

CREATE TABLE IF NOT EXISTS forestry_guide
(
forestry_id INT auto_increment PRIMARY KEY NOT NULL,
forestry_type  varchar(7) not null ,
present_in_nz varchar(3) not null,
common_name varchar(320) not null,
primary_image varchar(500) not null
);

CREATE TABLE IF NOT EXISTS forestry_detail
(
forestry_id INT NOT NULL,
scientific_name varchar(100) not null ,
key_characteristics text not null,
biology text not null,
symptoms text not null,
images varchar(500),
FOREIGN KEY (forestry_id) REFERENCES forestry_guide(forestry_id)
ON UPDATE CASCADE
);

