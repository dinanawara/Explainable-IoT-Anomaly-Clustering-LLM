# 🚀 Public Package Guide

## What's Included

This package contains everything needed to run the LLM-powered anomaly cluster interpretation analysis:

### ✅ Included
- ✅ **NOTEBOOKS/** - All Jupyter notebooks for analysis
- ✅ **DOCUMENTATION/** - Complete guides & methodology docs
- ✅ **Scripts/** - Utility scripts for data processing
- ✅ **Data/Bot-IoT-Dataset/** - Raw CSV data files
- ✅ **Data/*.json** - Processed cluster profiles & LLM outputs
- ✅ **Visualizations/** - Pre-generated charts & reports
- ✅ **README.md** - Full project documentation
- ✅ **requirements.txt** - Python dependencies
- ✅ **.env.example** - Template for API configuration

### ❌ NOT Included
- ❌ **.env** - Your secret OpenAI API key (create your own!)
- ❌ **.venv/** - Virtual environment (recreate locally)
- ❌ **__pycache__/** - Python cache files

---

## 🔒 Security Verified

Your OpenAI API key is **completely safe**:

✅ `.env` file is in `.gitignore` (never committed)  
✅ `.env.example` is safe template with no real keys  
✅ All code uses `python-dotenv` for secure key management  
✅ Pre-commit checks prevent accidental commits of secrets  

---

## 📦 Package Structure

```
LLM-Clustering-Paper-Public/
├── README.md                          ← Project overview (start here)
├── requirements.txt                   ← Python dependencies
├── .env.example                       ← Copy to .env and fill in key
├── .gitignore                         ← Protects secrets
│
├── NOTEBOOKS/
│   ├── Anomaly_Clustering_Analysis.ipynb         ← Main analysis
│   ├── Anomaly_Detection_Baselines.ipynb
│   ├── EDA_Balanced_Subset.ipynb
│   └── create_subset.ipynb
│
├── Data/
│   ├── cluster_profiles.json                     ← Cluster statistics
│   ├── llm_multi_persona_analysis.json           ← LLM outputs
│   ├── llm_cluster_prompts.json                  ← Prompts used
│   └── Bot-IoT-Dataset/
│       ├── UNSW_2018_IoT_Botnet_Full5pc_1.csv
│       ├── UNSW_2018_IoT_Botnet_Full5pc_2.csv
│       ├── UNSW_2018_IoT_Botnet_Full5pc_3.csv
│       └── UNSW_2018_IoT_Botnet_Full5pc_4.csv
│
├── Scripts/
│   ├── merge_datasets.py              ← Combine CSV files
│   ├── explore_labels.py              ← Dataset analysis
│   ├── create_balanced_subset.py      ← Create subsets
│   ├── generate_kmeans_viz.py         ← Visualization
│   └── compute_metrics.py             ← Metric calculation
│
├── Visualizations/
│   ├── hdbscan_top10_clusters_3d.png  ← 3D cluster view
│   ├── cluster_visualization.png      ← 2D view
│   ├── benign_vs_attack_distribution.png
│   ├── qualitative_insights_report.html
│   └── ... (other plots)
│
└── DOCUMENTATION/
    ├── START_HERE.md                  ← Project orientation
    ├── PROPOSED_METHODOLOGY.md        ← Paper structure (26KB)
    ├── METRIC_VALIDATION_REPORT.md    ← Full validation (17KB)
    ├── METRICS_QUICK_REFERENCE.md     ← Tables for papers
    ├── TECHNICAL_APPENDIX_METRICS.md  ← Methodology details
    └── GROUNDED_INTERPRETABILITY_DEMO.md ← Real examples
```

---

## 🔧 Setup Instructions

### 1. Clone/Download Package

```bash
# If from GitHub
git clone https://github.com/yourusername/LLM-Clustering-Paper.git
cd LLM-Clustering-Paper

# If downloaded as zip
unzip LLM-Clustering-Paper-Public.zip
cd LLM-Clustering-Paper-Public
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure OpenAI API

```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env
# or
code .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Get your key**: https://platform.openai.com/api-keys

### 5. Verify Setup

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check packages installed
pip list | grep -E "openai|pandas|scikit"

# Test .env file is readable
python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key configured:', bool(os.getenv('OPENAI_API_KEY')))"
```

---

## 🎯 Running the Analysis

### Quick Start (5 minutes)

```bash
# Start Jupyter
jupyter notebook

# Open NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
# Run cells 1-10 to see dataset overview and basic statistics
```

### Full Analysis (30-45 minutes)

```bash
# Cell 1-5: Load & explore data
# Cell 6-10: Data quality checks
# Cell 11-20: Clustering (K-Means & HDBSCAN)
# Cell 21-30: LLM interpretation (requires API key)
# Cell 31-35: Metrics validation
# Cell 36-40: Report generation
```

### Just View Results (2 minutes)

```bash
# Open pre-generated report
open Visualizations/qualitative_insights_report.html

# View metric validation
cat DOCUMENTATION/METRIC_VALIDATION_REPORT.md

# Check quick reference
cat DOCUMENTATION/METRICS_QUICK_REFERENCE.md
```

---

## 📊 What to Expect

### Data
- **Input**: 150,477 network flows from UNSW Bot-IoT dataset
- **Processed**: 5,000 top anomalies (by LOF scoring)
- **Clustering**: K-Means k=3, Silhouette score 0.6097

### Results
- **Clusters Found**: 3 distinct attack patterns
- **Interpretation**: 4 personas × 3 clusters = 12 analyses
- **Validation**: 5 metrics proving quality (100% grounding, 0 hallucinations)

### Output Files
- `cluster_profiles.json` - Quantitative statistics
- `llm_multi_persona_analysis.json` - LLM interpretations
- `Visualizations/*.png` - Charts and plots
- `Visualizations/*.html` - Interactive reports

---

## 🔐 Security Checklist

Before pushing to GitHub:

```bash
# ✅ Verify .env is ignored
grep "^\.env$" .gitignore
# Should return: .env

# ✅ Check no secrets in repo
git diff --cached | grep -i "api_key\|sk-"
# Should return nothing

# ✅ Verify .env.example has no real keys
cat .env.example
# Should show: OPENAI_API_KEY=sk-your-api-key-here

# ✅ Double-check before committing
git status
# Should NOT show .env file
```

---

## 🚀 Customization

### Use Different API Key File Location
```python
# In notebook cells or scripts:
from dotenv import load_dotenv
import os

# Load from specific .env location
load_dotenv('.env.production')
api_key = os.getenv('OPENAI_API_KEY')
```

### Use Different LLM Models
```python
# In notebook cell 25, modify:
client = OpenAI(api_key=api_key)

# Try different models:
models = [
    "gpt-4",           # Most capable (expensive)
    "gpt-3.5-turbo",   # Fast & cheap
    "gpt-4-turbo",     # New: faster, cheaper than gpt-4
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Change this line
    ...
)
```

### Adjust Persona Prompts
See `Data/llm_cluster_prompts.json` for current prompts. Modify to customize persona behavior.

---

## 📈 Understanding Results

### Metric Report
- **Grounding Fidelity** (100%): All numeric claims verified
- **Hallucination Detection** (0): No false claims found
- **Semantic Consistency** (100%): All personas agree on threat types
- **Feature Coverage** (100%): All cluster features mentioned
- **Inter-Persona Agreement** (87.5–93.75%): Strong alignment with expected role variation

See `DOCUMENTATION/METRIC_VALIDATION_REPORT.md` for detailed breakdown.

### Cluster Interpretation
- **Cluster 0**: HTTP C2 botnet (port 80 dominance)
- **Cluster 1**: Data exfiltration variant (larger payloads)
- **Cluster 2**: Supporting attack pattern (similar characteristics)

See `DOCUMENTATION/GROUNDED_INTERPRETABILITY_DEMO.md` for examples.

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'openai'"
```bash
# Solution: Install requirements
pip install -r requirements.txt
# Or specifically:
pip install openai
```

### Issue: ".env not found" or API key not loading
```bash
# Check .env exists
ls -la .env

# Check format
cat .env  # Should show OPENAI_API_KEY=sk-...

# Check it's not .env.example
ls -la .env*  # Should see both .env and .env.example
```

### Issue: "Invalid API key" error
```bash
# Verify key format starts with "sk-"
cat .env | grep OPENAI_API_KEY

# Get new key from https://platform.openai.com/api-keys
# Update .env with correct key
```

### Issue: Jupyter notebook won't start
```bash
# Verify installation
pip list | grep jupyter

# If missing, install:
pip install jupyter

# Try starting with verbose output:
jupyter notebook --debug
```

### Issue: Out of memory on large dataset
```bash
# Use smaller subset:
python3 Scripts/create_balanced_subset.py

# Modify notebook cells to use subset:
# df = pd.read_csv('Data/subset.csv')  # Instead of full dataset
```

---

## 📚 Learning Path

**New to the project?**
1. Read `README.md` (this file, top to bottom)
2. Read `DOCUMENTATION/START_HERE.md`
3. Open `NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb` and run first 10 cells
4. View `Visualizations/qualitative_insights_report.html`

**Want to understand the metrics?**
1. Read `DOCUMENTATION/METRIC_VALIDATION_REPORT.md`
2. Read `DOCUMENTATION/METRICS_QUICK_REFERENCE.md`
3. Review `DOCUMENTATION/TECHNICAL_APPENDIX_METRICS.md`

**Writing a paper with this?**
1. Copy tables from `DOCUMENTATION/METRICS_QUICK_REFERENCE.md`
2. Use language from `DOCUMENTATION/METRIC_VALIDATION_REPORT.md`
3. Reference `DOCUMENTATION/PROPOSED_METHODOLOGY.md` for structure
4. Include `DOCUMENTATION/TECHNICAL_APPENDIX_METRICS.md` as appendix

---

## 📞 Support & Contributions

**Found a bug?**
- Check existing issues on GitHub
- Open new issue with error message & Python version

**Have a question?**
- Check `README.md` FAQ section
- Review `DOCUMENTATION/` for answers
- Check Jupyter notebook cell comments

**Want to contribute?**
- Fork the repo
- Make changes on feature branch
- Submit pull request with description
- Ensure `.env` is never committed

---

## 📋 Pre-Commit Checklist

Before pushing to GitHub:

- [ ] `.env` file NOT staged (`git status` should not show it)
- [ ] `.env.example` has no real keys
- [ ] `requirements.txt` is up to date
- [ ] `.gitignore` includes `.env`, `*.pyc`, `.venv/`
- [ ] No API keys in commit message
- [ ] No large files (>100MB) committed
- [ ] README.md is current

---

## ✨ Next Steps

1. **Set up locally** (5 min)
   ```bash
   git clone ...
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your key
   ```

2. **Run analysis** (30 min)
   ```bash
   jupyter notebook
   # Run NOTEBOOKS/Anomaly_Clustering_Analysis.ipynb
   ```

3. **Review results** (10 min)
   - Check visualizations
   - Read metric report
   - Review interpretations

4. **Customize** (optional)
   - Modify prompts
   - Try different models
   - Adjust parameters

---

**Ready to start?** → Open `README.md` and follow Quick Start section!

**Version**: January 31, 2026  
**Status**: ✅ Public Release Ready  
**Security**: ✅ API Keys Protected
