#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/env/.env.dev"
PYTHON="python3"

# Prefer project virtualenv if available
if [ -x "$ROOT_DIR/waste_management_env/bin/python" ]; then
  PYTHON="$ROOT_DIR/waste_management_env/bin/python"
fi

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

echo "Ensuring dependencies are installed..."
if ! "$PYTHON" -c "import whitenoise" >/dev/null 2>&1; then
  "$PYTHON" -m pip install -r requirements.txt
fi

echo "Applying migrations..."
"$PYTHON" manage.py migrate

echo "Starting server at http://127.0.0.1:8000"
"$PYTHON" manage.py runserver 127.0.0.1:8000

