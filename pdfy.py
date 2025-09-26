""" 
Module: 
3250.1 Compilateurs 
Auteurs: 
WICKI Sélien 
Date: 26.01.2025 
"""

# System imports
import sys

# Import the lexer and parser
from pdfLexer import lexer
from pdfParser import parser
from pdfSemantic import semantical_analysis
from pdfGenerator import create_pdf

# For Generating the tree
from generate_ast import generate_tree_image


# Helper functions for printing the infos 
def print_help():
    print("Usage: python pdfy.py <input_file> <output_file> -[l/p/s]")
    print("Options:")
    print("  -l: Print the tokens")
    print("  -p: Parse the input")
    print("  -s: Run the semantic analysis")
    print("  -h: use <python pdfy.py -h> for help")
    exit(0)

def print_lexer(input_string):
    lexer.input(input_string)
    print("Tokens:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

def print_parser(input_string):
    parsed_data = parser.parse(input_string)
    print("Parsed data:")
    print("-------------")
    print(parsed_data)
    generate_tree_image(parsed_data)
    print()

def print_semantic(parsed_data):
    semantical_styles, semantical_page_number, semantical_title_numberization, semandical_doc_content, _, _ = semantical_analysis(parsed_data, print_errors=True)
    print("Semantic data:")
    print("-------------")
    print("\nStyles:", semantical_styles)
    print("\nPage Number Configuration:", semantical_page_number)
    print("\nTitle Numberization:", semantical_title_numberization)
    print("\nSections and Titles:", semandical_doc_content)



# Give the lexer some input
if __name__ == '__main__':

    # Read file given as argument
    input_string = ""
    output_file = ""

    if len(sys.argv) > 1:

        if sys.argv[1] == "-h":
            print_help()
        else:

            with open(sys.argv[1], 'r') as f:
                input_string = f.read()

                if len(sys.argv) > 2:
                    output_file = sys.argv[2]
                else:
                    print("No output file given, use <python pdfy.py -h> for help")

                

                # Check if the user wants to print the tokens
                for i in range(3, len(sys.argv)):
                    if len(sys.argv) > i and sys.argv[i] == "-l":
                        print_lexer(input_string)
                    elif len(sys.argv) > i and sys.argv[i] == "-p":
                        print_parser(input_string)
                    elif len(sys.argv) > i and sys.argv[i] == "-s":
                        parsed_data = parser.parse(input_string)
                        print_semantic(parsed_data)

                if len(sys.argv) == 3:
                    parsed_data = parser.parse(input_string)
                    semantical_styles, semantical_page_number, _ , semandical_doc_content, _, _ = semantical_analysis(parsed_data)
                    semantic_data = {"Styles": semantical_styles, "PageNumberConfig": semantical_page_number , "Content": semandical_doc_content}
                    create_pdf(semantic_data)

            
    else:
        print("No file to compile given, use <python pdfy.py -h> for help")

    

