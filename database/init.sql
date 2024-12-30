drop database shopsmart;

create database shopsmart;

use shopsmart;

create table user (
	id int auto_increment primary key,
    username varchar(128) unique not null,
    email varchar(128) unique not null,
    password varchar(128) not null
);

INSERT INTO user (id, username, email, password) VALUES (1, 'asdasdasd', 'alexhe2000@zju.edu.cn', 'asdasdasd');

select * from user;

create table cache (
	id int auto_increment primary key,
    search_name text not null,
    name text,
    class text,
    size text,
    image text,
    link text,
    platform varchar(128),
    price text,
    history_price text
);

select * from cache;
