
CREATE TABLE reviews(
    id int primary key AUTO_INCREMENT,
    review_id varchar(255) UNIQUE NOT NULL,
    restaurant_id int NOT NULL,
    title text,
    body longtext,
    rate float,
    url varchar(255),
    html longtext,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);
