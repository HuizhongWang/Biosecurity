use Biosecurity;

CREATE TABLE IF NOT EXISTS forester
(
forester_id INT auto_increment PRIMARY KEY NOT NULL,
roles varchar(10) not null default "forester", 
first_name varchar(30) not null,
family_name varchar(30) not null,
status_now tinyint not null default 1,
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
hire_date date,
staff_position varchar(100),
department varchar(100),
pin varchar(200) not null
);


CREATE TABLE IF NOT EXISTS users
(
roles varchar(10),
forester_id INT,
staff_id INT,
pin varchar(200),
status_now tinyint,
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
forestry_type  varchar(7) not null,
present_in_nz tinyint not null,
common_name varchar(100) not null,
scientific_name varchar(100) not null,
key_charac text,
biology text,
symptoms text,
image_num int
);


CREATE TABLE IF NOT EXISTS images
(
image_num INT auto_increment PRIMARY KEY NOT NULL,
forestry_id INT NOT NULL,
images mediumblob,
show_p tinyint default 0,
FOREIGN KEY (forestry_id) REFERENCES forestry(forestry_id)
on update cascade
ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER insert_forester
AFTER INSERT ON forester
FOR EACH ROW
BEGIN
    INSERT INTO users (forester_id,pin,status_now,roles)
    VALUES (NEW.forester_id,new.pin,new.status_now,new.roles);
END;
//

CREATE TRIGGER update_forester
AFTER UPDATE ON forester
FOR EACH ROW
BEGIN
    IF NEW.status_now != OLD.status_now THEN
        UPDATE users
        SET status_now = NEW.status_now
        WHERE forester_id = NEW.forester_id;
    END IF;
    IF NEW.pin != OLD.pin THEN 
		UPDATE users
        SET pin = NEW.pin
        WHERE forester_id = NEW.forester_id;
    END IF;
END;
//

CREATE TRIGGER update_staff
AFTER UPDATE ON staff_admin
FOR EACH ROW
BEGIN
    IF NEW.status_now != OLD.status_now THEN
        UPDATE users
        SET status_now = NEW.status_now
        WHERE staff_id = NEW.staff_id;
    END IF;
    IF NEW.pin != OLD.pin THEN 
		UPDATE users
        SET pin = NEW.pin
        WHERE staff_id = NEW.staff_id;
    END IF;
    IF NEW.roles != OLD.roles THEN 
		UPDATE users
        SET roles = NEW.roles
        WHERE staff_id = NEW.staff_id;
    END IF;
END;
//

DELIMITER ;







