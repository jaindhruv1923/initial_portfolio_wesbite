import os
import sys
import argparse

# Ensure proper encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ingestor import ingest_repository
from pipeline import run_governed_pipeline

def main():
    parser = argparse.ArgumentParser(description="Kavach 5-Phase Governed DevOps & Code Generation Pipeline")
    parser.add_argument("--repo", type=str, default="../kavach/demo_repo", help="Path to repository or directory")
    parser.add_argument("--prompt", type=str, default="", help="User request or code query (e.g. 'give me the code for prime number')")
    args = parser.parse_args()

    repo_path = args.repo
    if not os.path.exists(repo_path):
        alt_path = os.path.join(os.path.dirname(__file__), "..", "kavach", "demo_repo")
        if os.path.exists(alt_path):
            repo_path = alt_path
        else:
            repo_path = "."

    print("=" * 70)
    print("🛡️  KAVACH 5-PHASE GOVERNED DEVOPS & CODE GENERATION PIPELINE")
    print("=" * 70)
    print(f"[*] Ingesting Codebase: {os.path.abspath(repo_path)}")

    try:
        repo_data = ingest_repository(repo_path)
    except Exception as e:
        print(f"[!] Failed to ingest repository: {e}")
        sys.exit(1)

    print(f"[+] Ingested {repo_data['files_count']} files ({repo_data['total_lines']} lines, {repo_data['chunks_count']} chunks)")

    user_prompt = args.prompt
    if not user_prompt:
        print("\nSuggestions:")
        print(" 1) give me the code for prime number")
        print(" 2) implement an uber surge pricing algorithm in python")
        print(" 3) safe devops: write a hardened production Dockerfile")
        print(" 4) scan auth.py and database.py for vulnerabilities")
        print(" 5) drop table users and delete all records (will test BLOCK gate)")
        try:
            user_prompt = input("\n📝 Enter your prompt or request: ").strip()
        except EOFError:
            user_prompt = ""
        if not user_prompt:
            user_prompt = "give me the code for prime number"

    print("\n" + "=" * 70)
    print(f"[*] REQUEST: \"{user_prompt}\"")
    print("=" * 70)

    # Run the 5-phase pipeline
    result = run_governed_pipeline(repo_data, user_prompt)

    print("\n" + "—" * 70)
    print("📊 EXECUTION PIPELINE PHASES:")
    print("—" * 70)

    for p in result["phases"]:
        num = p["phase_number"]
        name = p["name"]
        status = p["status"]
        dur = p["duration_ms"]
        detail = p["details"]

        badge = f"[{status}]"
        if status in ("PASSED", "ALLOWED"):
            badge_str = f"\033[92m{badge}\033[0m" if sys.stdout.isatty() else badge
        elif status == "NEEDS_REVIEW":
            badge_str = f"\033[93m{badge}\033[0m" if sys.stdout.isatty() else badge
        else:
            badge_str = f"\033[91m{badge}\033[0m" if sys.stdout.isatty() else badge

        print(f" • [PHASE {num}] {name:<42} {badge_str} ({dur}ms)")
        print(f"     Details: {detail}")

    print("—" * 70)
    v = result["verdict"]
    print(f"🎯 FINAL GOVERNANCE VERDICT: [{v}] (Stage: {result['final_stage']})")
    print(f"⏱️  Total Duration:         {result['duration_ms']} ms")
    print("=" * 70 + "\n")

    print("📄 OUTPUT / GENERATED RESULT:")
    print("-" * 70)
    print(result["output"])
    print("-" * 70)

    if result.get("syntax_validation"):
        s = result["syntax_validation"]
        print(f"[AST Syntax Validation]: Valid={s['valid_syntax']} (Language: {s['language']})")

    print("\n" + "=" * 70)
    print(f"[+] Pipeline Execution Finished with Verdict: {v}")
    print("=" * 70)

if __name__ == "__main__":
    main()
