# Redis adatbázisban dolgoztam:
## Betöltés: 
Betöltöttem a SalesData.xlsx -ből az adatokat 3 „táblába „. Sales_origin(összes adatot tartalmazza), Sales(minden adat kivétel a Sales personoszlopot), Salesperson(salesperson, salespersonkey-t tartalmazza)
Úgymond 1-1 tábla betöltése: 25-33 másodpercet vesz igénybe.

## Lekérdezések 
sales_originban keresek:
Julio Lima tartozó adatok lekérdezési ideje kb 25 másodpercet vesz igénybe ami szerintem nagyon lassúnak mondható.

salesperson és a sales-ben keresek:
A „táblákat„ a salespersonkey alapján kapcsoltam össze és igy kerestem meg, hogy Julio Lima mennyi dolgot értékesített.

## Törlés
Én az összes kulcsérték párt törlöm ez kb 2 másodpercet vesz igénybe.
 
