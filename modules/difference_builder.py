from collections import defaultdict


class DifferenceBuilder:

    def __init__(self):
        self.reset_summary()

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def reset_summary(self):

        self.summary = {
            "total_issues": 0,
            "pages_with_issues": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "overall_status": "PASS"
        }

    # --------------------------------------------------
    # Main
    # --------------------------------------------------

    def build(self, match_result):

        self.reset_summary()

        report = defaultdict(list)

        self.add_issues(match_result["paragraphs"], "Paragraph", report)
        self.add_issues(match_result["images"], "Image", report)
        self.add_issues(match_result["tables"], "Table", report)

        self.summary["pages_with_issues"] = len(report)

        if self.summary["high"] > 0:
            self.summary["overall_status"] = "FAIL"

        elif self.summary["medium"] > 0:
            self.summary["overall_status"] = "WARNING"

        return {
            "summary": self.summary,
            "pages": dict(sorted(report.items()))
        }

    # --------------------------------------------------
    # Generic Builder
    # --------------------------------------------------

    def add_issues(self, objects, object_type, report):

        for item in objects:

            if item["status"] == "MATCH":
                continue

            issue = self.create_issue(object_type, item)

            report[issue["page"]].append(issue)

    # --------------------------------------------------
    # Create Issue
    # --------------------------------------------------

    def create_issue(self, object_type, item):

        severity = self.get_severity(item["status"])

        self.summary["total_issues"] += 1
        self.summary[severity.lower()] += 1

        return {

            "type": object_type,

            "status": item["status"],

            "severity": severity,

            "page": item.get("target_page") or item.get("source_page"),

            "message": self.get_message(object_type, item["status"]),

            "recommendation": self.get_recommendation(
                object_type,
                item["status"]
            )

        }

    # --------------------------------------------------
    # Severity
    # --------------------------------------------------

    def get_severity(self, status):

        severity = {

            "MISSING": "HIGH",

            "OVERFLOW": "HIGH",

            "UNDERFLOW": "HIGH",

            "PAGE_MOVED": "MEDIUM",

            "RESIZED": "MEDIUM",

            "EXTRA": "MEDIUM",

            "MOVED": "LOW"

        }

        return severity.get(status, "LOW")

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def get_message(self, object_type, status):

        messages = {

            ("Paragraph", "MISSING"):
                "Paragraph is missing.",

            ("Paragraph", "OVERFLOW"):
                "Text overflow detected.",

            ("Paragraph", "UNDERFLOW"):
                "Text underflow detected.",

            ("Paragraph", "MOVED"):
                "Paragraph position changed.",

            ("Paragraph", "PAGE_MOVED"):
                "Paragraph moved to another page.",

            ("Paragraph", "RESIZED"):
                "Paragraph size changed.",

            ("Image", "MISSING"):
                "Image is missing.",

            ("Image", "MOVED"):
                "Image position changed.",

            ("Image", "PAGE_MOVED"):
                "Image moved to another page.",

            ("Image", "RESIZED"):
                "Image size changed.",

            ("Table", "MISSING"):
                "Table is missing.",

            ("Table", "MOVED"):
                "Table position changed.",

            ("Table", "PAGE_MOVED"):
                "Table moved to another page.",

            ("Table", "RESIZED"):
                "Table size changed."

        }

        return messages.get(
            (object_type, status),
            "Layout issue detected."
        )

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    def get_recommendation(self, object_type, status):

        recommendations = {

            ("Paragraph", "MISSING"):
                "Insert the missing paragraph.",

            ("Paragraph", "OVERFLOW"):
                "Increase text frame or reduce font size.",

            ("Paragraph", "UNDERFLOW"):
                "Reduce frame height or verify content.",

            ("Paragraph", "MOVED"):
                "Align with source document.",

            ("Paragraph", "PAGE_MOVED"):
                "Move back to correct page.",

            ("Paragraph", "RESIZED"):
                "Resize text frame.",

            ("Image", "MISSING"):
                "Insert the missing image.",

            ("Image", "MOVED"):
                "Align image with source.",

            ("Image", "PAGE_MOVED"):
                "Move image to correct page.",

            ("Image", "RESIZED"):
                "Resize image.",

            ("Table", "MISSING"):
                "Insert the missing table.",

            ("Table", "MOVED"):
                "Align table with source.",

            ("Table", "PAGE_MOVED"):
                "Move table to correct page.",

            ("Table", "RESIZED"):
                "Resize table."

        }

        return recommendations.get(
            (object_type, status),
            "Verify against the source document."
        )