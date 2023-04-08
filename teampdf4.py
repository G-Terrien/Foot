import random
import pandas as pd

df = pd.read_csv("notes.csv")
liste = df[['Joueurs','Poste','Moyenne','Présent']].values.tolist()
df['Présent'] = df['Présent'].astype(bool)
print(liste)
players = []
for element in liste:
    if element[3]:
        dictionnaire = {'name': element[0], 'position': element[1], 'level': 100*float(element[2].replace(',', '.'))}
        players.append(dictionnaire)
  
def createteam(players):
    #création équipe random
    leveldef1=100
    leveldef2=0
    #bruteforce pour générer "toutes" les équipes équilibrées en position sans ce soucier du niveau ou presque
    #à améliorer/rationaliser
    for i in range(1000):
        random.shuffle(players)
        #classement des joueurs
        #players.sort(key=lambda x: x["level"], reverse=True)
        team1, team2 = {"Goalkeeper": [], "Defender": [], "Midfielder": [], "Forward": []}, {"Goalkeeper": [], "Defender": [], "Midfielder": [], "Forward": []}
        # équilibrer en position
        for player in players:
            if len(team2[player["position"]]) < len(team1[player["position"]]) or (len(team1["Goalkeeper"])+len(team1["Defender"])+len(team1["Midfielder"])+len(team1["Forward"])) == 5:
                team2[player["position"]].append(player)
            else:
                team1[player["position"]].append(player)
        # Simplication de la structure
        team1=team1["Goalkeeper"]+team1["Defender"]+team1["Midfielder"]+team1["Forward"]
        team2=team2["Goalkeeper"]+team2["Defender"]+team2["Midfielder"]+team2["Forward"]
        # Vérification de l'équlibre des niveaux (
        level1=sum(player["level"] for player in team1)
        level2=sum(player["level"] for player in team2)
        if abs(level2-level1)<abs(leveldef1-leveldef2):
            team1def,team2def = team1,team2
            leveldef1,leveldef2 = level1,level2
    return team1def,team2def,leveldef1,leveldef2

def afficher(team1,team2,leveldef1,leveldef2):
    print("Team 1: ",leveldef1)
    for player in team1:
        print(f"Nom: {player['name']}, Position: {player['position']}")
    print()
    print("Team 2:",leveldef2)
    for player in team2:
        print(f"Name: {player['name']}, Position: {player['position']}")
    print()

teams = createteam(players)
afficher(teams[0],teams[1],teams[2],teams[3])

