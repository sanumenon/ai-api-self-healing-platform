import re
from utils.milestone_printer import MilestonePrinter
from utils.dashboard import Dashboard

class AutoFixEngine:

    def __init__(self):
        self.printer = MilestonePrinter()
        self.dashboard = Dashboard()

    def apply_fix(self, failure, ai_result, collection_path):

        if failure.get("type") != "ASSERTION":
            return False

        correct_value = ai_result.get("correct_value")
        if not isinstance(correct_value, int):
            print("[AUTO-FIX] Skipping non-numeric fix")
            return False

        # validate numeric
        try:
            correct_value = int(correct_value)
        except:
            print("[AUTO-FIX] Invalid correct_value")
            return False

        try:
            with open(collection_path, "r") as f:
                data = f.read()

            original = data

            # 🔥 Handle multiple patterns
            patterns = [
                r"(response\.code\)\.to\.eql\()(\d+)(\))",
                r"(response\.code\)\.to\.equal\()(\d+)(\))",
                r"(pm\.response\.to\.have\.status\()(\d+)(\))",
                r"(to\.have\.status\()(\d+)(\))"
            ]

            for pattern in patterns:
                data = re.sub(pattern, lambda m: f"{m.group(1)}{correct_value}{m.group(3)}", data)

            if data == original:
                print("[AUTO-FIX] No change applied")
                return False

            with open(collection_path, "w") as f:
                f.write(data)

            print("[AUTO-FIX] Collection updated ✅")
            #self.printer.success("Auto-Fix Engine working")
            self.dashboard.log("Auto-Fix applied", "cyan")
            return True

        except Exception as e:
            print("[AUTO-FIX ERROR]", e)
            return False