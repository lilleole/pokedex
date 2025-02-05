import database
import getData

def main():
    db = database.Database()
    data = getData.GetData()

    db.createTable()
    data.parseData()
    for row in data.pokemonList:
        db.insertPokemon(row)

    print(f"{db.added} pokemon has been inserted.")

    db.close()

if __name__ == "__main__":
    main()