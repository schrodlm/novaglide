CREATE TABLE user_data (
    id SERIAL,
    Name VARCHAR(30),
    Password VARCHAR(30),
    Elo_1v1 SMALLINT,
    Elo_2v2 SMALLINT,
    Skin VARCHAR(15)
);


CREATE TABLE games_1v1 (
    id SERIAL,
    Player_1_id SMALLINT,
    Player_2_id SMALLINT,
    Player_1_elo SMALLINT,
    Player_2_elo SMALLINT,
    Goals_p1 SMALLINT,
    Goals_p2 SMALLINT,
    Date TIMESTAMP
);


CREATE TABLE games_2v2 (
    id SERIAL,
    Player_1_id SMALLINT,
    Player_2_id SMALLINT,
    Player_3_id SMALLINT,
    Player_4_id SMALLINT,
    Player_1_elo SMALLINT,
    Player_2_elo SMALLINT,
    Player_3_elo SMALLINT,
    Player_4_elo SMALLINT,
    Goals_p12 SMALLINT,
    Goals_p34 SMALLINT,
    Date TIMESTAMP
);


/* TO BE DELETED, JUST FOR TESTING*/

INSERT INTO user_data (Name, Password, Elo_1v1, Elo_2v2, Skin) VALUES
('JohnDoe', 'password123', 1500, 1600, 'Skin1'),
('AliceSmith', 'securepwd456', 1400, 1550, 'Skin2'),
('BobJohnson', 'strongpass789', 1550, 1650, 'Skin3'),
('EvaWilliams', 'myp@ssword', 1600, 1700, 'Skin4'),
('CharlieBrown', 'letmein123', 1450, 1600, 'Skin5'),
('GraceMiller', 'accessgranted', 1700, 1750, 'Skin6'),
('DavidJones', 'hiddenkey', 1520, 1620, 'Skin7'),
('SophieTaylor', 'qwerty567', 1580, 1680, 'Skin8'),
('MikeDavis', 'password!@#', 1650, 1750, 'Skin9'),
('OliviaWhite', 'p@ss123', 1480, 1580, 'Skin10'),
('RyanMoore', 'letmeinnow', 1720, 1820, 'Skin1'),
('EmmaThomas', 'secretcode', 1540, 1640, 'Skin2'),
('JackWilson', 'mypassword', 1620, 1720, 'Skin3'),
('LilyBrown', 'secure123', 1470, 1570, 'Skin4'),
('AidenSmith', 'passphrase', 1750, 1850, 'Skin5'),
('AvaJohnson', '123456789', 1550, 1650, 'Skin6'),
('CarterJones', 'ilovecoding', 1600, 1700, 'Skin7'),
('MiaWilson', 'codingisfun', 1680, 1780, 'Skin8'),
('NoahMoore', 'password1234', 1500, 1600, 'Skin9'),
('ChloeDavis', 'letmein456', 1570, 1670, 'Skin10');

INSERT INTO games_1v1 (Player_1_id, Player_2_id, Player_1_elo, Player_2_elo, Goals_p1, Goals_p2, Date) VALUES
(1, 2, 1500, 1400, 3, 1, '2023-12-01 14:30:00'),
(3, 4, 1550, 1600, 2, 2, '2023-12-02 15:45:00'),
(5, 6, 1450, 1700, 1, 4, '2023-12-03 16:00:00'),
(7, 8, 1520, 1580, 3, 2, '2023-12-04 17:15:00'),
(9, 10, 1650, 1480, 4, 1, '2023-12-05 18:30:00'),
(11, 12, 1700, 1540, 2, 3, '2023-12-06 19:45:00'),
(13, 14, 1620, 1470, 3, 2, '2023-12-07 20:00:00'),
(15, 16, 1580, 1750, 2, 4, '2023-12-08 21:15:00'),
(17, 18, 1750, 1550, 4, 1, '2023-12-09 22:30:00'),
(19, 20, 1480, 1570, 1, 3, '2023-12-10 23:45:00'),
(1, 3, 1500, 1550, 2, 2, '2023-12-11 12:00:00'),
(4, 5, 1600, 1450, 3, 1, '2023-12-12 13:15:00'),
(6, 7, 1750, 1520, 2, 4, '2023-12-13 14:30:00'),
(8, 9, 1650, 1580, 4, 3, '2023-12-14 15:45:00'),
(10, 11, 1480, 1650, 1, 2, '2023-12-15 16:00:00'),
(12, 13, 1540, 1620, 3, 2, '2023-12-16 17:15:00'),
(14, 15, 1620, 1470, 2, 4, '2023-12-17 18:30:00'),
(16, 17, 1680, 1750, 1, 3, '2023-12-18 19:45:00'),
(18, 19, 1580, 1500, 4, 2, '2023-12-19 20:00:00'),
(20, 1, 1570, 1550, 3, 1, '2023-12-20 21:15:00');

INSERT INTO games_2v2 (Player_1_id, Player_2_id, Player_3_id, Player_4_id, Player_1_elo, Player_2_elo, Player_3_elo, Player_4_elo, Goals_p12, Goals_p34, Date) VALUES
(1, 2, 3, 4, 1500, 1400, 1550, 1600, 3, 1, '2023-12-01 14:30:00'),
(5, 6, 7, 8, 1450, 1700, 1520, 1580, 2, 2, '2023-12-02 15:45:00'),
(9, 10, 11, 12, 1650, 1480, 1700, 1540, 1, 4, '2023-12-03 16:00:00'),
(13, 14, 15, 16, 1620, 1470, 1580, 1750, 3, 2, '2023-12-04 17:15:00'),
(17, 18, 19, 20, 1750, 1550, 1480, 1570, 4, 1, '2023-12-05 18:30:00'),
(1, 3, 5, 7, 1500, 1550, 1450, 1520, 2, 3, '2023-12-06 19:45:00'),
(9, 11, 13, 15, 1650, 1580, 1620, 1470, 3, 2, '2023-12-07 20:00:00'),
(17, 19, 1, 3, 1750, 1550, 1500, 1550, 2, 4, '2023-12-08 21:15:00'),
(5, 7, 9, 11, 1450, 1520, 1650, 1580, 4, 3, '2023-12-09 22:30:00'),
(13, 15, 17, 19, 1620, 1470, 1750, 1550, 1, 2, '2023-12-10 23:45:00'),
(2, 4, 6, 8, 1400, 1600, 1700, 1750, 3, 1, '2023-12-11 12:00:00'),
(10, 12, 14, 16, 1480, 1650, 1580, 1620, 2, 2, '2023-12-12 13:15:00'),
(18, 20, 1, 3, 1550, 1570, 1500, 1550, 4, 1, '2023-12-13 14:30:00'),
(6, 8, 10, 12, 1700, 1540, 1650, 1580, 3, 4, '2023-12-14 15:45:00'),
(14, 16, 18, 20, 1620, 1470, 1550, 1570, 2, 3, '2023-12-15 16:00:00'),
(3, 5, 7, 9, 1550, 1450, 1520, 1650, 3, 2, '2023-12-16 17:15:00'),
(11, 13, 15, 17, 1580, 1750, 1620, 1470, 2, 4, '2023-12-17 18:30:00'),
(19, 1, 3, 5, 1500, 1550, 1450, 1520, 1, 3, '2023-12-18 19:45:00'),
(7, 9, 11, 13, 1520, 1580, 1650, 1580, 4, 2, '2023-12-19 20:00:00'),
(15, 17, 19, 1, 1750, 1550, 1500, 1550, 3, 1, '2023-12-20 21:15:00');