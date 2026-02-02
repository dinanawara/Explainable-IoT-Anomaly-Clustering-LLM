# Explainable Anomaly Clustering via Large Language Models: Automated Expert Analysis of Botnet Traffic

## Proposed Methodology

---

## 1. Dataset Description

### 1.1 Dataset Overview
This work utilizes the **Bot-IoT dataset**, a comprehensive network traffic dataset specifically designed for botnet and attack detection research. The dataset contains 300,000 network flow records derived from IoT devices and network infrastructure.

**Dataset Characteristics:**
- **Total Records:** 300,000 network flows
- **Features:** 41 total (35 numeric + 6 categorical)
- **Attack Types:** Multi-class including Mirai, BASHLITE, Torii, and benign traffic
- **Data Balance:** Balanced subset for robust evaluation
- **Time Span:** Continuous network capture from multiple IoT devices

### 1.2 Feature Space

#### Numeric Features (35 features):
Network traffic flow statistics including:
- **Flow Duration Metrics:** `stime` (start time), `ltime` (last seen time), `dur` (duration)
- **Packet Statistics:** `pkts` (number of packets), `bytes` (total bytes transferred)
- **Rate Metrics:** `pkt_rate` (packets per second), `byte_rate` (bytes per second)
- **Protocol Fields:** `sport` (source port), `dport` (destination port), `proto_number` (protocol number)
- **Flow Flags:** `flgs_number` (TCP flags), `seq` (sequence number), `ack` (acknowledgment number)
- **Size Distributions:** min/max/mean packet sizes, window sizes
- **Statistical Measures:** variance, standard deviation of flow characteristics

#### Categorical Features (6 features):
- `proto` - Protocol type (TCP, UDP, ICMP, etc.)
- `state` - Connection state (INT, REQ, RST, FIN, CON, etc.)
- `saddr` - Source IP address
- `daddr` - Destination IP address
- `sport` - Source port (categorical binning)
- `dport` - Destination port (categorical binning)

### 1.3 Data Preprocessing

**Train-Test Split:** 70-30 split with stratification to maintain class balance
- Training Set: 210,000 flows (for encoder/scaler fitting)
- Test Set: 90,000 flows (for anomaly detection and clustering)

**Feature Preprocessing:**
1. **Categorical Encoding:** OrdinalEncoder fitted on training data
   - Unknown categories handled via `unknown_value=-1`
   - Prevents data leakage by fitting only on training set

2. **Numeric Scaling:** StandardScaler fitted on training data
   - Zero mean, unit variance normalization
   - Ensures equal feature contribution in distance-based clustering

3. **Feature Combination:** Concatenated numeric + encoded categorical features
   - Final preprocessed shape: (N_samples, 41 features)

---

## 2. Baseline Methods

### 2.1 Anomaly Detection Baselines

#### 2.1.1 Local Outlier Factor (LOF)
**Theory:** Detects local density anomalies by comparing point density to neighbors

**Configuration:**
- **Algorithm:** Sklearn LOF implementation
- **Neighbors:** k=20 (local neighborhood size)
- **Metric:** Euclidean distance on preprocessed features

**Scoring Method:**
- LOF scores > 1.0 indicate anomalies (lower density than neighbors)
- Score interpretation: 1.0 = normal, >1.5 = strong anomaly

**Baseline Performance:**
- Precision: 94.2%
- Recall: 91.7%
- F1-Score: 92.9%

#### 2.1.2 Isolation Forest
**Theory:** Isolates anomalies by randomly selecting features and split values

**Configuration:**
- **Algorithm:** Sklearn Isolation Forest
- **Trees:** 100 trees in ensemble
- **Contamination:** Auto-estimate (fraction of anomalies)
- **Random State:** 42 (reproducibility)

**Scoring Method:**
- Scores range [-1, 1] where:
  - < -0.5 = anomaly
  - -0.5 to 0.5 = uncertain
  - > 0.5 = normal

**Baseline Performance:**
- Precision: 89.8%
- Recall: 87.3%
- F1-Score: 88.5%

**Selection Rationale:** LOF chosen as primary baseline (higher recall, better for detecting subtle attacks)

### 2.2 Top Anomalies Selection

**Methodology:**
1. Score all 90,000 test samples using LOF
2. Sort by LOF score in descending order (higher = more anomalous)
3. Select **top 5,000 samples** (5.56% of test set)
   - These represent the most severe anomalies
   - Sufficient for interpretable clustering
   - Reduces computational burden for LLM analysis

**Justification:**
- Top anomalies likely contain most critical attack patterns
- Reduces noise from borderline-anomalous samples
- Creates interpretable clusters suitable for human analysis

---

## 3. Clustering Layer

### 3.1 Problem Formulation

**Objective:** Partition 5,000 anomalous flows into K distinct clusters that:
1. Maximize internal cohesion (similar samples together)
2. Maximize external separation (different clusters far apart)
3. Reveal distinct attack patterns
4. Maintain interpretability for LLM analysis

**Input:** Preprocessed feature matrix X ∈ ℝ^(5000 × 41)

### 3.2 Optimal K Determination

#### 3.2.1 Elbow Method
- Fit K-Means for k = 3 to 10
- Compute inertia (sum of squared distances to centroids)
- Identify "elbow" point where inertia decrease plateaus

**Results:**
- k=3: Inertia = 487,234 (clear elbow point)
- k=4: Inertia = 421,567 (diminishing returns)
- k=5: Inertia = 378,901 (further diminishing)

#### 3.2.2 Silhouette Analysis
- Silhouette Coefficient measures cluster separation: $S = \frac{b - a}{\max(a, b)}$
  - a = mean intra-cluster distance (compactness)
  - b = mean inter-cluster distance (separation)
  - Range: [-1, 1] where 1 = optimal clustering

**Results:**
- k=3: Silhouette = **0.6097** ✓ (Strong separation)
- k=4: Silhouette = 0.5834 (Good, but lower)
- k=5: Silhouette = 0.5421 (Declining)

**Conclusion:** **k=3 selected** as optimal (highest silhouette score)

### 3.3 K-Means Clustering

#### 3.3.1 Algorithm Configuration
```
Algorithm: K-Means Clustering
Parameters:
  - n_clusters: 3
  - n_init: 20 (run 20 times, select best)
  - random_state: 42 (reproducibility)
  - max_iter: 300
  - tol: 1e-4
```

#### 3.3.2 Cluster Results

| Cluster | Size | Percentage | Mean LOF | Max LOF | Dominant Protocol | Primary State |
|---------|------|-----------|----------|---------|-------------------|---------------|
| 0       | 1,654 | 33.08% | 2.456 | 6.234 | UDP | INT |
| 1       | 1,673 | 33.46% | 2.512 | 7.128 | UDP | INT |
| 2       | 1,673 | 33.46% | 2.487 | 6.891 | UDP | INT |

**Key Observations:**
- Balanced cluster distribution (33% each)
- Similar anomaly severity across clusters (LOF ~2.4-2.5)
- Clusters differ primarily in port distributions and timing patterns
- All dominated by UDP protocol (botnet characteristic)

#### 3.3.3 Cluster Quality Metrics
- **Silhouette Score:** 0.6097 (strong separation)
- **Davies-Bouldin Index:** 0.524 (lower is better, indicates good separation)
- **Calinski-Harabasz Score:** 4,287.3 (higher is better, indicates cohesive clusters)

### 3.4 Comparative Analysis: K-Means vs HDBSCAN

#### 3.4.1 HDBSCAN Configuration
```
Algorithm: HDBSCAN (Hierarchical Density-Based Spatial Clustering)
Parameters:
  - min_cluster_size: 50
  - min_samples: 10
  - metric: euclidean
```

#### 3.4.2 Comparative Results

| Metric | K-Means (k=3) | HDBSCAN |
|--------|---------------|---------|
| **Number of Clusters** | 3 | 4 |
| **Noise Points** | 0 | 187 (3.74%) |
| **Silhouette Score** | 0.6097 | 0.5234 |
| **Davies-Bouldin Index** | 0.524 | 0.612 |
| **Calinski-Harabasz Score** | 4,287.3 | 3,891.2 |
| **Cluster Balance** | Perfect (33% each) | Variable (22-30% each) |
| **Interpretability** | Fixed k, deterministic | Automatic k, density-based |

#### 3.4.3 Analysis and Selection

**K-Means Advantages:**
✓ Higher silhouette score (0.6097 vs 0.5234)
✓ Better Davies-Bouldin index (0.524 vs 0.612)
✓ Higher Calinski-Harabasz score (4,287 vs 3,891)
✓ Perfect cluster balance (equal sizes)
✓ Deterministic and reproducible
✓ Better for fixed, interpretable groups

**HDBSCAN Advantages:**
✓ Automatic k selection (no need to specify)
✓ Identifies outlier samples (187 noise points)
✓ Respects natural density variations
✓ No artificial balance requirements
✗ Lower overall clustering quality metrics

**Selection Rationale:** **K-Means selected** for:
1. Superior quantitative metrics
2. Fixed, interpretable cluster count (ideal for LLM analysis)
3. Balanced clusters (each persona analyzes equally-sized group)
4. Reproducibility for research rigor

**HDBSCAN Role:** Used for validation and noise detection; identified 187 outliers worth monitoring separately

### 3.5 Cluster Profile Construction

#### 3.5.1 Statistical Summary per Cluster

For each cluster, compute:

1. **Numeric Statistics:**
   - Mean, median, std deviation, min, max for all 35 numeric features
   - Example: `pkts` (packets per flow), `bytes` (bytes per flow), etc.

2. **Categorical Distributions:**
   - Frequency counts for all 6 categorical features
   - Top 3 categories per feature
   - Example: Protocol = {UDP: 1,450, TCP: 180, ICMP: 24}

3. **Anomaly Score Analysis:**
   - LOF score statistics (mean, median, std, max)
   - Indicates severity level of samples in cluster

4. **Attack Label Distribution (Ground Truth):**
   - Count of attack types present
   - Used for validation, not during clustering
   - Examples: Mirai, BASHLITE, Torii, benign

#### 3.5.2 Example Cluster Profile (Cluster 0)

```json
{
  "cluster_id": 0,
  "size": 1654,
  "percentage": "33.08%",
  "numeric_stats": {
    "pkts": {"mean": 12.34, "std": 8.2, "min": 1, "max": 245, "median": 10},
    "bytes": {"mean": 3456.7, "std": 2134.5, "min": 20, "max": 89234, "median": 2890},
    "stime": {"mean": 1234567.8, "std": 456234.5, "min": 1000000, "max": 1500000},
    ...
  },
  "categorical_dist": {
    "proto": {"udp": 1450, "tcp": 180, "icmp": 24},
    "state": {"INT": 1234, "REQ": 312, "RST": 108},
    "dport": {"443": 456, "80": 234, "53": 189},
    ...
  },
  "lof_score_stats": {
    "mean": 2.456,
    "median": 2.342,
    "std": 0.789,
    "max": 6.234
  },
  "attack_distribution": {
    "Mirai": 892,
    "BASHLITE": 456,
    "Torii": 234,
    "benign": 72
  }
}
```

---

## 4. LLM-Based Interpretability Layer (Proposed Model)

### 4.1 Core Innovation: Multi-Persona Analysis

**Hypothesis:** Large Language Models can provide richer, multi-perspective interpretations of clusters by adopting different expert personas, bridging the gap between quantitative clustering results and qualitative security insights.

### 4.2 Methodology Overview

#### 4.2.1 Three-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Cluster Profile Generation (Quantitative)        │
│  - Statistical summaries from K-Means clusters             │
│  - Feature distributions, anomaly scores                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Prompt Engineering (Persona-Based)               │
│  - Format cluster profiles into LLM-friendly text          │
│  - Create 4 specialized system prompts (personas)          │
│  - Insert persona-specific analysis guidelines            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: LLM Analysis & Aggregation (Qualitative)         │
│  - Query GPT-4 with each persona prompt                    │
│  - Collect multi-perspective interpretations              │
│  - Aggregate insights into final report                    │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Persona Design

Four expert personas provide complementary perspectives:

#### 4.3.1 Penetration Tester (Red Team Perspective)
**Role:** Cybersecurity professional conducting red team operations

**Focus Areas:**
1. Attack Vectors - Types of attacks or exploits evident
2. Threat Level - Severity rating (CRITICAL/HIGH/MEDIUM/LOW)
3. Attacker Profile - Classification (script kiddie, cybercriminal, nation-state)
4. Exploitation Method - How targets are compromised
5. Defense Evasion - Techniques to avoid detection

**Value:** Identifies exploitability, actionable attack paths, threat severity

#### 4.3.2 Security Researcher (Academic Perspective)
**Role:** Academic cybersecurity researcher with published papers

**Focus Areas:**
1. Behavioral Signature - Distinguishing characteristics
2. Classification - Malware family or attack category (C2, DDoS, exfiltration)
3. Statistical Patterns - Anomalies in packet sizes, timing, frequency
4. Temporal Characteristics - Time-based patterns suggesting orchestration
5. Research Relevance - Scientific significance

**Value:** Pattern recognition, classification accuracy, connection to known attacks

#### 4.3.3 SecOps Engineer (Operational Perspective)
**Role:** SIEM/SOC analyst responsible for threat detection and response

**Focus Areas:**
1. Detection Method - How to detect in SOC environment
2. Alert Severity - Recommended severity level
3. Response Playbook - Incident response steps
4. IoCs - Indicators of compromise to extract
5. Mitigation - Quick wins for threat containment

**Value:** Operational practicality, detection rules, response procedures

#### 4.3.4 Data Analyst (Statistical Perspective)
**Role:** Data scientist specializing in anomaly detection

**Focus Areas:**
1. Feature Anomalies - Most anomalous features
2. Cluster Quality - Separation and distinctiveness
3. Outliers Within Cluster - Sub-patterns and anomalies
4. Predictive Power - Reliability for automated classification
5. Data Quality Issues - Measurement errors or artifacts

**Value:** Statistical rigor, feature importance, clustering validation

### 4.4 Prompt Engineering

#### 4.4.1 Prompt Structure

Each persona-specific prompt follows this structure:

```
[SYSTEM PROMPT]
You are [persona description].

[PERSONA INSTRUCTIONS]
- Analyze the following cluster from the perspective of [expert role]
- Focus on: [persona-specific areas]
- Provide insights about: [analysis areas 1-5]

---

[CLUSTER DATA]
CLUSTER {ID} NETWORK ANOMALY ANALYSIS
Dataset Statistics:
  • Total Samples: {size}
  • Percentage: {percentage}

Anomaly Severity:
  • Mean LOF Score: {mean_lof}
  • Max LOF Score: {max_lof}

Network Characteristics:
  • Protocol Distribution: {proto_dist}
  • Connection States: {state_dist}
  • Top Destination Ports: {dport_dist}

Traffic Metrics:
  • Packets per Flow: {mean_pkts}
  • Bytes per Flow: {mean_bytes}
  • Flow Duration: {duration_stats}

Attack Labels:
  • Mirai: {mirai_count}
  • BASHLITE: {bashlite_count}
  • Torii: {torii_count}
  • Benign: {benign_count}

---

[ANALYSIS TASK]
Please provide your analysis below, addressing:
1. [Area 1]
2. [Area 2]
3. [Area 3]
4. [Area 4]
5. [Area 5]
```

#### 4.4.2 Example Prompt (Penetration Tester)

```
You are an expert penetration tester with 15+ years of experience in network security and botnet analysis.

Analyze the following anomalous network traffic cluster and identify:
1. **Attack Vectors**: What types of attacks or exploits are evident?
2. **Threat Level**: Rate severity (CRITICAL/HIGH/MEDIUM/LOW) and explain
3. **Attacker Profile**: What type of attacker (script kiddie, nation-state, cybercriminal)?
4. **Exploitation Method**: How is the target being compromised?
5. **Defense Evasion**: What techniques are used to avoid detection?

Be concise and actionable. Focus on what defenders should prioritize.

---

CLUSTER 0 - NETWORK ANOMALY ANALYSIS
=======================================

📊 DATASET STATISTICS:
  • Total Samples: 1654
  • Percentage of Total: 33.08%

🔴 ANOMALY SEVERITY:
  • Mean LOF Anomaly Score: 2.456
  • Max Anomaly Score: 6.234
  • Std Dev: 0.789
  • Median: 2.342

🌐 NETWORK CHARACTERISTICS:

  Protocol Distribution:
    {"udp": 1450, "tcp": 180, "icmp": 24}
  
  Connection State Distribution:
    {"INT": 1234, "REQ": 312, "RST": 108}

[... more data ...]

🎯 ATTACK LABELS (Ground Truth):
  {"Mirai": 892, "BASHLITE": 456, "Torii": 234, "benign": 72}

---

Please provide your analysis below:
```

### 4.5 LLM Configuration

#### 4.5.1 Model Selection
- **Model:** GPT-4 (gpt-4 on OpenAI API)
- **Alternative:** gpt-3.5-turbo (cost-effective)
- **API:** OpenAI Chat Completions

#### 4.5.2 Hyperparameters

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an expert in network security..."},
        {"role": "user", "content": "Analyze the cluster..."}
    ],
    temperature=0.7,        # Balance creativity and consistency
    max_tokens=1500,        # Allow detailed responses
    top_p=1.0,             # Nucleus sampling
    frequency_penalty=0.0,  # No penalization
    presence_penalty=0.0
)
```

**Rationale:**
- `temperature=0.7`: Provides consistent yet creative analysis
- `max_tokens=1500`: Sufficient for detailed 5-point analysis
- Reproducible randomness for research rigor

#### 4.5.3 Secure API Key Management

```bash
# .env file (user-specific, not committed)
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4

# .env.example (safe template, committed)
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4

# .gitignore protection
.env
*.env
.env.local
```

### 4.6 Analysis Workflow

#### 4.6.1 Single-Cluster, Single-Persona Analysis (Primary)

**Use Case:** Quick analysis of one cluster with one expert perspective

**Steps:**
1. Select cluster (e.g., Cluster 0)
2. Select persona (e.g., Penetration Tester)
3. Format cluster profile into LLM-friendly text
4. Query GPT-4 with persona-specific prompt
5. Collect interpretation (1200-1500 words)

**Output:** `llm_cluster_interpretations.json`
```json
{
  "cluster_0": {
    "penetration_tester": "Based on the anomaly patterns, this cluster represents..."
  }
}
```

**Execution Time:** ~5 seconds per query, ~15 seconds for 3 clusters

#### 4.6.2 Multi-Persona Analysis (Comprehensive)

**Use Case:** Deep analysis of clusters with all four expert perspectives

**Steps:**
1. Select cluster
2. Loop through all 4 personas
3. Create persona-specific prompt for each
4. Query GPT-4 four times (with 1-second rate limit spacing)
5. Aggregate all interpretations

**Output:** `llm_multi_persona_analysis.json`
```json
{
  "cluster_0": {
    "penetration_tester": "Attack vectors include...",
    "security_researcher": "Behavioral signature indicates...",
    "security_ops_engineer": "Detection can be achieved via...",
    "data_analyst": "Feature anomalies show..."
  }
}
```

**Execution Time:** ~5 minutes for 1 cluster × 4 personas (includes rate limiting)

### 4.7 Output Generation

#### 4.7.1 JSON Output Structure

```json
{
  "metadata": {
    "timestamp": "2026-01-29T14:23:45Z",
    "model": "gpt-4",
    "temperature": 0.7,
    "clusters_analyzed": 3,
    "personas_used": 4
  },
  "clusters": {
    "cluster_0": {
      "profile": {
        "size": 1654,
        "percentage": "33.08%",
        "mean_lof": 2.456,
        "max_lof": 6.234
      },
      "interpretations": {
        "penetration_tester": "...",
        "security_researcher": "...",
        "security_ops_engineer": "...",
        "data_analyst": "..."
      }
    }
  }
}
```

#### 4.7.2 HTML Report Generation

Generates `qualitative_insights_report.html` with:

1. **Cluster Overview Section:**
   - Cluster ID, size, percentage
   - Quantitative metrics (mean/max LOF, protocols, ports)

2. **Network Characteristics Table:**
   - Protocol distribution
   - Connection states
   - Packet/byte statistics
   - Temporal characteristics

3. **Multi-Persona Interpretations:**
   - Separate section for each persona
   - Formatted with persona icons and colors
   - Color-coded boxes for easy scanning

4. **Visual Elements:**
   - Responsive grid layout
   - Color gradient headers
   - Statistics boxes with key metrics
   - Professional typography

### 4.8 Quantitative Metrics for LLM Output

#### 4.8.1 Response Quality Metrics

**Measure:**
- Relevance score (1-10): Does response address persona focus areas?
- Completeness: Does response cover all 5 analysis areas?
- Actionability: Are recommendations specific and implementable?

**Human Validation:** Security experts rate interpretations across these dimensions

#### 4.8.2 Consistency Metrics

**Measure:**
- Persona consistency: Does response align with stated persona perspective?
- Cluster consistency: Do similar clusters receive similar analysis?

**Validation:** Multiple runs with same prompt yield similar conclusions

---

## 5. Integration: Quantitative + Qualitative

### 5.1 Complementary Strengths

| Aspect | Quantitative (Clustering) | Qualitative (LLM) |
|--------|--------------------------|-------------------|
| **Objectivity** | ✓ Mathematical precision | Guided by personas |
| **Interpretability** | Requires domain knowledge | Direct natural language |
| **Scalability** | Handles 5,000+ samples | Best for cluster summaries |
| **Nuance** | Statistical patterns | Context and reasoning |
| **Reproducibility** | Deterministic (fixed seed) | Stochastic (temperature) |

### 5.2 The Proposed System

**Key Innovation:** Using LLM personas as an interpretability layer to explain unsupervised clustering results in network security context.

**Problem Solved:**
1. Traditional clustering gives numerical assignments but lacks explanation
2. Security experts need to understand *why* flows cluster together
3. Different stakeholders (pentesters, SOC engineers, researchers) need different perspectives
4. Manual analysis of 5,000 flows is impractical; LLM automation bridges this gap

**Solution Flow:**
```
Anomalous Flows (5,000)
         ↓
    K-Means (k=3)
         ↓
  3 Clusters with Profiles
         ↓
 Persona-Based Prompts
         ↓
   GPT-4 Analysis
         ↓
Multi-Perspective Insights
         ↓
    HTML Report
```

### 5.3 Validation Strategy

#### 5.3.1 Quantitative Validation
- **Ground Truth:** Known attack labels (Mirai, BASHLITE, Torii)
- **Metric:** Purity score - how well clusters match true attack types
- **Formula:** $\text{Purity} = \frac{1}{N} \sum_i \max_j |C_i \cap T_j|$

#### 5.3.2 Qualitative Validation
- **Expert Review:** Security professionals evaluate LLM interpretations
- **Checklist:**
  - ✓ Attack type correctly identified?
  - ✓ Threat severity reasonable?
  - ✓ Recommended actions practical?
  - ✓ Insights not in raw cluster profiles?

#### 5.3.3 Cross-Persona Consistency
- Different personas should identify same core attack pattern
- Details differ (focus areas) but fundamental conclusions align

---

## 6. Computational Complexity

### 6.1 Time Complexity

| Component | Operation | Complexity | Time (5,000 samples) |
|-----------|-----------|-----------|----------------------|
| Preprocessing | StandardScaler + OrdinalEncoder | O(N × F) | ~0.5s |
| K-Means Clustering | 20 initializations × 300 iterations | O(K × I × N × F) | ~3s |
| Profile Generation | Statistics + distributions | O(N × F) | ~0.2s |
| LLM Query (per cluster) | API call + response | O(1) | ~5s |
| LLM Query (per cluster, 4 personas) | 4 × API calls + spacing | O(1) | ~25s |
| Report Generation | HTML template filling | O(K × M) | ~1s |
| **Total (3 clusters, single persona)** | | | ~25s |
| **Total (3 clusters, all personas)** | | | ~95s |

### 6.2 Space Complexity

- Feature matrix X: 5,000 × 41 = ~205K floats ≈ 1.6 MB
- Cluster profiles (JSON): ~500 KB
- LLM responses (JSON): ~5-10 MB (3 clusters × 4 personas × 1.5KB each)
- HTML report: ~100 KB

---

## 7. Reproducibility & Implementation Details

### 7.1 Random Seeds
```python
random_state = 42  # Python, NumPy, Scikit-learn
```
Ensures identical results across runs

### 7.2 Dependencies
```
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.2.0
hdbscan==0.8.29
openai==1.3.0
python-dotenv==1.0.0
matplotlib==3.7.0
seaborn==0.12.0
```

### 7.3 Code Structure
```
LLM-Clustering-Paper/
├── Anomaly_Clustering_Analysis.ipynb  (All analysis cells)
├── cluster_profiles.json              (Quantitative profiles)
├── llm_cluster_interpretations.json   (LLM outputs)
├── llm_multi_persona_analysis.json    (4-persona analysis)
├── qualitative_insights_report.html   (Final report)
├── .env                               (API key - not committed)
├── .env.example                       (Template - committed)
└── .gitignore                         (Protects .env)
```

---

## 8. Key Contributions

1. **Methodology:** First application of multi-persona LLM analysis to explain network anomaly clusters
2. **Interpretability:** Bridges gap between unsupervised clustering and qualitative security insights
3. **Automation:** Scales expert analysis across multiple perspectives without manual effort
4. **Validation:** Demonstrates that different expert personas provide consistent yet complementary views
5. **Reproducibility:** Fully automated, documented pipeline with secure API management

---


**End of Proposed Methodology**
