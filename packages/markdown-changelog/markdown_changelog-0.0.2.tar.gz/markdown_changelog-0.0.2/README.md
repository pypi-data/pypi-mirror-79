# Markdown-changelog

Markdown extension to enable easy addition of changelog badges to your documentation

## Installation

The easiest way to install `markdown-changelog` is to use pip

```bash
pip install markdown-changelog
```

## Usage
```python
import markdown

text = """;;fix;;"""
md = markdown.Markdown(extensions=["changelog"])
md.convert(text)
'<p><span class="badge badge-fix">Fix</span></p>'

# or
md = markdown.Markdown(extensions=["markdown_changelog.changelog"])
md.convert(text)
'<p><span class="badge badge-fix">Fix</span></p>'

# or 
from markdown_changelog import ChangelogExtension
md = markdown.Markdown(extensions=[ChangelogExtension()])

md.convert(text)
'<p><span class="badge badge-fix">Fix</span></p>'
```

## Supported tags

The following tags are supported by default:

- ;;fix;;
- ;;change;; (or ;;changes;;, ;;changed;;)
- ;;improvement;; (or ;;improvements;;, ;;enhancement;;, ;;enhancements;;)
- ;;new;;  (or ;;feature;;)
- ;;efficiency;;
- ;;docs;; (or ;;documentation;;)
