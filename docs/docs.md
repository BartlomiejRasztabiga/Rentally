# Dokumentacja Projektu PIPR
### (System do obsługi wypożyczalni pojazdów)

&nbsp;

## Wstęp
Realizacja projektu składa się z dwóch części:
- backend w postaci REST API
- frontend w postaci aplikacji webowej

### Backend
REST API w Pythonie zbudowane przy użyciu frameworka FastAPI [](https://fastapi.tiangolo.com/).

Baza danych użyta do zapisywania danych używanych w aplikacji to PostgreSQL.

API jest zgodne z poniższym arkuszem:
[](https://docs.google.com/spreadsheets/d/1ewicTL3VWaDlt85r7Q2gd7PxisjfbTwCgodmpcGsaMI/edit?usp=sharing)

![](api-design.png)

Model bazy danych jest zgodny z poniższym schematem relacji encji:
![](ERD.png)



&nbsp;

### Frontend
Aplikacja webowa zbudowana przy użyciu biblioteki React.js oraz bibliotek pomocnicznych (material-ui, axios).

## Jak uruchomić aplikację/testy

### Backend (testy)
Aby uruchomić testy, najlepiej uruchomić skrypt scripts/test-docker.sh który tworzy 2 kontenery Dockera przy pomocy docker-compose (backend + baza danych PostgreSQL) na podstawie zmiennych środowiskowych zawartych w pliku .env

```bash
cd backend
sudo chmod +x ./scripts/test-docker.sh
./scripts/test-docker.sh
```

Można też uruchomić testy w standardowy sposób, jednak wymaga to działającej instancji bazy danych PostgreSQL, zainicjalizowania środowiska wirtualnego aplikacji oraz uruchomienia skryptów prestart.sh i tests-start.sh.

### Backend (aplikacja)
Aby uruchomić aplikację należy najpierw zainstalować jej zależności oraz zainicjalizować środowisko wirtualne. Do zarządzania zależnościami, zamiast pip-a użyłem poetry, które działaniem przypomina node package manager (npm).

Narzędzie to należy zainstalować zgodnie z instrukcją na stronie producenta [](https://python-poetry.org/docs/)

Po zainstalowaniu poetry, należy wykonać następujące komendy:
```bash
cd backend
poetry install
poetry shell
```

Po wykonaniu powyższych komend powinniśmy znajdować się w kontekście środowiska wirtualnego aplikacji i możemy przejść do jej uruchomienia.

Aplikacja wymaga do działania bazy danych PostgreSQL z ustawieniami zgodnymi ze zmiennymi w pliku .env. Domyślne wartości to:
```properties
POSTGRES_SERVER=localhost:5432
POSTGRES_USER=rentally
POSTGRES_PASSWORD=rentally
POSTGRES_DB=rentally
```

W pliku .env znajdują się również login i hasło pierwszego użytkownika (z rolami administratora) oraz klucz używany do generowania tokenów JWT.

Ponadto, przed pierwszym uruchomieniem należy przeprowadzić migracje schematu bazy danych oraz utworzyć pierwszego użytkownika. Aby to zrobić należy uruchomić skrypt prestart.sh:
```bash
sudo chmod +x ./prestart.sh
./prestart.sh
```

Aby uruchomić aplikację należy uruchomić skrypt start.sh
```bash
sudo chmod +x ./start.sh
./start.sh
```

Domyślnie serwer uruchomi się na porcie 8080, można to zmienić w pliku start.sh lub podać zmienną środowiskową PORT.

### Frontend (aplikacja)

Aby uruchomić aplikację potrzebujemy środowiska node i menedżera pakietów npm [](https://nodejs.org/en/).

Następnie uruchamiamy poniższe komendy:
```bash
cd frontend
npm i
npm start
```

Domyślnie aplikacja uruchomi się na porcie 3000.
Aby aplikacja mogła skomunikować się z serwerem należy ustawić URL serwera w pliku src/config.js. Domyślnie jest to (zgodne z domyślnymi ustawieniami serwera):
```js
const API_URL = "http://localhost:8080/api/v1";
```

## Podział kodu