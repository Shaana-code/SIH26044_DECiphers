# 🎓 SIH26044 — DECiphers
### Portal for Academia–Industry Collaboration: Skill Mapping, Internships & Placement

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Shaana-code/SIH26044_DECiphers)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_Portal-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://sih26044deciphers-s2rrcxaomrlzm8wzbuemap.streamlit.app/#fast-api-python-advanced)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

### 🌐 Quick Links
- 🔗 **GitHub Public Repository:** [https://github.com/Shaana-code/SIH26044_DECiphers](https://github.com/Shaana-code/SIH26044_DECiphers)
- 🚀 **Live Streamlit Portal:** [https://sih26044deciphers-s2rrcxaomrlzm8wzbuemap.streamlit.app/#fast-api-python-advanced](https://sih26044deciphers-s2rrcxaomrlzm8wzbuemap.streamlit.app/#fast-api-python-advanced)

---

## 📌 Project Overview

**Problem Statement ID:** SIH26044  
**Title:** *Portal for Academia - Industry collaboration for Skill Mapping, Internships and Placement*  
**Team Name:** DECiphers  

The gap between academic curriculum standards and rapidly evolving industry demands is one of the primary hurdles students face when transitioning into professional careers. **DECiphers** solves this challenge by providing an intelligent, collaborative platform uniting **Students**, **Academic Institutions**, and **Industry Employers**.

The platform leverages data-driven skill mapping, semantic matchmaking algorithms, and interactive dashboards to enable students to identify skill gaps, provide institutions with curriculum alignment insights, and offer recruiters a pipeline of qualified talent for internships and placements.

---

## ✨ Key Features

- 🎯 **Automated Skill Mapping & Gap Analysis:** Identifies discrepancies between institutional course modules and industry job descriptions using NLP and taxonomy matching.
- 💼 **Smart Internship & Placement Matching:** Matches students with optimal opportunities based on verified proficiencies, projects, and career preferences.
- 🏢 **Multi-Stakeholder Portals:**
  - **Students:** Build profiles, take skill assessments, visualize gap roadmaps, and apply for openings.
  - **Academia / Faculty:** Monitor batch-wise performance metrics, track placement stats, and optimize curriculums.
  - **Industry / Recruiters:** Post vacancies, filter verified candidates based on technical proficiencies, and conduct interview drives.
- ⚡ **High-Performance FastAPI Backend:** Asynchronous RESTful APIs with Pydantic validation for fast data exchange and model serving.
- 📊 **Streamlit Interactive UI:** Responsive dashboard featuring dynamic data visualizations, real-time analytics, and status updates.

---

## 🏗 System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Streamlit Interactive UI                 │
│      (Student / Academia / Recruiter Dashboards)       │
└───────────────────────────▲────────────────────────────┘
                            │ REST API / HTTP
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│  ├── Authentication & RBAC (Role-Based Access Control) │
│  ├── Skill Extraction & Semantic Gap Analysis Engine   │
│  ├── Matchmaking & Recommendation Engine               │
│  └── Internship & Placement Management                 │
└───────────────────────────▲────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                  Data & Storage Layer                  │
│       (Relational Database / Skill Knowledge Graphs)   │
└────────────────────────────────────────────────────────┘

## 📂 Basic Project Directory Structure

```text
SIH26044_DECiphers/
├── .devcontainer/
│   └── devcontainer.json      # VS Code / Codespaces container development configuration
├── .env.example               # Environment variables template
├── .gitignore                 # Files and folders to ignore in Git version control
├── main1.py                   # FastAPI backend server application & API endpoints
├── portal.db                  # SQLite database file for application data & records
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies and packages
├── seed_db.py                 # Database initialization and sample data seeding script
└── streamlit_app.py           # Streamlit frontend user interface & dashboard


