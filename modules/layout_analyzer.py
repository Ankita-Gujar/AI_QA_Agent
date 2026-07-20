from math import sqrt


class LayoutAnalyzer:

    def __init__(self):

        self.position_threshold = 10
        self.margin_threshold = 10
        self.alignment_threshold = 8

    # --------------------------------------------------
    # Distance
    # --------------------------------------------------

    def distance(self, obj1, obj2):

        return sqrt(
            (obj1.x - obj2.x) ** 2 +
            (obj1.y - obj2.y) ** 2
        )

    # --------------------------------------------------
    # Alignment
    # --------------------------------------------------

    def check_alignment(self, source, target):

        shift = abs(source.x - target.x)

        if shift <= self.alignment_threshold:
            return None

        return {

            "status": "ALIGNMENT",

            "message": f"Object shifted horizontally by {round(shift,1)} pt.",

            "value": shift
        }

    # --------------------------------------------------
    # Margin
    # --------------------------------------------------

    def check_margin(self, source, target):

        margin = abs(source.x - target.x)

        if margin <= self.margin_threshold:
            return None

        return {

            "status": "MARGIN",

            "message": "Margin changed.",

            "value": margin
        }

    # --------------------------------------------------
    # Overflow
    # --------------------------------------------------

    def check_overflow(self, source, target):

        if target.height > source.height + 25:

            return {

                "status": "OVERFLOW",

                "message": "Text overflow detected.",

                "value": target.height - source.height

            }

        return None

    # --------------------------------------------------
    # Underflow
    # --------------------------------------------------

    def check_underflow(self, source, target):

        if source.height > target.height + 25:

            return {

                "status": "UNDERFLOW",

                "message": "Text underflow detected.",

                "value": source.height - target.height

            }

        return None

    # --------------------------------------------------
    # Width Change
    # --------------------------------------------------

    def check_width(self, source, target):

        change = abs(source.width - target.width)

        if change <= 10:
            return None

        return {

            "status": "WIDTH_CHANGED",

            "message": "Object width changed.",

            "value": change

        }

    # --------------------------------------------------
    # Height Change
    # --------------------------------------------------

    def check_height(self, source, target):

        change = abs(source.height - target.height)

        if change <= 10:
            return None

        return {

            "status": "HEIGHT_CHANGED",

            "message": "Object height changed.",

            "value": change

        }

    # --------------------------------------------------
    # Page Movement
    # --------------------------------------------------

    def check_page_move(self, source, target):

        if source.page != target.page:

            return {

                "status": "PAGE_MOVED",

                "message": f"Moved from page {source.page} to page {target.page}"

            }

        return None

    # --------------------------------------------------
    # Analyze One Object
    # --------------------------------------------------

    def analyze(self, source, target):

        issues = []

        checks = [

            self.check_page_move,

            self.check_alignment,

            self.check_margin,

            self.check_overflow,

            self.check_underflow,

            self.check_width,

            self.check_height

        ]

        for check in checks:

            result = check(source, target)

            if result:

                issues.append(result)

        return issues