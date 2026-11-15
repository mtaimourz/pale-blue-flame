
import csv
import math
from pathlib import Path
from collections import Counter

file_path = Path(__file__).parent / "material_tests.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    columns = reader.fieldnames

print("TOTAL ROWS:", len(rows))
print("TOTAL COLUMNS:", len(columns))

print("\n--- MISSING VALUES ---")

for column in columns:
    missing = sum(
        1 for row in rows
        if not (row[column] or "").strip()
    )
    print(f"{column}: {missing}")

print("\n--- EXACT DUPLICATE ROWS ---")

row_counts = Counter(
    tuple(row[column] for column in columns)
    for row in rows
)

duplicates = sum(
    count - 1 for count in row_counts.values()
    if count > 1
)

print("Duplicate rows:", duplicates)

print("\n--- DUPLICATE TEST IDs ---")

test_ids = Counter(
    (row["experiment"], row["test"])
    for row in rows
)

duplicate_ids = {
    key: count for key, count in test_ids.items()
    if count > 1
}

print(duplicate_ids if duplicate_ids else "No duplicate test IDs")

print("\n--- DUPLICATE ID DETAILS ---")

for key in duplicate_ids:
    print(f"\nExperiment: {key[0]}, Test: {key[1]}")

    for row in rows:
        if (row["experiment"], row["test"]) == key:
            print({
                "date": row["date"],
                "material": row["material"],
                "shape": row["shape"],
                "size_mm": row["size_mm"],
                "oxygen_pct": row["oxygen_pct"],
                "airflow_start_cm_s": row["airflow_start_cm_s"],
                "result": row["result"],
                "notes": row["notes"]
            })
print("\n--- MISSING VALUES BY EXPERIMENT ---")

experiments = sorted(set(row["experiment"] for row in rows))

check_columns = [
    "size_mm",
    "oxygen_pct",
    "airflow_start_cm_s",
    "airflow_min_cm_s",
    "flow_direction",
    "result"
]

for experiment in experiments:

    experiment_rows = [
        row for row in rows
        if row["experiment"] == experiment
    ]

    print(f"\nExperiment: {experiment}")
    print("Total records:", len(experiment_rows))

    for column in check_columns:

        missing = sum(
            1 for row in experiment_rows
            if not (row[column] or "").strip()
        )

        print(f"{column}: {missing}")

print("\n--- BASS-II MISSING RESULTS ---")

for row in rows:
    if row["experiment"] == "BASS-II" and not row["result"].strip():
        print({
            "test": row["test"],
            "material": row["material"],
            "date": row["date"],
            "notes": row["notes"]
        })
print("\n--- BASS-II NOTES ANALYSIS ---")

bass2_missing = [
    row for row in rows
    if row["experiment"] == "BASS-II"
    and not row["result"].strip()
]

notes_available = [
    row for row in bass2_missing
    if row["notes"].strip()
]

notes_missing = [
    row for row in bass2_missing
    if not row["notes"].strip()
]

print("Total missing results:", len(bass2_missing))
print("Records with notes:", len(notes_available))
print("Records without notes:", len(notes_missing))

category_counts = Counter()

print("\n--- BASS-II NOTES CLASSIFICATION ---")

for row in notes_available:

    note = row["notes"].strip().lower()

    if any(word in note for word in ["ign", "lit", "flame"]):
        category = "Ignition / flame observation"

    elif "fan" in note:
        category = "External reference"

    elif any(char.isdigit() for char in note):
        category = "Numerical observations"

    else:
        category = "Other observations"

    category_counts[category] += 1

    print(row["test"], ":", category, "|", row["notes"])

print("\n--- CATEGORY SUMMARY ---")

for category, count in category_counts.items():
    print(f"{category}: {count}")

print("\n--- GENERATING MISSING DATA REPORT ---")

report_path = file_path.parent / "missing_values_report.csv"

issue_columns = columns

missing_records = []

for row in rows:

    for column in issue_columns:

        if not (row[column] or "").strip():

            missing_records.append({
                "experiment": row["experiment"],
                "test": row["test"],
                "date": row["date"],
                "material": row["material"],
                "missing_column": column,
                "notes": row["notes"]
            })

with open(report_path, "w", encoding="utf-8", newline="") as file:

    fieldnames = [
        "experiment",
        "test",
        "date",
        "material",
        "missing_column",
        "notes"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(missing_records)

print("Missing entries:", len(missing_records))
print("Report saved at:", report_path)


def is_valid_number(value):

    try:
        number = float(value)
        return math.isfinite(number)

    except (ValueError, TypeError):
        return False

print(is_valid_number("21"))
print(is_valid_number("18.5"))
print(is_valid_number("twenty"))

print("\n--- NUMERIC DATA VALIDATION ---")

numeric_columns = [
    "size_mm",
    "oxygen_pct",
    "airflow_start_cm_s",
    "airflow_min_cm_s"
]

invalid_records = []

for row in rows:

    for column in numeric_columns:

        value = (row[column] or "").strip()

        if value and not is_valid_number(value):

            invalid_records.append({
                "experiment": row["experiment"],
                "test": row["test"],
                "column": column,
                "invalid_value": value
            })

invalid_path = file_path.parent / "invalid_numeric_values.csv"

with open(invalid_path, "w", encoding="utf-8", newline="") as file:

    fieldnames = [
        "experiment",
        "test",
        "column",
        "invalid_value"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(invalid_records)

print("Invalid numeric values:", len(invalid_records))
print("Report saved at:", invalid_path)

print("\n--- CLASSIFYING MISSING VALUES ---")

expected_missing = {
    ("BASS", "oxygen_pct"):
        "Oxygen not recorded in BASS table",

    ("BASS", "airflow_start_cm_s"):
        "Airflow not recorded in BASS table",

    ("BASS", "airflow_min_cm_s"):
        "Airflow not recorded in BASS table",

    ("BASS", "flow_direction"):
        "Not available in BASS table",

    ("BASS", "result"):
        "Result not available in BASS table",

    ("BASS-II", "flow_direction"):
        "Direction not specified per test",

    ("SAFFIRE-III", "oxygen_pct"):
        "Oxygen not reported for these tests"
}

classified = []

for row in rows:

    for column in columns:

        if not (row[column] or "").strip():

            key = (row["experiment"], column)

            if key in expected_missing:
                status = "expected_missing"
                reason = expected_missing[key]

            elif row["experiment"] == "BASS-II" and column == "result":
                status = "not_conclusive"
                reason = "Blank result does not establish burn outcome"

            else:
                status = "needs_review"
                reason = "Check original NASA source"

            classified.append({
                "experiment": row["experiment"],
                "test": row["test"],
                "column": column,
                "status": status,
                "reason": reason
            })

classification_path = (
    file_path.parent / "missingness_classification.csv"
)

with open(classification_path, "w", encoding="utf-8",
          newline="") as file:

    fields = [
        "experiment",
        "test",
        "column",
        "status",
        "reason"
    ]

    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(classified)

print("Total classified:", len(classified))

print("\nClassification summary:")

for status, count in Counter(
    item["status"] for item in classified
).items():
    print(status, ":", count)

print("Report saved:", classification_path)
