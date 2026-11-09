# SponsorTrack

An API for international students to find software engineering jobs that are likely to offer visa sponsorship.

## The Problem
International students waste hours applying to jobs, only to find out in the interview that the company does not sponsor visas. Job boards do not have a reliable filter for this.

## The Solution
SponsorTrack ingests job postings from the Adzuna API, scans the descriptions for positive and negative sponsorship signals, and assigns a confidence score (LIKELY, UNKNOWN, UNLIKELY) to each job.

## Tech Stack
- **Python 3.12+**
- **FastAPI** (API framework)
- **PostgreSQL** (Database)
- **SQLAlchemy + Alembic** (ORM and Migrations)
- **Docker Compose** (Local development environment)

## How to Run

1. Clone the repo and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt