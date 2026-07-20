from math import sqrt


class ObjectMatcher:

    def __init__(self):

        # Position difference (points)
        self.position_threshold = 60

        # Size difference
        self.size_threshold = 20

        # Font difference
        self.font_threshold = 2

        # Confidence required
        self.match_threshold = 80

    # --------------------------------------------------
    # Euclidean Distance
    # --------------------------------------------------

    def distance(self, obj1, obj2):

        return sqrt(

            (obj1.x - obj2.x) ** 2 +

            (obj1.y - obj2.y) ** 2

        )

    # --------------------------------------------------
    # Width Difference
    # --------------------------------------------------

    def width_difference(self, obj1, obj2):

        return abs(obj1.width - obj2.width)

    # --------------------------------------------------
    # Height Difference
    # --------------------------------------------------

    def height_difference(self, obj1, obj2):

        return abs(obj1.height - obj2.height)

    # --------------------------------------------------
    # Area Difference
    # --------------------------------------------------

    def area_difference(self, obj1, obj2):

        area1 = obj1.width * obj1.height

        area2 = obj2.width * obj2.height

        return abs(area1 - area2)

    # --------------------------------------------------
    # Movement
    # --------------------------------------------------

    def movement(self, obj1, obj2):

        return self.distance(obj1, obj2)

    # --------------------------------------------------
    # Paragraph Score
    # --------------------------------------------------

    def paragraph_score(self, source, target):

        score = 0

        # Position

        move = self.movement(source, target)

        if move <= 20:
            score += 35

        elif move <= 40:
            score += 25

        elif move <= 60:
            score += 15

        # Width

        if self.width_difference(source, target) <= 15:
            score += 20

        # Height

        if self.height_difference(source, target) <= 15:
            score += 20

        # Font

        if abs(source.font_size - target.font_size) <= self.font_threshold:
            score += 10

        # Reading Order

        if abs(source.id - target.id) <= 2:
            score += 15

        return score

    # --------------------------------------------------
    # Image Score
    # --------------------------------------------------

    def image_score(self, source, target):

        score = 0

        if self.width_difference(source, target) <= 15:
            score += 35

        if self.height_difference(source, target) <= 15:
            score += 35

        if self.movement(source, target) <= 50:
            score += 30

        return score

    # --------------------------------------------------
    # Table Score
    # --------------------------------------------------

    def table_score(self, source, target):

        score = 0

        if self.width_difference(source, target) <= 15:
            score += 35

        if self.height_difference(source, target) <= 15:
            score += 35

        if self.movement(source, target) <= 50:
            score += 30

        return score

    # --------------------------------------------------
    # Layout Classification
    # --------------------------------------------------

    def classify_layout_change(
        self,
        source,
        target,
        score
    ):

        move = self.movement(source, target)

        width_change = self.width_difference(source, target)

        height_change = self.height_difference(source, target)

        if score >= 85:

            return "MATCH"

        if move > 120:

            return "PAGE_MOVED"

        if move > 60:

            return "MOVED"

        if target.height > source.height + 40:
            return "OVERFLOW"

        if source.height > target.height + 40:
            return "UNDERFLOW"

        if target.height < source.height - 40:

            return "UNDERFLOW"

        if width_change > 30:

            return "RESIZED"

        return "MATCH"

    # --------------------------------------------------
    # Severity
    # --------------------------------------------------

    def severity(self, status):

        mapping = {

            "MATCH": "LOW",

            "MOVED": "LOW",

            "PAGE_MOVED": "MEDIUM",

            "RESIZED": "MEDIUM",

            "OVERFLOW": "HIGH",

            "UNDERFLOW": "HIGH",

            "MISSING": "HIGH",

            "EXTRA": "MEDIUM"

        }

        return mapping.get(status, "LOW")

# --------------------------------------------------
# Paragraph Matching
# --------------------------------------------------

    def match_paragraphs(self, source_doc, target_doc):

        matches = []

        # Flatten all target paragraphs
        target_objects = []

        for page in target_doc.pages:
            for para in page.paragraphs:
                target_objects.append(para)

        # Use page + id as unique identifier
        used = set()

        for source_page in source_doc.pages:

            for source_para in source_page.paragraphs:

                best_target = None
                best_score = -1

                for target_para in target_objects:

                    target_key = (
                        target_para.page,
                        target_para.id
                    )

                    if target_key in used:
                        continue

                    score = self.paragraph_score(
                        source_para,
                        target_para
                    )

                    if score > best_score:

                        best_score = score
                        best_target = target_para

                # ----------------------------
                # Missing paragraph
                # ----------------------------

                if best_target is None:

                    matches.append({

                        "type": "Paragraph",

                        "status": "MISSING",

                        "severity": "HIGH",

                        "confidence": 0,

                        "source_page": source_para.page,

                        "target_page": None,

                        "source_bbox": source_para.bbox,

                        "target_bbox": None

                    })

                    continue

                target_key = (
                    best_target.page,
                    best_target.id
                )

                used.add(target_key)

                status = self.classify_layout_change(

                    source_para,

                    best_target,

                    best_score

                )

                matches.append({

                    "type": "Paragraph",

                    "status": status,

                    "severity": self.severity(status),

                    "confidence": best_score,

                    "movement": round(
                        self.movement(
                            source_para,
                            best_target
                        ),
                        2
                    ),

                    "width_change": round(
                        self.width_difference(
                            source_para,
                            best_target
                        ),
                        2
                    ),

                    "height_change": round(
                        self.height_difference(
                            source_para,
                            best_target
                        ),
                        2
                    ),

                    "source_page": source_para.page,

                    "target_page": best_target.page,

                    "source_bbox": source_para.bbox,

                    "target_bbox": best_target.bbox

                })

        return matches
    # --------------------------------------------------
# Image Matching
# --------------------------------------------------

    def match_images(self, source_doc, target_doc):

        matches = []

        target_images = []

        for page in target_doc.pages:
            target_images.extend(page.images)

        used = set()

        for source_page in source_doc.pages:

            for source_img in source_page.images:

                best = None
                best_score = -1

                for target in target_images:

                    key = (
                        target.page,
                        target.id
                    )

                    if key in used:
                        continue

                    score = self.image_score(
                        source_img,
                        target
                    )

                    if score > best_score:

                        best_score = score
                        best = target

                if best is None:

                    matches.append({

                        "type": "Image",

                        "status": "MISSING",

                        "severity": "HIGH",

                        "confidence": 0,

                        "source_page": source_img.page

                    })

                    continue

                used.add((best.page, best.id))

                status = self.classify_layout_change(

                    source_img,

                    best,

                    best_score

                )

                matches.append({

                    "type": "Image",

                    "status": status,

                    "severity": self.severity(status),

                    "confidence": best_score,

                    "movement": round(
                        self.movement(
                            source_img,
                            best
                        ),
                        2
                    ),

                    "source_page": source_img.page,

                    "target_page": best.page

                })

        return matches
    # --------------------------------------------------
# Table Matching
# --------------------------------------------------

    def match_tables(self, source_doc, target_doc):

        matches = []

        target_tables = []

        for page in target_doc.pages:
            target_tables.extend(page.tables)

        used = set()

        for source_page in source_doc.pages:

            for source_tbl in source_page.tables:

                best = None
                best_score = -1

                for target in target_tables:

                    key = (
                        target.page,
                        target.id
                    )

                    if key in used:
                        continue

                    score = self.table_score(
                        source_tbl,
                        target
                    )

                    if score > best_score:

                        best_score = score
                        best = target

                if best is None:

                    matches.append({

                        "type": "Table",

                        "status": "MISSING",

                        "severity": "HIGH",

                        "confidence": 0,

                        "source_page": source_tbl.page

                    })

                    continue

                used.add((best.page, best.id))

                status = self.classify_layout_change(

                    source_tbl,

                    best,

                    best_score

                )

                matches.append({

                    "type": "Table",

                    "status": status,

                    "severity": self.severity(status),

                    "confidence": best_score,

                    "movement": round(
                        self.movement(
                            source_tbl,
                            best
                        ),
                        2
                    ),

                    "source_page": source_tbl.page,

                    "target_page": best.page

                })

        return matches
    # --------------------------------------------------
# Compare Complete Documents
# --------------------------------------------------

    def compare(self, source_doc, target_doc):

        paragraph_matches = self.match_paragraphs(
            source_doc,
            target_doc
        )

        image_matches = self.match_images(
            source_doc,
            target_doc
        )

        table_matches = self.match_tables(
            source_doc,
            target_doc
        )

        all_matches = (

            paragraph_matches +

            image_matches +

            table_matches

        )

        # ----------------------------------------
        # Summary
        # ----------------------------------------

        summary = {

            "total_objects": len(all_matches),

            "matched": 0,

            "moved": 0,

            "page_moved": 0,

            "resized": 0,

            "overflow": 0,

            "underflow": 0,

            "missing": 0,

            "extra": 0

        }

        for item in all_matches:

            status = item["status"]

            if status == "MATCH":
                summary["matched"] += 1

            elif status == "MOVED":
                summary["moved"] += 1

            elif status == "PAGE_MOVED":
                summary["page_moved"] += 1

            elif status == "RESIZED":
                summary["resized"] += 1

            elif status == "OVERFLOW":
                summary["overflow"] += 1

            elif status == "UNDERFLOW":
                summary["underflow"] += 1

            elif status == "MISSING":
                summary["missing"] += 1

            elif status == "EXTRA":
                summary["extra"] += 1

        # ----------------------------------------
        # Return
        # ----------------------------------------

        return {

            "summary": summary,

            "paragraphs": paragraph_matches,

            "images": image_matches,

            "tables": table_matches

        }