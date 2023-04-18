import pyexcel_ods
import random

session_info.show()

# nom de la feuille que vous voulez atteindre
nom_feuille = "Notes consolidées"

# chemin d'accès au fichier ods
file_path = "Estimatif.ods"

# Nombre de joueurs
file_path = "Estimatif.ods"

def read_ods_file(file_path,nom_feuille):
    """Lecture des données à partir d'un fichier ods"""
    data = pyexcel_ods.get_data(file_path)[nom_feuille]
    sheet = data[0]
    headers = sheet
    players_data = [dict(zip(headers, row)) for row in data[1:22]]
    return players_data

def sort_players(players_data, key):
    """Trier les joueurs en fonction d'une clé"""
    return sorted(players_data, key=lambda x: x[key], reverse=True)

def choose_best_players(players_data):
    """Choisir les 5 meilleurs joueurs de chaque équipe"""
    best_players = []
    for position in ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']:
        position_players = [player for player in players_data if player['Poste'].lower() == position]
        best_players += sorted(position_players, key=lambda x: x['Moyenne'], reverse=True)[:5]
    return best_players

def create_teams(file_path,nom_feuille):
    """Créer deux équipes équilibrées à partir d'un fichier ods"""
    players_data = read_ods_file(file_path,nom_feuille)
    """Choisir les joueurs présents"""
    players = []
    for player in players_data:
        if player['Présent'] == True:
            players.append(player)
    """"Créer les équipes"""
    leveldef1,leveldef2 = 1000, 0
    for i in range(10000):
        random.shuffle(players)
        #classement des joueurs
        team1, team2 = {"Goalkeeper": [], "Defender": [], "Midfielder": [], "Forward": []}, {"Goalkeeper": [], "Defender": [], "Midfielder": [], "Forward": []}
        # équilibrer en position
        for player in players:
            if len(team2[player["Position"]]) < len(team1[player["Position"]]) or (len(team1["Goalkeeper"])+len(team1["Defender"])+len(team1["Midfielder"])+len(team1["Forward"])) == 5:
                team2[player["Position"]].append(player)
            else:
                team1[player["Position"]].append(player)
        # Simplication de la structure
        team1=team1["Goalkeeper"]+team1["Defender"]+team1["Midfielder"]+team1["Forward"]
        team2=team2["Goalkeeper"]+team2["Defender"]+team2["Midfielder"]+team2["Forward"]
        # Vérification de l'équlibre des niveaux
        level1=sum(player["Moyenne"] for player in team1)
        level2=sum(player["Moyenne"] for player in team2)
        if abs(level2-level1)<abs(leveldef1-leveldef2):
            team1def,team2def = team1,team2
            leveldef1,leveldef2 = level1,level2
    return team1, team2

def afficher(team1,team2):
    print("Team 1 : ",  'Défense=', round(sum(player['Défense'] for player in team1)),
                        ' Tenue de balle=', round(sum(player['Tenue de balle'] for player in team1)),
                        ' Régularité=', round(sum(player['Régularité'] for player in team1)),
                        ' Endurance=', round(sum(player['Endurance'] for player in team1)),
                        ' Moyenne=', round(sum(player["Moyenne"] for player in team1))
          )
    for player in team1:
        print(player['Joueurs']," : ",player['Position'])
    print()
    print("Team 2 : ",  'Défense=', round(sum(player['Défense'] for player in team2)),
                        ' Tenue de balle=', round(sum(player['Tenue de balle'] for player in team2)),
                        ' Régularité=', round(sum(player['Régularité'] for player in team2)),
                        ' Endurance=', round(sum(player['Endurance'] for player in team2)),
                        ' Moyenne=', round(sum(player["Moyenne"] for player in team2))
          )
    for player in team2:
        print(player['Joueurs']," : ",player['Position'])
    print()


team1, team2 = create_teams(file_path,nom_feuille)
afficher(team1,team2)
