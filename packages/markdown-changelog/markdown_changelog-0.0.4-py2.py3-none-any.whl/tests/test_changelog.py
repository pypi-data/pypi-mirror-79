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
            extensions=[
                ChangelogExtension(
                    inline_style=bool_value,
                    auto_capitalize=bool_value,
                    text_color=color,
                    fix_color=color,
                    rounded_corners=bool_value,
                    version_color=color,
                )
            ]
        )
        ext = md.registeredExtensions[0]
        assert ext.config["inline_style"][0] == bool_value
        assert ext.config["auto_capitalize"][0] == bool_value
        assert ext.config["rounded_corners"][0] == bool_value
        assert ext.config["text_color"][0] == color
        assert ext.config["fix_color"][0] == color
        assert ext.config["version_color"][0] == color

    @pytest.mark.parametrize(
        "text_in, expected",
        (
            [""";;fix;;""", '<p><span class="badge badge-fix">Fix</span></p>'],
            [""";;fiX;;""", '<p><span class="badge badge-fix">Fix</span></p>'],
            [""";;change;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;changes;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;changed;;""", '<p><span class="badge badge-change">Change</span></p>'],
            [""";;new;;""", '<p><span class="badge badge-new">New</span></p>'],
            [""";;feature;;""", '<p><span class="badge badge-new">New</span></p>'],
            [""";;improvement;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;improved;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;improvements;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;enhancement;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;enhanced;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;enhancements;;""", '<p><span class="badge badge-improvement">Improvement</span></p>'],
            [""";;docs;;""", '<p><span class="badge badge-docs">Docs</span></p>'],
            [""";;doc;;""", '<p><span class="badge badge-docs">Docs</span></p>'],
            [""";;documentation;;""", '<p><span class="badge badge-docs">Docs</span></p>'],
            [""";;efficiency;;""", '<p><span class="badge badge-efficiency">Efficiency</span></p>'],
            [""";;VERv0.0.1;;""", '<p><span class="badge badge-version">v0.0.1</span></p>'],
            [""";;VER  v0.0.3;;""", '<p><span class="badge badge-version">v0.0.3</span></p>'],
        ),
    )
    def test_extension_parse(self, text_in, expected):
        md = markdown.Markdown(extensions=[ChangelogExtension()])
        result = md.convert(text_in)
        assert result == expected

    @pytest.mark.parametrize(
        "text_in, expected",
        (
            [""";;fix;;""", '<p><span class="badge badge-fix badge-square">Fix</span></p>'],
            [""";;fiX;;""", '<p><span class="badge badge-fix badge-square">Fix</span></p>'],
            [""";;change;;""", '<p><span class="badge badge-change badge-square">Change</span></p>'],
            [""";;changes;;""", '<p><span class="badge badge-change badge-square">Change</span></p>'],
            [""";;changed;;""", '<p><span class="badge badge-change badge-square">Change</span></p>'],
            [""";;new;;""", '<p><span class="badge badge-new badge-square">New</span></p>'],
            [""";;feature;;""", '<p><span class="badge badge-new badge-square">New</span></p>'],
            [""";;improvement;;""", '<p><span class="badge badge-improvement badge-square">Improvement</span></p>'],
            [""";;improvements;;""", '<p><span class="badge badge-improvement badge-square">Improvement</span></p>'],
            [""";;enhancement;;""", '<p><span class="badge badge-improvement badge-square">Improvement</span></p>'],
            [""";;enhancements;;""", '<p><span class="badge badge-improvement badge-square">Improvement</span></p>'],
            [""";;docs;;""", '<p><span class="badge badge-docs badge-square">Docs</span></p>'],
            [""";;documentation;;""", '<p><span class="badge badge-docs badge-square">Docs</span></p>'],
            [""";;efficiency;;""", '<p><span class="badge badge-efficiency badge-square">Efficiency</span></p>'],
            [""";;VERv0.0.1;;""", '<p><span class="badge badge-version badge-square">v0.0.1</span></p>'],
            [""";;VER  v0.0.3;;""", '<p><span class="badge badge-version badge-square">v0.0.3</span></p>'],
        ),
    )
    def test_extension_parse_square(self, text_in, expected):
        md = markdown.Markdown(extensions=[ChangelogExtension(rounded_corners=False)])
        result = md.convert(text_in)
        assert result == expected

    @pytest.mark.parametrize(
        "text_in", (";;fix;;", ";;new;;", ";;change;;", ";;improvement;;", ";;docs;;", ";;efficiency;;")
    )
    def test_extension_parse_inline_style(self, text_in):
        md = markdown.Markdown(extensions=[ChangelogExtension(inline_style=True, text_color="#FF00FF")])
        result = md.convert(text_in)
        assert "background-color:" in result
        assert "; color: #FF00FF;" in result

    @pytest.mark.parametrize("text_in", (";;VERv0.0.1;;",))
    def test_extension_parse_inline_style_version(self, text_in):
        md = markdown.Markdown(extensions=[ChangelogExtension(inline_style=True, text_color="#FF00FF")])
        result = md.convert(text_in)
        assert "background-color:" in result
        assert "; color: #FF00FF;" in result
        assert "font-weight" in result
