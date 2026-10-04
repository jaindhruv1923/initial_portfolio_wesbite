"""
Data Quality & Schema Validation Gate (Pandera)
===============================================
Enforces strict schema, range, and type constraints on raw scrapes and
processed datasets to prevent data quality regressions in production pipelines.
"""

import sys
import pandas as pd
try:
    import pandera.pandas as pa
    from pandera.pandas import Column, Check, DataFrameSchema
except ImportError:
    import pandera as pa
    from pandera import Column, Check, DataFrameSchema
from typing import Tuple, Dict, Any

job_listing_schema = DataFrameSchema(
    columns={
        "listing_id": Column(str, nullable=False, unique=True, coerce=True),
        "company_name": Column(str, nullable=False, coerce=True),
        "source": Column(str, Check.isin(["LinkedIn", "Indeed", "Glassdoor", "Naukri"]), nullable=False, coerce=True),
        "days_live": Column(float, Check.in_range(0.0, 730.0), nullable=True, coerce=True),
        "salary_min": Column(float, Check.ge(0.0), nullable=True, coerce=True),
        "salary_max": Column(float, Check.ge(0.0), nullable=True, coerce=True),
        "description_text": Column(str, Check.str_length(min_value=15), nullable=False, coerce=True),
    },
    strict=False,
    coerce=True
)

def validate_dataset(df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates a dataset against the production schema.
    Returns (is_valid, validation_report).
    """
    report = {
        "total_records": len(df),
        "passed": False,
        "errors": []
    }
    
    # Pre-check required columns
    required_cols = ["listing_id", "company_name", "source", "description_text"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        report["errors"].append(f"Missing required columns: {missing}")
        return False, report
        
    try:
        validated_df = job_listing_schema.validate(df, lazy=True)
        report["passed"] = True
        report["valid_records"] = len(validated_df)
        return True, report
    except pa.errors.SchemaErrors as err:
        report["passed"] = False
        failure_cases = err.failure_cases
        report["errors"] = failure_cases.to_dict(orient="records")[:10]  # sample first 10
        return False, report

if __name__ == "__main__":
    test_path = "01_Datasets_Raw_Scrapes/naukri_saaf_v3_dataset.csv"
    print(f"Validating dataset: {test_path}...")
    df = pd.read_csv(test_path)
    
    # Map title to job_title if needed
    if "job_title" not in df.columns and "title" in df.columns:
        df["job_title"] = df["title"]
        
    valid, rep = validate_dataset(df)
    if valid:
        print(f"Validation PASSED! Total valid records: {rep['total_records']:,}")
    else:
        print(f"Validation FAILED with {len(rep['errors'])} schema errors:")
        for e in rep["errors"]:
            print(f"  * {e}")
        sys.exit(1)
