---
theme: eloc
background: https://cover.sli.dev
title: Accelerating Research with Automation (Day 2)
class: text-center
drawings:
  persist: false
mdc: true
colorSchema: light
highlighter: shiki
---

# Accelerating Research with Automation (Day 2)

Nick Wiltsie, January 2025

---

## Recap of yesterday

![Alt](/IFTTT.svg)
<br />
![Alt](/IFTTT_Expanded.svg)

---

## Day Two

- Overview of YAML and JSON syntax
- Practical exercise in GitHub Actions

---

## YAML Syntax Overview

A Lightweight Data Format for Configuration and Serialization

---

## What is YAML?

- **YAML**: "YAML Ain't Markup Language"
- Human-readable and easy to write
- Commonly used for:
  - Configuration files
  - Data exchange between languages
  - Deployment scripts (e.g., GitHub Actions)

---

## Key Features

- Uses **indentation** to represent structure
- Relies on **key-value pairs**
- Supports comments with `#`
- File extension: `.yaml` or `.yml`

---
layout: two-cols
---

## Basic Structure: Key-Value Pairs

- Keys are strings
- Values can be:
  - Strings
  - Numbers
  - Booleans (true, false)
  - Null (null or ~)

::right::

```yaml
key: value
name: John Doe
age: 30
is_student: false
```

---
layout: two-cols
---

## Nested Data

Use indentation to create nested structures

- Indentation must use spaces (not tabs)
- Each level increases indentation

::right::

```yaml
person:
  name: John Doe
  age: 30
  address:
    street: 123 Elm St
    city: Springfield
```

---

## Lists

Represent lists with a `-`:

```yaml
shopping_list:
  - apples
  - bananas
  - oranges
```

```yaml
employees:
  - name: Alice
    role: Engineer
  - name: Bob
    role: Manager
```

---

## Multiline Strings

Handle multiline strings with `|` or `>`:

```yaml
paragraph: |
  This is a multiline string.
  Each new line is preserved.

single_line: >
  This is folded
  into a single line.
```

---

## Comments

Add comments with `#`:

```yaml
# This is a comment
name: John Doe  # Inline comment
```

---

## Common Pitfalls

- Indentation errors: Use consistent spaces (no tabs).
- Quotes:
  - Use single quotes `'` for literal strings.
  - Use double quotes `"` for escaping special characters.
  - Avoid trailing spaces.

---

## Complete YAML File

```yaml
application:
  name: MyApp
  version: 1.0.0
  contributors:
    - name: Alice
      role: Developer
    - name: Bob
      role: Tester
  settings:
    debug: true
    theme: dark
```

---

## JSON Syntax Overview

JavaScript Object Notation for Data Exchange

---

## What is JSON?

- **JSON**: JavaScript Object Notation
- Lightweight data-interchange format
- Commonly used for:
  - APIs and web applications
  - Configuration files
  - Data storage and exchange

---

## Key Features

- Text-based format
- Language-independent
- Uses **key-value pairs**
- File extension: `.json`

---
layout: two-cols
---

## Basic Structure: Objects

Objects are collections of key-value pairs.

- Keys are strings enclosed in double quotes.
- Values can be:
  - Strings
  - Numbers
  - Booleans (true, false)
  - null
  - Arrays
  - Objects

::right::

```json
{
  "name": "John Doe",
  "age": 30,
  "isStudent": false
}
```

---

## Strings

Strings must be enclosed in double quotes:

```json
{
  "greeting": "Hello, world!"
}
```

Invalid example (no single quotes or unquoted strings):

```json
{
  'greeting': Hello
}
```

---

## Numbers and Booleans

No quotes for numbers or booleans.

```json
{
  "integer": 42,
  "float": 3.14,
  "isAvailable": true,
  "isComplete": false
}
```

---

## Null

Use null to represent a missing or empty value:

```json
{
  "middleName": null
}
```

---
layout: two-cols
---

## Arrays

Represent lists with square brackets `[]`

Arrays can contain:

- Strings
- Numbers
- Booleans
- Objects
- Other arrays

::right::

```json
{
  "fruits": ["apple", "banana", "cherry"]
}
```

---

## Nested Objects

Use curly braces `{}` for nested structures:

```json
{
  "person": {
    "name": "John Doe",
    "age": 30,
    "address": {
      "street": "123 Elm St",
      "city": "Springfield"
    }
  }
}
```

---

## Mixed Arrays

Arrays can combine different types:

```json
{
  "data": [
    "text",
    42,
    true,
    null,
    { "key": "value" }
  ]
}
```

---

## Comments

JSON does not support comments natively.
For commenting, use an external file or inline documentation.

---

## Common Pitfalls

- Keys must be in double quotes:
  - `{"key": value}`
  - ❌ `{'key': value}`
- Trailing commas are not allowed:
  - ❌ `[1, 2, 3, ]`
- Must use UTF-8 encoding

---

## Example: Complete JSON File

```json
{
  "application": {
    "name": "MyApp",
    "version": "1.0.0",
    "contributors": [
      { "name": "Alice", "role": "Developer" },
      { "name": "Bob", "role": "Tester" }
    ],
    "settings": {
      "debug": true,
      "theme": "dark"
    }
  }
}
```

---
layout: two-cols
---

## JSON vs YAML

JSON:

- Uses curly braces `{}` and square brackets `[]`
- No support for comments
- Strict syntax (e.g., quotes)

::right::

YAML:

- Uses indentation
- Supports comments with `#`
- More human-readable

---

## CSV Syntax Overview

Comma-Separated Values for Tabular Data

---

## What is CSV?

- **CSV**: Comma-Separated Values
- Simple text format for tabular data
- Commonly used for:
  - Data exchange between systems
  - Spreadsheets and databases
  - Import/export in tools like Excel, pandas, etc.

---

## Key Features

- Plain text format
- **Rows** represent records
- **Columns** separated by commas
- File extension: `.csv`

---

## Basic Structure

A simple CSV file:

```csv
Name,Age,Location
John Doe,30,Springfield
Jane Smith,25,Shelbyville
```

First row: Column headers

Subsequent rows: Data records

Values separated by commas `,`

---

## Standardization

No Standard for Data Types

- All values are text by default
- Interpretation of numbers, dates, etc., depends on the application

```csv
Name,Age,IsStudent,Date
John,30,false,2024-01-01
Jane,25,true,2023-02-17
```

---

## Missing Values

Leave cells blank for missing values:

```csv
Name,Age,Location
John Doe,30,
Jane Smith,,Shelbyville
```

---
layout: two-cols
---

## Strengths of CSV

- Easy to read and write
- Widely supported across tools
- Compact representation for small datasets

::right::

## Limitations of CSV

- No built-in support for:
  - Hierarchical data
  - Data types (everything is text)
  - Metadata
- Limited handling of:
  - Special characters
  - Non-standard delimiters

---

## CSV vs JSON vs YAML

- CSV: Simple and compact, best for tabular data
- JSON: Structured, supports nested data
- YAML: Readable, supports comments and flexible syntax

---

## Practical Exercise
