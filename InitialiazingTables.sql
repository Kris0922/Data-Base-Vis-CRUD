-- Crearea bazei de date dacă nu există
CREATE DATABASE IF NOT EXISTS temabd;

-- Selectarea bazei de date pentru utilizare
USE temabd;

-- Crearea tabelului Mentor
CREATE TABLE IF NOT EXISTS Mentor (
                                      Mentor_Id INT AUTO_INCREMENT PRIMARY KEY,
                                      mentor_nume VARCHAR(100) NOT NULL,
                                      mentor_prenume VARCHAR(100) NOT NULL,
                                      Varsta INT CHECK (Varsta >= 18),
                                      CONSTRAINT CK_Mentor_Varsta CHECK (Varsta IS NULL OR (Varsta >= 18 AND Varsta <= 100))
);

-- Crearea tabelului Model
CREATE TABLE IF NOT EXISTS Model (
                                     Model_ID INT AUTO_INCREMENT PRIMARY KEY,
                                     Varsta INT NOT NULL,
                                     Nume VARCHAR(100) NOT NULL,
                                     Prenume VARCHAR(100) NOT NULL,
                                     Gen CHAR(1) CHECK (Gen IN ('M', 'F')),
                                     Mentor_Id INT,
                                     CONSTRAINT FK_Model_Mentor FOREIGN KEY (Mentor_Id)
                                         REFERENCES Mentor(Mentor_Id)
                                         ON DELETE SET NULL
                                         ON UPDATE CASCADE,
                                     CONSTRAINT CK_Model_Varsta CHECK (Varsta >= 14 AND Varsta <= 100)
);

-- Crearea tabelului MentorModel
CREATE TABLE IF NOT EXISTS MentorModel (
                                           Model_Id INT,
                                           Mentor_Id INT,
                                           Data_semnare_contract DATE NOT NULL,
                                           Data_incheiere DATE,
                                           Mentiuni_suplimentare TEXT,
                                           Contract_pdf LONGBLOB,
                                           Mentiuni_mentor TEXT,
                                           CONSTRAINT PK_MentorModel PRIMARY KEY (Model_Id, Mentor_Id),
                                           CONSTRAINT FK_MentorModel_Model FOREIGN KEY (Model_Id)
                                               REFERENCES Model(Model_ID)
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                           CONSTRAINT FK_MentorModel_Mentor FOREIGN KEY (Mentor_Id)
                                               REFERENCES Mentor(Mentor_Id)
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                           CONSTRAINT CK_MentorModel_Date CHECK (Data_incheiere IS NULL OR Data_incheiere >= Data_semnare_contract)
);

-- Crearea tabelului Jurat
CREATE TABLE IF NOT EXISTS Jurat (
                                     Jurat_ID INT AUTO_INCREMENT PRIMARY KEY,
                                     Nume VARCHAR(100) NOT NULL,
                                     Prenume VARCHAR(100) NOT NULL,
                                     Varsta INT,
                                     email VARCHAR(255),
                                     CONSTRAINT CK_Jurat_Varsta CHECK (Varsta IS NULL OR (Varsta >= 18 AND Varsta <= 100)),
                                     CONSTRAINT CK_Jurat_Email CHECK (email LIKE '%@%.%')
);

-- Crearea tabelului Competitie
CREATE TABLE IF NOT EXISTS Competitie (
                                          Competitie_ID INT AUTO_INCREMENT PRIMARY KEY,
                                          Nume_Eveniment VARCHAR(255) NOT NULL,
                                          Data DATE NOT NULL,
                                          Locatie VARCHAR(255) NOT NULL,
                                          CONSTRAINT CK_Competitie_Data CHECK (Data >= '2000-01-01')
);

-- Crearea tabelului JuratCompetitie
CREATE TABLE IF NOT EXISTS JuratCompetitie (
                                               Jurat_ID INT,
                                               Competitie_ID INT,
                                               Rol VARCHAR(50) DEFAULT 'Membru juriu',
                                               CONSTRAINT PK_JuratCompetitie PRIMARY KEY (Jurat_ID, Competitie_ID),
                                               CONSTRAINT FK_JuratCompetitie_Jurat FOREIGN KEY (Jurat_ID)
                                                   REFERENCES Jurat(Jurat_ID)
                                                   ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
                                               CONSTRAINT FK_JuratCompetitie_Competitie FOREIGN KEY (Competitie_ID)
                                                   REFERENCES Competitie(Competitie_ID)
                                                   ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
                                               CONSTRAINT CK_JuratCompetitie_Rol CHECK (Rol IN ('Membru juriu', 'Președinte juriu', 'Vicepreședinte juriu'))
);

-- Crearea tabelului ModelCompetitie
CREATE TABLE IF NOT EXISTS ModelCompetitie (
                                               Model_ID INT,
                                               Competitie_ID INT,
                                               Data_participare DATE NOT NULL,
                                               Durata_participare INT, -- în minute
                                               CONSTRAINT PK_ModelCompetitie PRIMARY KEY (Model_ID, Competitie_ID),
                                               CONSTRAINT FK_ModelCompetitie_Model FOREIGN KEY (Model_ID)
                                                   REFERENCES Model(Model_ID)
                                                   ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
                                               CONSTRAINT FK_ModelCompetitie_Competitie FOREIGN KEY (Competitie_ID)
                                                   REFERENCES Competitie(Competitie_ID)
                                                   ON DELETE CASCADE
                                                   ON UPDATE CASCADE,
                                               CONSTRAINT CK_ModelCompetitie_Durata CHECK (Durata_participare > 0)
);

-- Crearea indexurilor doar dacă nu există

