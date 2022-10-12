#!/usr/bin/env python
# coding: utf-8

# # Projet maison n° 4

# In[1]:


# imports
import requests
from bs4 import BeautifulSoup


# **Partie A**
# 
# Ecrire une fonction `get_prices_from_url()` qui extrait des informations à partir des 2 pages ci-dessous.
# 
# ```python
# URL_PAGE2 = "https://kim.fspot.org/cours/page2.html"
# URL_PAGE3 = "https://kim.fspot.org/cours/page3.html"
# ```
# 
# Avec `URL_PAGE2`, la fonction doit retourner :
# 
# ```json
# {'Personal': {'price': '$5', 'storage': '1GB', 'databases': 1},
#  'Small Business': {'price': '$25', 'storage': '10GB', 'databases': 5},
#  'Enterprise': {'price': '$45', 'storage': '100GB', 'databases': 25}}
# ```

# In[2]:


# partie A
URL_PAGE2 = "https://kim.fspot.org/cours/page2.html"
URL_PAGE3 = "https://kim.fspot.org/cours/page3.html"

def get_prices_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    prices = {}
    
    pricing_table = soup.find_all(class_="pricing-table")
    for t in pricing_table:
        product_name = t.find("h2").text
        price = t.find(class_="pricing-table-price").text.strip().split()[0]
        storage, db = t.select(".pricing-table-list li")[3:5]
        prices[product_name] = {
            'price': price,
            'storage': storage.text.split()[0],
            'databases': int(db.text.split()[0]),
        }
    
    return prices


# **Partie B**
# 
# *L'abus d'alcool est dangereux pour la santé, à consommer avec modération.*
# 
# 1) Ecrire une fonction `extract_beer_infos()` qui extrait des informations sur une bière du site de bières *beowulf*.
# 
# Exemple d'URL: https://www.beerwulf.com/fr-fr/p/bieres/cuvee-des-trolls.33 
# 
# La fonction doit retourner :
# ```json
# {'Nom': 'Cuvée des Trolls',
#  'Style': 'Bière Blonde',
#  'Contenu': 25,
#  'Degré d’alcool': 7.0,
#  'Origine': 'Belgique',
#  'Brasseur': 'Brasserie Dubuisson Freres'}
# ```
# 
# 2) L'URL ci-après retourne un JSON avec une liste de bières :
# 
# ```python
# URL_BEERLIST_FRANCE = "https://www.beerwulf.com/fr-FR/api/search/searchProducts?country=France&container=Bouteille"
# ```
# 
# Ecrire une fonction `extract_beer_list_infos(url)` qui prend en argument cet URL et retourne les informations sur une liste de bières du site *beowulf*.
# 
# Cette fonction doit retourner la liste des informations obtenues par la fonction précédemment définie `extract_beer_infos()`.
# 
# Exemple de retour :
# 
# ```json
# [{'Nom':'Desperados','Style':'Lager','Contenu':33,'Degré d’alcool':5.9,'Origine':'France','Brasseur':'Desperados'},
# {'Nom':'La Lager Sans Gluten de Vézelay','Style':'Lager','Contenu':25,'Degré d’alcool':4.0,'Origine':'France','Brasseur':'Brasserie de Vézelay'},
# {'Nom':'Mélusine Bio','Style':'Pale Ale','Contenu': 33,'Degré d’alcool': 5.0,'Origine':'France','Brasseur':'Mélusine'},
# {'Nom':'La Parisienne Le Titi Parisien','Style':'IPA','Contenu':33,'Degré d’alcool':5.5,'Origine':'France','Brasseur': 'Brasserie la Parisienne'},
# {'Nom':'Brasserie De Sutter Brin de Folie','Style':'Bière Blonde','Contenu': 33,'Degré d’alcool':6.5,'Origine':'France','Brasseur':'Brasserie de Sutter'}]
# ```
# 
# **Facultatif**
# 
# Chercher comment optimiser cette fonction en utilisant `multiprocessing.Pool()` pour paralléliser les accès web.

# In[3]:


# partie B-1
def extract_beer_infos(url):
   
    # get soup from url
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
   # beer_info
    beer_infos = {}
    
    # Extract name:
    beer_infos["Nom"] = soup.find("h1").text
    
    # Extract infos:
    for dt in soup.find_all('dt'):
        dd = dt.find_next()
        if dt.text in ['Style', 'Contenu', 'Degré d’alcool', 'Origine', 'Brasseur']:
            value = dd.text.strip("\n\r ")
            if dt.text == "Contenu":
                value = int(value[:3])
            elif dt.text == "Degré d’alcool":
                value = float(value[:-1].replace(",", "."))
            beer_infos[dt.text] = value
                
    return beer_infos


# In[8]:


# partie B-2
URL_BEERLIST_FRANCE = "https://www.beerwulf.com/fr-FR/api/search/searchProducts?country=Belgique&container=Bouteille"

def extract_beer_list_infos(url):
    res = requests.get(url).json()
    beer_pages = ['https://www.beerwulf.com' + item['contentReference'] for item in res['items']]
    
    # Sequential version (slow):
    #beers = [extract_beer_infos(u) for u in beer_pages]
    
    # Parallel version (faster):
    # Windows workaround
    # see: https://medium.com/@grvsinghal/speed-up-your-python-code-using-multiprocessing-on-windows-and-jupyter-or-ipython-2714b49d6fac
    #
    from multiprocessing import Pool
    with Pool() as p:
        beers = p.map(extract_beer_infos, beer_pages)
    
    return beers


# In[5]:


import unittest

class Session4Tests(unittest.TestCase):
    def test_01_get_prices_from_url_page2(self):
        prices = get_prices_from_url(URL_PAGE2)
        # We should have found 3 products:
        self.assertIsInstance(prices, dict)
        self.assertEqual(len(prices), 3)
        self.assertIn('Personal', prices)
        self.assertIn('Small Business', prices)
        self.assertIn('Enterprise', prices)
        
        personal = prices['Personal']
        self.assertIn('price', personal)
        self.assertIn('storage', personal)
        self.assertIn('databases', personal)
        self.assertEqual(personal['price'], '$5')
        self.assertEqual(personal['storage'], '1GB')
        self.assertEqual(personal['databases'], 1)
        
    def test_02_get_prices_from_url_page3(self):
        prices = get_prices_from_url(URL_PAGE3)
        self.assertIsInstance(prices, dict)
        self.assertEqual(len(prices), 4)
        self.assertEqual(
            prices['Privilege'],
            {'databases': 100, 'price': '$99', 'storage': '1TB'}
        )
    
    def test_03_extract_beer_list_infos(self):
        infos = extract_beer_list_infos(URL_BEERLIST_FRANCE)
        self.assertIsInstance(infos, list)
        self.assertGreater(len(infos), 1)
        # Contenu = int
        # Degré d’alcool = float
        for beer in infos:
            self.assertIsInstance(beer['Nom'], str)
            self.assertIsInstance(beer['Style'], str)
            self.assertIsInstance(beer['Contenu'], int)
            self.assertIsInstance(beer['Degré d’alcool'], float)
            self.assertEqual(beer['Origine'], "Belgique")
            self.assertIsInstance(beer['Brasseur'], str)

            
def run_tests():
    test_suite = unittest.makeSuite(Session4Tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)


# In[6]:


if __name__ == '__main__':
    run_tests()

