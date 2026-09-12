import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix


# ---------------------------------------------------------
# Load ML dataset
# ---------------------------------------------------------
input_file = "results/ml_training_dataset.csv"

data = pd.read_csv(input_file)


# ---------------------------------------------------------
# Features and target
# ---------------------------------------------------------
feature_columns = [
    "spatial_query",
    "temporal_query",
    "attribute_query",
    "has_2dsphere",
    "has_time_filter",
    "number_of_filters",
    "query_selectivity"
]

X = data[feature_columns]
y = data["best_index"]


# ---------------------------------------------------------
# Create Decision Tree
# ---------------------------------------------------------
model = DecisionTreeClassifier(
    random_state=42,
    max_depth=4
)


# ---------------------------------------------------------
# Leave-One-Out Cross Validation
# ---------------------------------------------------------
loo = LeaveOneOut()

scores = cross_val_score(
    model,
    X,
    y,
    cv=loo,
    scoring="accuracy"
)

cv_accuracy = scores.mean() * 100


# ---------------------------------------------------------
# Train model on complete dataset
# ---------------------------------------------------------
model.fit(X, y)


# ---------------------------------------------------------
# Predictions on complete dataset
# ---------------------------------------------------------
predictions = model.predict(X)

training_accuracy = accuracy_score(
    y,
    predictions
) * 100


# ---------------------------------------------------------
# Display predictions
# ---------------------------------------------------------
results = data[
    ["query_id", "query_type", "best_index"]
].copy()

results["predicted_index"] = predictions

results["correct"] = (
    results["best_index"]
    == results["predicted_index"]
)


print("\n=== ML ROUTER PREDICTIONS ===\n")

print(
    results.to_string(index=False)
)


# ---------------------------------------------------------
# Confusion matrix
# ---------------------------------------------------------
labels = sorted(y.unique())

cm = confusion_matrix(
    y,
    predictions,
    labels=labels
)

print("\n=== CONFUSION MATRIX ===\n")

print("Index classes:")
for i, label in enumerate(labels):
    print(f"{i}: {label}")

print("\n")
print(cm)


# ---------------------------------------------------------
# Accuracy results
# ---------------------------------------------------------
print("\n=== ML ROUTER PERFORMANCE ===")

print(
    f"Training accuracy: "
    f"{training_accuracy:.2f}%"
)

print(
    f"Leave-One-Out CV accuracy: "
    f"{cv_accuracy:.2f}%"
)

print(
    f"\nTotal queries: {len(data)}"
)

print(
    f"Correct predictions: "
    f"{results['correct'].sum()}"
)

print(
    f"Incorrect predictions: "
    f"{(~results['correct']).sum()}"
)