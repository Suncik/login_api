# Bookstore — Login API

JWT autentifikatsiyali Login va Current User API (Django, Django REST Framework, PostgreSQL, Simple JWT).

## Endpointlar

- `POST /api/auth/login/` access va refresh token qaytaradi
- `GET /api/auth/me/` joriy foydalanuvchi, faqat token bilan

## Struktura

- `config/settings/base.py`, `dev.py`, `prod.py`: DRF, Simple JWT, PostgreSQL, JWT sozlamalari
- `config/urls.py`: `api/auth/` yo'li
- `core/exceptions.py`: `InvalidCredentials` (401)
- `apps/users/`: models, selectors, services, serializers, views, urls, admin
- `apps/users/tests/`: factories, service va view testlari
- `pytest.ini`, `requirements.txt`

## Ishga tushirish

1. `python -m venv .venv`, muhitni yoqish
2. `pip install -r requirements.txt`
3. PostgreSQL da `bookstore` bazasini yaratish
4. `python manage.py migrate`
5. `python manage.py runserver`
6. `pytest`

## API test natijalari

| Holat | Status |
|---|---|
| To'g'ri login va parol | 200 |
| Noto'g'ri parol | 401 |
| Mavjud bo'lmagan username | 401 |
| Bo'sh ma'lumotlar | 400 |
| Tokensiz `/api/auth/me/` | 401 |
| To'g'ri token bilan `/api/auth/me/` | 200 |