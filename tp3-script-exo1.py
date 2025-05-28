def analyser_logs_reseau(nom_fichier="network_log_1.txt"):
    """
    Analyse un fichier de logs réseau et affiche des statistiques :
    - Nombre total de lignes
    - Nombre de connexions par protocole
    - Nombre et liste des adresses IP uniques

    Args:
        nom_fichier (str): Le nom du fichier de logs à analyser

    Returns:
        list: La liste complète des lignes de logs pour une utilisation ultérieure
    """
    try:
        # Ouvre le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            nombre_total_lignes = 0  # Compteur de lignes
            connexions_par_protocole = {}  # Dictionnaire pour compter les connexions par protocole
            adresses_ip_uniques = set()  # Ensemble pour stocker les adresses IP uniques
            logs_complets = []  # Liste pour stocker toutes les lignes de logs

            # Parcours chaque ligne du fichier
            for ligne in fichier:
                ligne = ligne.strip()  # Supprime les espaces en début/fin de ligne
                if not ligne:
                    continue  # Ignore les lignes vides
                nombre_total_lignes += 1  # Incrémente le compteur de lignes
                logs_complets.append(ligne)  # Ajoute la ligne à la liste des logs

                # Supposons que le format est : timestamp,IP_source,IP_dest,protocole,port_source,port_dest
                parties = ligne.split(',')  # Sépare la ligne en différentes parties
                if len(parties) < 4:
                    continue  # Ignore les lignes mal formées

                ip_source = parties[1].strip()  # Récupère l'adresse IP source
                ip_dest = parties[2].strip()    # Récupère l'adresse IP destination
                protocole = parties[3].strip()  # Récupère le protocole utilisé

                adresses_ip_uniques.add(ip_source)  # Ajoute l'IP source à l'ensemble
                adresses_ip_uniques.add(ip_dest)    # Ajoute l'IP destination à l'ensemble

                # Compte le nombre de connexions par protocole
                if protocole in connexions_par_protocole:
                    connexions_par_protocole[protocole] += 1
                else:
                    connexions_par_protocole[protocole] = 1

        # Affiche les statistiques calculées
        print(f"Nombre total de lignes : {nombre_total_lignes}")
        print("Connexions par protocole :")
        for proto, count in connexions_par_protocole.items():
            print(f"  {proto}: {count}")
        print(f"Nombre d'adresses IP uniques : {len(adresses_ip_uniques)}")
        print(f"Adresses IP uniques : {adresses_ip_uniques}")

        # Retourne la liste complète des logs pour d'autres traitements
        return logs_complets

    except FileNotFoundError:
        # Gestion de l'erreur si le fichier n'existe pas
        print(f"Erreur : Le fichier '{nom_fichier}' n'existe pas")
        return []
    except Exception as e:
        # Gestion d'autres exceptions
        print(f"Une erreur est survenue : {e}")
        return []

def rechercher_connexions_ip(logs, ip_recherche):
    # Rechercher et retourner toutes les connexions pour une IP donnée
    pass

# Programme principal
if __name__ == "__main__":
    nom_fichier = "network_log.txt"
    analyser_logs_reseau(nom_fichier)
    
    # Demander à l'utilisateur une adresse IP à rechercher
    ip_recherche = input("Entrez une adresse IP à rechercher : ")
    # Afficher les résultats