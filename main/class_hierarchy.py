class ClauseHierarchy:
    def __init__(self, name, number, rank, desc=None, preamble=None, parent=None):
        self.name = name
        self.number = number
        self.rank = rank
        self.desc = desc
        self.preamble = preamble
        self.parent = parent
        self.internal_reference = []
        self.external_reference = []

    def __str__(self):
        return (f"{self.name} {self.number} (Rank: {self.rank})\n"
                f"Description: {self.desc}\nPreamble: {self.preamble}")
    
    @property
    def title(self):
        if isinstance(self, Title):
            return self
        elif self.parent:
            return self.parent.title
        else:
            return None
    @property
    def chapter(self):
        if isinstance(self, Chapter):
            return self
        elif self.parent:
            return self.parent.chapter
        else:
            return None
    @property
    def subchapter(self):
        if isinstance(self, Subchapter):
            return self
        elif self.parent:
            return self.parent.subchapter
        else:
            return None
    @property
    def part(self):
        if isinstance(self, Part):
            return self
        elif self.parent:
            return self.parent.part
        else:
            return None
    @property
    def section(self):
        if isinstance(self, Section):
            return self
        elif self.parent:
            return self.parent.section
        else:
            return None
    @property
    def subsection(self):
        if isinstance(self, Subsection):
            return self
        elif self.parent:
            return self.parent.subsection
        else:
            return None
    @property
    def paragraph(self):
        if isinstance(self, Paragraph):
            return self
        elif self.parent:
            return self.parent.paragraph
        else:
            return None
    @property
    def subparagraph(self):
        if isinstance(self, Subparagraph):
            return self
        elif self.parent:
            return self.parent.subparagraph
        else:
            return None
    @property
    def clause(self):
        if isinstance(self, Clause):
            return self
        elif self.parent:
            return self.parent.clause
        else:
            return None
    @property
    def subclause(self):
        if isinstance(self, Subclause):
            return self
        elif self.parent:
            return self.parent.subclause
        else:
            return None
        
# Subclasses
class Title(ClauseHierarchy):
    def __init__(self, number, name="Title", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=1, desc=None, preamble=preamble, parent=parent)

class Chapter(ClauseHierarchy):
    def __init__(self, number, name="Chapter", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=2, desc=None, preamble=preamble, parent=parent)

class Subchapter(ClauseHierarchy):
    def __init__(self, number, name="Subchapter", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=3, desc=None, preamble=preamble, parent=parent)

class Part(ClauseHierarchy):
    def __init__(self, number, name="Part", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=4, desc=None, preamble=preamble, parent=parent)

class Section(ClauseHierarchy):
    def __init__(self, number, name="Section", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=5, desc=None, preamble=preamble, parent=parent)

class Subsection(ClauseHierarchy):
    def __init__(self, number, name="Subsection", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=6, desc=None, preamble=preamble, parent=parent)

class Paragraph(ClauseHierarchy):
    def __init__(self, number, name="Paragraph", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=7, desc=None, preamble=preamble, parent=parent)

class Subparagraph(ClauseHierarchy):
    def __init__(self, number, name="Subparagraph", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=8, desc=None, preamble=preamble, parent=parent)

class Clause(ClauseHierarchy):
    def __init__(self, number, name="Clause", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=9, desc=None, preamble=preamble, parent=parent)

class Subclause(ClauseHierarchy):
    def __init__(self, number, name="Subclause", preamble=None, parent=None):
        super().__init__(name=name, number=number, rank=10, desc=None, preamble=preamble, parent=parent)