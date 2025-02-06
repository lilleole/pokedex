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


    searchdata(db)

    db.close()



def searchdata(db):
    while True:
        i = int(input("[1] search pokemon by id\n"
                      "[2] search pokemon by name\n"
                      "[3] quit\n"))

        if i == 1:
            id = int(input("input pokemon id: \n"))
            db.searchDatabaseID(id)
        elif i == 2:
            name = input("input pokemon name: \n")
            db.searchDatabaseName(name)
        elif i == 3:
            break
        else:
            print("invalid input")

if __name__ == "__main__":
    main()