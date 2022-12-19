create table budget(
    codename varchar(255) primary key,
    daily_limit integer
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_codename integer,
    raw_text text,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "food", true, "snacks"),
    ("coffee", "cafeteria", true, "coffeeshop"),
    ("dinner", "lunch", true, "brunch"),
    ("cafe", "restaurant", true, "pizza, kfc, McDonald's"),
    ("transport", "gas", false, "metro, subway"),
    ("phone", "provider", false, "calls"),
    ("books", "magazines", false, "literature"),
    ("internet", "Internet", false, "inet"),
    ("subscriptions", "movies", false, "netflix"),
    ("other", "extra", true, "entertainment");

insert into budget(codename, daily_limit) values ('base', 500);
