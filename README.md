# SUPPORT DE TPS : Les Fichiers & les Exceptions
**Auteur : Pierre-Henry Barge**
 SUPPORT DE TPS : Les Fichiers & les Exceptions

Ce document décrit les besoins de rédaction du code source pour trois exercices pratiques autour de la gestion des fichiers, des exceptions et de l'analyse réseau en Python.

---

## Annexe : Fichiers fournis

### 1. `network_log.txt`
Ce fichier contient des exemples de logs réseau à analyser dans l’Exercice 1. Chaque ligne représente une connexion réseau, incluant généralement la date, l’heure, le protocole utilisé, l’adresse IP source et destination, ainsi que d’autres informations pertinentes. Utilisez ce fichier pour tester vos scripts d’analyse de logs.

### 2. `TP3.pdf`
Ce document PDF correspond à l’énoncé complet du TP3. Il détaille les objectifs pédagogiques, les consignes, et fournit des exemples ou des explications complémentaires pour la réalisation des exercices. Référez-vous à ce fichier pour toute précision sur le déroulement du TP.

---

---

## Exercice 1 : Analyse de logs réseau

**Objectif :**  
Développer un programme Python pour analyser un fichier `network_log.txt` contenant des logs réseau.

**Spécifications :**
- Compter le nombre total de lignes dans le fichier.
- Compter le nombre de connexions par protocole (HTTP, HTTPS, DNS, etc.).
- Identifier toutes les adresses IP uniques et les stocker dans un ensemble (`set`).
- Rechercher toutes les connexions impliquant une adresse IP saisie par l'utilisateur.

**Gestion des exceptions :**
- Vérifier l'existence du fichier.
- Gérer les erreurs de lecture.
- Gérer les entrées incorrectes de l'utilisateur.

---

## Exercice 2 : Scanner de ports

**Objectif :**  
Créer un scanner de ports simple pour une adresse IP donnée et sauvegarder les résultats.

**Modules à utiliser :**
- `socket`
- `os`
- `time`
- `json`
- `datetime` (depuis `datetime`)

**Fonctionnalités attendues :**
- Fonction pour scanner un port spécifique.
- Fonction pour scanner une plage de ports.
- Fonction pour sauvegarder les résultats dans un fichier JSON.
- Fonction pour charger et comparer des résultats précédents.

---

## Exercice 3 : Découverte et cartographie du réseau local

**Objectif :**  
Développer un outil pour découvrir les appareils sur le réseau local et générer une cartographie dans différents formats (TXT, CSV, JSON).

**Modules à utiliser :**
- `subprocess`
- `platform`
- `os`
- `csv`
- `json`
- `socket`
- `ipaddress`
- `concurrent.futures`
- `time`
- `datetime` (depuis `datetime`)

**Structure de données :**
Utiliser des dictionnaires pour stocker les informations sur chaque appareil réseau, par exemple :

```python
def creer_appareil(ip, nom=None, mac=None, temps_reponse=None, ports_ouverts=None):
    return {
        "ip": ip,
        "nom": nom,
        "mac": mac,
        "temps_reponse": temps_reponse,
        "ports_ouverts": ports_ouverts if ports_ouverts else [],
        "en_ligne": True if temps_reponse is not None else False
    }
```

---

## Bonnes pratiques

- Documenter chaque fonction et chaque étape du code.
- Utiliser la gestion d’exceptions pour garantir la robustesse.
- Structurer le code pour faciliter la maintenance et la réutilisation.


---

## Utilisation du bloc principal (`if __name__ == "__main__":`)

À la fin de votre fichier Python, placez le bloc suivant pour exécuter des exemples d'utilisation des fonctions développées dans les exercices précédents. Ce bloc permet de tester rapidement les fonctionnalités principales du script sans modifier le reste du code.

```python
if __name__ == "__main__":
    # Exemple d'utilisation :
    # Scanner les ports d'une IP cible
    ip_cible = "192.168.1.120"
    ports_a_scanner = list(range(20, 1025))
    scanner_ports_et_sauvegarder(ip_cible, ports_a_scanner)

    # Découvrir les hôtes sur un réseau local
    network_cidr = "192.168.1.0/24"
    hosts = discover_network(network_cidr)

    # Sauvegarder la cartographie du réseau dans différents formats
    save_network_map_txt(hosts, "network_map.txt")
    save_network_map_csv(hosts, "network_map.csv")
    save_network_map_json(hosts, "network_map.json")
```

**Remarques :**
- Adaptez les adresses IP et les plages de ports selon votre environnement réseau.
- Ce bloc doit être placé à la toute fin du fichier Python.
- Veillez à ne pas dupliquer la définition de fonctions (par exemple, `scanner_plage_ports`) dans votre code.