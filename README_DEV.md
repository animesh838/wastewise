Local Development
=================

Quick start for running the project locally with a separate dev environment.

1) Create dev env file

Create env/.env.dev with:

```
DEBUG=true
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=

# Optional: Django logging level
DJANGO_LOG_LEVEL=DEBUG
```

2) Run with helper script

```
bash scripts/dev.sh
```

This will:
- export variables from env/.env.dev
- apply migrations
- run the dev server on http://127.0.0.1:8000

3) Static & media

- Static is served by Django automatically in DEBUG mode
- Uploads go to ./media

4) Tips

- To override DB locally, set `DATABASE_URL=postgres://...` in env/.env.dev
- To stop the server, press Ctrl+C
