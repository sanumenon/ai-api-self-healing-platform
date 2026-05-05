import os
import json

class AIAnalyzer:

    def __init__(self, config):
        self.config = config
        self.provider = config.get("llm", {}).get("provider", "none")
        self.model = config.get("llm", {}).get("model", "gpt-4o-mini")

        self.call_count = 0
        self.max_calls = 10

        self.client = None

        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=api_key)
                except Exception as e:
                    print(f"[AI INIT ERROR] {str(e)}")
            else:
                print("[AI INIT] No API key found")

    def analyze(self, failure):

        if self.provider != "openai":
            return {"insight": "LLM disabled"}

        if not self.client:
            return {"insight": "OpenAI client not initialized"}

        if self.call_count >= self.max_calls:
            return {"insight": "AI limit reached"}

        self.call_count += 1
        print(f"[AI CALL] {self.call_count}/{self.max_calls}")

        prompt = self._build_prompt(failure)

        return self._call_openai(prompt)

    def _build_prompt(self, failure):

        return f"""
You are an API test failure analyzer.

Failure:
- Name: {failure.get("name")}
- Type: {failure.get("type")}
- Status: {failure.get("status")}
- Message: {failure.get("message")}

Tasks:
1. Identify root cause (AUTH / DATA / ASSERTION / SERVER / PERMISSION)
2. If ASSERTION:
   - What should the correct expected value be?
   - Why did it fail?
3. Suggest fix (test change or data fix)
4. Confidence (0-100)

Return STRICT JSON only:
{{
  "root_cause": "ASSERTION",
  "suggested_fix": "Change expected status to 404",
  "correct_value": 404,
  "confidence": 90
}}
"""

    def _call_openai(self, prompt):

        if not self.client:
            return {"insight": "No API client initialized"}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            content = response.choices[0].message.content

            try:
                return json.loads(content)
            except:
                print("[AI ERROR] Invalid JSON:", content)
                return {}

        except Exception as e:
            return {"error": str(e)}
    
    def _safe_json_parse(self, content):

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            print("[AI ERROR] Invalid JSON:", content)

            # Attempt recovery if model added extra text
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                cleaned = content[start:end]
                return json.loads(cleaned)
            except Exception:
                return {"insight": "Invalid JSON from AI"}
