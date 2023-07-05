from flask import Flask, render_template, request

# Module de connexion à la base de données
import sqlite3

web_site = Flask(__name__)

# chemin de la base de données
DATABASE = './db/movies.sqlite'


# Page d'accueil
@web_site.route('/')
def index():
    #DATABASE = './db/movies.sqlite'
    #conn = sqlite3.connect(DATABASE)
    #cursor = conn.cursor()

    #creationNotes = """
    #CREATE TABLE Notation (
    #idFilm INT,
    #note INT
    #)
    #"""
    #cursor.execute(creationNotes)
    #conn.commit()
    return render_template('index.html')


# Recherche des films effectuée par le client par formulaire
@web_site.route('/movies/')
def rechercher_films():
    # Votre code ici
    # On récupére les arguments et on les écrits dans la console côté serveur
    recherche = "%" + request.args.get("recherche") + "%"
    etou = request.args.get("etou")
    nom = "%" + request.args.get("nom") + "%"
    print(recherche, etou, nom)

    # On élimine possibilié où utilisateur ne rentre rien
    if recherche == "%%" and nom == "%%":
        return render_template('films.html')

    # Connexion à la base de donnée
    DATABASE = './db/movies.sqlite'
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Différentes requêtes SQL possibles selon arguments utilisateur
    if etou == "ou" and recherche != "%%":
        nomsMovies = """
        SELECT title, movie_id
        FROM movie
        WHERE title LIKE ? 
        """
        return render_template('films.html',
                               titres=cursor.execute(nomsMovies,
                                                     (recherche, )))
    elif etou == "ou" and nom != "%%":
        nomsMovies = """
        SELECT title, movie_id
        FROM movie JOIN movie_crew USING (movie_id)
        JOIN person USING (person_id)
        WHERE person_name LIKE ? 
        """
        return render_template('films.html',
                               titres=cursor.execute(nomsMovies, (nom, )))
    else:
        nomsMovies = """
        SELECT title, movie_id
        FROM movie JOIN movie_crew USING (movie_id)
        JOIN person USING (person_id)
        WHERE title LIKE ?
        AND person_name LIKE ?
        """
        return render_template('films.html',
                               titres=cursor.execute(nomsMovies,
                                                     (recherche, nom)))

    # Fermeture connexion à la base de donnée
    cursor.close()
    conn.close


# Afichage d'une fiche de film appelée par le client
@web_site.route('/movie/<movie_id>')
def aficher_film(movie_id):
    # Votre code ici
    DATABASE = './db/movies.sqlite'
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    infosMovies = """
    SELECT title, movie_id, tagline, release_date, overview, popularity, budget, revenue, homepage
    FROM movie
    WHERE movie_id = ?
    """

    return render_template("fiche_film.html",
                           infos=cursor.execute(infosMovies, (movie_id, )))
    cursor.close()
    conn.close


# Lancement du serveur et écoute des requêtes
web_site.run(host='0.0.0.0', port=8080)
