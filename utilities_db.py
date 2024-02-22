##################################################################################################################################################
#
#                         UTILITAIRES POUR LA BASE DE DONNEE - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################

import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()



def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True

def insert_data(data):
    # Exécute la requête SQL
    cursor.execute("INSERT INTO users (pseudo, password) VALUES (:pseudo, :password);", data)
    # Valide les modifications
    conn.commit()

def insert_data_score(pseudo, score):
    # Vérifie si l'utilisateur existe dans la base de données
    cursor.execute("SELECT id,score FROM users WHERE pseudo = :pseudo", {"pseudo": pseudo})
    result = cursor.fetchone()

    # L'utilisateur n'existe pas (impossible a ce stade)
    if result is None:
        raise Exception("The given user does not exist: " + pseudo)
    
    # L'utilisateur existe mais son score n'est pas definit ou est superieur
    if result[1] is None or result[1] > score:
        cursor.execute("UPDATE users SET score = :score WHERE id = :user_id", {"score": score, "user_id": result[0]})
        conn.commit()