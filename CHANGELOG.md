# Changelog

Format wzorowany na [Keep a Changelog](https://keepachangelog.com/).

## 2026-11-04

### Added
- Aplikacja `buildings`: modele `Floor` i `Room` z ograniczeniami w bazie
  (unikalny numer piętra, unikalna nazwa sali na piętrze, pojemność > 0), migracja `0001`, panel admina.
- Pusta aplikacja `bookings` (przygotowanie pod model rezerwacji).
- Konfiguracja Ruff (`backend/ruff.toml`).
- PostgreSQL 18 w Docker Compose (wolumin, healthcheck `pg_isready`).
- `django.contrib.postgres` i `rest_framework` w `INSTALLED_APPS`.
- README i CHANGELOG.

### Changed
- Baza danych Django przełączona z SQLite na PostgreSQL.
- Ustawienia: język `pl`, strefa czasowa `Europe/Warsaw`, `USE_TZ=True`.

### Fixed
- README w repozytorium był pusty po poprzednim commicie; uzupełniony.

## 2026-11-03

### Added
- Szkielet projektu Django (`config`), Django 6.1, DRF 3.18, psycopg 3.

### Removed
- Plik `db.sqlite3` usunięty z repozytorium (dodany do `.gitignore`).