class FailureAnalyzer:

    def analyze(self, report):

        failures = []

        for f in report.get("run", {}).get("failures", []):

            error = f.get("error", {})
            source = f.get("source", {})

            failure = {
                "name": source.get("name") or f.get("at"),
                "status": error.get("statusCode"),
                "message": self.extract_message(f),
                "type": self.classify_failure(f, error),
                "raw": error,
                "source": source
            }

            failures.append(failure)

        return failures

    def extract_message(self, f):

        error = f.get("error", {})

        if error.get("message"):
            return error.get("message")

        if f.get("at"):
            return f.get("at")

        return str(error) if error else "Unknown error"

    def classify_failure(self, f, error):

        msg = str(error).lower()

        if "prerequest" in f.get("at", "").lower():
            return "PREREQUEST"

        if "401" in msg or "unauthorized" in msg:
            return "AUTH"

        if any(code in msg for code in ["500", "502", "503"]):
            return "SERVER"
        
        if "expected 403" in msg:
            return "PERMISSION"

        if "assertionerror" in msg or "expected" in msg:
            return "ASSERTION"

        if "cannot read" in msg or "undefined" in msg:
            return "DATA"

        return "UNKNOWN"