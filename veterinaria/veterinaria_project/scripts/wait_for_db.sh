set -e

host="$1"
shift
port="$1"
shift

if [ -z "$host" ]; then
    host=$POSTGRES_HOST
fi

if [ -z "$port" ]; then
    port=$POSTGRES_PORT
fi

until nc -z "$host" "$port"; do
  echo "Waiting for PostgreSQL at $host:$port..."
  sleep 1
done

echo "PostgreSQL started"

exec "$@"