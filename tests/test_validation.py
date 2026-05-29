"""Validation tests for the cybersecurity handbooks repository."""
import os
import re
import urllib.parse

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HANDBOOKS_DIR = os.path.join(ROOT, "handbooks")
README_PATH = os.path.join(ROOT, "README.md")


def list_handbooks():
    return sorted(f for f in os.listdir(HANDBOOKS_DIR) if f.endswith(".md"))


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestRepositoryStructure:

    def test_handbooks_directory_exists(self):
        assert os.path.isdir(HANDBOOKS_DIR)

    def test_readme_exists(self):
        assert os.path.isfile(README_PATH)

    def test_license_exists(self):
        assert os.path.isfile(os.path.join(ROOT, "LICENSE"))

    def test_images_directory_exists(self):
        assert os.path.isdir(os.path.join(ROOT, "images"))

    def test_ci_workflow_exists(self):
        ci_path = os.path.join(ROOT, ".github", "workflows", "ci.yml")
        assert os.path.isfile(ci_path), "CI/CD workflow ci.yml is missing"
        content = read_file(ci_path)
        assert "CI/CD Pipeline" in content
        assert "lint:" in content
        assert "test:" in content
        assert "build:" in content
        assert "deploy:" in content


class TestHandbookFiles:

    @pytest.fixture(scope="class")
    def handbooks(self):
        return list_handbooks()

    def test_all_handbooks_have_content(self, handbooks):
        for hb in handbooks:
            path = os.path.join(HANDBOOKS_DIR, hb)
            content = read_file(path)
            assert len(content.strip()) > 100, f"{hb} is too short (< 100 chars)"

    def test_all_handbooks_have_title(self, handbooks):
        for hb in handbooks:
            path = os.path.join(HANDBOOKS_DIR, hb)
            content = read_file(path)
            has_title = bool(re.search(r"^#\s+.+", content, re.MULTILINE))
            assert has_title, f"{hb} is missing a top-level heading (# Title)"

    def test_all_handbooks_have_toc(self, handbooks):
        for hb in handbooks:
            path = os.path.join(HANDBOOKS_DIR, hb)
            content = read_file(path)
            has_toc = "## Table of Contents" in content or "## Contents" in content
            if not has_toc:
                has_toc = bool(re.search(r"^-\s+\[.*\]\(#", content, re.MULTILINE))
            assert has_toc, f"{hb} is missing a table of contents"

    def test_handbooks_file_size_within_reasonable_limits(self, handbooks):
        max_bytes = 1024 * 1024  # 1 MB
        for hb in handbooks:
            path = os.path.join(HANDBOOKS_DIR, hb)
            size = os.path.getsize(path)
            assert size <= max_bytes, f"{hb} exceeds 1 MB ({size} bytes)"


class TestReadme:

    def test_readme_has_title(self):
        content = read_file(README_PATH)
        assert "# Awesome Cybersecurity Handbooks" in content

    def test_readme_has_table_of_contents(self):
        content = read_file(README_PATH)
        assert "## Table of Contents" in content

    def test_readme_linked_files_exist(self):
        content = read_file(README_PATH)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        handbook_links = [
            (name, path) for name, path in links
            if path.startswith("handbooks/")
        ]
        missing = []
        for name, path in handbook_links:
            decoded = urllib.parse.unquote(path)
            full_path = os.path.join(ROOT, decoded)
            if not os.path.isfile(full_path):
                missing.append(f"{name} -> {path} (decoded: {decoded})")
        assert not missing, f"Missing handbook files: {missing}"

    def test_readme_linked_images_exist(self):
        content = read_file(README_PATH)
        images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
        missing = []
        for alt, path in images:
            if path.startswith(("http://", "https://", "//")):
                continue
            full_path = os.path.join(ROOT, path)
            if not os.path.isfile(full_path):
                missing.append(f"{alt} -> {path}")
        assert not missing, f"Missing image files: {missing}"

    def test_readme_badges_use_shields_io(self):
        content = read_file(README_PATH)
        badges = re.findall(r"https://img\.shields\.io/[^\s)\"]+", content)
        assert len(badges) > 0, "No shields.io badges found in README"


class TestMarkdownQuality:

    def _strip_code_blocks(self, markdown_content):
        result = re.sub(r"```[\s\S]*?```", "", markdown_content)
        result = re.sub(r"`[^`]+`", "", result)
        return result

    def _looks_like_file_path(self, link):
        decoded = urllib.parse.unquote(link)
        if "/" not in decoded and not decoded.endswith(".md"):
            return False
        return True

    def test_no_broken_internal_links(self):
        all_md_files = [os.path.join(HANDBOOKS_DIR, f) for f in list_handbooks()]
        all_md_files.append(README_PATH)

        internal_links = {}
        for md_file in all_md_files:
            rel_path = os.path.relpath(md_file, ROOT)
            content = self._strip_code_blocks(read_file(md_file))
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            internal_links[rel_path] = links

        broken = []
        for filepath, links in internal_links.items():
            basedir = os.path.dirname(os.path.join(ROOT, filepath))
            for name, link in links:
                if link.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                decoded = urllib.parse.unquote(link)
                if not self._looks_like_file_path(decoded):
                    continue
                if decoded.startswith("/"):
                    target = os.path.join(ROOT, decoded[1:])
                else:
                    target = os.path.normpath(os.path.join(basedir, decoded))
                if not os.path.exists(target):
                    broken.append(f"{filepath}: '{name}' -> '{link}' (resolved: {target})")

        assert not broken, f"Broken internal links:\n" + "\n".join(broken[:20])

    @pytest.mark.parametrize("ext", [".yml", ".yaml", ".toml", ".json"])
    def test_config_files_are_valid(self, ext):
        config_dir = os.path.join(ROOT, ".github")
        if not os.path.isdir(config_dir):
            pytest.skip("No .github directory")
        for root, dirs, files in os.walk(ROOT):
            for f in files:
                if f.endswith(ext):
                    path = os.path.join(root, f)
                    content = read_file(path)
                    assert len(content) > 0, f"Empty config file: {path}"
