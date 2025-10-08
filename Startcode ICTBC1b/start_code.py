# import modulen
from pathlib import Path
import json
import pprint
from database_wrapper import Database


# initialisatie

# parameters voor connectie met de database
db = Database(host="localhost", gebruiker="root", wachtwoord="", database="attractiepark")


# main

# Haal de eigenschappen op van een personeelslid
# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan om het juiste personeelslid te selecteren
select_query = "SELECT * FROM personeelslid WHERE id = 1"
personeelslid = db.execute_query(select_query)

# altijd verbinding sluiten met de database als je klaar bent
db.close()


# Haal alle onderhoudstaken op
# altijd verbinding openen om query's uit te voeren
db.connect()

# pas deze query aan en voeg queries toe om de juiste onderhoudstaken op te halen
select_query = "SELECT * FROM onderhoudstaak WHERE beroepstype = 'Mechanisch Monteur' AND bevoegdheid = 'Senior'"
onderhoudstaken = db.execute_query(select_query)
pprint.pp(onderhoudstaken)
# altijd verbinding sluiten met de database als je klaar bent
db.close()

# Bereken het totale duur van de onderhoudstaken
totale_duur = sum(
    taak.get("duur", 0)
    for taak in onderhoudstaken
    if isinstance(taak.get("duur"), (int, float))
)

# verzamel alle benodigde gegevens in een dictionary
dagtakenlijst = {
    "personeelsgegevens": {
        "naam": personeelslid[0]["naam"],
        "werktijd": personeelslid[0]["werktijd"],
        "beroepstype": personeelslid[0]["beroepstype"],
        "bevoegdheid": personeelslid[0]["bevoegdheid"],
        "specialist_in_attracties": personeelslid[0]["specialist_in_attracties"],
        "pauze_opsplitsen": personeelslid[0]["pauze_opsplitsen"],
        "max_fysieke_belasting": personeelslid[0]["verlaagde_fysieke_belasting"]
    },
    "weergegevens" : {
        # STAP 4: vul aan met weergegevens
    }, 
    "dagtaken": [
        onderhoudstaken
    ] 
    ,
    "totale_duur": totale_duur 
}

# uiteindelijk schrijven we de dictionary weg naar een JSON-bestand, die kan worden ingelezen door de acceptatieomgeving
with open('dagtakenlijst_personeelslid_' + personeelslid[0]["naam"] + '.json', 'w') as json_bestand_uitvoer:
    json.dump(dagtakenlijst, json_bestand_uitvoer, indent=4)