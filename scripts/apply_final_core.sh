#!/bin/sh
set -e

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TS="$(date +%F_%H%M%S)"

backup_file() {
  if [ -f "$1" ]; then
    cp -a "$1" "$1.before_final_core_$TS"
  fi
}

echo "== C2-TA | Aplicando troca final do núcleo =="

backup_file "$ROOT_DIR/config/urls.py"
backup_file "$ROOT_DIR/triagem/admin.py"

cp -f "$ROOT_DIR/config/urls_portainer_ready.py" "$ROOT_DIR/config/urls.py"
cp -f "$ROOT_DIR/triagem/admin_consolidated.py" "$ROOT_DIR/triagem/admin.py"

chmod 644 "$ROOT_DIR/config/urls.py" "$ROOT_DIR/triagem/admin.py"

echo "== Arquivos aplicados =="
echo "- config/urls.py"
echo "- triagem/admin.py"

echo "== Próximos comandos sugeridos =="
echo "python manage.py makemigrations"
echo "python manage.py migrate"
echo "python manage.py bootstrap_c2ta"
echo "python manage.py check_external_base"
