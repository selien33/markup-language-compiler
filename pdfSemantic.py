""" 
Module: 
3250.1 Compilateurs 
Auteur: 
WICKI Sélien 
Date: 26.01.2025 
"""


# For font check : https://docs.reportlab.com/reportlab/userguide/ch3_fonts/
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

# import the allowed arguments
from default import style_arguments, page_number_arguments, section_arguments, title_arguments, numberize_title_arguments

#import the default values
from default import default_section_style, default_title_style, default_page_number, default_title, default_section, default_font, default_color, default_font_size, default_page_number_position, default_numberize_title

# Import the nested instructions for the section
from default import section_nested_instructions

# Import the allowed page number positions
from default import allowed_page_nb_positions

# Import the range for the arguments
from default import font_size_range, title_level_range


# For errors 
def check_allows_arguments(instruction, allowed_arguments):
    for arg in instruction["arguments"]:
        if arg not in allowed_arguments:
            return False
    return True

#For Warnings
def check_font(font_name):
    try:
        if font_name in pdfmetrics.getRegisteredFontNames():
            return True  # Font is registered
        else:
            return False  # Font is not registered
    except Exception as e:
        print(f"Error checking font {font_name}: {e}")
        return False
    
def check_color(color):
    available_colors = colors.getAllNamedColors()
    return color in available_colors


def check_out_of_range(value, lower, upper):
    #convert to int if it is a string
    if isinstance(value, str):
        try:
            return lower <= int(value) <= upper
        except ValueError:
            return False



def semantical_analysis(parsed_code, print_errors=False):
    """
    Rules for the semantical analysis:

    $style arguments :
    #name -> Mendatory
    #font
    #fontSize
    #font_color

    $pageNumber arguments :
    #pageNumberPosition {"bottom-left", "bottom-rigth", "top-left", "top-right"}
    #pageNumberFontSize
    #pageNumberFont
    #pageNumberFontColor
    #pageNumberStart
    #pageNumberEnd

    $section arguments :
    #style

    $title arguments :
    #style 
    #level

    $bold, $italic, $underlined have no arguments !
    $stlye and $pageNumber have no content (no braces) !

    I want the styles to be stored in a list of dict
    I want the pageNumber to be defined in a dict
    I want the content ($section and $title) to be in a list (chronological) of dict (arguments)

    The page number can only be called once ! An example of a code that does not work (Error : $pageNumber called multiple times)
    $pageNumber(#pageNumberPosition="bottom-left",#pageNumberFont="Times New Roman",#pageNumberFontSize=10)
    $pageNumber(#pageNumberFont="Times New Roman")
    """

    # Store the results
    styles = [default_section_style, default_title_style]
    page_number = {}
    numberize_titles = {}
    doc_content = []

    # For the rule that the name of the syle is unique !
    unique_style_names = set()
    unique_style_names.add(default_section_style["#name"])
    unique_style_names.add(default_title_style["#name"]) 

    # To collect error messages
    error_messages = []      
    warning_messages = []

    # Check page called once 
    page_number_called = False

    # Numberize title 
    is_title_numberized = False

    # Analysing parsed data
    for instruction in parsed_code:

        #############################################################################
        #                                   Style                                   #
        ############################################################################# 

        if instruction["instruction"] == "$style":

            #ERRORS 

            # Check if the arguments are allowed
            if not check_allows_arguments(instruction, style_arguments):
                error_messages.append(
                    f"Error: $style instruction does not allow the arguments {instruction['arguments']}."
                )
                continue

            # $style must have "#name" argument
            if "#name" not in instruction["arguments"]:
                error_messages.append(
                    "Error: $style instruction is missing the mandatory #name argument."
                )
                continue  # Skip further processing for invalid $style

            style_name = instruction["arguments"]["#name"]

            # Check for duplicate #name values
            if style_name in unique_style_names:
                error_messages.append(
                    f"Error: The #name value {style_name} is the same for two different styles. The style names must be unique."
                )
                continue  # Skip adding this style to the list

            # Add the style name to the set
            unique_style_names.add(style_name)


            #WARNINGS

            # Check if specified font exists
            if "#font" in instruction["arguments"]:
                if not check_font(instruction["arguments"]["#font"]):
                    warning_messages.append(
                        f"Warning: In {instruction['instruction']}, {instruction['arguments']['#font']} does not exist. Using default font {default_font}."
                    )
                    instruction["arguments"]["#font"] = default_font

            # Check if specified color exists
            if "#font_color" in instruction["arguments"]:
                if not check_color(instruction["arguments"]["#font_color"]):
                    warning_messages.append(
                        f"Warning: In {instruction['instruction']}, {instruction['arguments']['#font_color']} does not exist. Using default color {default_color}."
                    )
                    instruction["arguments"]["#font_color"] = default_color

            # Check if the font size is in the range
            if "#fontSize" in instruction["arguments"]:
                if not check_out_of_range(instruction["arguments"]["#fontSize"], font_size_range[0], font_size_range[1]):
                    warning_messages.append(
                        f"Warning: In {instruction['instruction']}, {instruction['arguments']['#fontSize']} is out of range. Using default font size {default_section_style['#fontSize']}."
                    )
                    instruction["arguments"]["#fontSize"] = default_font_size


            # For the mergiing of two dicts (Assign default values):
            # https://www.freecodecamp.org/news/python-merge-dictionaries-merging-two-dicts-in-python/

            # Assign default values
            args = {**default_section_style, **instruction["arguments"]}
            args["#name"] = style_name
            styles.append(args)





        #############################################################################
        #                                   PageNumber                              #
        #############################################################################

        elif instruction["instruction"] == "$pageNumber":

            #ERRORS

            # Check if the arguments are allowed
            if not check_allows_arguments(instruction, page_number_arguments):
                error_messages.append(
                    f"Error: $style instruction does not allow the arguments {instruction['arguments']}."
                )
                continue

            # Only one $pageNumber instruction !
            if page_number_called:
                error_messages.append(
                    "Error: $pageNumber can only be called once."
                )
                continue
            
            page_number_called = True


            #WARNINGS

            # Check if the specified font exists; fall back to the default font if it doesn't
            if "#pageNumberFont" in instruction["arguments"]:
                if not check_font(instruction["arguments"]["#pageNumberFont"]):
                    warning_messages.append(
                        f"Warning: Font {instruction["arguments"]['#pageNumberFont']} for $pageNumber does not exist. Using default font {default_font}."
                    )
                    instruction["arguments"]["#pageNumberFont"] = default_font

            # Check if the specified position is allowed
            if "#pageNumberPosition" in args and args["#pageNumberPosition"] not in allowed_page_nb_positions:
                warning_messages.append(
                    f"Warning: The specified position {args['#pageNumberPosition']} for $pageNumber is not allowed. Using default position 'bottom-left'."
                )
                page_number["#pageNumberPosition"] = default_page_number_position

            # Check if the font size is in the range
            if "#pageNumberFontSize" in args:
                if not check_out_of_range(args["#pageNumberFontSize"], font_size_range[0], font_size_range[1]):
                    warning_messages.append(
                        f"Warning: The specified font size {args['#pageNumberFontSize']} for $pageNumber is out of range. Using default font size {default_page_number['#pageNumberFontSize']}."
                    )
                    page_number["#pageNumberFontSize"] = default_page_number["#pageNumberFontSize"]


            # Assign default values (if arguments not provided)
            args = {**default_page_number, **instruction["arguments"]}  # Merge defaults with provided values
            page_number = args





        #############################################################################
        #                                   Section                                 #
        #############################################################################

        elif instruction["instruction"] == "$section":

            #ERRORS

            # Check if the arguments are allowed
            if not check_allows_arguments(instruction, section_arguments):
                error_messages.append(
                    f"Error: $section instruction does not allow the arguments {instruction['arguments']}."
                )
                continue

            # Check that the specified style exists
            if "#style" in args and args["#style"] not in unique_style_names:
                error_messages.append(
                    f"Error: The #style '{args['#style']}' specified in $section does not exist."
                )
                continue

            for section_content in instruction.get("content", []):
                
                # Check that the section only contains $bold, $italic, $underlined, and regular text (no $title, $section allowed)
                if isinstance(section_content, dict):
                    if section_content.get("instruction") not in section_nested_instructions:
                        error_messages.append(
                            f"Error: {section_content['instruction']} is not allowed inside a $section."
                        )
                elif isinstance(section_content, str):  # Plain text -> Should be alrigth
                    continue

                # Check $bold, $italic, and $underlined have no arguments and non-empty content
                if isinstance(section_content, dict) and section_content.get("instruction") in section_nested_instructions:
                    if "arguments" in section_content and section_content["arguments"]:
                        error_messages.append(
                            f"Error: {section_content['instruction']} should not have any arguments."
                        )
                        continue
                    elif not section_content.get("content"):
                        error_messages.append(
                            f"Error: {section_content['instruction']} has empty content."
                        )
                        continue


            # Assign default values (if arguments not provided)
            args = {**default_section, **instruction["arguments"]}
            doc_content.append({"type": "section", "arguments": args, "content": instruction["content"]})
        







        #############################################################################
        #                                   Title                                   #
        #############################################################################
        
        elif instruction["instruction"] == "$title":

            #ERRORS

            # Check if the arguments are allowed
            if not check_allows_arguments(instruction, title_arguments):
                error_messages.append(
                    f"Error: $title instruction does not allow the arguments {instruction['arguments']}."
                )
                continue
            
            # Check that the #style exists if specified
            if "#style" in instruction["arguments"]:
                style_name = instruction["arguments"]["#style"]
                if style_name not in unique_style_names:
                    error_messages.append(
                        f"Error: The referenced #style '{style_name}' in $title does not exist."
                    )
                    continue

            # Check that $title content does not contain nested instructions
            for title_content in instruction.get("content", []):
                if isinstance(title_content, dict):
                    error_messages.append(
                        f"Error: Nested instruction '{title_content['instruction']}' is not allowed inside a $title."
                    )
                    continue
            

            #WARNINGS

            # Check if the title level is in the range
            if "#level" in instruction["arguments"]:
                if not check_out_of_range(instruction["arguments"]["#level"], title_level_range[0], title_level_range[1]):
                    warning_messages.append(
                        f"Warning: The specified title level {instruction['arguments']['#level']} is out of range."
                    )
                    instruction["arguments"]["#level"] = default_title["#level"]
            
            # Assign default values (if arguments not provided)
            args = {**default_title, **instruction["arguments"]}  # Apply default if not provided
            doc_content.append({"type": "title", "arguments": args, "content": instruction["content"]})
        
           




        #############################################################################
        #                          Bolt, Italic, Underlined                         #
        #############################################################################

        elif instruction["instruction"] in section_nested_instructions:
            error_messages.append(f"Error: {section_content['instruction']} can only be declared inside a section")






        
        #############################################################################
        #                               Numberize Title                             #
        #############################################################################

        elif instruction["instruction"] == "$numberizeTitle":

            #ERRORS

            # Check if the arguments are allowed
            if not check_allows_arguments(instruction, numberize_title_arguments):
                error_messages.append(f"Error: $numberizeTitle instruction does not allow the arguments {instruction['arguments']}.")
                continue
            
            #WARNINGS

            # Check if the numberizeTitleStart is in the range
            if "#numberizeTitleStart" in instruction["arguments"]:
                if not check_out_of_range(instruction["arguments"]["#numberizeTitleStart"], title_level_range[0], title_level_range[1]):
                    warning_messages.append(
                        f"Warning: The specified title level {instruction['arguments']['#numberizeTitleStart']} is out of range."
                    )
                    instruction["arguments"]["#numberizeTitleStart"] = default_title["#level"]

            # Assign default values (if arguments not provided)
            args = {**default_numberize_title, **instruction["arguments"]}  # Apply default if not provided    
            numberize_titles = args

            is_title_numberized = True
        
        else:
            error_messages.append(f"Error: Undefined instruction {instruction['instruction']}.")


    # If numberize_title is set add numbers to the titles from the #numberizeTitleStart value and based on the #level of the title
    if is_title_numberized:
        try:
            start_title_level = int(numberize_titles["#numberizeTitleStart"])
        except ValueError:
            start_title_level = default_numberize_title["#numberizeTitleStart"]

        titles_levels = [ 1 for i in range(title_level_range[0], title_level_range[1] + 1)]
        for item in doc_content:
            if item["type"] == "title":
                
                try:
                    title_level = int(item["arguments"]["#level"])
                except ValueError:
                    title_level = default_title["#level"]

                if title_level < start_title_level:
                    continue

                title_number = '.'.join(str(titles_levels[i]) for i in range(start_title_level - 1, title_level)) 
                
                # Add number prefix to the title content
                title_text = f"{title_number}. {''.join(item['content'])}"

                # Update the title content to include the number prefix
                item['content'] = [title_text]

                # Increment the title number for the current level
                titles_levels[title_level - 1] += 1

                # Reset lower levels to ensure correct numbering for further nested titles
                for i in range(title_level, len(titles_levels)):
                    titles_levels[i] = 1
                
                

    # Print out any error messages and exit
    if error_messages and print_errors:
        for error in error_messages:
            print()
            print(error)
            print()
         

    if warning_messages and print_errors:
        for warning in warning_messages:
            print()
            print(warning) 
            print()

    if len(page_number) == 0:
        page_number = default_page_number

    return styles, page_number, numberize_titles, doc_content, error_messages, warning_messages
