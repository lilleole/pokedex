from bs4 import BeautifulSoup
import requests


class GetData:
    def __init__(self):
        self.pokemonList = []
        try:
            r = requests.get('https://pokemondb.net/pokedex/all', timeout=10)
            r.raise_for_status()  # Raises HTTPError for bad responses
            print(f'Response Status: {r.status_code}')
            self.soup = BeautifulSoup(r.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            self.soup = None

    def parseData(self):
        if not self.soup:
            print("No data to parse.")
            return

        content = self.soup.find('tbody')
        rows = content.find_all('tr')

        for tr in rows:
            try:
                tds = tr.find_all('td')
                pokemon = {
                    "id": tds[0].get('data-sort-value', '0'),  # Fallback if None
                    "NAME": tds[1].text.strip(),
                    "TYPE": self.getTypes(tds[2].find_all('a')),
                    "TOTAL": int(tds[3].text),
                    "HP": int(tds[4].text),
                    "ATTACK": int(tds[5].text),
                    "DEFENSE": int(tds[6].text),
                    "SP_ATTACK": int(tds[7].text),
                    "SP_DEFENSE": int(tds[8].text),
                    "SPEED": int(tds[9].text),
                    "Match_UP": get_matchups(self.getTypes(tds[2].find_all('a')).split(" "))
                }
                self.pokemonList.append(pokemon)

            except Exception as e:
                print(f"Error parsing Pokémon data: {e}")

    def getTypes(self, type_elements):
        return " ".join([data.text.strip() for data in type_elements])


def get_matchups(types, get_coverage=False, inverse=False):
    type_matchups = {
        "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                   "Fighting": 2, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1,
                   "Rock": 1, "Ghost": 0, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Fire": {"Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 0.5, "Ice": 0.5,
                 "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 0.5,
                 "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 0.5},

        "Water": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 2, "Grass": 2, "Ice": 0.5,
                  "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 1,
                  "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},

        "Electric": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 0.5, "Grass": 1, "Ice": 1,
                     "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 1,
                     "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},

        "Grass": {"Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 0.5, "Grass": 0.5, "Ice": 2,
                  "Fighting": 1, "Poison": 2, "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 2,
                  "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Ice": {"Normal": 1, "Fire": 2, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 0.5,
                "Fighting": 2, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1,
                "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 2, "Fairy": 1},

        "Fighting": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                     "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 2, "Psychic": 2, "Bug": 0.5,
                     "Rock": 0.5, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 2},

        "Poison": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                   "Fighting": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 1, "Psychic": 2, "Bug": 0.5,
                   "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 0.5},

        "Ground": {"Normal": 1, "Fire": 1, "Water": 2, "Electric": 0, "Grass": 2, "Ice": 2,
                   "Fighting": 1, "Poison": 0.5, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1,
                   "Rock": 0.5, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Flying": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 2, "Grass": 0.5, "Ice": 2,
                   "Fighting": 0.5, "Poison": 1, "Ground": 0, "Flying": 1, "Psychic": 1, "Bug": 1,
                   "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Psychic": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                    "Fighting": 0.5, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 0.5, "Bug": 2,
                    "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 2, "Steel": 1, "Fairy": 1},

        "Bug": {"Normal": 1, "Fire": 2, "Water": 1, "Electric": 1, "Grass": 0.5, "Ice": 1,
                "Fighting": 0.5, "Poison": 1, "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 1,
                "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Rock": {"Normal": 0.5, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 2, "Ice": 1,
                 "Fighting": 2, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 1,
                 "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1},

        "Ghost": {"Normal": 0, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                  "Fighting": 0, "Poison": 0.5, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 0.5,
                  "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 2, "Steel": 1, "Fairy": 1},

        "Dragon": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Grass": 0.5, "Ice": 2,
                   "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1,
                   "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1, "Steel": 1, "Fairy": 2},

        "Dark": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                 "Fighting": 2, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 0, "Bug": 2,
                 "Rock": 1, "Ghost": 0.5, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 2},

        "Steel": {"Normal": 0.5, "Fire": 2, "Water": 1, "Electric": 1, "Grass": 0.5, "Ice": 0.5,
                  "Fighting": 2, "Poison": 0, "Ground": 2, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5,
                  "Rock": 0.5, "Ghost": 1, "Dragon": 0.5, "Dark": 1, "Steel": 0.5, "Fairy": 0.5},

        "Fairy": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                  "Fighting": 0.5, "Poison": 2, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 0.5,
                  "Rock": 1, "Ghost": 1, "Dragon": 0, "Dark": 0.5, "Steel": 2, "Fairy": 1}
    }

    matchups = {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1, "Ice": 1,
                "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1,
                "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 1, "Fairy": 1}

    for t in types:
        for x in type_matchups:
            if get_coverage:
                if matchups[x] == 1:
                    if inverse:
                        matchups[x] /= type_matchups[x][t]
                    else:
                        matchups[x] *= type_matchups[x][t]
            else:
                if inverse:
                    matchups[x] /= type_matchups[t][x]
                else:
                    matchups[x] *= type_matchups[t][x]

    return matchups

