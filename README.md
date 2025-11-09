# ☀️ Solar Data Analysis Challenge (Week 0)

## 🌍 Project Overview
This project is part of the **10 Academy Artificial Intelligence Mastery Program (Week 0 Challenge)**.  
The goal is to perform a **comprehensive data analysis** of solar farm environmental data from three different countries — **Benin**, **Sierra Leone**, and **Togo** — to identify the highest-potential region for a new solar energy investment.

### 🔍 The analysis involves:
- **Data Cleaning & Quality Assurance:** Handling missing values, correcting sensor errors (e.g., negative irradiance), and standardizing formats.  
- **Exploratory Data Analysis (EDA):** Exploring region-specific trends in solar irradiance, wind patterns, temperature, and soiling.  
- **Statistical Comparison:** Applying the **Kruskal-Wallis test** to evaluate differences in solar potential across regions.  
- **Strategic Recommendations:** Translating insights into actionable business strategies for **MoonLight Energy Solutions**.

---

## 📊 Key Findings & Recommendations

### 🌞 Highest Solar Potential: **Benin**
- Benin demonstrated the **highest mean and median** values for both **Global Horizontal Irradiance (GHI)** and **Direct Normal Irradiance (DNI)**.
- Statistical testing confirmed that the differences in solar potential between Benin and the other regions are **significant** (*p < 0.05*).

### 🏗️ Engineering Considerations
- **Wind Patterns:** Benin shows a single dominant wind direction (SW), simplifying structural design.  
- **Maintenance:** A **strict cleaning schedule** is required for all sites due to significant soiling effects on sensor and panel performance.

---

## 📁 Repository Structure

```bash
solar-challenge-week0/
├── .github/workflows/   # CI/CD pipeline (GitHub Actions)
├── data/                # Raw and cleaned data files (not committed to Git)
├── notebooks/           # Jupyter notebooks for EDA and comparison
│   ├── benin_eda.ipynb
│   ├── sierraleone_eda.ipynb
│   ├── togo_eda.ipynb
│   └── compare_countries.ipynb
├── images/              # Images used in the final report
├── .gitignore           # Specifies intentionally untracked files
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── report.md            # Final strategy report

```
## 🧠 Setup Instructions

Follow the steps below to reproduce the analysis on your local machine:

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd solar-challenge-week0
```
### 2️⃣ Create a virtual environment
```bash
python -m venv .venv

```
### 3️⃣ Activate the environment
```bash
source .venv/bin/activate   # On Windows: .venv\bin\activate
```
### 4️⃣ Install dependencies
```bash
pip install -r requirements.txt

```

### 5️⃣ Add the raw data files
## Place these CSVs into the data/ directory:
### - benin-malanville.csv
### - sierraleone-bumbuna.csv
### - togo-dapaong_qc.csv


## ⚙️ Usage

Once the setup is complete, follow these steps to run the analysis:

### 1️⃣ Run the EDA Notebooks
Open and run the following notebooks in the `notebooks/` directory:

- `benin_eda.ipynb`  
- `sierraleone_eda.ipynb`  
- `togo_eda.ipynb`

These notebooks clean, preprocess, and analyze the solar irradiance and environmental data for each respective country.

Example command:
```bash
jupyter notebook notebooks/benin_eda.ipynb
```

## 🧰 Tools Used

| Category | Tool | Purpose |
|-----------|------|----------|
| **Programming** | Python 3.10+ | Core analysis environment |
| **Data Handling** | Pandas | Data cleaning, transformation, and manipulation |
| **Visualization** | Matplotlib, Seaborn | Static plots for irradiance, temperature, and wind data |
| **Interactive Visualization** | Plotly | Dynamic charts and Wind Rose plots for deeper insights |
| **Statistical Testing** | SciPy | Kruskal–Wallis test for comparing irradiance distributions |
| **IDE / Environment** | Jupyter Notebook | Running and documenting the full analysis workflow |

## 👩‍💻 Author

**Yonatan**  
_Data Analyst | Machine Learning Enthusiast | AI Mastery Trainee_  

### 🌞 Final Note

This project supports **MoonLight Energy Solutions** in making data-driven, sustainable investment decisions.
The analysis identifies **Benin** as the optimal location for solar farm installation, balancing energy yield, engineering feasibility, and environmental sustainability.