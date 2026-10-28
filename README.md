# CustomerPulse AI
### Customer Intelligence, NLP & Predictive Analytics

CustomerPulse AI is an end-to-end customer intelligence project that combines **exploratory data analysis, natural language processing (NLP), machine learning, business recommendations, and interactive Tableau dashboards** to turn customer reviews into actionable business insights.

The project analyses customer feedback from a women's e-commerce clothing dataset to identify dissatisfaction drivers, predict product recommendations, and support data-driven business decisions.

## Project Objectives

- Analyse customer ratings and recommendation behaviour.
- Identify recurring complaints from customer review text.
- Build a machine learning model to predict customer recommendations.
- Develop an interactive, rule-based customer intelligence agent.
- Compare performance across product departments.
- Visualise customer experience metrics in Tableau.
- Generate practical recommendations for improving customer satisfaction.

## Dataset

**Source:** Women's E-Commerce Clothing Reviews — Kaggle

The dataset contains customer reviews, product ratings, recommendation indicators, and product department information.

The Tableau analysis covers **23,465 customer reviews**.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and application logic |
| Pandas | Data cleaning and aggregation |
| Scikit-learn | Machine learning and model evaluation |
| TF-IDF | Text feature extraction |
| Logistic Regression | Recommendation prediction |
| Regular Expressions | Keyword-based complaint detection |
| Joblib | Model persistence |
| Tableau | Interactive business intelligence dashboard |
| Jupyter Notebook | Exploratory analysis and model development |

## Machine Learning Model

A text classification model was developed to predict whether a customer would recommend a product based on their written review.

**Methodology:**
- Text features: Customer review text
- Target: Recommended IND
- Vectorisation: TF-IDF
- Classification: Logistic Regression
- Training/testing split: 80% / 20%
- Baseline: Dummy Classifier (most frequent class)

### Model Performance

| Metric | Result |
|---|---:|
| Baseline Accuracy | 81.89% |
| Model Accuracy | **86.77%** |
| Accuracy Improvement | +4.88 percentage points |
| Test Samples | 4,528 |

### Classification Report

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Not Recommended | 0.60 | 0.82 | 0.69 |
| Recommended | 0.96 | 0.88 | 0.92 |
| Weighted Average | 0.89 | 0.87 | 0.88 |

The model outperformed the majority-class baseline and achieved 82% recall for identifying reviews that did not recommend a product.

However, the lower precision for the Not Recommended class indicates that some positive reviews may be incorrectly flagged as negative.

## NLP Complaint Analysis

A rule-based complaint detection system identifies customer dissatisfaction signals using regular expressions and predefined keyword patterns.

Complaint categories include:

- Sizing & Fit
- Fabric & Quality
- Design & Appearance
- Price & Value
- Comfort
- Delivery & Condition

A review may match multiple complaint categories.

The system also generates category-specific business recommendations.

**Example:**

Input:

`The dress is too small and the fabric is terrible.`

Detected issues:

`Sizing & Fit, Fabric & Quality`

The agent recommends improving sizing guidance and reviewing fabric quality.

## Customer Intelligence Agent

The project includes a command-line, rule-based customer intelligence agent that integrates the trained machine learning model with complaint detection and business analytics.

### Agent Capabilities

**Review Prediction**

Predicts whether a customer review indicates a recommendation and displays model confidence.

**Complaint Analysis**

Detects predefined complaint patterns and generates business recommendations.

**Department Performance**

Calculates review counts, average ratings, recommendation rates, and dissatisfaction rates by department.

**Overall Business Summary**

Reports overall review volume, recommendation rate, and average rating.

### Example Commands

```text
analyse: The dress is too small and the fabric is terrible.
```

```text
predict: I love this dress!
```

```text
Which department has the highest dissatisfaction rate?
```

```text
What is the overall recommendation rate?
```

### Validated Agent Examples

For the negative review example, the agent returned:

- Prediction: Not Recommended
- Model Confidence: 87.14%
- Detected Issues: Sizing & Fit, Fabric & Quality

For the department dissatisfaction query:

- Department: Trend
- Dissatisfaction Rate: 26.05%
- Total Reviews: 119
- Average Rating: 3.82/5

**Note:** This is a rule-based analytical agent supported by machine learning, not a generative AI or large language model (LLM) agent.

## Tableau Executive Dashboard

An interactive Tableau dashboard was created to monitor customer experience performance.

### Key Performance Indicators

| KPI | Value |
|---|---:|
| Total Reviews | 23,465 |
| Recommendation Rate | 82.22% |
| Average Rating | 4.20 / 5 |
| Complaint Rate | 19.07% |

### Dashboard Features

- Reviews by Department
- Recommendation Rate by Department
- Complaints by Category
- Interactive department filtering
- Executive KPI cards
- Business insights and recommendations

The dashboard allows users to select a department and explore its associated performance metrics.

### Dashboard Preview

![Dashboard](<visuals/CustomerPulse AI Executive Dashboard.png>)

## Key Business Insights

**1. Highest Review Volume**

The Tops department has the highest review volume, with 10,455 customer reviews.

**2. Highest Recommendation Rate**

Bottoms has the highest recommendation rate among the main departments, at 85.12%.

**3. Primary Customer Pain Point**

Sizing & Fit represents approximately 72.3% of categorised complaint occurrences in the dashboard analysis.

**4. Highest Department Dissatisfaction**

Trend has the highest dissatisfaction rate at 26.05%, although its relatively small sample of 119 reviews should be considered when interpreting this result.

## Business Recommendations

**Improve Product Sizing**

Review size charts, improve fit descriptions, and investigate products receiving repeated sizing complaints.

**Strengthen Quality Control**

Monitor fabric-related complaints and review suppliers associated with recurring quality issues.

**Monitor Department Performance**

Prioritise departments with high dissatisfaction while accounting for differences in review volume.

**Use Predictive Feedback Monitoring**

Use the classification model to help flag potentially negative reviews for further investigation.

**Validate Complaint Categories**

Review keyword-based complaint classifications before using them for high-impact business decisions.

## Project Structure

```text
CustomerPulse-AI/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── recommendation_model.joblib
├── notebooks/
│   └── 01_data_exploration.ipynb
├── src/
│   ├── agent/
│   │   └── customer_agent.py
│   └── nlp/
│       └── complaint_analysis.py
├── tableau/
│   └── CustomerPulse_AI_Dashboard.twbx
├── visuals/
├── README.md
└── requirements.txt
```

## How to Run

Clone the repository and open the project directory.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the customer intelligence agent from the project root:

```bash
python src/agent/customer_agent.py
```

The agent requires the processed customer review dataset and the saved machine learning model at their expected project paths.

Open `tableau/CustomerPulse_AI_Dashboard.twbx` in a compatible Tableau application to explore the dashboard.

## Limitations

- The dataset represents a specific women's clothing review context and may not generalise to other industries.
- The recommendation model has lower precision for the Not Recommended class.
- Keyword-based complaint detection may miss nuanced language, sarcasm, and indirect complaints.
- Multiple complaint categories can be detected in a single review.
- Model confidence should not be interpreted as guaranteed correctness.
- Smaller departments may have less stable performance estimates.
- The agent supports predefined commands rather than unrestricted natural-language conversation.

## Conclusion

CustomerPulse AI demonstrates how customer feedback can be transformed into actionable intelligence through NLP, predictive machine learning, business analytics, and interactive visualisation.

The project combines technical implementation with business-focused insights to support better customer experience decisions.