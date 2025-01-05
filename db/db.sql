create table Roles (
role_id serial primary key unique ,
role varchar(50)
);


create table Users (
user_id serial unique primary key,
firstname varchar(50) not null,
surname varchar(50) not null,
email varchar(50) not null unique,
user_password varchar(256) not null,
role_id int,
foreign key(role_id) references Roles (role_id)
);


insert into Roles (role) values
('Администратор'),
('Пользователь');


insert into Users (firstname, surname, email, user_password, role_id) values
('root', 'admin', 'root@gmail.com',
'32768:8:1$bvGb6C698gdrnUsp$726025969cd512feb7bb51652347e0ec20431ff2417ce4284213cf2714d9977d533ac54f50170f6f10abd192674a1252a29c637bbdbec77ab85cb4ed83694074', 1);
