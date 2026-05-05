
from openpyxl import Workbook

class ReportBuilder:

    def __init__(self):
        self.results = []

    def add_result(self, test_name, status, collection, details=None):
        self.results.append({
            "collection": collection,
            "test": test_name,
            "status": status,
            "details": details
        })

    def generate(self):

        print("\n===== TEST REPORT =====")

        wb = Workbook()
        ws = wb.active
        ws.title = "Test Results"

        # Header
        ws.append(["Collection", "Test Name", "Status", "Details"])

        # Data
        for r in self.results:
            print(f"{r['test']} → {r['status']} ({r.get('details', '-')})")

            ws.append([
                r["collection"],
                r["test"],
                r["status"],
                str(r.get("details", "-"))
            ])

        # Save file
        wb.save("test_report.xlsx")

        print("\n📊 Excel report generated: test_report.xlsx")

    def generate_html(self):

        html = """
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body { font-family: Arial; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; }
                th { background-color: #f2f2f2; }
                .PASS { background-color: #d4edda; }
                .FAILED { background-color: #f8d7da; }
                .HEALED_PASS { background-color: #fff3cd; }
            </style>
        </head>
        <body>
            <h2>API Test Report</h2>
            <table>
                <tr>
                    <th>Collection</th>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Details</th>
                </tr>
        """

        for r in self.results:
            status_class = r["status"]

            html += f"""
            <tr class="{status_class}">
                <td>{r['collection']}</td>
                <td>{r['test']}</td>
                <td>{r['status']}</td>
                <td>{r.get('details', '-')}</td>
            </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        with open("test_report.html", "w") as f:
            f.write(html)

        print("🌐 HTML report generated: test_report.html")