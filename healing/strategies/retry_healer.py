import time

class RetryHealer:

    def __init__(self, config):
        self.max_attempts = config["retry"]["max_attempts"]
        self.retry_codes = config["retry"]["retry_status_codes"]

    def should_retry(self, failure):
        return failure["status"] in self.retry_codes

    def retry(self, rerun_callback):

        for attempt in range(self.max_attempts):
            print(f"[RETRY] Attempt {attempt+1}")

            result = rerun_callback()

            if result:
                return True

            time.sleep(1)

        return False