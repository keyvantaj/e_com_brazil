# Brazilian E-Commerce Public Dataset by Olist

# Data Stack Project

Stack used containerized with Docker: PostgreSQL + Airflow + Dbt + Python.

## 🚀 Launch The Project

```bash
docker-compose up --build
```

## 📂 Composants

- **PostgreSQL** – base de données analytique
- **Airflow** – orchestration
- **Dbt** – tranformation
- **Python** – scripts Ingestion
- **data/** – fichiers sources CSV

## ⚙️ GitHub Actions

tested with `.github/workflows/ci.yml`:
- PostgreSQL connectivity
- Python script execution
- Dbt models execution
