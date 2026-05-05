import yaml
from analyzer.failure_analyzer import FailureAnalyzer
from healing.healing_engine import HealingEngine
from reporting.report_builder import ReportBuilder
from ai.ai_analyzer import AIAnalyzer


def load_config():
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)


# 🔥 MOCK FAILURE (simulate Newman output)
def get_mock_failures():
    return [
        {
            "name": "TC01 Unauthorized access",
            "status": 401,
            "message": "Unauthorized",
            "type": "AUTH",
            "source": {
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": "https://api.example.com/user"
                    },
                    "header": []
                }
            }
        },
        {
            "name": "TC02 Expected 403 but got 200",
            "status": 200,
            "message": "expected 403 but got 200",
            "type": "PERMISSION",
            "source": {}
        },
        {
            "name": "TC03 Server error",
            "status": 500,
            "message": "Internal Server Error",
            "type": "SERVER",
            "source": {
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": "https://api.example.com/retry"
                    },
                    "header": []
                }
            }
        }
    ]


def main():

    print("🧪 Phase 2 Test Harness Running...\n")

    config = load_config()

    analyzer = FailureAnalyzer()
    healer = HealingEngine(config)
    reporter = ReportBuilder()
    ai_analyzer = AIAnalyzer(config)

    failures = get_mock_failures()

    for failure in failures:

        print(f"\n🔍 Testing: {failure['name']}")

        healed = healer.heal(
            failure,
            lambda: True,
            "collections/env/user_env.json"   # dummy path
        )

        if healed:
            reporter.add_result(
                failure["name"],
                "HEALED_PASS",
                "mock",
                details="Healed successfully"
            )
        else:
            ai_result = ai_analyzer.analyze(failure)

            reporter.add_result(
                failure["name"],
                "FAILED",
                "mock",
                details=f"{failure['message']} | AI: {ai_result}"
            )

    reporter.generate()
    reporter.generate_html()


if __name__ == "__main__":
    main()