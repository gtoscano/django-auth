# django-auth

This repository is a **classroom demo** for CUA’s 406/506 Introduction to Secure Computing. The goal is to show that:
- Rolling your own login flow is risky.
- Default framework protections help, but still benefit from hardening.
- A simple dictionary attack can succeed against weak passwords.
- Tools like **django-axes** add guardrails (rate limiting / lockout) that help reduce risk.

This is for **educational use only** on systems you own or have permission to test. Do not run the attack scripts against real or unauthorized targets.

---

## What this demo contains

- A **custom login** endpoint (`/login/`) that is intentionally weak for teaching purposes.
- A **Django built-in login** endpoint (`/login_django/`) that uses standard protections.
- Two brute-force scripts in `scripts/` that try to crack a weak password using a dictionary.
- An optional **django-axes** configuration to show how lockouts stop attacks.

---

## Prerequisites

- Docker + Docker Compose
- A local copy of `rockyou.txt` (dictionary list)

Place `rockyou.txt` in `scripts/`:
```
scripts/rockyou.txt
```

---

## Quick start (no Axes yet)

1. Start the containers:
```
docker compose up -d
```

2. Create the database schema:
```
docker compose exec -it web bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser with a **weak password** (so the demo can succeed):
```
python manage.py createsuperuser
```

Example (use something like `superman` on purpose for the demo):
```
Username: admin
Email address: your_email@example.com
Password: superman
Password (again): superman
```
If Django warns that the password is too common, choose `y` to proceed.

4. Verify the dictionary file is present:
```
ls scripts/
```

---

## Run the attacks

From inside the container:

1. Attack the **custom login** (`/login/`):
```
python scripts/bruteforce.py
```
This attempts logins against `http://localhost:8000/login/` using `rockyou.txt`.

2. Attack the **Django built-in login** (`/login_django/`):
```
python scripts/bruteforce-django.py
```
This script handles CSRF and can still crack the password **if it exists in the dictionary**.

---

## Enable django-axes (lockout protection)

Axes adds lockouts after repeated failed logins. For this demo, you’ll enable it manually.

1. Edit `main/settings.py` and **uncomment** the following:

- `INSTALLED_APPS`:
```
'axes',
```

- `MIDDLEWARE`:
```
'axes.middleware.AxesMiddleware',
```

- Axes settings (near the bottom of the file):
```
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_LOCKOUT_TEMPLATE = "axes/lockout.html"
```

2. Rebuild the database:
```
docker compose down
docker compose up -d
docker compose exec -it web bash
python manage.py makemigrations
python manage.py migrate
```

3. Re-run the brute-force scripts and observe that Axes blocks repeated attempts.

Tip: run `docker compose up` (without `-d`) if you want to see lockout logs live. In detached mode, use `docker compose logs`.

---

## Key takeaways (what students should learn)

- Do **not** build your own authentication unless absolutely necessary.
- Use framework-provided auth (Django’s built-in login).
- Strengthen authentication with defenses like **rate limiting, lockout, and MFA**.
- Weak passwords are easy to crack with public dictionaries.

---

## Lab checklist (student verification)

Use this as a quick completion guide.

1. Environment
- Docker containers are running (`docker compose ps`).
- `rockyou.txt` is present at `scripts/rockyou.txt`.

2. Account setup
- A superuser exists (e.g., `admin`).
- The password is intentionally weak for the demo.

3. Attacks
- `bruteforce.py` succeeds against `/login/`.
- `bruteforce-django.py` succeeds against `/login_django/`.

4. Hardening
- Axes is enabled in `main/settings.py`.
- After enabling Axes, repeated login attempts are locked out.

5. Reflection (short answers)
- Why is a custom login flow riskier than Django’s built-in one?
- How did CSRF affect the first script?
- What did Axes change about the attack outcome?

---

## Troubleshooting

- If the site doesn’t load, confirm the container is running:
```
docker compose ps
```
- If scripts can’t find `rockyou.txt`, confirm it’s in `scripts/`.
- If you get CSRF errors in the Django login brute-force, use `bruteforce-django.py`.

