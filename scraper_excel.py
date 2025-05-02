import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import re
from difflib import SequenceMatcher  # Import pour la similarité
import unicodedata  # Pour normaliser les titres

def nettoyer_titre(titre):
    """
    Nettoie le titre pour enlever la date, les titres alternatifs et normaliser les caractères.
    Exemple: "Les Anges déchus (Duo luo tian shi (Fallen Angels)) (1997)" → "Les Anges déchus"
    """
    # Enlever la date et tout texte entre parenthèses
    titre_clean = re.sub(r"\s*\([^)]*\)", "", titre).strip()
    # Normaliser les caractères (supprimer les accents et caractères spéciaux)
    titre_clean = unicodedata.normalize('NFD', titre_clean).encode('ascii', 'ignore').decode('utf-8')
    return titre_clean.lower().strip()

def get_film_urls_by_year(year):
    url = f"https://www.jpbox-office.com/bilanfr.php?view=1&yr={year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    film_urls = []
    for a in soup.select("table.news a[href^='fichfilm.php?id=']"):
        href = a.get("href")
        full_url = f"https://www.jpbox-office.com/{href}"
        film_urls.append(full_url)

    return list(set(film_urls))

def get_film_title_and_release(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find("title").text.strip().split(" - ")[0]

    sortie = None
    table = soup.find("table", class_="entete")
    if table:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                if "Sortie France" in label:
                    sortie = value
                    break

    return title, sortie

def scrape_film_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = {
        "Démarrage": None,
        "Entrées": None,
        "Démarrage Paris": None,
        "Entrées Paris": None,
        "Rentabilité": None,
        "Entrées Hors France": None
    }

    table = soup.find("table", class_="entete")
    if not table:
        return result

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        label = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)

        if "Démarrage France" in label:
            result["Démarrage"] = value
        elif "Entrées France" in label:
            result["Entrées"] = value
        elif "Démarrage Paris" in label:
            result["Démarrage Paris"] = value
        elif "Entrées Paris" in label:
            result["Entrées Paris"] = value
        elif "Rentabilité" in label:
            result["Rentabilité"] = value
        elif "Entrées hors France" in label:
            result["Entrées Hors France"] = value

    return result

# Charger le fichier Excel
df = pd.read_excel("BDD_FILMS.xlsx", sheet_name="Tableau")
df=df.head(5)  # Modifier en fonction du nombre de films que tu veux traiter
# Ajouter une colonne "Sortie France année" en extrait uniquement l'année de la date de sortie
df['Sortie France année'] = pd.to_datetime(df['Sortie France'], errors='coerce').dt.year.astype('Int64')

# Ajouter les colonnes s’il manque pour les informations supplémentaires
colonnes_infos = [
    "Démarrage", "Entrées", "Démarrage Paris",
    "Entrées Paris", "Rentabilité", "Entrées Hors France"
]

for col in colonnes_infos:
    if col not in df.columns:
        df[col] = None

# Fonction pour mesurer la similarité des titres
def calculer_similarity(titre_bdd_clean, titre_site_clean):
    return SequenceMatcher(None, titre_bdd_clean, titre_site_clean).ratio()

# Traiter chaque film
for i, row in df.iterrows():
    titre_bdd_clean = nettoyer_titre(row["Nom"]).strip().lower()
    sortie_bdd_annee = row["Sortie France année"]

    # Recherche de l'année sur JPBox
    print(f"🎬 Traitement film {i+1}: {row['Nom']}")
    print(f"→ Titre nettoyé : {titre_bdd_clean}")
    print(f"→ Année extraite : {sortie_bdd_annee}")

    # Récupérer les URLs des films pour l'année correspondante
    urls = get_film_urls_by_year(sortie_bdd_annee)

    matched_url = None
    for url in urls:
        try:
            titre_site, sortie_site = get_film_title_and_release(url)
        except Exception as e:
            print(f"Erreur lors de l'accès à {url}: {e}")
            continue

        if not titre_site or not sortie_site:
            continue

        titre_site_clean = nettoyer_titre(titre_site).strip().lower()

        # Calculer la similarité entre le titre de la BDD et le titre du site
        similarity = calculer_similarity(titre_bdd_clean, titre_site_clean)
        print(f"   ↪ Comparé à : {titre_site_clean} (similarité : {similarity:.2f})")

        if similarity > 0.5:  # Seuil de similarité à ajuster si nécessaire
            matched_url = url
            break

    if matched_url:
        print(f"→ Match trouvé : {matched_url}")
        data = scrape_film_data(matched_url)
        for key in colonnes_infos:
            df.at[i, key] = data.get(key)
    else:
        print("❌ Aucun match trouvé.")

    sleep(1)  # pour éviter de surcharger le serveur

# Sauvegarde du fichier avec les nouvelles colonnes
df.to_excel("films_avec_infos.xlsx", index=False)
print("✅ Fichier mis à jour : films_avec_infos.xlsx")



