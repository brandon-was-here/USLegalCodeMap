from bs4 import BeautifulSoup
from main.class_hierarchy import Title, Chapter, Subchapter, Part, Section
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

def compile_subsection(soup):
    subsection_dict = {}
    pattern = re.compile(r"\((\w)\)")
    for element in soup.find_all(class_="subsection-head"):
        text_parts = [str(part) for part in element.contents if not part.name == "sup"]
        main_text = "".join(text_parts).strip()
        match = pattern.search(main_text)
        if match:
            key = match.group(1)
            sup_tag = element.find("sup")
            if sup_tag and sup_tag.find("a"):
                key += f"_{sup_tag.find('a').get_text(strip=True)}"
            description = pattern.sub("", main_text, count=1).strip()
            if "Repealed" in description:
                description = description.split("Repealed")[0].strip() + "Repealed"

            subsection_dict[key] = description
    return subsection_dict



def parse_section_content(soup):
    """
    Parses the section content by dividing it into blocks based on `substructure-location` tags and extracting content within field markers.
    """
    section = parse_viewheader(soup)
    if not section:
        print("This is not a section page")
        return None

    section_header = soup.find(class_="section-head")
    if section_header:
        header_text = section_header.get_text(strip=True)
        section_number, description = header_text.split(". ", 1) if ". " in header_text else (header_text, None)
        section.number = section_number # Set section number and description
        section.desc = description if description else section.desc  # Only set desc if present
        print(f"Parsing section {section_number}")



    section_data = []
    current_block = None

        