PRAGMA foreign_keys = ON;

CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE Publication (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author INTEGER REFERENCES User(id),
    content TEXT,
    status INTEGER
);

CREATE TABLE Owner2Book (
    id INTEGER PRIMARY KEY,
    owner INTEGER REFERENCES User(id),
    book INTEGER REFERENCES Publication(id)
);

CREATE TABLE Payment (
    id INTEGER PRIMARY KEY,
    from_ INTEGER REFERENCES User(id),
    "to" INTEGER REFERENCES User(id),
    quantity INTEGER
);

CREATE TABLE "Order" (
    id INTEGER PRIMARY KEY,
    client INTEGER REFERENCES User(id),
    service INTEGER REFERENCES User(id),
    publication INTEGER REFERENCES Publication(id),
    status TEXT,
    cost INTEGER,
    quantity INTEGER,
    payment INTEGER REFERENCES Payment(id)
);
