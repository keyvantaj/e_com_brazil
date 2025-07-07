# Data Stack Project

Un stack analytique local basé sur Docker : PostgreSQL + dbt + Airflow + Python.

## 🚀 Lancer le projet

```bash
docker-compose up --build
```

## 📂 Composants

- **PostgreSQL** – base de données analytique
- **dbt** – transformation des données
- **Airflow** – orchestration
- **Python** – scripts ETL
- **data/** – fichiers sources CSV ou JSON

## ⚙️ GitHub Actions

Le fichier `.github/workflows/ci.yml` teste :
- la connectivité avec PostgreSQL
- l'exécution du script Python
- la compilation du projet dbt
