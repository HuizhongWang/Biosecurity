use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(10) default "forester", 
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint default 1,
address varchar(500),
email varchar(300) not null,
phone varchar(11) not null,
date_joined date,
pin varchar(200) not null
);


CREATE TABLE IF NOT EXISTS staff_admin
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(10) default "staff",
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint default 1,
email varchar(300) not null,
phone varchar(11) not null,
hire_date date not null,
staff_position varchar(100),
department varchar(100),
pin varchar(200) not null
);


CREATE TABLE IF NOT EXISTS users
(
roles varchar(10) not null default "forester",
forester_id INT,
staff_id INT,
pin varchar(200) not null,
FOREIGN KEY (forester_id) REFERENCES forester(forester_id)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (staff_id) REFERENCES staff_admin(staff_id)
ON UPDATE CASCADE
ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS forestry
(
forestry_id INT auto_increment PRIMARY KEY NOT NULL,
forestry_type  varchar(7) not null ,
present_in_nz tinyint not null,
common_name varchar(100) not null,
scientific_name varchar(100) not null ,
key_charac text,
biology text,
symptoms text,
image_num int not null
);


CREATE TABLE IF NOT EXISTS images
(
image_num INT auto_increment PRIMARY KEY NOT NULL,
forestry_id INT NOT NULL,
images mediumblob,
show_p tinyint,
FOREIGN KEY (forestry_id) REFERENCES forestry(forestry_id)
on update cascade
ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER insert_id
AFTER INSERT ON forester
FOR EACH ROW
BEGIN
    INSERT INTO users (forester_id,pin) VALUES (NEW.forester_id,new.pin);
END;
//

DELIMITER ;







