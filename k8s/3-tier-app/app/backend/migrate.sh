#!/bin/bash

set -euo pipefail

export FLASK_APP="${FLASK_APP:-run.py}"

MIGRATION_ACTION="${MIGRATION_ACTION:-upgrade}"
MIGRATION_TARGET="${MIGRATION_TARGET:-head}"

revision_id() {
    echo "$1" | grep -oE '[a-f0-9]{12}' | head -1
}

current_revision() {
    revision_id "$(flask db current 2>/dev/null || true)"
}

head_revision() {
    revision_id "$(flask db heads 2>/dev/null || true)"
}

require_migrations() {
    if [ ! -d "migrations" ] || [ ! -d "migrations/versions" ]; then
        echo "ERROR: migrations directory not found. Run 'flask db init' locally and commit migration files."
        exit 1
    fi
    if [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
        echo "ERROR: no migration files in migrations/versions. Create migrations locally and commit them."
        exit 1
    fi
}

run_upgrade() {
    local target="${1:-head}"
    echo "Upgrading database to: ${target}"
    if ! flask db upgrade "${target}"; then
        echo "ERROR: flask db upgrade ${target} failed"
        exit 1
    fi

    local current head
    current="$(current_revision)"
    head="$(head_revision)"

    if [ "${target}" = "head" ]; then
        echo "Migration status: current=${current:-<none>}, head=${head:-<none>}"
        if [ -z "${current}" ] || [ -z "${head}" ] || [ "${current}" != "${head}" ]; then
            echo "ERROR: database is not at the latest migration revision"
            exit 1
        fi
    else
        echo "Migration status: current=${current:-<none>}, target=${target}"
        local expected
        expected="$(revision_id "${target}")"
        if [ -z "${current}" ] || [ -z "${expected}" ] || [ "${current}" != "${expected}" ]; then
            echo "ERROR: database revision (${current:-<none>}) does not match upgrade target (${expected})"
            exit 1
        fi
    fi
}

run_downgrade() {
    local target="$1"
    if [ -z "${target}" ] || [ "${target}" = "head" ]; then
        echo "ERROR: MIGRATION_TARGET must be a specific revision id for downgrade (e.g. a05e32811b08)"
        exit 1
    fi
    echo "Downgrading database to: ${target}"
    if ! flask db downgrade "${target}"; then
        echo "ERROR: flask db downgrade ${target} failed"
        exit 1
    fi

    local current expected
    current="$(current_revision)"
    expected="$(revision_id "${target}")"
    echo "Migration status: current=${current:-<none>}, target=${expected}"
    if [ -z "${current}" ] || [ -z "${expected}" ] || [ "${current}" != "${expected}" ]; then
        echo "ERROR: database revision (${current:-<none>}) does not match downgrade target (${expected})"
        exit 1
    fi
}

run_stamp() {
    local target="$1"
    if [ -z "${target}" ]; then
        echo "ERROR: MIGRATION_TARGET is required for stamp"
        exit 1
    fi
    echo "Stamping database at revision: ${target}"
    if ! flask db stamp "${target}"; then
        echo "ERROR: flask db stamp ${target} failed"
        exit 1
    fi
}

run_current() {
    echo "Current database revision:"
    flask db current
}

maybe_seed() {
    if [ -z "${DB_HOST:-}" ] || [ -z "${DB_USERNAME:-}" ] || [ -z "${DB_PASSWORD:-}" ] || [ -z "${DB_NAME:-}" ]; then
        echo "Skipping seed check: DB connection env vars not set"
        return 0
    fi

    echo "Checking if seed data is needed..."
    local port="${DB_PORT:-5432}"
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$port" -U "$DB_USERNAME" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM topics" 2>/dev/null | grep -q "0"; then
        echo "Running seed data..."
        python seed_data.py
    else
        echo "Database already contains data, skipping seed"
    fi
}

echo "Running database migrations (action=${MIGRATION_ACTION}, target=${MIGRATION_TARGET})..."
require_migrations

case "${MIGRATION_ACTION}" in
    upgrade)
        run_upgrade "${MIGRATION_TARGET}"
        maybe_seed
        ;;
    downgrade)
        run_downgrade "${MIGRATION_TARGET}"
        ;;
    stamp)
        run_stamp "${MIGRATION_TARGET}"
        ;;
    current)
        run_current
        ;;
    *)
        echo "ERROR: unknown MIGRATION_ACTION '${MIGRATION_ACTION}'. Use upgrade, downgrade, stamp, or current."
        exit 1
        ;;
esac

echo "Database migration completed successfully!"
