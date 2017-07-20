USE matsumura_tabelog;

CREATE TABLE IF NOT EXISTS pals(
    id int primary key AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    code varchar(255) NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE IF NOT EXISTS lst_prfs(
    id int primary key AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    code varchar(255) NOT NULL,
    pal_id int NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE IF NOT EXISTS lst_ares(
    id int primary key AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    code varchar(255) NOT NULL,
    lst_prf_id int NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE IF NOT EXISTS stations(
    id int primary key AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    code varchar(255) NOT NULL,
    lst_are_id int NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);
