# Brazilian E-Commerce Public Dataset by Olist

# Data Stack Project

Un stack analytique local basé sur Docker : PostgreSQL + Airflow + Python.

## 🚀 Lancer le projet

```bash
docker-compose up --build
```

## 📂 Composants

- **PostgreSQL** – base de données analytique
- **Airflow** – orchestration & dbt
- **Python** – scripts Ingestion
- **data/** – fichiers sources CSV

## ⚙️ GitHub Actions

Le fichier `.github/workflows/ci.yml` teste :
- la connectivité avec PostgreSQL
- l'exécution du script Python
- l'exécution des modèles dbt
