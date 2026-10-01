# Static Site Generator

A lightweight, zero-dependency Static Site Generator built in Python from first principles.

This project converts raw Markdown files and directory hierarchies into static HTML websites using an Abstract Syntax Tree (AST) node pipeline, dynamic templating, recursive directory crawling, and asset synchronization.

Deployed live on GitHub Pages: **[Live Demo](https://KreimerJ.github.io/static_site_generator/)**

---

## Architecture & Pipeline

The system processes content through a four-stage unidirectional pipeline:

```
[Raw Markdown] → [Inline & Block Parsers] → [HTML Node AST] → [Template Engine] → [Docs Output]
```

### 1. Data Layer (`src/textnode.py`, `src/htmlnode.py`)
* **`TextNode`**: Represents inline text tokens paired with a `TextType` enum (`PLAIN`, `BOLD`, `ITALIC`, `CODE`, `LINK`, `IMAGE_LINK`).
* **`HTMLNode` Hierarchy**:
  * `HTMLNode`: Abstract base representation of an HTML element.
  * `LeafNode`: Terminal HTML elements without children (`<p>`, `<b>`, `<img>`, `<a>`).
  * `ParentNode`: Composite HTML container elements holding nested children (`<div>`, `<ul>`, `<ol>`, `<blockquote>`).

### 2. Parser Layer (`src/inline_markdown_syntax.py`, `src/block_markdown_syntax.py`)
* **Inline Parser**: Splits raw text into typed tokens using delimiter algorithms (`**`, `_`, `` ` ``) and regular expressions with negative lookbehinds for non-colliding image (`![alt](url)`) and link (`[anchor](url)`) extraction.
* **Block Parser**: Slices multi-line documents into structural blocks, identifies block types (`HEADING`, `PARAGRAPH`, `CODE`, `QUOTE`, `UNORDERED_LIST`, `ORDERED_LIST`), and constructs corresponding AST subtrees.
* **Title Extraction**: Automatically parses the primary `# ` document header to populate HTML `<title>` tags dynamically.

### 3. Build & Generation Engine (`src/copy_static.py`, `src/generate_page.py`)
* **Asset Pipeline**: Purges and mirrors the `static/` asset directory into `docs/` recursively.
* **Page Generator**: Recursively crawls `content/`, generates corresponding `.html` files in `docs/` preserving folder hierarchy, and injects rendered HTML into `template.html`.
* **Configurable Basepath**: Supports relative and root path rewrites (`href` and `src` attributes) via CLI arguments for deployment flexibility between local development and GitHub Pages subdirectories.

---

## Project Structure

```text
├── content/              # Source Markdown documents
├── docs/                 # Production build output (served by GitHub Pages)
├── static/               # Source static assets (CSS, images)
├── src/
│   ├── textnode.py               # TextNode model & enum converter
│   ├── htmlnode.py               # HTMLNode AST base class
│   ├── leafnode.py               # Terminal HTML node representation
│   ├── parentnode.py             # Composite HTML container node
│   ├── inline_markdown_syntax.py # Inline token delimiter & regex parsers
│   ├── block_markdown_syntax.py  # Block-level parser & AST builder
│   ├── copy_static.py            # Static directory replication utility
│   ├── generate_page.py          # Recursive page builder & template injector
│   ├── main.py                   # CLI entrypoint and argument parser
│   └── test_*.py                 # Comprehensive unit test suites
├── template.html         # HTML layout template with {{ Title }} and {{ Content }}
├── main.sh               # Local build and HTTP development server script
├── build.sh              # Production build script for GitHub Pages deployment
└── test.sh               # Automated test runner script
```

---

## Getting Started

### Prerequisites
* Python 3.10 or higher.
* Standard Library only — no third-party packages or virtual environments required.

### Running the Test Suite
The project includes automated unit test coverage across all AST nodes, delimiter splitters, regex extractors, and block parsers:

```bash
./test.sh
```
*(Runs `python3 -m unittest discover -s src`)*

### Local Development Server
To generate the static pages for local testing and start the local development web server:

```bash
./main.sh
```

By default, the development server runs at:
```text
http://localhost:8888
```

---

## Deployment (GitHub Pages)

To compile the site for production hosting on GitHub Pages:

1. Run the production build script:
   ```bash
   ./build.sh
   ```
   *(Executes `python3 src/main.py "/static_site_generator/"` targeting the `/docs` directory).*

2. Commit the generated `/docs` directory to `main` and push to GitHub.
3. In GitHub repository settings under **Pages**, configure the source to deploy from the `/docs` folder on the `main` branch.
