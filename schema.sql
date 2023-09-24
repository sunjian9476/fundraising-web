DROP TABLE volunteers;
DROP TABLE donations;
DROP TABLE events;
DROP TABLE users;


CREATE TABLE users (
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       username VARCHAR(50) UNIQUE NOT NULL,
                       password VARCHAR(255) NOT NULL,
                       email VARCHAR(255) UNIQUE NOT NULL,
                       name VARCHAR(100),
                       join_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        goal DECIMAL(10,2) NOT NULL,
                        start_date DATE,
                        end_date DATE,
                        creator_id INT NOT NULL,
                        FOREIGN KEY (creator_id) REFERENCES users(id)
);

CREATE TABLE donations (
                           id INT PRIMARY KEY AUTO_INCREMENT,
                           user_id INT NOT NULL,
                           event_id INT NOT NULL,
                           amount DECIMAL(10,2) NOT NULL,
                           donate_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (user_id) REFERENCES users(id),
                           FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE volunteers (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            user_id INT NOT NULL,
                            join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id)
);