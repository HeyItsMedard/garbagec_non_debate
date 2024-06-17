# CASSANDRA adatbázis

Cassandra adatbázissal dolgoztam az alábbi feladatokon:
1. A SalesData.xlsx adatainak beolvasása
2. WHERE feltételes keresés
3. 2 táblás keresés

## Betöltés
A SalesData.xlsx beolvasása hosszú ideig tartott pythonban.
A Cassandrába való adatok írása viszonylag hosszabb ideig tartanak. Batch nélkül akár több óra, Batch használatával ~12 perc.

## Lekérdezések
Akár 1 táblából kérdezek le akár több táblából, rendszerint csak néhány másodpercre van szüksége, hogy keressen.
Az adatok törlése általában nem vesz igénybe 1 másodpercet sem.