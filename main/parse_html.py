from bs4 import BeautifulSoup
from main.class_hierarchy import Title, Chapter, Subchapter, Part, Section, Subsection, Paragraph, Subparagraph, Clause, Subclause
import re


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
    chapter = Chapter(number=hierarchy_data.get("chapter", ""),parent=title)
    subchapter = Subchapter(number=hierarchy_data.get("subchapter", ""),parent=chapter)
    part = Part(number=hierarchy_data.get("part", ""), parent=subchapter)
    section = Section(number=hierarchy_data.get("section", ""), parent=part)

    return section


def parse_block(soup):
    """Main parsing function to process the block within field-start and field-end markers."""
    # Define current parent and initialize stack for tracking hierarchy
    current_parent = None
    stack = []

    current_parent = parse_viewheader(soup)

    # Loop through tags within the block
    for tag in soup.find_all():
        if "subsection-head" in tag.get("class", []):
            # Subsection-level handling
            subsection = Subsection(number=extract_number(tag), name=extract_name(tag))
            subsection.preamble = tag.get_text(strip=True)  # Set preamble
            if current_parent:
                current_parent.add_child(subsection)
            current_parent = subsection
            stack.append(current_parent)

        elif "paragraph-head" in tag.get("class", []):
            # Paragraph-level handling
            paragraph = Paragraph(number=extract_number(tag), name=extract_name(tag))
            if current_parent:
                current_parent.add_child(paragraph)
            current_parent = paragraph
            stack.append(current_parent)

        elif "subparagraph-head" in tag.get("class", []):
            # Subparagraph-level handling
            subparagraph = Subparagraph(number=extract_number(tag), name=extract_name(tag))
            if current_parent:
                current_parent.add_child(subparagraph)
            current_parent = subparagraph
            stack.append(current_parent)

        elif "clause-head" in tag.get("class", []):
            # Clause-level handling
            clause = Clause(number=extract_number(tag), name=extract_name(tag))
            clause.preamble = tag.get_text(strip=True)  # Set preamble
            if current_parent:
                current_parent.add_child(clause)
            current_parent = clause
            stack.append(current_parent)

        elif "statutory-body" in tag.get("class", []):
            # Statutory-body handling
            if current_parent:
                current_parent.desc = tag.get_text(strip=True)

        elif "statutory-body-2em" in tag.get("class", []):
            # Nested statutory-body elements can be Clauses or Subclauses based on indentation
            clause = Clause(number=extract_number(tag), name=extract_name(tag))
            clause.desc = tag.get_text(strip=True)
            if current_parent:
                current_parent.add_child(clause)
            current_parent = clause
            stack.append(current_parent)

        elif "statutory-body-3em" in tag.get("class", []):
            # Additional nested element
            subclause = Subclause(number=extract_number(tag), name=extract_name(tag))
            subclause.desc = tag.get_text(strip=True)
            if current_parent:
                current_parent.add_child(subclause)
            current_parent = subclause
            stack.append(current_parent)

    # At the end of parsing, the root element in the stack will represent the top of the parsed hierarchy
    return stack[0] if stack else None

# Helper Functions
def extract_number(tag):
    """Extracts the number from the tag's text."""
    return tag.get_text(strip=True).split(" ", 1)[0]

def extract_name(tag):
    """Extracts the name or title from the tag's text after the number."""
    parts = tag.get_text(strip=True).split(" ", 1)
    return parts[1] if len(parts) > 1 else ""


# def compile_subsection(soup):
#     subsection_dict = {}
#     pattern = re.compile(r"\((\w)\)")
#     for element in soup.find_all(class_="subsection-head"):
#         text_parts = [str(part) for part in element.contents if not part.name == "sup"]
#         main_text = "".join(text_parts).strip()
#         match = pattern.search(main_text)
#         if match:
#             key = match.group(1)
#             sup_tag = element.find("sup")
#             if sup_tag and sup_tag.find("a"):
#                 key += f"_{sup_tag.find('a').get_text(strip=True)}"
#             description = pattern.sub("", main_text, count=1).strip()
#             if "Repealed" in description:
#                 description = description.split("Repealed")[0].strip() + "Repealed"

#             subsection_dict[key] = description
#     return subsection_dict



# def parse_section_content(soup):
#     """
#     Parses the section content by dividing it into blocks based on `substructure-location` tags and extracting content within field markers.
#     """
#     section = parse_viewheader(soup)
#     if not section:
#         print("This is not a section page")
#         return None

#     section_header = soup.find(class_="section-head")
#     if section_header:
#         header_text = section_header.get_text(strip=True)
#         section_number, description = header_text.split(". ", 1) if ". " in header_text else (header_text, None)
#         section.number = section_number # Set section number and description
#         section.desc = description if description else section.desc  # Only set desc if present
#         print(f"Parsing section {section_number}")



#     section_data = []
#     current_block = None

        