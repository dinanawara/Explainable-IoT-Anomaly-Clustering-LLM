# 🔍 LLM-Powered Anomaly Cluster Interpretation

**A systematic approach to interpreting network anomaly clusters using domain-expert personas with GPT-4.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)

---

## 🎯 Overview

This project demonstrates a novel approach to **grounded LLM interpretation of anomaly clusters**:

- **Input**: Unsupervised clustering results (K-Means on 5,000 network anomalies)
- **Process**: Four domain-expert personas (Penetration Tester, Security Researcher, SecOps Engineer, Data Analyst) provide independent interpretations
- **Output**: Grounded, validated, hallucination-free cluster insights with quantitative metrics

**Key Achievement**: ✅ 100% grounding fidelity (all LLM claims verified to source data), zero hallucinations detected

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| **Dataset** | UNSW Bot-IoT (5,000 top anomalies) |
| **Clustering** | K-Means (k=3) + HDBSCAN (33 density clusters) |
| **Personas** | 4 expert types × 3 clusters = 12 interpretations |
| **Validation** | 5 quantitative metrics, 100% grounding verified |
| **Hallucinations** | 0 detected (systematic verification) |
| **Feature Coverage** | 100% of cluster characteristics addressed |

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/LLM-Clustering-Paper.git
cd LLM-Clustering-Paper
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure OpenAI API



### 3. Run Analysis

```bash
# Open the main Jupyter notebook
jupyter notebook NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb

# Or run the preprocessing scripts
python3 merge_datasets.py          # Merge raw CSV files
python3 explore_labels.py          # Analyze dataset balance
python3 create_balanced_subset.py  # Create subset for quick testing
```

### 4. View Results

- **Clustering visualizations**: `*.png` files (3D scatter plots, distributions)
- **Metric report**: `DOCUMENTATION/METRIC_VALIDATION_REPORT.md`
- **Grounding demo**: `DOCUMENTATION/GROUNDED_INTERPRETABILITY_DEMO.md`
- **Interactive HTML**: `qualitative_insights_report.html`

---

## 📁 Project Structure

```
LLM-Clustering-Paper/
├── NOTEBOOKS/
│   ├── Anomaly_Clustering_Analysis.ipynb      ← Main analysis (start here)
│   ├── Anomaly_Detection_Baselines.ipynb      ← Baseline comparisons
│   ├── EDA_Balanced_Subset.ipynb              ← Quick EDA
│   └── create_subset.ipynb                    ← Data subsetting
│
├── Data/
│   ├── Bot-IoT-Dataset/                       ← Raw CSV files
│   │   ├── UNSW_2018_IoT_Botnet_Full5pc_*.csv
│   │   └── ... (4 files total)
│   ├── cluster_profiles.json                  ← Quantitative cluster stats
│   └── llm_multi_persona_analysis.json        ← LLM outputs
│
├── DOCUMENTATION/
│   ├── START_HERE.md                          ← Project orientation
│   ├── PROPOSED_METHODOLOGY.md                ← Paper methodology (26KB)
│   ├── METRIC_VALIDATION_REPORT.md            ← Full validation (17KB)
│   ├── METRICS_QUICK_REFERENCE.md             ← Tables for papers (8KB)
│   ├── TECHNICAL_APPENDIX_METRICS.md          ← Methodology details (13KB)
│   ├── GROUNDED_INTERPRETABILITY_DEMO.md      ← Grounding examples
│   └── ... (other guides)
│
├── Scripts/
│   ├── merge_datasets.py                      ← Combine CSV files
│   ├── explore_labels.py                      ← Dataset analysis
│   ├── create_balanced_subset.py              ← Create subsets
│   ├── generate_kmeans_viz.py                 ← K-Means visualization
│   └── compute_metrics.py                     ← Metrics calculation
│
├── Visualizations/
│   ├── hdbscan_top10_clusters_3d.png          ← 3D cluster view (t-SNE)
│   ├── cluster_visualization.png               ← 2D visualization
│   ├── benign_vs_attack_distribution.png      ← Dataset balance
│   └── ... (other plots)
│
├── .env.example                               ← Template (fill in your key)
├── .gitignore                                 ← Protect .env & secrets
├── requirements.txt                           ← Python dependencies
└── README.md                                  ← This file
```

---

## 📚 Main Workflow

### Step 1: Data Preparation
```bash
python3 merge_datasets.py          # Combines 4 CSV files into single dataset
```

### Step 2: Exploratory Analysis
```bash
# Open notebook and run cells 1-5
jupyter notebook NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
```

### Step 3: Clustering & Anomaly Detection
```bash
# Run cells 6-20 in main notebook
# K-Means: Silhouette = 0.6097, excellent separation
# HDBSCAN: 33 density clusters, silhouette = 0.6806
```

### Step 4: LLM Interpretation (Requires OpenAI API Key)
```bash
# Run cells 21-30 for persona-based analysis
# Personas: Pentest, Researcher, SecOps, Analyst
# Output: llm_multi_persona_analysis.json
```

### Step 5: Metric Validation
```bash
# Run cell 31-35 to validate outputs
# Metrics: Grounding (100%), Hallucinations (0), Consensus (100%)
python3 compute_metrics.py  # Generate detailed report
```

### Step 6: Report Generation
```bash
# Run final cells to create HTML report
# Output: qualitative_insights_report.html
```

---

## 🔍 Understanding the Metrics

This project validates LLM outputs using **5 quantitative metrics**:

| Metric | What It Measures | Target | Result |
|--------|-----------------|--------|--------|
| **Grounding Fidelity** | % of numeric claims matching source data | >95% | **100%** ✅ |
| **Hallucination Detection** | Count of false/unsupported claims | <5% | **0** ✅ |
| **Semantic Consistency** | Agreement on threat classifications | >75% | **100%** ✅ |
| **Feature Coverage** | % of cluster features mentioned | >80% | **100%** ✅ |
| **Inter-Persona Agreement** | Theme alignment across personas | >75% | **87.5–93.75%** ✅ |

**Why these metrics?**
- ✅ Domain-specific (security, ML clustering)
- ✅ Directly measure interpretability quality
- ✅ Reproducible and verifiable

See `DOCUMENTATION/TECHNICAL_APPENDIX_METRICS.md` for formulas and verification procedures.


## 🧬 Dataset

**Source**: UNSW Bot-IoT Dataset (2018)
- **Full dataset**: 150,477 network flows
- **Analysis subset**: 5,000 top anomalies (by LOF scoring)
- **Class balance**: 99.7% attacks, 0.3% benign
- **Features**: 41 (35 numeric, 6 categorical)

**In this repo**: 4 CSV files in `Data/Bot-IoT-Dataset/`
- `UNSW_2018_IoT_Botnet_Full5pc_1.csv`
- `UNSW_2018_IoT_Botnet_Full5pc_2.csv`
- `UNSW_2018_IoT_Botnet_Full5pc_3.csv`
- `UNSW_2018_IoT_Botnet_Full5pc_4.csv`

**Processing**: Merge & LOF scoring → top 5,000 → K-Means clustering

---

## 🤖 LLM Integration

### GPT-4 Personas

Each persona receives the same cluster statistics but with role-specific prompts:

1. **Penetration Tester**
   - Focus: Attack tactics, exploitation, evasion
   - Output: Threat classification, attacker profile, defense evasion techniques

2. **Security Researcher**
   - Focus: Malware classification, patterns, academic rigor
   - Output: Behavioral signatures, known families, statistical analysis

3. **SecOps Engineer**
   - Focus: Operational response, incident handling, IoCs
   - Output: Alert severity, response playbook, isolation procedures

4. **Data Analyst**
   - Focus: Clustering quality, statistical validation, outliers
   - Output: Anomaly metrics, predictive power, data quality assessment

### How It Works

```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

for persona in ["penetration_tester", "security_researcher", ...]:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a {persona}..."},
            {"role": "user", "content": f"Analyze this cluster: {cluster_stats}"}
        ]
    )
    analyses[persona] = response.choices[0].message.content
```

See `NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb` cells 21-30 for full implementation.

---

## 📊 Clustering Results

### K-Means (k=3)
- **Silhouette Score**: 0.6097 (good separation)
- **Davies-Bouldin Index**: 0.6848 (excellent, <1 is target)
- **Cluster sizes**: 1,594 (31.88%), 1,700 (34%), 1,706 (34.12%)

### Cluster Characteristics
- **Cluster 0**: HTTP-based C2 botnet (port 80 dominance)
- **Cluster 1**: Data exfiltration variant (larger payloads)
- **Cluster 2**: Supporting attack pattern (similar characteristics)

### All Clusters
- ✅ 100% labeled as attacks (true positives)
- ✅ Distinct feature patterns
- ✅ Well-separated in feature space

---

## 🔄 Reproducibility

### Verify Grounding
```python
import json

# Load baseline
with open('Data/cluster_profiles.json') as f:
    baseline = json.load(f)

# Load LLM outputs
with open('Data/llm_multi_persona_analysis.json') as f:
    llm_outputs = json.load(f)

# Check: All numbers in llm_outputs match baseline
for cluster_id, analyses in llm_outputs.items():
    for persona, text in analyses.items():
        # Extract numbers and verify against baseline
        # See TECHNICAL_APPENDIX_METRICS.md for procedure
        pass
```

### Regenerate Metrics
```bash
python3 compute_metrics.py
# Outputs: METRICS_VALIDATION_REPORT.json
```

### Re-run Clustering
```bash
# Open NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
# Run cells 1-20 to reproduce all clustering & visualizations
jupyter notebook NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
```

---

## 💻 Requirements

**Python**: 3.8+

**Key packages**:
```
python-dotenv==1.0.0          # .env management
openai==1.0+                  # GPT-4 API
pandas==2.0+                  # Data manipulation
scikit-learn==1.3+            # Clustering & metrics
matplotlib==3.7+              # Visualization
seaborn==0.13+                # Statistical plotting
jupyter==1.0+                 # Notebooks
hdbscan==0.8+                 # Density clustering (optional)
```

See `requirements.txt` for complete dependencies.

---

## 🚀 Next Steps

1. **Clone this repo**
   ```bash
   git clone https://github.com/yourusername/LLM-Clustering-Paper.git
   ```

2. **Set up environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key**
   ```bash
   cp .env.example .env
   # Edit .env and add OPENAI_API_KEY=sk-...
   ```

4. **Run the analysis**
   ```bash
   jupyter notebook NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
   ```

5. **Review results**
   - Clustering visualizations: `*.png` files
   - Metric report: `DOCUMENTATION/METRIC_VALIDATION_REPORT.md`
   - Interactive report: `qualitative_insights_report.html`

---

## 📖 Learn More

- **Project Overview**: `DOCUMENTATION/START_HERE.md`
- **Full Methodology**: `DOCUMENTATION/PROPOSED_METHODOLOGY.md`
- **Validation Details**: `DOCUMENTATION/METRIC_VALIDATION_REPORT.md`
- **Grounding Examples**: `DOCUMENTATION/GROUNDED_INTERPRETABILITY_DEMO.md`
- **Technical Details**: `DOCUMENTATION/TECHNICAL_APPENDIX_METRICS.md`

---


## 📝 Citation

If you use this project in research, please cite:

```bibtex
@software{llm_clustering_2026,
  title={LLM-Powered Anomaly Cluster Interpretation},
  year={2026},
  url={https://github.com/yourusername/LLM-Clustering-Paper}
}
```

---

## ⚖️ License

MIT License - See LICENSE file for details.

Free to use, modify, and distribute. Attribution appreciated but not required.

---

## ❓ FAQ

**Q: Do I need an OpenAI API key?**
A: Yes, to generate LLM interpretations. Clustering & visualization work without it. Estimated cost: $0.30-0.50 for all 12 interpretations.

**Q: Can I use a different LLM?**
A: Yes! Replace the OpenAI API calls in cells 21-30 with your preferred model (Claude, Gemini, etc.). See code for details.

**Q: How do I verify the metrics?**
A: All verification procedures documented in `TECHNICAL_APPENDIX_METRICS.md`. Run `compute_metrics.py` to regenerate.

**Q: What if I don't have the full dataset?**
A: Use `NOTEBOOKS/create_subset.ipynb` to generate smaller subsets for testing.

**Q: Are the LLM outputs reproducible?**
A: No—LLM outputs have inherent randomness. However, the personas' *conclusions* are highly consistent (100% consensus on threat types).


