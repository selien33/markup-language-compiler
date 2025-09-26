# Pdfy - markup-language-compiler

Pdfy is a domain-specific language designed for generating PDF files. The project draws inspiration from LaTeX, HTML, and other document generation languages. While initially appearing simple, the complexity of the task led to focusing on a restricted set of features to ensure proper compiler functionality.

The language supports creating styles, sections, titles, page numbering functions, and text formatting options including bold, italic, and underlined text.


## Installation and Usage

### Prerequisites

Before using Pdfy, ensure you have the following installed:

- **Python 3.6+**
- **pip** (Python package installer)

### Required Dependencies

Install the required Python packages:

```bash
pip install ply reportlab graphviz
```

#### Package Details:
- `ply` - Python Lex-Yacc for lexical analysis and parsing
- `reportlab` - PDF generation library
- `graphviz` - For generating Abstract Syntax Tree visualizations

### Installation

1. Clone or download the Pdfy compiler files to your local directory
2. Ensure all Python files are in the same directory:
   - `pdfy.py` (main compiler)
   - `pdfLexer.py` (lexical analyzer)
   - `pdfParser.py` (parser)
   - `pdfSemantic.py` (semantic analyzer)
   - `pdfGenerator.py` (PDF generator)
   - `default.py` (default configurations)
   - `generate_ast.py` (AST visualization)

### Usage

#### Basic Compilation

To compile a Pdfy source file to PDF:

```bash
python pdfy.py <input_file> <output_file>
```

**Example:**
```bash
python pdfy.py document.pdfy output.pdf
```

#### Development and Debugging Options

The compiler provides several flags for development and debugging:

```bash
python pdfy.py <input_file> <output_file> [options]
```

**Available Options:**
- `-l` : Print lexical tokens
- `-p` : Display parse tree and generate AST visualization
- `-s` : Run semantic analysis and display results
- `-h` : Show help message

**Examples:**

```bash
# View lexical tokens
python pdfy.py document.pdfy output.pdf -l

# See parse tree and generate parse_tree.png
python pdfy.py document.pdfy output.pdf -p

# Run semantic analysis
python pdfy.py document.pdfy output.pdf -s

# Combine multiple options
python pdfy.py document.pdfy output.pdf -l -p -s

# Get help
python pdfy.py -h
```

#### Input File Format

Your input file should contain Pdfy language instructions. Example (`document.pdfy`):

```pdfy
$style(#name="titleStyle", #font="Arial", #fontSize=16, #font_color="blue")
$pageNumber(#pageNumberPosition="bottom-right", #pageNumberStart=1)

$title(#style="titleStyle", #level=1){My Document Title}

$section(){
    This is the content of my document with $bold(){bold text} and $italic(){italic text}.
}
```

#### Output Files

- **PDF Output**: Generated at the specified output path
- **AST Visualization**: When using `-p` flag, generates `parse_tree.png` in the current directory


## Documentation Pdfy - PDF Generation Language

*Documentation by Sélien Wicki - Compiler Course 3250.1 - January 26, 2025*


### Language Syntax

The language uses instructions that can contain arguments and/or content:

- **Instructions without content**: `$instruction(#argument1=..., )`
- **Instructions with content**: `$instruction(#argument1=..., ){Content}`

Default values are included for each argument, meaning instructions don't necessarily need to assign a value to every argument (except for Styles, see below). When an unrecognized value is provided (color, font size, etc.), a warning is displayed in the console and the default value is used.

### Available Instructions

- `$style(#name=, #args=...)`
- `$pageNumber(#args=…)`
- `$numberizeTitle(#args=…)`
- `$section(#args=…){Content goes between braces}`
- `$title(#args=…){Content goes between braces}`
- `$bold(){Content goes between braces}`
- `$italic(){Content goes between braces}`
- `$underlined(){Content goes between braces}`

### Instruction Details

#### `$style(#name=..., #args=...)`

**Purpose**: Declares a new style with modifiable arguments.

**Arguments**:
- `#name` (Required): The style name. Each style name must be unique.
- `#font` (Optional): The text font name.
- `#fontSize` (Optional): Font size, range [4, 100].
- `#font_color` (Optional): Text color, must be a valid color (simple recognized color names: black, white, blue, etc.).

**Value Ranges**:
- Font size must be between 4 and 100 pixels.

**Rules**:
- The `#name` must be unique. If a style has the same name as another style, an error occurs.
- Two default styles are pre-created: "defaultSectionStyle" and "defaultTitleStyle". These names cannot be used for custom styles.
- If arguments like `#font`, `#fontSize`, or `#font_color` are incorrect (non-existent font or invalid color), they take default values (Helvetica, black, font size 12).



#### `$pageNumber(#args=...)`

**Purpose**: Defines the appearance and placement of page numbers.

**Arguments**:
- `#pageNumberPosition` (Optional): Page number position. Possible positions: "bottom-left", "bottom-right", "top-left", "top-right" (default: "bottom-left").
- `#pageNumberFontSize` (Optional): Page number font size, range [4, 100].
- `#pageNumberFont` (Optional): Font used for page numbers.
- `#pageNumberFontColor` (Optional): Page number font color.
- `#pageNumberStart` (Optional): Starting page number (default: 1).

**Value Ranges**:
- Page number font size must be between 4 and 100.

**Rules**:
- This instruction can only be called once per document.
- Once defined, other calls to this instruction will result in an error.

#### `$section(#args=...){content}`

**Purpose**: Declares a section with specific content whose style and form can be customized.

**Arguments**:
- `#style` (Optional): The style to apply to this section. This style must exist in the list of defined styles. If not specified, a default style is used.

**Value Ranges**:
- The `#style` must be a valid name of an already defined style.

**Rules**:
- The `#style` argument must not reference a non-existent style.
- Nested instructions like `$title`, `$section` are not allowed within a section. Only instructions like `$bold`, `$italic`, or `$underlined` are permitted inside a section.

#### `$title(#args=...){content}`

**Purpose**: Declares a title in the document with a style and level.

**Arguments**:
- `#style` (Optional): The title style. This style must be a pre-defined style.
- `#level` (Optional): The title level, which determines the title's importance in the document hierarchy. Allowed range [1, 10], with a default level of 1.

**Value Ranges**:
- Title level must be an integer between 1 and 10.

**Rules**:
- No nested instructions are allowed in a title. This means instructions like `$section`, `$bold`, `$italic`, etc., cannot be used inside a title.
- The `#style`, if mentioned, must point to an already defined style.

#### `$numberizeTitle(#args=...)`

**Purpose**: Enables numbering of titles starting from a given level.

**Arguments**:
- `#numberizeTitleStart` (Optional): The title level from which number addition begins (default: 1).

**Value Ranges**:
- The starting level for title numbering must be a number between [1, 10].

**Rules**:
- This instruction can only be used once to start the title numbering process in a document.

**Functionality**: The algorithm traverses the content and adds numbers to titles based on their level. For example, if numbering starts at level 2, titles of level 2 and higher will be automatically numbered.

### Text Formatting Instructions

#### `$bold(){content}`
#### `$italic(){content}` 
#### `$underlined(){content}`

**Purpose**: Format text content as bold, italic, or underlined respectively.

**Arguments**: No arguments are allowed.

**Rules**:
- These instructions must be included within a section only.
- No nested instructions are allowed within these blocks.

**Functionality**: These instructions format the text contained within the section as bold, italic, or underlined.

## Usage Examples

```pdfy
$style(#name=myStyle, #font=Arial, #fontSize=14, #font_color=blue)

$pageNumber(#pageNumberPosition=bottom-right, #pageNumberStart=1)

$numberizeTitle(#numberizeTitleStart=2)

$title(#style=myStyle, #level=1){Introduction}

$section(#style=defaultSectionStyle){
    This is a regular section with $bold(){bold text} and $italic(){italic text}.
}

$title(#level=2){Chapter 1}

$section(){
    Another section with $underlined(){underlined text}.
}
```

## Error Handling

The compiler provides warnings and errors for:
- Duplicate style names
- References to non-existent styles
- Invalid argument values (colors, font sizes, etc.)
- Multiple calls to single-use instructions (`$pageNumber`, `$numberizeTitle`)
- Invalid nesting of instructions

When invalid values are provided, default values are used and a warning is displayed in the console.
