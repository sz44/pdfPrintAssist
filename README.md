## PDF packing tool

Takes as input pdf files and merges them into a single page for convinent printing and saving paper.


## Installation

### Clone this repository:
```bash
git clone https://github.com/yourusername/pdf-packing-tool.git
cd pdf-packing-tool
```

### Install dependencies using uv:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage
Basic usage:
```bash
python main.py input1.pdf input2.pdf input3.pdf
```
## Dependencies

This project uses the following Python packages:
- Python 3.10 or higher
- numpy (≥2.2.2)
- pillow (≥11.1.0)
- pymupdf (≥1.25.2)
- pypdf (≥5.1.0)
- ruff (≥0.9.2)

All dependencies are managed through `pyproject.toml` and can be installed automatically using `uv`.
