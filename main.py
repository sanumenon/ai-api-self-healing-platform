import yaml
from runner.newman_runner import NewmanRunner
from analyzer.failure_analyzer import FailureAnalyzer
from healing.healing_engine import HealingEngine
from reporting.report_builder import ReportBuilder
from ai.ai_analyzer import AIAnalyzer
from healing.auto_fix_engine import AutoFixEngine
import os
from dotenv import load_dotenv
from pathlib import Path
from utils.milestone_printer import MilestonePrinter
from utils.dashboard import Dashboard

# 1. Try default loading (current + parent dirs)
load_dotenv()

# 2. Force load from project root (safe fallback)
env_path = Path(__file__).resolve().parent / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def load_config():
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)

def main():

    config = load_config()

    runner = NewmanRunner()
    analyzer = FailureAnalyzer()
    healer = HealingEngine(config)
    reporter = ReportBuilder()
    ai_analyzer = AIAnalyzer(config)
    auto_fixer = AutoFixEngine()
    #printer = MilestonePrinter()
    dashboard = Dashboard()

    #printer.banner("AI SELF-HEALING PLATFORM STARTED")
    dashboard.banner("AI SELF-HEALING PLATFORM")
    #print("🚀 Running Collection...")
    dashboard.log("Running collections...")

    for collection in config["collections"]:

        print(f"\n🚀 Running Collection: {collection['name']}")

        try:
            result = runner.run(
                collection["path"],
                collection.get("environment")
            )
        except FileNotFoundError as e:
            print(f"[WARNING] Skipping collection: {collection['name']} → {e}")
            continue
        except Exception as e:
            print(f"[ERROR] Unexpected error in {collection['name']} → {e}")
            continue

        
        failures = analyzer.analyze(result)

        if not failures:
            print(f"✅ {collection['name']} passed")
            continue

        for failure in failures:
            healed = healer.heal(
                failure,
                lambda: True ,
                collection.get("environment")
            )

            if healed:
                #printer.success("Healing Engine is working")
                dashboard.log("Healing Engine working")
                reporter.add_result(
                    failure["name"],
                    "HEALED_PASS",
                    collection["name"],
                    details=f"[{failure['type']}] Fixed and verified"
                )
            else:
                ai_result = None

                if failure["type"] in ["ASSERTION"]:
                    print(f"[AI TRIGGER] {failure['name']}")
                    ai_result = ai_analyzer.analyze(failure)
                    #printer.success("AI Analyzer is active")
                    dashboard.log("AI Analyzer active", "yellow")
                    if ai_result.get("confidence", 0) < 70:
                        print("[AI] Low confidence, skipping auto-fix")
                        continue
                    fixed = auto_fixer.apply_fix(
                        failure,
                        ai_result,
                        collection["path"]
                    )

                    if fixed:
                        print("[AUTO-FIX] Re-running collection...")

                        result = runner.run(
                            collection["path"],
                            collection.get("environment")
                        )

                        # re-check this failure
                        new_failures = analyzer.analyze(result)

                        if not any(f["name"] == failure["name"] for f in new_failures):
                            reporter.add_result(
                                failure["name"],
                                "AUTO_FIXED",
                                collection["name"],
                                details=f"AI fix applied → {ai_result}"
                            )
                            continue

                reporter.add_result(
                    failure["name"],
                    "FAILED",
                    collection["name"],
                    details=f"[{failure['type']}] {failure.get('message')} | AI: {ai_result}"
                )
                

    reporter.generate()        # Excel
    reporter.generate_html()  # HTML
    # printer.phase("PHASE 1")
    # printer.success("Self-healing engine stable")
    # printer.success("Auth + Retry working")

    # printer.phase("PHASE 2")
    # printer.success("AI Analyzer integrated")
    # printer.success("Auto-fix engine stable")
    # printer.success("No runtime failures")
    # printer.highlight("System is production-ready for evolution 🚀")
    dashboard.banner("PHASE COMPLETION")

    dashboard.log("Phase 1 → Healing Engine Stable")
    dashboard.log("Phase 2 → AI + Auto-Fix Integrated")
    dashboard.log("System Ready for Phase 3", "cyan")

    dashboard.summary(reporter.results)
if __name__ == "__main__":
    main()