from datetime import datetime
print("NEW REPORT GENERATOR LOADED")

class ReportGenerator:

    def __init__(self):
        pass

    # ----------------------------------------------------
    # Generate Text Report
    # ----------------------------------------------------

    def generate(
        self,
        source_file,
        target_file,
        source_language,
        target_language,
        difference_report
    ):

        report = []

        report.append("=" * 70)
        report.append("                     AI DTP QA REPORT")
        report.append("=" * 70)
        report.append("")
        report.append(f"Generated        : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append(f"Source PDF       : {source_file}")
        report.append(f"Target PDF       : {target_file}")
        report.append(f"Source Language  : {source_language}")
        report.append(f"Target Language  : {target_language}")
        report.append("")

        summary = difference_report["summary"]

        report.append("=" * 70)
        report.append("SUMMARY")
        report.append("=" * 70)

        report.append(f"Overall Status   : {summary.get('overall_status')}")
        report.append(f"Total Pages      : {summary.get('total_pages')}")
        report.append(f"Pages With Issues: {summary.get('pages_with_issues')}")
        report.append(f"Total Issues     : {summary.get('total_issues')}")
        report.append(f"High Severity    : {summary.get('high')}")
        report.append(f"Medium Severity  : {summary.get('medium')}")
        report.append(f"Low Severity     : {summary.get('low')}")

        report.append("")

        report.append("=" * 70)
        report.append("PAGE WISE ISSUES")
        report.append("=" * 70)

        pages = difference_report.get("pages", {})

        for page_no, issues in pages.items():

            report.append("")
            report.append("-" * 70)
            report.append(f"PAGE : {page_no}")
            report.append(f"TOTAL ISSUES : {len(issues)}")
            report.append("-" * 70)

            for i, issue in enumerate(issues, start=1):

                report.append("")
                report.append(f"Issue #{i}")

                report.append(f"Type            : {issue.get('type')}")
                report.append(f"Status          : {issue.get('status')}")
                report.append(f"Severity        : {issue.get('severity')}")
                report.append(f"Message         : {issue.get('message')}")
                report.append(f"Recommendation  : {issue.get('recommendation')}")
                report.append(f"Confidence      : {issue.get('confidence',0)}%")
                report.append(f"Movement        : {issue.get('movement',0)}")
                report.append(f"Width Change    : {issue.get('width_change',0)}")
                report.append(f"Height Change   : {issue.get('height_change',0)}")

                bbox = issue.get("bbox")

                if bbox:
                    report.append(f"Bounding Box    : {bbox}")

                report.append("")

        report.append("=" * 70)
        report.append("DESIGNER ACTIONS")
        report.append("=" * 70)

        report.append("")
        report.append("HIGH PRIORITY")
        report.append("• Fix missing images.")
        report.append("• Fix missing paragraphs.")
        report.append("• Resolve text overflow.")
        report.append("• Resolve text underflow.")

        report.append("")
        report.append("MEDIUM PRIORITY")
        report.append("• Restore objects moved to wrong pages.")
        report.append("• Correct page flow.")

        report.append("")
        report.append("LOW PRIORITY")
        report.append("• Align paragraphs.")
        report.append("• Align images.")
        report.append("• Improve layout consistency.")

        report.append("")
        report.append("=" * 70)
        report.append("END OF REPORT")
        report.append("=" * 70)

        return "\n".join(report)

    # ----------------------------------------------------
    # Save Report
    # ----------------------------------------------------

    def save(self, report_text, output_file):

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_text)
print("========== REPORT GENERATOR ==========")
print(ReportGenerator.generate)