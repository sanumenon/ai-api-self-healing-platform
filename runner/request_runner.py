import requests


class RequestRunner:

    def run(self, request_obj, env):

        method = request_obj.get("method")
        url = self._build_url(request_obj.get("url"), env)

        if not url:
            print("[ERROR] URL could not be built from request")
            return None

        headers = {}

        # 🔁 Replace variables in headers
        for h in request_obj.get("header", []):
            headers[h["key"]] = self._replace_vars(h["value"], env)

        # 🔥 FORCE AUTH HEADER
        for v in env["values"]:
            if v["key"].startswith("auth0_access_token"):
                headers["Authorization"] = f"Bearer {v['value']}"
                break

        data = None
        if request_obj.get("body"):
            if request_obj["body"].get("mode") == "raw":
                data = self._replace_vars(request_obj["body"].get("raw"), env)

        print(f"[RERUN] {method} {url}")

        # 🔥 Safety check
        if not url or "None" in url:
            print("[ERROR] Invalid URL after processing")
            return None

        try:
            return requests.request(
                method,
                url,
                headers=headers,
                data=data,
                timeout=15  # 🔥 prevent hanging
            )
        except Exception as e:
            print(f"[REQUEST ERROR] {e}")
            return None

    def _replace_vars(self, text, env):

        if not text:
            return text

        for v in env["values"]:
            key = v["key"]
            value = v["value"]

            if f"{{{{{key}}}}}" in text:
                print(f"[VAR] {key} → {value}")
                text = text.replace(f"{{{{{key}}}}}", str(value))

        return text

    def _build_url(self, url_obj, env):

        if not url_obj:
            return None

        # ✅ Use raw URL from Postman
        if isinstance(url_obj, dict) and url_obj.get("raw"):
            raw_url = url_obj["raw"]

            # 🔥 Fix double protocol issue
            raw_url = raw_url.replace("https://https://", "https://")
            raw_url = raw_url.replace("http://http://", "http://")

            url = self._replace_vars(raw_url, env)

            if not url or "None" in url:
                return None

            return url

        # fallback
        if isinstance(url_obj, str):
            url = self._replace_vars(url_obj, env)

            if not url or "None" in url:
                return None

            return url

        return None