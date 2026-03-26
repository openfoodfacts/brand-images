#!/bin/bash

# ==============================================================================
# Script pour renommer des fichiers en fonction d'un mappage CSV.
#
# Description :
# Ce script lit un fichier CSV (`pod.csv` par défaut) qui contient une ligne
# d'en-tête, des ID dans la première colonne et les noms correspondants dans
# la deuxième colonne. Les valeurs peuvent être entourées de guillemets.
# Il recherche dans le répertoire courant les fichiers dont le nom (sans
# l'extension) correspond à un ID et les renomme en utilisant le nom de la
# deuxième colonne, tout en conservant l'extension d'origine.
#
# Utilisation :
# 1. Enregistrez ce script sous le nom `rename_files.sh`.
# 2. Placez-le dans le même répertoire que vos fichiers image et `pod.csv`.
# 3. Rendez-le exécutable avec la commande : chmod +x rename_files.sh
# 4. Exécutez-le depuis votre terminal : ./rename_files.sh
#
# ==============================================================================

# Définit le nom du fichier CSV à utiliser
CSV_FILE="pod.csv"

# Vérifie si le fichier CSV existe dans le répertoire courant
if [ ! -f "$CSV_FILE" ]; then
    echo "Erreur : Le fichier CSV '$CSV_FILE' n'a pas été trouvé."
    echo "Veuillez vous assurer que le script est dans le même répertoire que $CSV_FILE."
    exit 1
fi

echo "Début du processus de renommage..."

# Utilise `tail -n +2` pour lire le fichier CSV à partir de la deuxième ligne,
# ignorant ainsi la ligne d'en-tête.
tail -n +2 "$CSV_FILE" | while IFS=, read -r id_col brand_name_col etc
do
    # Nettoie les variables lues du CSV :
    # 1. Enlève les caractères de retour chariot (problème courant avec les fichiers Windows/DOS).
    id_col=${id_col//$'\r'/}
    brand_name_col=${brand_name_col//$'\r'/}
    # 2. Enlève les guillemets (") qui pourraient entourer les valeurs.
    id_col=${id_col//\"/}
    brand_name_col=${brand_name_col//\"/}


    # Boucle sur tous les fichiers du répertoire courant
    for filename in *
    do
        # Vérifie si le fichier est un fichier ordinaire (pas un répertoire)
        if [ -f "$filename" ]; then
            # Extrait le nom du fichier sans l'extension
            base_name="${filename%.*}"
            # Extrait l'extension du fichier
            extension="${filename##*.}"

            # Compare le nom de base du fichier avec l'ID de la première colonne du CSV
            if [ "$base_name" == "$id_col" ]; then

                # Nettoie le nom de la marque pour l'utiliser comme nom de fichier :
                # - Supprime les espaces de début/fin.
                # - Remplace les espaces et les caractères spéciaux par des underscores (_).
                # - Supprime tout ce qui n'est pas alphanumérique, point, ou underscore.
                new_name=$(echo "$brand_name_col" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | tr ' ' '_' | sed 's/[^a-zA-Z0-9_.-]//g')

                # Construit le nouveau nom de fichier complet avec l'extension
                new_filename="${new_name}.${extension}"

                # Vérifie si un fichier avec le nouveau nom existe déjà
                if [ -f "$new_filename" ]; then
                    echo "Attention : Un fichier nommé '$new_filename' existe déjà. Renommage de '$filename' ignoré."
                else
                    # Renomme le fichier
                    mv -v "$filename" "$new_filename"
                fi
                # Passe au prochain enregistrement CSV une fois qu'une correspondance est trouvée et traitée
                break
            fi
        fi
    done
done

echo "Processus de renommage terminé."
