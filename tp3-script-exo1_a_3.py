import socket
import os
import time
import json
from datetime import datetime
import subprocess
import platform
import csv
import ipaddress
from collections import Counter

def scanner_port(ip, port, timeout=1):
    """
    Scanne un port spécifique sur une adresse IP donnée.

    Args:
        ip (str): Adresse IP à scanner.
        port (int): Numéro du port à tester.
        timeout (int, optional): Durée maximale (en secondes) d'attente pour la connexion. Défaut : 1.

    Returns:
        bool: True si le port est ouvert, False sinon.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            result = s.connect_ex((ip, port))
            return result == 0
        except Exception:
            return False

def scanner_ports_et_sauvegarder(ip, ports, fichier_log=None):
    """
    Scanne une liste de ports sur une IP et sauvegarde les résultats dans un fichier log JSON.

    Args:
        ip (str): Adresse IP à scanner.
        ports (list): Liste des ports à scanner.
        fichier_log (str, optional): Chemin complet du fichier de log JSON.
    """
    if fichier_log is None:
        fichier_log = r"\Documents\scanner_log.json"
    resultats = {}
    for port in ports:
        ouvert = scanner_port(ip, port)
        etat = "ouvert" if ouvert else "fermé"
        print(f"{ip}:{port} {etat}")
        resultats[str(port)] = etat
    with open(fichier_log, "w", encoding="utf-8") as f:
        json.dump({"ip": ip, "resultats": resultats}, f, indent=4)
    print(f"Résultats sauvegardés dans {fichier_log}")

# Exemple d'utilisation :
# ip_cible = "192.168.1.105"
# ports_a_scanner = list(range(20, 1025))
# scanner_ports_et_sauvegarder(ip_cible, ports_a_scanner)

def extraire_et_compter_ip(fichier_log):
    """
    Extrait toutes les adresses IP du fichier log, les compte et les affiche triées par nombre d'occurrences.

    Args:
        fichier_log (str): Chemin du fichier log à analyser.

    Returns:
        dict: Dictionnaire {ip: nombre d'occurrences}
    """
    ip_list = []
    try:
        with open(fichier_log, 'r') as f:
            for ligne in f:
                parties = ligne.strip().split()
                # Supposons que le format est : [timestamp] [IP source] [IP dest] [protocole] [port]
                if len(parties) >= 3:
                    ip_src = parties[1]
                    ip_dest = parties[2]
                    ip_list.extend([ip_src, ip_dest])
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_log}' n'existe pas.")
        return {}
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return {}

    compteur = Counter(ip_list)
    print("Adresses IP classées par nombre d'occurrences :")
    for ip, count in compteur.most_common():
        print(f"  {ip} : {count}")
    return dict(compteur)

# --- Ajout d'une fonction pour séparer les connexions par protocoles connus ---

def compter_connexions_par_protocoles(connexions_par_protocole):
    """
    Sépare et compte les connexions par protocoles connus (http, https, ssh, dns, etc.)
    et regroupe les autres sous 'autres'.
    """
    protocoles_connus = {
        "http": ["http", "80"],
        "https": ["https", "443"],
        "ssh": ["ssh", "22"],
        "dns": ["dns", "53"],
        "ftp": ["ftp", "21"],
        "smtp": ["smtp", "25"],
        "pop3": ["pop3", "110"],
        "imap": ["imap", "143"],
        "telnet": ["telnet", "23"],
    }
    compte = {proto: 0 for proto in protocoles_connus}
    compte["autres"] = 0

    for protocole, count in connexions_par_protocole.items():
        trouve = False
        for proto, aliases in protocoles_connus.items():
            if protocole.lower() in aliases or protocole.lower() == proto:
                compte[proto] += count
                trouve = True
                break
        if not trouve:
            compte["autres"] += count
    return compte

# Affichage du résultat dans le terminal lors de l'analyse des logs
def afficher_connexions_par_protocoles(connexions_par_protocole):
    compte = compter_connexions_par_protocoles(connexions_par_protocole)
    print("Connexions regroupées par protocoles connus :")
    for proto, nb in compte.items():
        print(f"  {proto} : {nb}")

# --- Définition des structures de données ---

# Structure pour stocker les informations sur un appareil réseau
# Utilisation de tuples et de dictionnaires
def creer_appareil(ip, nom=None, mac=None, temps_reponse=None, ports_ouverts=None):
    return {
        "ip": ip,
        "nom": nom,
        "mac": mac,
        "temps_reponse": temps_reponse,
        "ports_ouverts": ports_ouverts if ports_ouverts else [],
        "en_ligne": True if temps_reponse is not None else False
    }

# --- Découverte et cartographie du réseau local ---

import concurrent.futures

def ping_ip(ip):
    """Teste si une IP répond au ping."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, "1", "-w", "1000", str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False

def get_hostname(ip):
    """Tente de récupérer le nom d'hôte pour une IP."""
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except Exception:
        return ""

def discover_network(network_cidr):
    """Découvre les appareils actifs sur le réseau local."""
    print(f"Découverte du réseau {network_cidr} en cours...")
    hosts = []
    network = ipaddress.ip_network(network_cidr, strict=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_ip, ip): ip for ip in network.hosts()}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            if future.result():
                hostname = get_hostname(ip)
                hosts.append({"ip": str(ip), "hostname": hostname})
    print(f"Découverte terminée : {len(hosts)} hôte(s) trouvé(s).")
    return hosts

def save_network_map_txt(hosts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for host in hosts:
            f.write(f"{host['ip']}\t{host['hostname']}\n")
    print(f"Cartographie réseau sauvegardée dans {filename}")

def save_network_map_csv(hosts, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ip", "hostname"])
        writer.writeheader()
        for host in hosts:
            writer.writerow(host)
    print(f"Cartographie réseau sauvegardée dans {filename}")

def save_network_map_json(hosts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(hosts, f, indent=4)
    print(f"Cartographie réseau sauvegardée dans {filename}")

# if __name__ == "__main__":
    # Exemple d'utilisation :
    # ip_cible = "192.168.1.120"
    # ports_a_scanner = list(range(20, 1025))
    # scanner_ports_et_sauvegarder(ip_cible, ports_a_scanner)
    # network_cidr = "192.168.1.0/24"
    # hosts = discover_network(network_cidr)
    # save_network_map_txt(hosts, "network_map.txt")
    # save_network_map_csv(hosts, "network_map.csv")
    # save_network_map_json(hosts, "network_map.json")

# (Bloc main déplacé à la fin du fichier)

# (Suppression de la définition dupliquée de scanner_plage_ports)

def sauvegarder_resultats_json(resultats, fichier):
    """Sauvegarde les résultats du scan dans un fichier JSON."""
    try:
        with open(fichier, 'w') as f:
            json.dump(resultats, f, indent=4)
        print(f"Résultats sauvegardés dans {fichier}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def charger_et_comparer_resultats(fichier1, fichier2):
    """Charge deux fichiers JSON de résultats et compare les différences."""
    try:
        with open(fichier1, 'r') as f1, open(fichier2, 'r') as f2:
            res1 = json.load(f1)
            res2 = json.load(f2)
        differences = {}
        tous_les_ports = set(res1.keys()) | set(res2.keys())
        for port in tous_les_ports:
            etat1 = res1.get(str(port), "inconnu")
            etat2 = res2.get(str(port), "inconnu")
            if etat1 != etat2:
                differences[port] = {"avant": etat1, "après": etat2}
        if differences:
            print("Différences détectées :")
            for port, etats in differences.items():
                print(f"Port {port}: {etats['avant']} -> {etats['après']}")
        else:
            print("Aucune différence détectée entre les deux scans.")
        return differences
    except Exception as e:
        print(f"Erreur lors de la comparaison : {e}")
        return {}

def analyser_logs(fichier_log):
    total_lignes = 0
    connexions_par_protocole = {}
    adresses_ip_uniques = set()
    lignes = []

    try:
        with open(fichier_log, 'r') as f:
            for ligne in f:
                total_lignes += 1
                lignes.append(ligne)
                parties = ligne.strip().split()
                # Supposons que le format est : [timestamp] [IP source] [IP dest] [protocole] [port]
                if len(parties) >= 4:
                    ip_src = parties[1]
                    ip_dest = parties[2]
                    protocole = parties[3]
                    adresses_ip_uniques.add(ip_src)
                    adresses_ip_uniques.add(ip_dest)
                    connexions_par_protocole[protocole] = connexions_par_protocole.get(protocole, 0) + 1
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_log}' n'existe pas.")
        return
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    print(f"Nombre total de lignes : {total_lignes}")
    print("Connexions par protocole :")
    for protocole, count in connexions_par_protocole.items():
        print(f"  {protocole} : {count}")
    print(f"Nombre d'adresses IP uniques : {len(adresses_ip_uniques)}")
    print("Adresses IP uniques :")
    for ip in adresses_ip_uniques:
        print(f"  {ip}")

    # Recherche des connexions pour une IP spécifique
    while True:
        ip_recherche = input("Entrez une adresse IP à rechercher (ou 'exit' pour quitter) : ").strip()
        if ip_recherche.lower() == 'exit':
            break
        if not ip_recherche or any(c for c in ip_recherche if c not in "0123456789."):
            print("Entrée invalide. Veuillez entrer une adresse IP valide.")
            continue
        resultats = [ligne for ligne in lignes if ip_recherche in ligne]
        if resultats:
            print(f"Connexions impliquant {ip_recherche} :")
            for res in resultats:
                print(res.strip())
        else:
            print(f"Aucune connexion trouvée pour l'adresse IP {ip_recherche}.")

if __name__ == "__main__":
    fichier_log = "network_log.txt"
    analyser_logs(fichier_log)
if __name__ == "__main__":
    # Utilisez le chemin absolu ou relatif selon votre besoin
    fichier_log = r"\Documents\network_log.txt"
    analyser_logs(fichier_log)
    # Suppression du bloc redondant et incorrect ici.

def scanner_plage_ports(ip, port_debut, port_fin, timeout=1):
    """Scanne une plage de ports sur une adresse IP donnée."""
    resultats = {}
    for port in range(port_debut, port_fin + 1):
        ouvert = scanner_port(ip, port, timeout)
        resultats[port] = "ouvert" if ouvert else "fermé"
    return resultats

def sauvegarder_resultats_json(resultats, fichier):
    """Sauvegarde les résultats du scan dans un fichier JSON."""
    try:
        with open(fichier, 'w') as f:
            json.dump(resultats, f, indent=4)
        print(f"Résultats sauvegardés dans {fichier}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def charger_et_comparer_resultats(fichier1, fichier2):
    """Charge deux fichiers JSON de résultats et compare les différences."""
    try:
        with open(fichier1, 'r') as f1, open(fichier2, 'r') as f2:
            res1 = json.load(f1)
            res2 = json.load(f2)
        differences = {}
        tous_les_ports = set(res1.keys()) | set(res2.keys())
        for port in tous_les_ports:
            etat1 = res1.get(str(port), "inconnu")
            etat2 = res2.get(str(port), "inconnu")
            if etat1 != etat2:
                differences[port] = {"avant": etat1, "après": etat2}
        if differences:
            print("Différences détectées :")
            for port, etats in differences.items():
                print(f"Port {port}: {etats['avant']} -> {etats['après']}")
        else:
            print("Aucune différence détectée entre les deux scans.")
        return differences
    except Exception as e:
        print(f"Erreur lors de la comparaison : {e}")
        return {}
