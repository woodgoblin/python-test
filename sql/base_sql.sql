CREATE TABLE Cat (
    ID SERIAL PRIMARY KEY,
    birth_date DATE NOT NULL,
    paws_quantity INT CHECK (paws_quantity >= 0),
    name VARCHAR(50) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    tails_quantity INT CHECK (tails_quantity >= 0)
);

CREATE TABLE Rat (
    ID SERIAL PRIMARY KEY,
    birth_date DATE NOT NULL,
    courage INT CHECK (courage BETWEEN 1 AND 10),
    stupidity INT CHECK (stupidity BETWEEN 1 AND 10),
    is_eaten BOOLEAN DEFAULT FALSE,
    cat_id INT,
    CONSTRAINT fk_cat
      FOREIGN KEY(cat_id)
      REFERENCES Cat(ID)
      ON DELETE SET NULL
);

-- Insert some sample data
INSERT INTO Cat (birth_date, paws_quantity, name, gender, tails_quantity)
VALUES
('2020-01-01', 4, 'Whiskers', 'M', 1),
('2021-05-15', 4, 'Mittens', 'F', 1);

INSERT INTO Rat (birth_date, courage, stupidity, is_eaten, cat_id)
VALUES
('2022-03-01', 8, 3, TRUE, 1),
('2022-04-10', 5, 5, FALSE, NULL),
('2022-05-20', 3, 7, TRUE, 2);