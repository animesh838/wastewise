#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/env/.env.dev"

if [ ! -f "$ENV_FILE" ]; then
  echo "env/.env.dev not found. Creating a template..."
  mkdir -p "$ROOT_DIR/env"
  cat > "$ENV_FILE" <<'EOF'
DEBUG=true
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
DJANGO_LOG_LEVEL=DEBUG
EOF
  echo "Template written to $ENV_FILE. Edit as needed."
fi

echo "Loading $ENV_FILE"
set -a
source "$ENV_FILE"
set +a

cd "$ROOT_DIR"

echo "Applying migrations..."
python manage.py migrate

echo "Starting server at http://127.0.0.1:8000"
python manage.py runserver 127.0.0.1:8000

