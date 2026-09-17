# SPECTR: Secure Point-of-care Enrollment and Centralized Trial Randomization

A lightweight, GCP-compliant central allocation engine for multicenter clinical trials. SPECTR provides central randomization and allocation concealment for investigator-initiated and multicentric randomized controlled trials.

Built with **FastAPI** (backend) and **React + Vite** (frontend).

## Overview

SPECTR eliminates the need for cumbersome physical envelopes and cost-prohibitive enterprise IWRS/RTSM software, delivering instant, tamper-proof treatment allocations directly to site investigators.

Designed by trial methodologists, it supports:

- **Methodological flexibility** — Import pre-computed stratified block sequences from R, Stata, or SAS, or generate sequences in-app with simple/block randomization and stratification.
- **Point-of-care allocation** — Site investigators use a fast interface to confirm eligibility, randomize participants, and receive immediate treatment assignments.
- **Audit trails** — Every allocation is logged with participant IDs, stratum tags, and UTC timestamps. Central trial coordinators and site investigators can review and export history in real time.
- **GCP integrity** — Allocation concealment, database-level concurrency locks, and role-based access control across participating centers.

## User roles

| Role | Purpose |
|------|---------|
| **Admin** | First-run setup; create and manage central trial coordinator accounts |
| **Central Trial Coordinator** | Create studies, configure arms and randomization, onboard site investigators |
| **Site Investigator** | Randomize eligible participants at the point of care |

## How to use

### 1. Initial setup (Admin)

1. Deploy SPECTR and open the home page (`/`).
2. On first run, complete **First-Run Setup** with the server `SETUP_TOKEN` and create the admin account (password minimum 12 characters).
3. Log in at `/admin`.
4. Create central trial coordinator accounts.

### 2. Configure a study (Central Trial Coordinator)

1. Log in at `/organizer/login`.
2. Create a new study with protocol metadata, blinding type, and inclusion/exclusion criteria.
3. Define **treatment arms** and allocation ratios at `/organizer/studies/{id}/arms`.
4. Set up randomization using one of:
   - **CSV import** — Upload a pre-computed sequence at `/organizer/studies/{id}/upload-csv` (see `backend/sample_randomization.csv` for format).
5. Add **sites** and **site investigators** per site. Credentials (Trial ID, username, temporary password) are emailed automatically when SMTP is configured; otherwise they appear in backend logs during development.
6. Activate the study when configuration is complete.

### 3. Randomize participants (Site Investigator)

1. Log in at `/investigator/login` with **Trial ID** (study protocol code), **username**, and **password** from the credential email.
2. Change the temporary password if prompted.
3. On the site investigator home page:
   - Confirm inclusion/exclusion criteria when configured.
   - Enter or confirm the participant ID.
   - Select the appropriate stratum (if stratified).
   - Submit to receive the next sequential allocation from the concealed sequence.
4. Export allocation history from the dashboard when needed.

### 4. Monitor and export (Central Trial Coordinator)

From the study home page (`/organizer/studies/{id}/home`), central trial coordinators can:

- Review all randomization records and assignment status.
- Filter by site, stratum, or assignment state.
- Export allocation logs for monitoring and audit.

## Host it yourself

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Option A: Local development

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set DATABASE_URL, SECRET_KEY, FRONTEND_URL, etc.
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: `http://localhost:8000`  
API docs (development only): `http://localhost:8000/docs`

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: `http://localhost:5173`

### Option B: Docker (single container)

The included `Dockerfile` builds the React frontend and serves it from the FastAPI backend. PostgreSQL is external.

```bash
# Build
docker build -t spectr .

# Run (PostgreSQL must already be reachable)
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/spectr \
  -e SECRET_KEY=your-secret-key \
  -e SETUP_TOKEN=your-setup-token \
  -e ENVIRONMENT=production \
  -e FRONTEND_URL=https://your-domain.example \
  -e CORS_ORIGINS=https://your-domain.example \
  spectr
```

The container entrypoint runs Alembic migrations automatically before starting Uvicorn. For same-origin deployment, leave `VITE_API_URL` empty at build time so the frontend uses relative API paths.

### Production configuration

Copy `backend/.env.example` to `backend/.env` and set:

| Variable | Required | Description |
|----------|----------|-------------|
| `ENVIRONMENT` | Yes | Set to `production` |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes | Strong random key for JWT signing |
| `SETUP_TOKEN` | Yes | Protects first-run admin setup |
| `FRONTEND_URL` | Yes | Public URL used in site investigator credential emails |
| `CORS_ORIGINS` | Yes | Comma-separated allowed frontend origins |
| `SMTP_*` or `RESEND_API_KEY` | Yes | Email delivery for site investigator credentials |

For cross-domain HTTPS deployments, also set `COOKIE_SECURE=true` and `COOKIE_SAMESITE=none`.

Without SMTP in development, site investigator credentials are written to the backend console instead of being emailed.

### Deploying to Railway

The repository includes a `railway.toml` and `Dockerfile` for Railway. Add a PostgreSQL plugin, set the environment variables above, and deploy. The health check endpoint is `/health`.

## Project structure

```
.
├── backend/          # FastAPI + SQLAlchemy + Alembic
├── frontend/         # React SPA
├── Dockerfile        # Combined frontend + backend image
├── docker-entrypoint.sh
└── docs/
    └── ENGINEERING.md
```

## Documentation

For architecture, API reference, authentication, database schema, and troubleshooting, see **[docs/ENGINEERING.md](docs/ENGINEERING.md)**.

## Citation

When reporting methodology in trial protocols, ethics submissions, or peer-reviewed publications, please cite:

> Pradeep M, Kumar D. SPECTR: Secure Point-of-care Enrollment and Centralized Trial Randomization [Computer software]. Available from: https://mmmr.in/services/spectr

## Developed and maintained by

Dr. Manu Pradeep and Dhanush Kumar

A free open-source tool by MM Medical Research (OPC) Pvt. Ltd., Cherthala, Kerala, India.

- Source: https://github.com/dhanush-kuma/SPECTR
- Inquiries: mmedicalresearch@outlook.in

## License

SPECTR: Secure Point-of-care Enrollment and Centralized Trial Randomization  
Copyright (C) 2026 Manakkodam Manu Medical Research (OPC) Pvt. Ltd.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
