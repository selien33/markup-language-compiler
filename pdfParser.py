""" 
Module: 
3250.1 Compilateurs 
Auteur: 
WICKI Sélien 
Date: 26.01.2025 
"""

# Importing yacc
import ply.yacc as yacc

# Import the tokens from the lexer
from pdfLexer import tokens



# Grammar Rules
def p_document(p):
    """document : instructions"""
    p[0] = p[1]

def p_instructions(p):
    """
    instructions :    instruction instructions
                    | instruction
    """
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_instruction(p):
    """             
    instruction :     TITLE LPAREN arguments RPAREN LBRACE content RBRACE
                    | TITLE LPAREN RPAREN LBRACE content RBRACE
                    | SECTION LPAREN arguments RPAREN LBRACE content RBRACE
                    | SECTION LPAREN RPAREN LBRACE content RBRACE
                    | BOLD LPAREN RPAREN LBRACE bold_content RBRACE
                    | ITALIC LPAREN RPAREN LBRACE italic_content RBRACE
                    | UNDERLINED LPAREN RPAREN LBRACE underlined_content RBRACE
                    | STYLE LPAREN arguments RPAREN 
                    | PAGE_NUMBER LPAREN arguments RPAREN
                    | NUMBERIZE_TITLE LPAREN arguments RPAREN
                    | NUMBERIZE_TITLE LPAREN RPAREN
    """
    if len(p) == 8:  # Instruction with arguments and content
        p[0] = {"instruction": p[1], "arguments": p[3], "content": p[6]}
    elif len(p) == 7:  # Instruction without arguments but with content
        p[0] = {"instruction": p[1], "content": p[5]}
    elif len(p) == 5:  # Instruction with arguments but without content
        p[0] = {"instruction": p[1], "arguments": p[3]}
    else:  # Instruction  without arguments and without content
        p[0] = {"instruction": p[1]}

def p_arguments(p):
    """arguments : arguments COMMA argument
                 | argument"""
    if len(p) == 4:  # Handle multiple arguments
        p[0] = {**p[1], **p[3]}
    else:  # Single argument
        p[0] = p[1]

def p_argument(p):
    """argument :     ARG_NAME EQUALS STRING
                    | ARG_STYLE EQUALS STRING
                    | ARG_FONT_SIZE EQUALS NUMBER
                    | ARG_FONT EQUALS STRING
                    | ARG_FONT_COLOR EQUALS STRING
                    | ARG_LEVEL EQUALS NUMBER
                    | ARG_PAGE_NUMBER_POSITION EQUALS STRING
                    | ARG_PAGE_NUMBER_FONT_SIZE EQUALS NUMBER
                    | ARG_PAGE_NUMBER_FONT EQUALS STRING
                    | ARG_PAGE_NUMBER_FONT_COLOR EQUALS STRING
                    | ARG_PAGE_NUMBER_START EQUALS NUMBER
                    | ARG_NUMBERIZE_TITLE_START EQUALS NUMBER
    """
    p[0] = {p[1]: p[3]}

def p_content(p):
    """content :      content TEXT
                    | TEXT
                    | content instruction
                    | instruction"""
    print(p)

    if len(p) == 3:  # Handle multiple content parts
        if isinstance(p[2], str):  # TEXT
            p[0] = p[1] + [p[2]] if isinstance(p[1], list) else [p[1], p[2]]
        else:  # instruction
            p[0] = p[1] + [p[2]] if isinstance(p[1], list) else [p[1], p[2]]
    else:  # Single TEXT or instruction
        p[0] = [p[1]]

def p_bold_content(p):
    """bold_content : TEXT"""
    p[0] = {"bold": p[1]}

def p_italic_content(p):
    """italic_content : TEXT"""
    p[0] = {"italic": p[1]}

def p_underlined_content(p):
    """underlined_content : TEXT"""
    p[0] = {"underlined": p[1]}

def p_error(p):
    if p:
        print(f"Syntax error at {p.value!r} (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

