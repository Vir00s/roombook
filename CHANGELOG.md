# Changelog

Format wzorowany na [Keep a Changelog](https://keepachangelog.com/).

## 2026-11-05

### Added
- Testy pytest na prawdziwym PostgreSQL: reguły ograniczeń rezerwacji (nakładanie się,
  styk terminów, inna sala, nieaktywne statusy, uczestnicy) oraz test współbieżności
  (osiem wątków, wygrywa dokładnie jedna rezerwacja).
- `requirements-dev.txt` (pytest, pytest-django, ruff) i `pytest.ini`.
- Komentarze w języku angielskim w modelach, panelu admina, testach i konfiguracji.

### Changed
- Test współbieżności akceptuje oba kody odrzucenia z PostgreSQL: naruszenie ograniczenia
  wykluczającego (`23P01`) i deadlock (`40P01`).

### Removed
- Puste szablony `tests.py` w aplikacjach `buildings` i `bookings`.

## 2026-11-04

### Added
- Model `Booking` (aplikacja `bookings`): sala, organizator, tytuł, przedział czasu (`DateTimeRangeField`),
  liczba uczestników, status.
- `ExclusionConstraint` w bazie: brak nakładających się aktywnych rezerwacji tej samej sali;
  migracja włącza rozszerzenie `btree_gist`.
- Panel admina rezerwacji z kalendarzem (`datetime-local`) i domyślnym terminem
  (najbliższa pełna godzina + 1 godzina).
- Aplikacja `buildings`: modele `Floor` i `Room` z ograniczeniami w bazie
  (unikalny numer piętra, unikalna nazwa sali na piętrze, pojemność > 0), migracja `0001`, panel admina.
- Konfiguracja Ruff (`backend/ruff.toml`).
- PostgreSQL 18 w Docker Compose (wolumin, healthcheck `pg_isready`).
- `django.contrib.postgres` i `rest_framework` w `INSTALLED_APPS`.
- README i CHANGELOG.

### Changed
- Baza danych Django przełączona z SQLite na PostgreSQL.
- Ustawienia: język `pl`, strefa czasowa `Europe/Warsaw`, `USE_TZ=True`.
- `settings.py` przeformatowany przez Ruff (cudzysłowy).

### Fixed
- README w repozytorium był pusty po poprzednim commicie; uzupełniony.

## 2026-11-03

### Added
- Szkielet projektu Django (`config`), Django 6.1, DRF 3.18, psycopg 3.

### Removed
- Plik `db.sqlite3` usunięty z repozytorium (dodany do `.gitignore`).