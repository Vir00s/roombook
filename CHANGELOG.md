# Changelog

Format wzorowany na [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- PostgreSQL 18 w Docker Compose (wolumin, healthcheck `pg_isready`).
- `django.contrib.postgres` i `rest_framework` w `INSTALLED_APPS`.
- README i CHANGELOG.

### Changed
- Baza danych Django przełączona z SQLite na PostgreSQL.
- Ustawienia: język `pl`, strefa czasowa `Europe/Warsaw`, `USE_TZ=True`.

### Removed
- Plik `db.sqlite3` usunięty z repozytorium (dodany do `.gitignore`).

## 2026-11-03

### Added
- Szkielet projektu Django (`config`), Django 6.1, DRF 3.18, psycopg 3.