"""
Interactive CLI Labeling Tool for the Gold Standard Set
=======================================================
Run with: python src/labeling/annotate_cli.py

Presents listings one-by-one with key forensic signals and prompts for a human verdict.
Automatically saves after every annotation so progress survives across sessions.
"""

import os
import sys
import pandas as pd

CSV_PATH = "data/gold_labeling_sheet.csv"

def interactive_annotate():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found. Run sample_gold_set.py first.")
        return
        
    df = pd.read_csv(CSV_PATH)
    total = len(df)
    
    # Identify unlabeled rows
    def is_unlabeled(val):
        s = str(val).strip()
        return s not in ["0", "1", "0.0", "1.0", "-1"]
        
    unlabeled_indices = [i for i, v in enumerate(df["gold_label"]) if is_unlabeled(v)]
    labeled_count = total - len(unlabeled_indices)
    
    print("=" * 75)
    print("  NAUKRI SAAF — INTERACTIVE GOLD SET ANNOTATION TOOL")
    print(f"  Total Listings: {total} | Already Labeled: {labeled_count} | Remaining: {len(unlabeled_indices)}")
    print("=" * 75)
    print("Commands:")
    print("  [1] Flag as GHOST / FAKE (no real hiring intent)")
    print("  [0] Vouch as GENUINE (active, credible job)")
    print("  [-1] or [s] Mark as AMBIGUOUS / UNSURE")
    print("  [q] Quit and save")
    print("=" * 75)
    
    if len(unlabeled_indices) == 0:
        print("\nAll 180 listings are already annotated! Run `python src/labeling/evaluate_labels.py` to evaluate.")
        return
        
    for count, idx in enumerate(unlabeled_indices, start=1):
        row = df.iloc[idx]
        print(f"\n--- [{labeled_count + count}/{total}] Listing ID: {row['listing_id']} | Source: {row['source']} ---")
        print(f"Title       : {row['job_title']}")
        print(f"Company     : {row['company_name']}")
        print(f"Location    : {row['location_city']}")
        print(f"Days Live   : {row['days_live']} days")
        print(f"Salary      : {row['salary_range']}")
        print(f"Repost Count: {row['repost_count']}")
        print("\nDescription Snippet:")
        print("-" * 50)
        desc = str(row['description_snippet'])
        print(desc[:400] + ("..." if len(desc) > 400 else ""))
        print("-" * 50)
        
        while True:
            choice = input("Verdict [1=Ghost, 0=Genuine, -1/s=Unsure, f=Full Desc, q=Quit]: ").strip().lower()
            if choice == "q":
                df.to_csv(CSV_PATH, index=False)
                print(f"\nProgress saved. {labeled_count + count - 1}/{total} total labeled.")
                return
            elif choice == "f":
                print("\n=== FULL DESCRIPTION ===")
                print(str(row['full_description'])[:2000])
                print("========================\n")
            elif choice in ["1", "0", "-1"]:
                df.at[idx, "gold_label"] = int(choice)
                df.to_csv(CSV_PATH, index=False)
                break
            elif choice == "s":
                df.at[idx, "gold_label"] = -1
                df.to_csv(CSV_PATH, index=False)
                break
            else:
                print("Invalid input. Please enter 1, 0, -1, s, f, or q.")
                
    df.to_csv(CSV_PATH, index=False)
    print("\n" + "=" * 75)
    print(f"  CONGRATULATIONS! All {total} listings have been annotated.")
    print("  Run `python src/labeling/evaluate_labels.py` now to compute agreement metrics!")
    print("=" * 75)

if __name__ == "__main__":
    interactive_annotate()
