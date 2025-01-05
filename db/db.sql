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
foreign key(role_id) references Roles (role_id)
);


insert into Users (id, firstname, surname, email, user_password, role_id) values
(1, 'root', 'admin', 'root@gmail.com',
'8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1);
-- пароль - админ