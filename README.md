# RoomBook

Backend systemu rezerwacji sal konferencyjnych w biurowcu (Python, Django, PostgreSQL).
Projekt portfolio, w trakcie budowy.

**Cel:** zagwarantować, że żadna sala nie zostanie zarezerwowana dwa razy, nawet
przy równoległych żądaniach. Egzekwuje to sama baza danych (ograniczenie wykluczające
PostgreSQL), a nie kod aplikacji.

## Status

Projekt jest na wczesnym etapie. Działa szkielet aplikacji, baza danych, model budynku
(piętra i sale) oraz model rezerwacji z ograniczeniem przeciw nakładaniu się terminów.
Brakuje jeszcze testów automatycznych i API.

- [x] Szkielet Django + Django REST Framework
- [x] PostgreSQL uruchamiany w Dockerze, Django skonfigurowane do pracy z nim
- [x] Model budynku: piętra i sale (ograniczenia unikalności i pojemności w bazie), panel admina
- [x] Model rezerwacji z `ExclusionConstraint` + `btree_gist`, panel admina z wyborem daty i godziny
- [ ] Testy (pytest), w tym test współbieżności
- [ ] API REST: sale, wyszukiwarka dostępności, rezerwacje
- [ ] JWT i role użytkowników
- [ ] Docker Compose dla całej aplikacji
- [ ] CI (GitHub Actions)
- [ ] Celery + Redis (wygasanie blokad, no-show)
- [ ] Symulator urządzeń (Flask, webhooki HMAC)
- [ ] Wdrożenie online

## Stack

| Warstwa | Technologia |
|---|---|
| Język | Python 3.13 |
| Framework | Django 6.1, Django REST Framework 3.18 |
| Baza danych | PostgreSQL 18 (Docker) |
| Sterownik bazy | psycopg 3 |
| Linter i formater | Ruff |
| Środowisko | Docker Compose, venv |

## Dlaczego PostgreSQL

Zakaz nakładania się rezerwacji tej samej sali realizuję przez `ExclusionConstraint`
(typ zakresu czasu + operator nakładania), który istnieje tylko w PostgreSQL.
Dzięki temu poprawność nie zależy od tego, że kod aplikacji "zdąży sprawdzić"
przed zapisem. Walidacja w Django daje czytelny komunikat, a gwarancję zapewnia baza.

## Model danych (stan obecny)

- `Floor` — piętro (unikalny numer, opcjonalna nazwa).
- `Room` — sala przypisana do piętra: pojemność, wyposażenie (projektor, tablica,
  wideokonferencja), flaga aktywności.
- `Booking` — rezerwacja sali: organizator, tytuł, przedział czasu (`tstzrange`),
  liczba uczestników, status (oczekująca, potwierdzona, anulowana, zakończona, nieodebrana).

Reguły egzekwowane przez bazę: unikalny numer piętra, unikalna nazwa sali w obrębie
piętra, pojemność większa od zera, liczba uczestników większa od zera, zakaz usunięcia
piętra z salami i sali z rezerwacjami, **brak nakładających się aktywnych rezerwacji tej
samej sali** (przedziały półotwarte: rezerwacje stykające się o pełnej godzinie nie kolidują;
anulowane rezerwacje nie blokują sali).

**Świadome uproszczenia:** model zakłada jeden budynek (hierarchia piętro → sala),
jedna rezerwacja dotyczy jednej sali, a bufor po spotkaniu i sale łączone dojdą w kolejnych etapach.

## Uruchomienie lokalne (Windows, PowerShell)

Wymagania: Python 3.13, Docker Desktop, Git.

```powershell
# 1. Baza danych
docker compose up -d

# 2. Środowisko Python
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

# 3. Migracje i serwer
cd backend
python manage.py migrate
python manage.py runserver
```

Panel administracyjny: http://127.0.0.1:8000/admin/ (konto utworzysz poleceniem
`python manage.py createsuperuser`).

Domyślne dane bazy w `docker-compose.yml` (`roombook` / `roombook`) służą wyłącznie
do pracy lokalnej.

## Struktura repozytorium

```
roombook/
├── docker-compose.yml     # PostgreSQL
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── ruff.toml          # konfiguracja lintera
│   ├── config/            # ustawienia projektu Django
│   ├── buildings/         # piętra i sale (modele, migracje, admin)
│   └── bookings/          # rezerwacje (model, migracje, admin)
├── README.md
└── CHANGELOG.md
```

## Plan prac

1. Testy rdzenia: nakładanie rezerwacji, rezerwacje kolejne, anulowane nie blokują, współbieżność
2. API sal i wyszukiwarka dostępności
3. Rezerwacje przez API (idempotentność, kod 409 przy konflikcie)
4. JWT, role, CI
5. Celery, symulator urządzeń, wdrożenie

Zmiany: zob. [CHANGELOG.md](CHANGELOG.md).