USE matsumura_tabelog;

CREATE TABLE restaurants(
    id int primary key AUTO_INCREMENT,
    restaurant_id int UNIQUE NOT NULL,
    name varchar(255) NOT NULL,
    genre varchar(255),
    address varchar(255),
    pal varchar(255) NOT NULL,
    LstPrf varchar(255) NOT NULL,
    LstAre varchar(255) NOT NULL,
    open_time varchar(255),
    regular_holiday varchar(255),
    budget varchar(255),
    budget_from_reviews varchar(255),
    seats varchar(255),
    private_room text,
    private_use varchar(255),
    smoking varchar(255),
    space_or_facilities varchar(255),
    occasion varchar(255),
    location varchar(255),
    service varchar(255),
    homepage varchar(255),
    remarks text,
    rate float,
    pr_comment_title text,
    pr_comment_body text,
    url varchar(255),
    html longtext
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);
