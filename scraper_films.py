from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unidecode
from data import load_data
from difflib import SequenceMatcher
import traceback

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


films_non_trouves = []

if __name__ == "__main__":
    df,_ = load_data()

    df['Démarrage USA']=''
    df['Box office USA']=''
    df['Box office reste du Monde']=''
    df['Box office France']=''
    df['Box office total']=''

    df['DEMARRAGE']=''
    df['ENTREES']=''
    df['DEMARRAGE PARIS']=''
    df['ENTREES PARIS']=''
    df['Rentabilité France']=''
    df['Entrées hors France']=''

    def safe_get(driver, url, element_check_by, element_check_value, timeout=10, retries=3):
        for attempt in range(retries):
            try:
                driver.get(url)
                wait = WebDriverWait(driver, timeout)
                wait.until(EC.presence_of_element_located((element_check_by, element_check_value)))
                return True  # <-- Ajout ici
            except Exception as e:
                if attempt < retries - 1:
                    print(f"⚠️ Tentative {attempt + 1} échouée pour charger {url}, actualisation...")
                    time.sleep(2)
                else:
                    print(f"❌ Échec total pour charger {url} : {e}")
                    return False  # <-- Ajout ici

                
    def safe_search(driver, film_name, retries=3):
        for attempt in range(retries):
            try:
                search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search")))
                search_bar.clear()
                search_bar.send_keys(film_name)
                search_bar.send_keys(Keys.RETURN)

                # Attente que la page de résultats s'affiche
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.col_poster_titre")))
                return True
            except Exception as e:
                print(f"❗ Échec recherche '{film_name}' (tentative {attempt + 1}) : {e}")
                time.sleep(2)
                driver.refresh()  # recharge la page
        return False
    
    def safe_click(driver, element, confirm_by, confirm_value, max_retries=3, wait_time=10):
        for attempt in range(max_retries):
            try:
                element.click()
                WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((confirm_by, confirm_value))
                )
                return True  # Le clic et le chargement ont réussi
            except Exception as e:
                print(f"[Tentative {attempt+1}/{max_retries}] Échec du clic ou du chargement : {e}")
                try:
                    driver.refresh()
                    WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.NAME, "search"))  # Retour à un état stable
                    )
                except:
                    pass
        return False

    df['Nom']=df['Nom'].astype('str')
    options = Options()
    options.add_argument("--ignore-certificate-errors") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    wait = WebDriverWait(driver, 10)

    row_number = df.index.get_loc(df[df['Nom'] == 'Garde à vue'].index[0])        
    for i in range(row_number,df.shape[0]):
        try:
            nom_film=df.iloc[i]['Nom'].strip()
            sortie=df.iloc[i]['Sortie']
            sortie_france=int(df.iloc[i]['Année fr'])
            liste_sortie_france=[i for i in range(sortie_france-1,sortie_france+2)]
            print(liste_sortie_france)
            realisateur=df.iloc[i]['Réalisateur']

            nom_du_film = f"{nom_film} ({sortie_france})"

            try:
                safe_get(driver, "https://www.jpbox-office.com/", By.NAME, "search")
            except Exception:
                print(f"Erreur d'accès au site pour {nom_film}")
                films_non_trouves.append(nom_film)
                continue

            if not safe_search(driver, nom_film):
                print(f"❌ Recherche échouée pour : {nom_film}")
                films_non_trouves.append(nom_film)
                continue


            try:
                #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.col_poster_titre")))
                films_site = driver.find_elements(By.CSS_SELECTOR, "td.col_poster_titre")
            except Exception as e:
                print(f"[{nom_film}] Problème lors de la récupération des résultats : {e}")
                films_non_trouves.append(nom_film)
                continue        


            film_voulu = None
            lien_voulu=None
            for film in films_site:
                lien = film.find_element(By.TAG_NAME, "a")
                titre_film_site = lien.text.strip()
                titre_film_sans_date = titre_film_site[:-6].strip()

                titre_clean_site = unidecode.unidecode(titre_film_sans_date.lower())
                nom_clean = unidecode.unidecode(nom_film.lower())


                print(f"Je cherche {nom_film}")
                print(titre_film_sans_date)
                if (nom_clean in titre_clean_site or similar(nom_clean, titre_clean_site) > 0.8) and \
                    (str(sortie_france) in titre_film_site or str(sortie) in titre_film_site or any(str(annee) in titre_film_site for annee in liste_sortie_france)):
                    lien_voulu = lien
                    break

            if lien_voulu is None:
                print(f"Aucun film trouvé correspondant à : {nom_film}")
                films_non_trouves.append(nom_film)
                continue


            ok = safe_click(driver, lien_voulu, By.CLASS_NAME, "tablesmall1b")
            if not ok:
                print(f"Erreur lors de l'ouverture de la fiche du film : {nom_film}")
                films_non_trouves.append(nom_film)
                continue

            
                
            tables = driver.find_elements(By.CLASS_NAME, "tablesmall1b")
            demarrage_usa = box_office_usa = box_office_reste_du_monde = box_office_france = box_office_total = None
            demarrage = entrees = demarrage_paris = entrees_paris = entrees_hors_france = rentabilite_france = None

            if len(tables) == 2:
                table1 = tables[0]
                rows_1 = table1.find_elements(By.TAG_NAME, "tr")

                for row in rows_1:
                    cells_1 = row.find_elements(By.TAG_NAME, "td")
                    if len(cells_1) == 2:
                        label = cells_1[0].text.strip().lower()
                        value = cells_1[1].text.strip().replace(" ", "")
                        if "démarrage usa" in label:
                            demarrage_usa = value
                        elif "etats-unis" in label:
                            box_office_usa = value
                        elif "reste du monde"== label:
                            box_office_reste_du_monde = value
                        elif "dont france" in label:
                            box_office_france = value
                        elif "total salles"== label:
                            box_office_total = value

                table_france = tables[1]
            else:
                print("⚠️ Table box-office global absente, uniquement les entrées disponibles.")
                table_france = tables[0]

            
            rows = table_france.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) == 2:
                    label = cells[0].text.strip().lower()
                    value = cells[1].text.strip().replace(" ", "")
                    if "démarrage paris" in label:
                        demarrage_paris = value
                    elif "démarrage" in label:
                        demarrage = value
                    elif "entrées paris" in label:
                        entrees_paris = value
                    elif "entrées"== label:
                        entrees = value
                    elif "entrées hors france" == label:
                        entrees_hors_france = value
                    elif "rentabilité"== label:
                        rentabilite_france = value

            df.iloc[i, df.columns.get_loc('Démarrage USA')] = demarrage_usa
            df.iloc[i, df.columns.get_loc('Box office USA')] = box_office_usa
            df.iloc[i, df.columns.get_loc('Box office reste du Monde')] = box_office_reste_du_monde
            df.iloc[i, df.columns.get_loc('Box office France')] = box_office_france
            df.iloc[i, df.columns.get_loc('Box office total')] = box_office_total

            df.iloc[i, df.columns.get_loc('DEMARRAGE PARIS')] = demarrage_paris
            df.iloc[i, df.columns.get_loc('DEMARRAGE')] = demarrage
            df.iloc[i, df.columns.get_loc('ENTREES PARIS')] = entrees_paris
            df.iloc[i, df.columns.get_loc('ENTREES')] = entrees 
            df.iloc[i, df.columns.get_loc('Rentabilité France')] = rentabilite_france
            df.iloc[i, df.columns.get_loc('Entrées hors France')] = entrees_hors_france 

        except Exception as e:
            print(f"Erreur pour le film {nom_film} : {e}")
            traceback.print_exc()
            films_non_trouves.append(nom_film)
            continue

    driver.quit()
    print(films_non_trouves)
    df_scrap = df[[df.columns[0]] + list(df.columns[-11:])]
    df_scrap.to_excel("BDD_scraping_temp.xlsx")