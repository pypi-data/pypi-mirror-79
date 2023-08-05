"""Test mdx_changelog extension"""
from markdown_changelog import ChangelogExtension
import pytest
import markdown


class TestMarkdownChangelogExtension:
    def test_load_extension_as_string(self):
        md = markdown.Markdown(extensions=["markdown_changelog.changelog"])
        assert len(md.registeredExtensions) == 1

    def test_load_extension_as_string_alt(self):
        md = markdown.Markdown(extensions=["changelog"])
        assert len(md.registeredExtensions) == 1

    def test_load_extension_as_instance(self):
        md = markdown.Markdown(extensions=[ChangelogExtension()])
        assert len(md.registeredExtensions) == 1

    @pytest.mark.parametrize("bool_value", [True, False])
    @pytest.mark.parametrize("color", ["#FF00FF"])
    def test_configs_parameter(self, bool_value, color):
        md = markdown.Markdown(
            extensions=[ChangelogExtension(inline_style=bool_value, auto_capitalize=bool_value, text_color=color)]
        )
        ext = md.registeredExtensions[0]
        assert ext.config["inline_style"][0] == bool_value
        assert ext.config["auto_capitalize"][0] == bool_value
        assert ext.config["text_color"][0] == color

    @pytest.mark.parametrize(
        "text_in, expected",
        (
            [""";;fix;;""", '<p><span class="badge badge-fix">Fix</span></p>'],
            [""";;change;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;changes;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;changed;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;new;;""", '<p><span class="badge badge-new">New</span></p>'],
            [""";;feature;;""", '<p><span class="badge badge-new">New</span></p>'],
            [""";;improvement;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;improvements;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;enhancement;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;enhancements;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;docs;;""", '<p><span class="badge badge-docs">Docs</span></p>'],
            [""";;documentation;;""", '<p><span class="badge badge-docs">Docs</span></p>'],
            [""";;efficiency;;""", '<p><span class="badge badge-efficiency">Efficiency</span></p>'],
        ),
    )
    def test_extension_parse(self, text_in, expected):
        md = markdown.Markdown(extensions=[ChangelogExtension()])
        result = md.convert(text_in)
        assert result == expected
