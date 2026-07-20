import json


class PromptBuilder:

    def __init__(
        self,
        source_language,
        target_language
    ):

        self.source_language = source_language
        self.target_language = target_language

    # -------------------------------------------------

    def build(self, differences):

        prompt = f"""
ROLE: You are a Senior DTP QA Engineer with 15+ years of experience in multilingual publishing, localization QA, and desktop publishing.

====================================================
PROJECT INFORMATION
====================================================

Source Language : {self.source_language}

Target Language : {self.target_language}

The translation has already been approved.

DO NOT CHECK

- Translation
- Grammar
- Spelling
- Meaning
- Font Name
- Minor Font Size Difference

ONLY CHECK

- Missing Paragraphs
- Missing Images
- Missing Tables
- Text Overflow
- Text Underflow
- Layout Changes
- Object Movement
- Alignment Problems
- Page Flow

====================================================
COMPARISON RESULT
====================================================

{json.dumps(differences, separators=(",", ":"))}
====================================================
TASK
====================================================

Using ONLY the comparison result above, prepare a professional DTP QA report.

IMPORTANT RULES

1. DO NOT return JSON.

2. DO NOT return Python dictionaries.

3. DO NOT explain your reasoning.

4. DO NOT mention AI.

5. DO NOT use Markdown code blocks.

6. Write a clean professional report.

====================================================
REPORT FORMAT
====================================================

AI DTP QA REPORT

----------------------------------------------------

DOCUMENT INFORMATION

Source Language :
Target Language :

----------------------------------------------------

OVERALL STATUS

PASS / WARNING / FAIL

----------------------------------------------------

QA SUMMARY

Total Pages :
Pages With Issues :
Total Issues :
High Severity :
Medium Severity :
Low Severity :

----------------------------------------------------

PAGE 1

Issue 1

Type :

Severity :

Status :

Problem :

Recommendation :

--------------------------------

Issue 2

Type :

Severity :

Status :

Problem :

Recommendation :

Continue the same format for every issue on every page.

----------------------------------------------------

DESIGNER ACTION ITEMS

HIGH PRIORITY

- ...

- ...

MEDIUM PRIORITY

- ...

LOW PRIORITY

- ...

----------------------------------------------------

FINAL REMARK

Write a short professional conclusion for the designer.

End of report.

Return ONLY the report.
"""

        return prompt