""" 
Module: 
3250.1 Compilateurs 
Auteur: 
WICKI Sélien 
Date: 26.01.2025 
"""

import ply.lex as lex

# Tokens
tokens = (

    # Tokens for instructions without content
    "STYLE", 
    "PAGE_NUMBER", 

    # Tokens for instructions with content but without arguments
    "BOLD", 
    "ITALIC", 
    "UNDERLINED", 

    # Tokens for instructions without content and  without arguments
    "NUMBERIZE_TITLE",

    # Tokens for instructions with content and arguments
    "TITLE",
    "SECTION", 

    # Tokens for argument parsing
    "ARG_NAME",
    "ARG_STYLE",
    "ARG_FONT_SIZE",
    "ARG_FONT",
    "ARG_FONT_COLOR",
    "ARG_LEVEL",
    "ARG_PAGE_NUMBER_POSITION",
    "ARG_PAGE_NUMBER_FONT_SIZE",
    "ARG_PAGE_NUMBER_FONT",
    "ARG_PAGE_NUMBER_FONT_COLOR",
    "ARG_PAGE_NUMBER_START",
    "ARG_NUMBERIZE_TITLE_START",

    # Tokens for argument values
    "NUMBER",
    "STRING",
    "LPAREN", 
    "RPAREN",
    "LBRACE", 
    "RBRACE", 
    "COMMA",
    "EQUALS",

    # Token for content
    "TEXT"
)


"""
potential to add :
    "HEADER", 
    "FOOTER", 
    "NAME", 
    "EQUALS", 
"""


# https://snatverk.blogspot.com/2012/01/how-to-work-with-states-in-ply.html
states = (
    ('arg', 'inclusive'),  # For argument parsing
)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

# Rules for the 'INITIAL' state (before parsing arguments)
def t_STYLE(t):
    r"\$style"
    return t

def t_PAGE_NUMBER(t):
    r"\$pageNumber" 
    return t

def t_NUMBERIZE_TITLE(t):
    r"\$numberizeTitle"
    return t

def t_TITLE(t):
    r"\$title"
    return t

def t_SECTION(t):
    r"\$section"
    return t

def t_BOLD(t):
    r"\$bold"
    return t

def t_ITALIC(t):
    r"\$italic"
    return t

def t_UNDERLINED(t):
    r"\$underlined"
    return t

# Rules for argument tokens
def t_arg_ARG_NAME(t):
    r"\#name"
    return t

def t_arg_ARG_STYLE(t):
    r"\#style"
    return t

def t_arg_ARG_FONT_SIZE(t):
    r"\#fontSize"
    return t

def t_arg_ARG_FONT(t):
    r"\#font"
    return t

def t_arg_ARG_FONT_COLOR(t):
    r"\#fontColor"
    return t

def t_arg_ARG_LEVEL(t):
    r"\#level"
    return t

def t_arg_ARG_PAGE_NUMBER_POSITION(t):
    r"\#pageNumberPosition"
    return t

def t_arg_ARG_PAGE_NUMBER_FONT_SIZE(t):
    r"\#pageNumberFontSize"
    return t

def t_arg_ARG_PAGE_NUMBER_FONT(t):
    r"\#pageNumberFont"
    return t

def t_arg_ARG_PAGE_NUMBER_FONT_COLOR(t):
    r"\#pageNumberFontColor"
    return t

def t_arg_ARG_PAGE_NUMBER_START(t):
    r"\#pageNumberStart"
    return t

def t_arg_ARG_NUMBERIZE_TITLE_START(t):
    r"\#numberizeTitleStart"
    return t

def t_arg_STRING(t):
    r'"[^"]*"'  # Matches anything between double quotes
    return t

def t_arg_NUMBER(t):
    r'[0-9][0-9]*'  # Matches anything between double quotes
    return t

def t_arg_COMMA(t):
    r","
    return t

def t_arg_EQUALS(t):
    r"="
    return t

# Rule for  content
def t_TEXT(t):
    r"[a-zA-Z0-9\s\.\,\!\?\-\é\è\ê\ë\à\ç\â\ä\î\ï\ô\ö\ù\û\ü\'\;\_]+"    
    return t

# State handler
def t_LPAREN(t):
    r"\("
    t.lexer.begin('arg')  # Switch to 'arg' state
    return t

def t_RPAREN(t):
    r"\)"
    t.lexer.begin('INITIAL')  # Switch back to 'initial' state after parsing argument
    return t

def t_LBRACE(t):
    r"\{"
    return t

def t_RBRACE(t):
    r"\}"
    return t

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()