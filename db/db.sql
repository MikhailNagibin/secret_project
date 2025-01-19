create table Roles (
id serial primary key unique ,
role varchar(50)
);


create table Users (
id serial unique primary key,
firstname varchar(50) not null,
surname varchar(50) not null,
email varchar(50) not null unique,
user_password varchar(256) not null,
role_id int,
foreign key(role_id) references Roles (id)
);


create table Conditions (
id serial primary key unique,
condition varchar(30)
);


create table inventory_name (
id serial primary key unique,
name varchar(50) unique
);


create table Inventory (
id serial primary key unique,
name int,
user_id int default -1,
condition_id int,
foreign key(user_id) references Users (id),
foreign key(condition_id) references Conditions (id),
foreign key(name)  references inventory_name(id)
);



create table purchase_plan (
id serial primary key unique,
name varchar(50),
count int,
price int,
supplier varchar(50)
);


create table reports (
id serial primary key unique,
name varchar(50),
report text
);


create table request_status (
id serial primary key unique,
status varchar(50)
);


create table requests (
id serial primary key unique,
user_id int,
inventory_name_id int,
count int,
status_id int,
foreign key (user_id) references Users(id),
foreign key (inventory_name_id) references inventory_name(id),
foreign key (status_id) references request_status(id)
);


create table repair_requests (
id serial primary key unique,
inventory_name_id int,
count int,
replace bool,
foreign key (inventory_name_id) references inventory_name(id)
);


insert into Roles (role) values
('Администратор'),
('Пользователь');


insert into request_status(status) values
('Не рассмотрен'),
('Одобрен'),
('Отклонен');

insert into Conditions(condition) values
('Новый'),
('Используемый'),
('Сломанный');


insert into Users (id, firstname, surname, email, user_password, role_id) values
(0, 'root', 'admin', 'root@gmail.com',
'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1),
-- пароль - admin
(-1, 'Null', 'Null', 'Null', 'Null', 1);