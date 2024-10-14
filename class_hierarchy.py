class ClauseHierarchy:
    def __init__(self, name, number, rank, desc=None, preamble=None):
        self.name = name
        self.number = number
        self.rank = rank
        self.desc = desc
        self.preamble = preamble
        self.internal_reference = [] # Clause reference within the same Section
        self.external_reference = [] # Clause reference external to the Section

    def __str__(self):
        return (f"{self.name} {self.number} (Rank: {self.rank})\n"
                f"Description: {self.desc}\nPreamble: {self.preamble}")

# Title Class
class Title(ClauseHierarchy):
    def __init__(self, number, desc, name="Title", preamble=None):
        super().__init__(name, number, rank=1, desc=desc, preamble=preamble)

# Chapter Class within a Title
class Chapter(ClauseHierarchy):
    def __init__(self, number, desc, title, name="Chapter", preamble=None):
        super().__init__(name, number, rank=2, desc=desc, preamble=preamble)
        self.title = title
    @property
    def full_title(self):
        return self.title

# Subchapter Class within a Chapter
class Subchapter(ClauseHierarchy):
    def __init__(self, number, desc, chapter, name="Subchapter", preamble=None):
        super().__init__(name, number, rank=3, desc=desc, preamble=preamble)
        self.chapter = chapter
        self.title = chapter.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter

# Part Class within a Subchapter
class Part(ClauseHierarchy):
    def __init__(self, number, desc, subchapter, name="Part", preamble=None):
        super().__init__(name, number, rank=4, desc=desc, preamble=preamble)
        self.subchapter = subchapter
        self.chapter = subchapter.chapter
        self.title = subchapter.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter
    @property
    def full_subchapter(self):
        return self.subchapter

# Section Class within a Part
class Section(ClauseHierarchy):
    def __init__(self, number, desc, part, name="Section", preamble=None):
        super().__init__(name, number, rank=5, desc=desc, preamble=preamble)
        self.part = part
        self.subchapter = part.subchapter
        self.chapter = part.chapter
        self.title = part.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter
    @property
    def full_subchapter(self):
        return self.subchapter
    @property
    def full_part(self):
        return self.part

# Subsection Class within a Section
class Subsection(ClauseHierarchy):
    def __init__(self, number, desc, section, name="Subsection", preamble=None):
        super().__init__(name, number, rank=6, desc=desc, preamble=preamble)
        self.section = section
        self.part = section.part
        self.subchapter = section.subchapter
        self.chapter = section.chapter
        self.title = section.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter
    @property
    def full_subchapter(self):
        return self.subchapter
    @property
    def full_part(self):
        return self.part
    @property
    def full_section(self):
        return self.section

# Clause Class within a Subsection
class Clause(ClauseHierarchy):
    def __init__(self, number, desc, subsection, name="Clause", preamble=None):
        super().__init__(name, number, rank=7, desc=desc, preamble=preamble)
        self.subsection = subsection
        self.section = subsection.section
        self.part = subsection.part
        self.subchapter = subsection.subchapter
        self.chapter = subsection.chapter
        self.title = subsection.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter
    @property
    def full_subchapter(self):
        return self.subchapter
    @property
    def full_part(self):
        return self.part
    @property
    def full_subsection(self):
        return self.subsection
    @property
    def full_section(self):
        return self.section

# Subclause Class within a Clause
class Subclause(ClauseHierarchy):
    def __init__(self, number, desc, clause, name="Subclause", preamble=None):
        super().__init__(name, number, rank=8, desc=desc, preamble=preamble)
        self.clause = clause
        self.subsection = clause.subsection
        self.section = clause.section
        self.part = clause.part
        self.subchapter = clause.subchapter
        self.chapter = clause.chapter
        self.title = clause.title
    @property
    def full_title(self):
        return self.title
    @property
    def full_chapter(self):
        return self.chapter
    @property
    def full_subchapter(self):
        return self.subchapter
    @property
    def full_part(self):
        return self.part
    @property
    def full_subsection(self):
        return self.subsection
    @property
    def full_clause(self):
        return self.clause
    @property
    def full_section(self):
        return self.section

CLASS_MAP = {
    
}