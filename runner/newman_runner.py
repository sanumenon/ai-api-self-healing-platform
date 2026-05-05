import subprocess
import json
import os

class NewmanRunner:

    def run(self, collection_path, env_path=None):

        # ✅ Get project root
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # ✅ Convert to absolute paths
        full_collection_path = os.path.join(BASE_DIR, collection_path)
        full_env_path = os.path.join(BASE_DIR, env_path) if env_path else None

        # 🔍 Debug prints
        print(f"[DEBUG] Collection Path: {full_collection_path}")
        print(f"[DEBUG] Env Path: {full_env_path}")

        # ❌ Validate existence BEFORE running
        if not os.path.exists(full_collection_path):
            raise FileNotFoundError(f"Collection not found: {full_collection_path}")

        if full_env_path and not os.path.exists(full_env_path):
            raise FileNotFoundError(f"Environment file not found: {full_env_path}")

        report_path = os.path.join(BASE_DIR, "newman_report.json")

        command = [
            "newman", "run", full_collection_path,
            "--reporters", "json",
            "--reporter-json-export", report_path
        ]

        if full_env_path:
            command.extend(["--environment", full_env_path])

        print(f"[RUNNING] {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        print(result.stdout)
        print(result.stderr)

        if result.returncode != 0:
            print("[WARNING] Newman reported failures, continuing...")

        # Still check if report exists
        if not os.path.exists(report_path):
            raise FileNotFoundError("Newman report not generated")

        if not os.path.exists(report_path):
            raise FileNotFoundError("Newman report not generated")

        with open(report_path) as f:
            return json.load(f)