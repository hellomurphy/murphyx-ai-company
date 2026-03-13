# Pet Grooming SaaS — flagship demo

Example SaaS product built on the MurphyX framework. Demonstrates the output shape a `build_saas` workflow produces.

## Structure

- `apps/web/` — Nuxt 3 frontend (placeholder shell)
- `packages/api/` — FastAPI backend with appointments CRUD (in-memory store)
- `docker-compose.yml` — local stack for the demo

## Running locally

```bash
cd apps/pet-grooming-saas
docker compose up
# API available at http://localhost:8001
# Health: GET http://localhost:8001/health
# Appointments: POST/GET http://localhost:8001/api/v1/appointments
```

## Note

This is a demo scaffold, not a production application. The API uses an in-memory store — data resets on restart. Connect a real database via environment variables for production use.
