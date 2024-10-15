from bs4 import BeautifulSoup
from USLegalCodeMap.main.parse_html import parse_viewheader, parse_block, compile_subsection
import os
import json

# Sample HTML content ksmimicking `viewheader_subdiv`
file_path = os.path.join("data", "section1182.xhtml" if os.path.exists("data/section1182.xhtml") else "section1182.html")


with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

section1182 = parse_block(soup)

print(section1182)


# section = parse_viewheader(soup)

# section1182 = compile_subsection(soup)
# print(json.dumps(section1182, indent=4))

# # Print the returned Section instance to view its structure
# print("Parsed Hierarchy:")
# print(section)

# # For detailed inspection, print attributes of each level
# print("\nDetailed Hierarchy:")
# print("Title:", section.title)
# print("Chapter:", section.chapter)
# print("Subchapter:", section.subchapter)
# print("Section:", section)
