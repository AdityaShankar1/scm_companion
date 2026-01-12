# SCM Companion: AI-Driven Supply Chain & Logistics Optimizer
SCM Companion is a full-stack supply chain management platform deployed on Google Cloud Platform (GCP). It leverages geospatial intelligence and machine learning to optimize inventory and logistics, providing a real-time dashboard for asset tracking and market forecasting.

## Problem Statement & Proposed Solution:
Fragmented data causes inefficient logistics management, failing to anticipate market fluctuations.
This is a GCP-hosted platform integrating FastAPI, PostGIS, and PyTorch models within a containerized Docker architecture, enabling proactive decision-making via automated forecasting and optimized routing to reduce transit costs and stockouts.

## 🚀 Features

Cloud-Native Deployment: Professionally hosted on GCP Compute Engine using a custom-configured VPC and firewall.

Geospatial Logistics: Uses PostGIS to calculate optimal routes between distribution hubs and railheads.

ML Forecasting: Integrated PyTorch and HuggingFace Transformers to predict product price trends and demand.

Production-Ready Stack: High-performance FastAPI backend served via Nginx and containerized with Docker.

## 🛠 Tech Stack

Cloud Infrastructure: Google Cloud Platform (GCP)

Backend: FastAPI (Python 3.11)

Database: PostgreSQL with PostGIS extension

Machine Learning: PyTorch, Transformers

DevOps: Docker, Docker Compose, Nginx

Deployment: GCP Compute Engine (Ubuntu Instance)

## 🏗 Cloud Architecture

The application is hosted on a GCP Compute Engine instance running Ubuntu. The architecture follows modern DevOps practices:

Nginx Reverse Proxy: Handles incoming traffic on Port 80.

Dockerized Services: Isolates the Web API and the PostGIS database.

Persistence: Managed via Docker Volumes for reliable data storage.

## 📦 Installation & Deployment

1. GCP Environment Setup

Instance: Compute Engine (e.g., e2-medium or higher)

Allowed Firewall Ports: TCP: 80 (HTTP), 443 (HTTPS), 5432 (Postgres)

2. Launching the Project

Bash
```
git clone https://github.com/AdityaShankar1/scm_companion.git
cd scm_companion
sudo docker-compose up -d --build
```
3. Database Initialization
Bash
```
sudo docker-compose exec web python scripts/init_db.py
```

## 🔌 API Documentation
The production API is accessible via:

Swagger UI: http://34.100.228.234//docs

## Screenshots:

### Login:
<img width="1470" height="956" alt="Screenshot 2026-01-13 at 12 52 53 AM" src="https://github.com/user-attachments/assets/dbbd1531-4a50-4db6-b446-649b22b6fd80" />

### Main Page:
<img width="1470" height="956" alt="Screenshot 2026-01-13 at 12 46 00 AM" src="https://github.com/user-attachments/assets/1ffa2a37-33b7-4a10-a846-8f7e6d474149" />

