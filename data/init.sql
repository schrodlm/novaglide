CREATE TABLE user_data (
    id SERIAL,
    Name VARCHAR(30),
    Password VARCHAR(30),
    Elo SMALLINT,
    Winrate SMALLINT,
    Skin VARCHAR(15)
);
CREATE TABLE games_1v1 (
    id SERIAL,
    Player_1_name VARCHAR(30),
    Player_2_name VARCHAR(30),
    Player_1_elo SMALLINT,
    Player_2_elo SMALLINT,
    Goals_p1 SMALLINT,
    Goals_p2 SMALLINT,
    Date TIMESTAMP
);
CREATE TABLE games_2v2 (
    id SERIAL,
    Player_1_name VARCHAR(30),
    Player_2_name VARCHAR(30),
    Player_3_name VARCHAR(30),
    Player_4_name VARCHAR(30),
    Player_1_elo SMALLINT,
    Player_2_elo SMALLINT,
    Player_3_elo SMALLINT,
    Player_4_elo SMALLINT,
    Goals_p12 SMALLINT,
    Goals_p34 SMALLINT,
    Date TIMESTAMP
);
/* TO BE DELETED, JUST FOR TESTING*/
INSERT INTO user_data (Name, Password, Elo, Winrate, Skin)
VALUES 
  ('User1', 'password1', 1200, 70, 'Skin1'),
  ('User2', 'password2', 1300, 65, 'Skin2'),
  ('User3', 'password3', 1400, 80, 'Skin3'),
  ('User4', 'password4', 1100, 45, 'Skin4'),
  ('User5', 'password5', 1250, 60, 'Skin5'),
  ('User6', 'password6', 1350, 75, 'Skin6'),
  ('User7', 'password7', 1150, 50, 'Skin7'),
  ('User8', 'password8', 1450, 85, 'Skin8'),
  ('User9', 'password9', 1300, 70, 'Skin9'),
  ('User10', 'password10', 1250, 55, 'Skin10'),
  ('User11', 'password11', 1350, 65, 'Skin11'),
  ('User12', 'password12', 1400, 75, 'Skin12'),
  ('User13', 'password13', 1200, 60, 'Skin13'),
  ('User14', 'password14', 1300, 70, 'Skin14'),
  ('User15', 'password15', 1150, 45, 'Skin15'),
  ('User16', 'password16', 1200, 55, 'Skin16'),
  ('User17', 'password17', 1350, 80, 'Skin17'),
  ('User18', 'password18', 1400, 65, 'Skin18'),
  ('User19', 'password19', 1300, 75, 'Skin19'),
  ('User20', 'password20', 1400, 70, 'Skin20');
INSERT INTO games_1v1 (Player_1_name, Player_2_name, Player_1_elo, Player_2_elo, Goals_p1, Goals_p2, Date)
VALUES
  ('User1', 'User2', 1200, 1300, 2, 1, '2024-01-01 12:00:00'),
  ('User3', 'User1', 1400, 1200, 3, 2, '2024-01-02 14:30:00'),
  ('User4', 'User5', 1100, 1150, 1, 3, '2024-01-03 16:45:00'),
  ('User6', 'User7', 1350, 1350, 2, 2, '2024-01-04 10:15:00'),
  ('User8', 'User9', 1450, 1250, 4, 1, '2024-01-05 18:30:00'),
  ('User10', 'User11', 1250, 1300, 2, 1, '2024-01-06 21:45:00'),
  ('User12', 'User13', 1400, 1250, 3, 2, '2024-01-07 14:00:00'),
  ('User14', 'User15', 1300, 1200, 1, 3, '2024-01-08 12:30:00'),
  ('User16', 'User17', 1200, 1400, 2, 2, '2024-01-09 16:15:00'),
  ('User18', 'User19', 1400, 1300, 3, 1, '2024-01-10 10:00:00'),
  ('User20', 'User1', 1400, 1200, 2, 3, '2024-01-11 22:45:00'),
  ('User2', 'User3', 1300, 1400, 1, 4, '2024-01-12 08:30:00'),
  ('User4', 'User5', 1100, 1150, 3, 1, '2024-01-13 11:15:00'),
  ('User6', 'User7', 1350, 1350, 2, 2, '2024-01-14 17:30:00'),
  ('User8', 'User9', 1450, 1250, 4, 0, '2024-01-15 19:45:00'),
  ('User10', 'User11', 1250, 1300, 1, 2, '2024-01-16 23:00:00'),
  ('User12', 'User13', 1400, 1250, 3, 2, '2024-01-17 14:15:00'),
  ('User14', 'User15', 1300, 1200, 2, 3, '2024-01-18 16:30:00'),
  ('User16', 'User17', 1200, 1400, 1, 1, '2024-01-19 09:45:00'),
  ('User18', 'User19', 1400, 1300, 2, 2, '2024-01-20 20:00:00');
INSERT INTO games_2v2 (Player_1_name, Player_2_name, Player_3_name, Player_4_name, Player_1_elo, Player_2_elo, Player_3_elo, Player_4_elo, Goals_p12, Goals_p34, Date)
VALUES
  ('User1', 'User2', 'User3', 'User4', 1200, 1300, 1400, 1100, 4, 3, '2024-01-01 12:00:00'),
  ('User5', 'User6', 'User7', 'User8', 1250, 1350, 1450, 1200, 2, 2, '2024-01-02 14:30:00'),
  ('User9', 'User10', 'User11', 'User12', 1300, 1250, 1350, 1300, 3, 1, '2024-01-03 16:45:00'),
  ('User13', 'User14', 'User15', 'User16', 1200, 1350, 1400, 1150, 4, 2, '2024-01-04 10:15:00'),
  ('User17', 'User18', 'User19', 'User20', 1350, 1400, 1300, 1400, 3, 3, '2024-01-05 18:30:00'),
  ('User1', 'User2', 'User3', 'User4', 1200, 1300, 1400, 1100, 2, 1, '2024-01-06 21:45:00'),
  ('User5', 'User6', 'User7', 'User8', 1250, 1350, 1450, 1200, 1, 4, '2024-01-07 14:00:00'),
  ('User9', 'User10', 'User11', 'User12', 1300, 1250, 1350, 1300, 3, 2, '2024-01-08 12:30:00'),
  ('User13', 'User14', 'User15', 'User16', 1200, 1350, 1400, 1150, 2, 3, '2024-01-09 16:15:00'),
  ('User17', 'User18', 'User19', 'User20', 1350, 1400, 1300, 1400, 4, 1, '2024-01-10 10:00:00'),
  ('User1', 'User2', 'User3', 'User4', 1200, 1300, 1400, 1100, 2, 3, '2024-01-11 22:45:00'),
  ('User5', 'User6', 'User7', 'User8', 1250, 1350, 1450, 1200, 1, 2, '2024-01-12 08:30:00'),
  ('User9', 'User10', 'User11', 'User12', 1300, 1250, 1350, 1300, 3, 1, '2024-01-13 11:15:00'),
  ('User13', 'User14', 'User15', 'User16', 1200, 1350, 1400, 1150, 2, 2, '2024-01-14 17:30:00'),
  ('User17', 'User18', 'User19', 'User20', 1350, 1400, 1300, 1400, 1, 3, '2024-01-15 19:45:00'),
  ('User1', 'User2', 'User3', 'User4', 1200, 1300, 1400, 1100, 3, 0, '2024-01-16 23:00:00'),
  ('User5', 'User6', 'User7', 'User8', 1250, 1350, 1450, 1200, 2, 2, '2024-01-17 14:15:00'),
  ('User9', 'User10', 'User11', 'User12', 1300, 1250, 1350, 1300, 3, 1, '2024-01-18 16:30:00'),
  ('User13', 'User14', 'User15', 'User16', 1200, 1350, 1400, 1150, 1, 1, '2024-01-19 09:45:00'),
  ('User17', 'User18', 'User19', 'User20', 1350, 1400, 1300, 1400, 2, 2, '2024-01-20 20:00:00');
