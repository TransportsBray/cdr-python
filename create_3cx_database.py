import mysql.connector

db_name = "3cx_db"

try:
    # Connexion MySQL sans base sélectionnée au départ
    conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="T87g@LmP2!xK"
    )
    cursor = conn.cursor()

    # Création de la base si elle n'existe pas
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    print(f"✅ Base de données '{db_name}' créée (si elle n'existait pas).")

    # Sélection de la base de données
    conn.database = db_name

    # Création de la table Appels
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Appels (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        CallID VARCHAR(50) UNIQUE,
        HistoryID VARCHAR(50),
        Duration INT,
        TimeStart DATETIME,
        TimeAnswered DATETIME,
        TimeEnd DATETIME,
        ReasonTerminated VARCHAR(100),
        FromNumber VARCHAR(20),
        ToNumber VARCHAR(20),
        FromDN VARCHAR(100),
        ToDN VARCHAR(100),
        DialedNumber VARCHAR(20),
        FinalNumber VARCHAR(20),
        FinalDN VARCHAR(100),
        BillCode VARCHAR(50),
        BillRate DECIMAL(10,2),
        BillCost DECIMAL(10,2),
        BillName VARCHAR(100),
        Chain VARCHAR(200),
        MissedQueueCalls TEXT,
        Status ENUM('manque','abandon','traite','en_attente') DEFAULT 'traite',
        Service VARCHAR(100),
        Agent VARCHAR(100)
    )
    """)

    # Création de la table Compteurs Journaliers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Compteurs_Journaliers (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Service VARCHAR(100),
        Date DATE,
        AppelsManques INT DEFAULT 0,
        AppelsAbandonnes INT DEFAULT 0,
        AppelsTraites INT DEFAULT 0,
        AppelsEnAttente INT DEFAULT 0,
        UNIQUE KEY unique_service_date (Service, Date)
    )
    """)

    # Création de la table Performances Agents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Performances_Agents (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Agent VARCHAR(100),
        Service VARCHAR(100),
        Date DATE,
        NombreAppels INT DEFAULT 0,
        TauxRappel FLOAT DEFAULT 0,
        TempsMoyenResponse FLOAT DEFAULT 0,
        NombreAbandons INT DEFAULT 0,
        UNIQUE KEY unique_agent_service_date (Agent, Service, Date)
    )
    """)

    # Création de la table Rapports Entreprise
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Rapports_Entreprise (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Service VARCHAR(100),
        DateDebut DATE,
        DateFin DATE,
        TotalAppels INT DEFAULT 0,
        AppelsManques INT DEFAULT 0,
        AppelsAbandonnes INT DEFAULT 0,
        AppelsTraites INT DEFAULT 0,
        AppelsEnAttente INT DEFAULT 0
    )
    """)

    # Création de la table cdr_logs (pour insertion CDR)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cdr_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        call_id VARCHAR(100) NOT NULL,
        caller VARCHAR(50),
        callee VARCHAR(50),
        call_start DATETIME,
        call_end DATETIME,
        duration INT,
        call_type VARCHAR(20),
        status VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    print("✅ Toutes les tables ont été créées avec succès dans la base de données.")

except mysql.connector.Error as err:
    print(f"❌ Erreur lors de la création de la base ou des tables : {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("🔗 Connexion MySQL fermée.")
