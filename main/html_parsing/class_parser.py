from main.models.class_hierarchy import Title, Chapter, Subchapter, Part, Section, Subsection, Paragraph, Subparagraph, Clause, Subclause

STACK=[] # Stack is comprised of a single instance of a each class.

def parse_viewheader(soup)->Section:
    """
    Parses the viewheader to identify section details and ensure we are on a section page.
    Returns a Section object if this is a section page, otherwise returns None.
    """
    viewheader_div = soup.find("div", class_="viewheader_subdiv")
    if not viewheader_div:
        print("Viewheader not found.")
        return None
    # If a Section page is loaded, "§" will be in the <span> element of viewhead_div
    section_page_check = viewheader_div.find("span", string=lambda text:text and "§" in text)
    if not section_page_check:
        print("This is not a section page.")
        return None
    
    hierarchy_data = {}

    if not viewheader_div:
        print("Warning: viewheader_subdiv not found on this page.")
        return None
    
    elements = viewheader_div.find_all(["a", "span"])

    for element in elements:
        text = element.get_text(strip=True)
        parts = text.split(" ", 1)

        if len(parts) == 2:
            level_name, number = parts
            if level_name == '§':
                level_name = 'section'
                number = f'§{number}'
            hierarchy_data[level_name.lower()] = number

    title = Title(number=hierarchy_data.get("title", ""))
    STACK.append(title)
    chapter = Chapter(number=hierarchy_data.get("chapter", ""),parent=title)
    title.add_child(chapter)
    STACK.append(chapter)
    subchapter = Subchapter(number=hierarchy_data.get("subchapter", ""),parent=chapter)
    chapter.add_child(subchapter)
    STACK.append(subchapter)
    part = Part(number=hierarchy_data.get("part", ""), parent=subchapter)
    subchapter.add_child(part)
    STACK.append(part)
    section = Section(number=hierarchy_data.get("section", ""), parent=part)
    part.add_child(section)
    STACK.append(section)

    return section


def parse_block(soup):
    """Main parsing function to process the block within field-start and field-end markers."""
    # Define current parent and initialize STACK for tracking hierarchy
    current_parent = parse_viewheader(soup)
    # Loop through tags within the block
    for tag in soup.find_all():

        lead_text, content_body = extract_content(tag)

        if "subsection-head" in tag.get("class", []):
            # Subsection-level handling
            subsection = Subsection(number=lead_text)
            subsection.desc=content_body
            if current_parent:
                current_parent = compare_rank(current_parent, subsection)

        elif "paragraph-head" in tag.get("class", []):
            # Paragraph-level handling
            paragraph = Paragraph(number=lead_text)
            paragraph.desc = content_body
            if current_parent:
                current_parent = compare_rank(current_parent, paragraph)

        elif "subparagraph-head" in tag.get("class", []):
            # Subparagraph-level handling
            subparagraph = Subparagraph(number=lead_text)
            if current_parent:
                current_parent = compare_rank(current_parent, subparagraph)

        elif "clause-head" in tag.get("class", []):
            # Clause-level handling
            clause = Clause(number=lead_text)
            clause.preamble = tag.get_text(strip=True)  # Set preamble
            if current_parent:
                current_parent = compare_rank(current_parent, clause)

        elif "statutory-body" in tag.get("class", []):
            # Statutory-body handling
            if current_parent:
                if current_parent == isinstance(current_parent, Section):
                    current_parent.preamble = tag.get_text(strip=True)
                else:
                    current_parent.desc = tag.get_text(strip=True)

        elif "statutory-body-2em" in tag.get("class", []):
            # Nested statutory-body elements can be Clauses or Subclauses based on indentation
            clause = Clause(number=lead_text)
            clause.desc = content_body
            if current_parent:
                current_parent.add_child(clause)
            current_parent = clause
            STACK.append(current_parent)

        elif "statutory-body-3em" in tag.get("class", []):
            # Additional nested element
            subclause = Subclause(number=lead_text)
            subclause.desc = content_body
            if current_parent:
                current_parent.add_child(subclause)
            current_parent = subclause
            STACK.append(current_parent)

    # At the end of parsing, the root element in the STACK will represent the top of the parsed hierarchy
    return STACK[0] if STACK else None

# Helper Functions
def extract_content(tag):
    """Extracts tag text. Determines if lead text is a clause label number, else sets lead_text to None."""
    text = tag.get_text(strip=True)
    parts = text.split(" ", 1)
    
    # Check if the first part is a label (e.g., "(1)", "(a)")
    if len(parts) > 1 and parts[0].startswith("(") and parts[0].endswith(")"):
        lead_text = parts[0]
        content_body = parts[1]
    else:
        lead_text = None
        content_body = text  # Use the entire text if no label is present
    
    return lead_text, content_body

def compare_rank(current_parent, currentNode):
    """Compares the ranks of the current parent and the current node. Appends latest high or equal rank to STACK. 
        Returns currentNode.
    """
    if current_parent.rank > currentNode.rank:
        current_parent.add_child(currentNode)
        currentNode.parent = current_parent
        STACK.append(currentNode)
    elif current_parent.rank == currentNode.rank:
        currentNode.parent = current_parent.parent
        STACK.pop(current_parent)
        STACK.append(currentNode)
    return currentNode


        