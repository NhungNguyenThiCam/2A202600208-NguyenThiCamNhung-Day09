"""
run_all.py — Run full pipeline: build index → test → evaluate
Chạy script này để hoàn thành toàn bộ lab.

Usage:
    python run_all.py
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and print status"""
    print("\n" + "=" * 60)
    print(f"▶ {description}")
    print("=" * 60)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Success: {description}")
    return True

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   Lab Day 09 — Multi-Agent Orchestration                ║
║   Full Pipeline Runner                                   ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # Step 1: Build index
    if not run_command("python build_index.py", "Step 1: Build ChromaDB Index"):
        print("\n⚠️  Index build failed. Check if sentence-transformers is installed.")
        print("   Run: pip install sentence-transformers")
        return
    
    # Step 2: Test graph
    if not run_command("python graph.py", "Step 2: Test Graph with Sample Queries"):
        print("\n⚠️  Graph test failed. Check errors above.")
        return
    
    # Step 3: Run evaluation
    if not run_command("python eval_trace.py", "Step 3: Run Evaluation on Test Questions"):
        print("\n⚠️  Evaluation failed. Check errors above.")
        return
    
    # Step 4: Analyze traces
    if not run_command("python eval_trace.py --analyze", "Step 4: Analyze Traces"):
        print("\n⚠️  Analysis failed.")
        return
    
    # Step 5: Compare single vs multi
    if not run_command("python eval_trace.py --compare", "Step 5: Compare Single vs Multi"):
        print("\n⚠️  Comparison failed.")
        return
    
    print("\n" + "=" * 60)
    print("✅ ALL STEPS COMPLETED!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("   1. Review traces in: artifacts/traces/")
    print("   2. Check eval report: artifacts/eval_report.json")
    print("   3. Fill in documentation templates in: docs/")
    print("   4. Write group report: reports/group_report.md")
    print("   5. Write individual reports: reports/individual/")
    print("\n⏰ At 17:00, run: python eval_trace.py --grading")
    print("   to generate grading_run.jsonl")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
