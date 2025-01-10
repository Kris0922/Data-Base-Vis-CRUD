USE temabd;

-- Popularea tabelului Mentor
INSERT INTO Mentor (mentor_nume, mentor_prenume, Varsta) VALUES
                                                             ('Popescu', 'Ion', 35),
                                                             ('Ionescu', 'Maria', 42),
                                                             ('Popa', 'Alexandru', 38),
                                                             ('Dumitrescu', 'Elena', 45),
                                                             ('Mihai', 'Andrei', 40);

-- Popularea tabelului Model
INSERT INTO Model (Varsta, Nume, Prenume, Gen, Mentor_Id) VALUES
                                                              (19, 'Gheorghe', 'Ana', 'F', 1),
                                                              (21, 'Stan', 'Maria', 'F', 2),
                                                              (20, 'Dinu', 'Elena', 'F', 1),
                                                              (22, 'Barbu', 'Cristina', 'F', 3),
                                                              (18, 'Neagu', 'Diana', 'F', 4),
                                                              (23, 'Marin', 'Alexandru', 'M', 5);

-- Popularea tabelului MentorModel
INSERT INTO MentorModel (Model_Id, Mentor_Id, Data_semnare_contract, Data_incheiere, Mentiuni_suplimentare, Mentiuni_mentor) VALUES
                                                                                                                                 (1, 1, '2023-01-15', '2024-01-15', 'Contract anual standard', 'Progres foarte bun'),
                                                                                                                                 (2, 2, '2023-02-20', '2024-02-20', 'Contract anual extins', 'Necesită mai multă practică'),
                                                                                                                                 (3, 1, '2023-03-10', '2024-03-10', 'Contract cu opțiune de prelungire', 'Evoluție constantă'),
                                                                                                                                 (4, 3, '2023-04-05', '2024-04-05', 'Contract special evenimente', 'Talent deosebit'),
                                                                                                                                 (5, 4, '2023-05-01', '2024-05-01', 'Contract standard', 'Punctualitate exemplară');

-- Popularea tabelului Jurat
INSERT INTO Jurat (Nume, Prenume, Varsta, email) VALUES
                                                     ('Marinescu', 'Adrian', 45, 'adrian@example.com'),
                                                     ('Gheorghiu', 'Elena', 50, 'elena@example.com'),
                                                     ('Vasilescu', 'Mihai', 48, 'mihai@example.com'),
                                                     ('Stanescu', 'Diana', 42, 'diana@example.com'),
                                                     ('Ionescu', 'Gabriel', 55, 'gabriel@example.com');

-- Popularea tabelului Competitie
INSERT INTO Competitie (Nume_Eveniment, Data, Locatie) VALUES
                                                           ('Fashion Week București', '2024-03-15', 'Palatul Parlamentului'),
                                                           ('Gala Modelelor', '2024-04-20', 'Hotel Intercontinental'),
                                                           ('Summer Fashion Show', '2024-06-10', 'Arena Națională'),
                                                           ('Young Models Competition', '2024-07-05', 'Sala Palatului'),
                                                           ('Winter Collection Show', '2024-12-01', 'Romexpo');

-- Popularea tabelului JuratCompetitie
INSERT INTO JuratCompetitie (Jurat_ID, Competitie_ID, Rol) VALUES
                                                               (1, 1, 'Președinte juriu'),
                                                               (2, 1, 'Membru juriu'),
                                                               (3, 1, 'Membru juriu'),
                                                               (4, 2, 'Președinte juriu'),
                                                               (5, 2, 'Membru juriu'),
                                                               (1, 3, 'Membru juriu'),
                                                               (2, 3, 'Președinte juriu');

-- Popularea tabelului ModelCompetitie
INSERT INTO ModelCompetitie (Model_ID, Competitie_ID, Data_participare, Durata_participare) VALUES
 (1, 1, '2024-03-15', 45),
 (2, 1, '2024-03-15', 30),
 (3, 2, '2024-04-20', 40),
 (4, 2, '2024-04-20', 35),
 (5, 3, '2024-06-10', 50),
 (1, 3, '2024-06-10', 45);