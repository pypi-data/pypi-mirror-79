# Markdown-changelog

Markdown extension to enable easy addition of changelog badges to your documentation

## Installation

The easiest way to install `markdown-changelog` is to use pip

```bash
pip install markdown-changelog
```

## Usage

Changelog adds the ability to insert styled `<span>TAG</span>` tags that with appropriate CSS are rendered as 
changelog badges in your documentation. The syntax requires the text to be surrounded by double semi-colon (;) signs.

To add a badge to your documentation simply surround the appropriate tag with double `;`.

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

## Options

- `inline_style` - if `True`, the CSS style will be set inline rather so no additional CSS file(s) are required
- `auto_capitalize` - if `True`, the tag will be automatically capitalized
- `text_color` - color of the text (use HEX with # e.g. #FFFFFF)
- `fix_color` - color of the `Fix` tag
- `change_color` - color of the `Change` tag
- `improvement_color` - color of the `Improvement` tag
- `new_color` - color of the `New` tag
- `docs_color` - color of the `Docs` tag
- `efficiency_color` - color of the `Efficency` tag

## Supported tags

The following tags are supported by default:

- fix
- change (or changes changed)
- improvement (or improvements, enhancement, enhancements)
- new (or feature)
- efficiency
- docs (or documentation)

All must be wrapped in double `;`

## CCS

Minimum style required to render the badges correctly. You can instead use the `inline_style=True` if you want the
style to be set on each item separately

```css
.badge {
  display: inline-block;
  font-size: 14px;
  line-height: 14px;
  color: #ffffff;
  vertical-align: baseline;
  white-space: nowrap;
  background-color: #999999;
  padding: 2px 9px;
  border-radius: 9px;
}
.badge-fix {
    background-color: #dc3545;
}
.badge-change {
  background-color: #fd7e14;
}
.badge-improvement {
  background-color: #007bff;
}
.badge-new {
  background-color: #28a745;
}
.badge-docs {
  background-color: #6610f2;
}
.badge-efficiency {
  background-color: #17a2b8;
}

```