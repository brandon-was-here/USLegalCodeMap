from bs4 import BeautifulSoup
from main.html_parsing.class_parser import parse_block
import os
import json

file_path = os.path.join("data", "section1182.xhtml" if os.path.exists("data/section1182.xhtml") else "section1182.html")


with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

section1182 = parse_block(soup)

def hierarchy_to_dict(node):
    """Recursively convert a ClauseHierarchy object and its children to a dictionary."""
    return {
        "name": node.name,
        "number": node.number,
        "rank": node.rank,
        "preamble": node.preamble,
        "desc": node.desc,
        "children": [hierarchy_to_dict(child) for child in node.children]
    }

# Function to export the JSON to a text file
def export_hierarchy_to_json_text(root_node, filename="hierarchy_structure.txt"):
    output_path = os.path.join("output", filename)
    hierarchy_dict = hierarchy_to_dict(root_node)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(hierarchy_dict, file, indent=4)
    print(f"Hierarchy exported to {filename}")

# Assuming `section1182` is the root node of the parsed structure
export_hierarchy_to_json_text(section1182)


# Sample HTML content ksmimicking `viewheader_subdiv`



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
