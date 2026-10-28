
from pathlib import Path
import sys
import pandas as pd

# Find project root
ROOT = Path(__file__).resolve().parents[2]

# Allow importing our existing agent
sys.path.insert(0, str(ROOT / "src" / "agent"))

from customer_agent import detect_complaints

# Load cleaned reviews
data_path = (
    ROOT / "data" / "processed"
    / "customer_reviews_cleaned.csv"
)

df = pd.read_csv(data_path)

# Detect complaints in each review
df["Detected_Complaints"] = (
    df["Review Text"]
    .fillna("")
    .apply(
        lambda text: ", ".join(detect_complaints(text))
    )
)

df["Complaint_Count"] = df["Detected_Complaints"].apply(
    lambda text: len(text.split(", ")) if text else 0
)

# Save Tableau-ready dataset
output_path = (
    ROOT / "data" / "processed"
    / "customer_reviews_tableau.csv"
)

df.to_csv(output_path, index=False)

print("Complaint analysis completed!")
print("Total reviews:", len(df))
print(
    "Reviews with detected complaints:",
    (df["Complaint_Count"] > 0).sum()
)
print("Saved to:", output_path)

# Export one row per detected complaint category
complaints_long = df.loc[
    df["Complaint_Count"] > 0,
    ["Detected_Complaints", "Department Name", "Rating", "Recommended IND"]
].copy()

complaints_long["Complaint_Category"] = (
    complaints_long["Detected_Complaints"].str.split(", ")
)

complaints_long = complaints_long.explode("Complaint_Category")

complaints_path = (
    ROOT / "data" / "processed"
    / "complaints_by_category.csv"
)

complaints_long.to_csv(complaints_path, index=False)

print("\nComplaint categories exported!")
print(complaints_long["Complaint_Category"].value_counts())
print("Saved to:", complaints_path)
