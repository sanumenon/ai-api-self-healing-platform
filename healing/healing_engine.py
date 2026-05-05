from healing.strategies.auth_healer import AuthHealer
from healing.strategies.retry_healer import RetryHealer
from utils.env_updater import update_env_token, load_env
from runner.request_runner import RequestRunner


class HealingEngine:

    def __init__(self, config):
        self.config = config
        self.auth_healer = AuthHealer(config)
        self.retry_healer = RetryHealer(config)
        self.request_runner = RequestRunner()
        self.token_attempted_users = set()

    def heal(self, failure, rerun_callback, env_path):

        failure_type = failure.get("type")
        status = failure.get("status")

        env = load_env(env_path)

        # 🔥 Only heal meaningful failures
        if failure_type not in ["AUTH", "SERVER"]:
            print(f"[SKIP HEAL] {failure_type}")
            return False

        request_obj = failure.get("source", {}).get("request")

        # 🔥 Strict validation (Newman limitation handling)
        if not request_obj:
            print("[SKIP HEAL] No request object")
            return False

        url_obj = request_obj.get("url")

        if not url_obj:
            print("[SKIP HEAL] Missing URL in request")
            return False

        if isinstance(url_obj, dict) and not url_obj.get("raw"):
            print("[SKIP HEAL] URL has no raw value")
            return False

        if isinstance(url_obj, str) and not url_obj.strip():
            print("[SKIP HEAL] Empty URL string")
            return False

        # 🔐 AUTH HEAL
        if failure_type == "AUTH":

            user_email = self.extract_user_from_failure(failure)

            # ✅ Reuse token if already fetched
            if user_email in self.token_attempted_users:
                print("[HEAL] Using existing token")

                response = self.request_runner.run(request_obj, env)

                if response and response.status_code == 200:
                    print("[HEAL SUCCESS] ✅")
                    return True

                print("[HEAL FAILED] ❌")
                return False

            # 🔥 First-time token fetch
            self.token_attempted_users.add(user_email)

            token = self.auth_healer.get_token(user_email)

            if token:
                key = f"auth0_access_token_{user_email}"
                update_env_token(env_path, key, token)

                print("[HEAL] Token updated → verifying...")

                env = load_env(env_path)

                response = self.request_runner.run(request_obj, env)

                if response and response.status_code == 200:
                    print("[HEAL SUCCESS] ✅")
                    return True

            print("[HEAL FAILED] ❌")
            return False

        # 🔁 SERVER RETRY HEAL
        if status in [500, 502, 503]:

            print("[HEAL] Retrying request...")

            response = self.request_runner.run(request_obj, env)

            if response and response.status_code < 500:
                print("[RETRY SUCCESS] ✅")
                return True

        print(f"[DEBUG] Failure Type: {failure_type}")
        return False

    def extract_user_from_failure(self, failure):

        name = (failure.get("name") or "").lower()

        if "admin" in name or "super" in name or "chimp admin" in name:
            return "qa-regression-user-super@ci.com"

        return "qa-regression-user@ci.com"