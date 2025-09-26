""" 
Module: 
3250.1 Compilateurs 
Auteur: 
WICKI Sélien 
Date: 26.01.2025 
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

def create_pdf(semantic_data, filename="output.pdf"):
    # Get data
    styles_data = semantic_data["Styles"]
    page_config = semantic_data["PageNumberConfig"]
    content_data = semantic_data["Content"]

    # Extract the page start value (default is 1 if not specified or if error)
    try:
        page_number_start = int(page_config.get("#pageNumberStart", 1))
    except ValueError:
        page_number_start = 1

    # Define styles dictionary to hold dynamic styles
    styles = getSampleStyleSheet()

    # Apply styles from semantic data
    for style in styles_data:
        style_name = style["#name"].strip('"')  # Sanitize style name by removing surrounding quotes
        font = style.get("#font", "Helvetica")
        font_size = int(style.get("#fontSize", 12))
        font_color = style.get("#font_color", "black")
        
        # Create a ParagraphStyle and add it to styles
        styles.add(ParagraphStyle(
            name=style_name,
            fontName=font,
            fontSize=font_size,
            textColor=colors.HexColor(font_color) if font_color.startswith("#") else colors.toColor(font_color),
            leading=font_size + 2
        ))

    # Setup the PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    # Helper to add formatted text to the story
    def add_paragraph(text, style_name):
        sanitized_style_name = style_name.strip('"')  # Sanitize style name before using
        story.append(Paragraph(text, styles[sanitized_style_name]))
        story.append(Spacer(1, 12))

    # Render content based on structure
    for item in content_data:
        item_type = item.get("type")
        args = item.get("arguments")
        content = item.get("content", [])

        if item_type == "title":
            style_name = args.get("#style", "defaultTitleStyle")
            level = args.get("#level", 1)
            title_text = " ".join(content)  # Join content for title
            add_paragraph(f"<b>{title_text}</b>", style_name)
        
        elif item_type == "section":
            style_name = args.get("#style", "defaulSectiontStyle")
            section_content = []

            for section_item in content:
                if isinstance(section_item, str):  # Plain text
                    section_content.append(section_item)
                elif isinstance(section_item, dict):  # Styled text
                    nested_instr = section_item.get("instruction")
                    nested_content = section_item.get("content", {})
                    for key, value in nested_content.items():
                        if nested_instr == "$bold":
                            section_content.append(f"<b>{value}</b>")
                        elif nested_instr == "$italic":
                            section_content.append(f"<i>{value}</i>")
                        elif nested_instr == "$underlined":
                            section_content.append(f"<u>{value}</u>")

            # Add full section text with applied styles
            add_paragraph(" ".join(section_content), style_name)

    # Generate and apply page number
    def add_page_number(canvas_doc, doc):
        canvas_doc.saveState()
        font = page_config["#pageNumberFont"].strip('"')  # Sanitize font name
        font_size = int(page_config["#pageNumberFontSize"])
        position = page_config["#pageNumberPosition"].strip('"')  # Sanitize position

        canvas_doc.setFont(font, font_size)
        
        # Only start numbering after the specified page start number
        page_text = ""
        if doc.page >= page_number_start:
            page_text = f"Page {doc.page - (page_number_start - 1)}"
        else:
            page_text = ""  # Do not display page number before the start page
        

        # Determine position
        if position == "bottom-left":
            x, y = 50, 30
        elif position == "bottom-right":
            x, y = A4[0] - 50, 30
        elif position == "bottom-center":
            x, y = A4[0] / 2, 30
        elif position == "top-left":
            x, y = 50, A4[1] - 30
        elif position == "top-right":
            x, y = A4[0] - 50, A4[1] - 30
        elif position == "top-center":
            x, y = A4[0] / 2, A4[1] - 30
        else:
            x, y = A4[0] / 2, 30  # Default to bottom center if no match

        if page_text:  # Only print page number if the text is not empty
            canvas_doc.drawCentredString(x, y, page_text)
        canvas_doc.restoreState()

    # Build the PDF
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

