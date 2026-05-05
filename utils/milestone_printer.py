import time
import sys

class MilestonePrinter:

    def typewriter(self, text, delay=0.02):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def banner(self, text):
        print("\n" + "=" * 60)
        self.typewriter(f"🚀 {text}", 0.01)
        print("=" * 60)

    def success(self, text):
        self.typewriter(f"✅ {text}", 0.01)

    def highlight(self, text):
        self.typewriter(f"🔥 {text}", 0.01)

    def phase(self, phase_name):
        print("\n")
        self.banner(f"{phase_name} COMPLETED")