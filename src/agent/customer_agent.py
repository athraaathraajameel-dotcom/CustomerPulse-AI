
from pathlib import Path
import pandas as pd
import joblib
import re

# ==========================================
# 1. LOAD DATA AND TRAINED MODEL
# ==========================================

ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT / "data" / "processed"
    / "customer_reviews_cleaned.csv"
)

MODEL_PATH = (
    ROOT / "models"
    / "recommendation_model.joblib"
)

df = pd.read_csv(DATA_PATH)
prediction_model = joblib.load(MODEL_PATH)


# ==========================================
# 2. COMPLAINT DETECTION
# ==========================================

COMPLAINT_PATTERNS = {
    "Sizing & Fit": [
        r"\btoo small\b",
        r"\btoo big\b",
        r"\bruns small\b",
        r"\bruns large\b",
        r"\bdoes not fit\b",
        r"\bdoesn't fit\b",
        r"\btight\b",
        r"\bloose\b",
        r"\bawkward fit\b",
        r"\bpoor fit\b",
        r"\bsizing issue\b",
    ],
    "Fabric & Quality": [
        r"\bcheap fabric\b",
        r"\bpoor quality\b",
        r"\blow quality\b",
        r"\bterrible fabric\b",
        r"\bfabric is terrible\b",
        r"\bscratchy\b",
        r"\bitchy\b",
        r"\brough material\b",
        r"\bthin material\b",
        r"\bfalling apart\b",
        r"\bdefective\b",
    ],
    "Design & Appearance": [
        r"\bugly\b",
        r"\bbad design\b",
        r"\blooks different\b",
        r"\bnot as pictured\b",
        r"\bdoes not look like\b",
        r"\bweird shape\b",
        r"\bunflattering\b",
        r"\bdisappointing design\b",
    ],
    "Price & Value": [
        r"\boverpriced\b",
        r"\btoo expensive\b",
        r"\bnot worth\b",
        r"\bwaste of money\b",
        r"\bpoor value\b",
        r"\bprice is too high\b",
    ],
    "Comfort": [
        r"\buncomfortable\b",
        r"\bnot comfortable\b",
        r"\bpainful\b",
        r"\birritating\b",
        r"\btoo hot\b",
        r"\btoo heavy\b",
    ],
    "Delivery & Condition": [
        r"\barrived damaged\b",
        r"\blate delivery\b",
        r"\bshipping delay\b",
        r"\bmissing item\b",
        r"\barrived dirty\b",
        r"\bwrong item\b",
    ],
}

RECOMMENDATIONS = {
    "Sizing & Fit": (
        "Review size charts, investigate fit consistency, "
        "and use customer feedback to improve sizing guidance."
    ),
    "Fabric & Quality": (
        "Audit supplier quality, inspect fabric durability, "
        "and prioritise products with repeated quality complaints."
    ),
    "Design & Appearance": (
        "Review product photography and descriptions, "
        "and investigate design-related dissatisfaction."
    ),
    "Price & Value": (
        "Compare pricing with customer-perceived value "
        "and review products receiving repeated price complaints."
    ),
    "Comfort": (
        "Investigate comfort-related feedback and review "
        "material selection and garment construction."
    ),
    "Delivery & Condition": (
        "Review packaging, fulfilment processes, "
        "and delivery-related quality checks."
    ),
}


def detect_complaints(review_text):
    text = review_text.lower()
    detected = []

    for category, patterns in COMPLAINT_PATTERNS.items():
        if any(re.search(pattern, text) for pattern in patterns):
            detected.append(category)

    return detected


# ==========================================
# 3. PREDICTION + BUSINESS INTELLIGENCE
# ==========================================

def predict_recommendation(review_text):
    prediction = prediction_model.predict(
        [review_text]
    )[0]

    probabilities = prediction_model.predict_proba(
        [review_text]
    )[0]

    confidence = max(probabilities) * 100

    label = (
        "Recommended"
        if prediction == 1
        else "Not Recommended"
    )

    return label, confidence


def analyse_review(review_text):
    if not review_text.strip():
        return "Please enter a customer review."

    label, confidence = predict_recommendation(
        review_text
    )

    complaints = detect_complaints(review_text)

    result = [
        "CUSTOMERPULSE AI - REVIEW ANALYSIS",
        "---------------------------------",
        f"Prediction: {label}",
        f"Model Confidence: {confidence:.2f}%",
        "",
    ]

    if complaints:
        result.append(
            "Detected Issues: " + ", ".join(complaints)
        )
        result.append("")
        result.append("BUSINESS RECOMMENDATIONS:")

        for category in complaints:
            result.append(
                f"- {category}: {RECOMMENDATIONS[category]}"
            )

    else:
        result.append(
            "Detected Issues: No matching complaint patterns."
        )

        if label == "Not Recommended":
            result.append(
                "Recommendation: Manually review this feedback "
                "to identify the cause of dissatisfaction."
            )
        else:
            result.append(
                "Recommendation: Monitor positive feedback "
                "and identify strengths worth maintaining."
            )

    result.append("")
    result.append(
        "Note: Complaint categories are keyword-based "
        "indicators and should be validated."
    )

    return "\n".join(result)


# ==========================================
# 4. OVERALL BUSINESS SUMMARY
# ==========================================

def overall_summary():
    total = len(df)

    recommendation_rate = (
        df["Recommended IND"].mean() * 100
    )

    average_rating = df["Rating"].mean()

    return {
        "Total Reviews": total,
        "Recommendation Rate": round(
            recommendation_rate, 2
        ),
        "Average Rating": round(
            average_rating, 2
        ),
    }


# ==========================================
# 5. DEPARTMENT PERFORMANCE
# ==========================================

def department_performance():
    summary = (
        df.groupby("Department Name")
        .agg(
            Total_Reviews=("Rating", "count"),
            Average_Rating=("Rating", "mean"),
            Recommendation_Rate=(
                "Recommended IND", "mean"
            ),
        )
        .reset_index()
    )

    summary["Recommendation_Rate"] *= 100

    summary["Dissatisfaction_Rate"] = (
        100 - summary["Recommendation_Rate"]
    )

    return (
        summary.round(2)
        .sort_values(
            "Dissatisfaction_Rate",
            ascending=False
        )
    )


# ==========================================
# 6. AGENT QUESTION HANDLING
# ==========================================

def answer_question(question):
    question = question.strip()
    lower_question = question.lower()

    if lower_question.startswith("predict:"):
        review_text = question.split(":", 1)[1].strip()

        if not review_text:
            return "Please enter a review after predict:"

        label, confidence = predict_recommendation(
            review_text
        )

        return (
            f"Prediction: {label}\n"
            f"Model Confidence: {confidence:.2f}%"
        )

    if lower_question.startswith("analyse:") or \
       lower_question.startswith("analyze:"):

        review_text = question.split(":", 1)[1].strip()
        return analyse_review(review_text)

    if "department" in lower_question:
        summary = department_performance()

        if (
            "highest" in lower_question
            and "dissatisfaction" in lower_question
        ):
            top = summary.iloc[0]

            return (
                f"Department: {top['Department Name']}\n"
                f"Dissatisfaction Rate: "
                f"{top['Dissatisfaction_Rate']:.2f}%\n"
                f"Total Reviews: "
                f"{int(top['Total_Reviews'])}\n"
                f"Average Rating: "
                f"{top['Average_Rating']:.2f}/5\n\n"
                "Recommendation: Investigate customer feedback "
                "and compare complaint volume with other departments."
            )

        return summary.to_string(index=False)

    if (
        "recommendation" in lower_question
        or "rating" in lower_question
    ):
        return str(overall_summary())

    return (
        "I can analyse customer reviews, predict "
        "recommendations, and report department performance.\n\n"
        "Try:\n"
        "- analyse: The fabric is terrible and the dress is too small.\n"
        "- predict: I love this dress!\n"
        "- Which department has the highest dissatisfaction rate?\n"
        "- What is the overall recommendation rate?"
    )


# ==========================================
# 7. INTERACTIVE AGENT
# ==========================================

if __name__ == "__main__":
    print("CustomerPulse Intelligence Agent")
    print("--------------------------------")

    while True:
        question = input(
            "\nAsk a question (or exit): "
        )

        if question.lower().strip() == "exit":
            break

        print("\n" + answer_question(question))
