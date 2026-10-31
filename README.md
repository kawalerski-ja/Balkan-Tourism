# Analiza potencjału turystycznego regionów Bałkanów

Projekt poświęcony jest wielowymiarowej ocenie atrakcyjności turystycznej regionów Bałkanów na poziomie NUTS 2. Na podstawie danych statystycznych porównujemy regiony, tworzymy rankingi oraz identyfikujemy grupy obszarów o podobnym profilu turystycznym.

## Cel projektu

Celem analizy jest sprawdzenie, jak regiony Bałkanów różnią się pod względem skali ruchu turystycznego, infrastruktury, dostępności transportowej, cen i jakości środowiska. Zastosowanie kilku metod porządkowania i grupowania pozwala spojrzeć na wyniki z różnych perspektyw.

Analiza obejmuje lata 2018–2024. Zakres danych i ich dostępność mogą różnić się między wskaźnikami.

## Zakres geograficzny

W projekcie uwzględniono wybrane kraje i regiony bałkańskie:

- Grecja (EL)
- Bułgaria (BG)
- Rumunia (RO)
- Chorwacja (HR)
- Słowenia (SI)
- Serbia (RS)
- Albania (AL)
- Czarnogóra (ME)
- Macedonia Północna (MK)

Dane regionalne analizowane są na poziomie NUTS 2. Część wskaźników, m.in. poziom cen i jakość wód kąpielowych, jest dostępna na poziomie krajowym (NUTS 0), dlatego przypisano je regionom na podstawie kodu kraju.

## Dane i wskaźniki

Dane pochodzą z bazy [Eurostat](https://ec.europa.eu/eurostat). W zależności od dostępności w zbiorze wykorzystano m.in.:

- liczbę noclegów ogółem i noclegów udzielonych turystom zagranicznym,
- liczbę obiektów noclegowych,
- ruch lotniczy,
- poziom cen,
- jakość wód kąpielowych,
- wskaźnik zagraniczności ruchu turystycznego.

Zbiór wynikowy zawiera ponadto etykiety klastrów, wartości miar rankingowych oraz pozycje regionów w rankingach.

## Metody

- **Eksploracyjna analiza danych (EDA)** — statystyki opisowe, korelacje, rozkłady, obserwacje odstające i porównania w czasie.
- **Standaryzacja zmiennych** — przygotowanie wskaźników o różnych skalach do wspólnej analizy.
- **Porządkowanie liniowe** — ranking regionów metodą wzorcową Hellwiga oraz metodą bezwzorcową opartą na standaryzowanych wartościach.
- **Analiza skupień** — hierarchiczna metoda Warda oraz metoda k-średnich; jako jedno z kryteriów oceny liczby skupień wykorzystano współczynnik silhouette.

## Zawartość repozytorium

| Plik | Opis |
|---|---|
| `EDA.ipynb` | Eksploracyjna analiza danych i wizualizacje. |
| `Projekt_Balkany_Analiza_V3.ipynb` | Główna analiza: przygotowanie cech, ranking regionów i klasteryzacja. |
| `getdata.py` | Skrypt pobierający i przygotowujący wybrane dane z Eurostatu. |
| `baza_balkany.xlsx` | Arkusz danych wykorzystywany przez notebooki. |
| `Balkany_Wyniki_Taksonomia.csv` | Wyniki analizy taksonomicznej w formacie CSV. |

## Uruchomienie

### Wymagania

Wymagany jest Python 3 oraz Jupyter Notebook. Projekt korzysta z bibliotek:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy openpyxl eurostat
```

W notebooku zawierającym mapę wykorzystywane są również `geopandas` i `shapely`. Instalacja tych pakietów może zależeć od systemu operacyjnego i środowiska Python.

### Analiza

1. Sklonuj repozytorium i przejdź do katalogu projektu.
2. Zainstaluj wymagane biblioteki.
3. Uruchom Jupyter:

   ```bash
   jupyter notebook
   ```

4. Otwórz `EDA.ipynb`, aby zapoznać się z eksploracją danych, lub `Projekt_Balkany_Analiza_V3.ipynb`, aby przejść do głównej analizy.

Notebooki korzystają z lokalnego pliku `baza_balkany.xlsx`. Skrypt `getdata.py` pobiera aktualne dane z Eurostatu, dlatego jego uruchomienie wymaga połączenia z internetem. Dane Eurostatu mogą być aktualizowane, a wyniki pobrania mogą różnić się od dołączonych plików.

## Wyniki

Końcowe wyniki porządkowania i grupowania regionów zapisano w `Balkany_Wyniki_Taksonomia.csv`. Zawierają one m.in. identyfikator regionu (`geo`), rok, wybrane wskaźniki, przypisania do klastrów, wyniki metod Hellwiga i bezwzorcowej oraz pozycje w rankingach.

## Źródła

- [Eurostat — baza danych](https://ec.europa.eu/eurostat/data/database)
- [Eurostat — klasyfikacja NUTS](https://ec.europa.eu/eurostat/web/nuts)

## Autorzy

Projekt akademicki przygotowany w ramach analizy danych dotyczących turystyki w regionach bałkańskich.
