CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    classes TEXT,
    instruction TEXT,
    user_id INTEGER REFERENCES users
);
