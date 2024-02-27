use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(20) not null, 
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint not null,
address varchar(500),
email varchar(300) not null,
phone varchar(11) not null,
date_joined date not null,
pin varchar(30) not null
);


CREATE TABLE IF NOT EXISTS staff_admin
(
staff_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(20) not null,
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint not null,
email varchar(300) not null,
phone varchar(11) not null,
hire_date date not null,
staff_position varchar(100) not null,
department varchar(100) not null,
pin varchar(30) not null
);


CREATE TABLE IF NOT EXISTS users
(
roles varchar(20) not null,
forester_id INT,
staff_id INT,
pin varchar(30) not null,
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
    INSERT INTO users (forester_id) VALUES (NEW.forester_id);
END;
//

DELIMITER ;




