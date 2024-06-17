# Konklúzió

## Betöltés
A betöltés a python-os megoldással elég hosszadalmas (6 perc) nagy dataset esetén. 
Érdemesebb inkább a Neo4j adatbázisba beépített importálás modulokat használni(pl .csv fájl)
A query az importálásra nem a legjobb, javítási lehetőség biztosan van, de idő szűkében nehezen leltem volna rá.

## Lekérdezések
Lekérdezések gyorsak nagy adatmennyiség esetén is. A példánk alapján az emberek kapcsolatainak lekérése kb. 2 másodperc.
Ebbe persze beleszámítjuk a gépen a háttérben folyó folyamatokat is, hálózat esetén pedig a késleltetést.
Nagyobb adatmennyiség lekérdezése esetén feltételezhető, hogy nagyobb lesz a feldolgozási idő, mivel az adatbázis 312 ezer relációval dolgozik.

## Törlés
A törlési idő nem gyors és nem is hosszú idő: 10 másodperc. Ez a nagy adatmennyiségnek és relációknak köszönhető.

## Adatátalakítás
Az egész excel fájl átadása pythonon keresztül nagyon nehézkes lett volna, több óra is elment vele, az első próbálkozásaim során.
Így először az adatot átalakítottam olyan formába, ahol nincsen duplikáció, azaz minden adat egy OrderNumber alatt van, hiába vannak különböző tárgyak benne.
Ezzel a beolvasandó sorokat sikeresen csökkentettem 260 ezer sorról -> 52 ezer sorra. 
