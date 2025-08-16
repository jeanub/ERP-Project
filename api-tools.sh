API=http://localhost:8000/api

login() { 
  local u="${1:-jean}" p="${2:-jean123k}"
  TOKENS=$(curl -s -X POST "$API/auth/token/" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"$u\",\"password\":\"$p\"}")
  ACCESS=$(echo "$TOKENS"  | jq -r .access)
  REFRESH=$(echo "$TOKENS" | jq -r .refresh)
  export ACCESS REFRESH
  echo "ACCESS y REFRESH listos"
}

refresh() {
  [ -z "$REFRESH" ] && { echo "No hay REFRESH. Ejecuta login primero."; return 1; }
  ACCESS=$(curl -s -X POST "$API/auth/refresh/" \
    -H 'Content-Type: application/json' \
    -d "{\"refresh\":\"$REFRESH\"}" | jq -r .access)
  export ACCESS
  echo "ACCESS renovado"
}

authcurl() { 
  curl -s -H "Authorization: Bearer $ACCESS" "$@"
}
