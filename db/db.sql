create table Roles (
id serial primary key unique ,
role varchar(50)
);

insert into Roles (role) values
('Администратор'),
('Пользователь');

create table Users (
id serial unique primary key,
firstname varchar(50) not null,
surname varchar(50) not null,
email varchar(50) not null unique,
user_password varchar(256) not null,
role_id int,
foreign key(role_id) references Roles (id)
);


insert into Users (firstname, surname, email, user_password, role_id) values
('root', 'admin', 'root@gmail.com',
'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1),
-- пароль - admin
(-1, 'Null', 'Null', 'Null', 'Null', 1);


create table Conditions (
id serial primary key unique,
condition varchar(30)
);


insert into Conditions(condition) values
('Новый'),
('Используемый'),
('Сломанный');


create table Inventory (
id serial primary key unique,
name varchar(50),
user_id int default -1,
condition_id int,
foreign key(user_id) references Users (id),
foreign key(condition_id) references Conditions (id)
);