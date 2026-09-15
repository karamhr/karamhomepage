import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def article(article_id):
    return {
        "id": article_id,
        "slug": f"article-{article_id}",
        "kicker": "TEST",
        "category": "검증",
        "title": f"테스트 글 {article_id}",
        "summary": f"테스트 글 {article_id} 요약",
        "reading_minutes": 3,
        "lead": f"테스트 글 {article_id} 리드",
        "body_html": "<h2><span>POINT 01</span>검증</h2><p>본문</p>",
        "notice": "안내문",
        "cta_title": "상담 제목",
        "cta_text": "상담 설명",
    }


class ColumnGeneratorTest(unittest.TestCase):
    def generate(self, project, columns):
        (project / "content").mkdir()
        (project / "content" / "columns.json").write_text(
            json.dumps({"columns": columns}, ensure_ascii=False), encoding="utf-8"
        )
        generator = Path(__file__).parent / "tools" / "generate_columns.py"
        return subprocess.run(
            [sys.executable, str(generator), "--project", str(project)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_generator_creates_articles_only_in_columns_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.generate(project, [article(1), article(2)])

            self.assertEqual(result.returncode, 0, result.stderr)
            listing = (project / "columns.html").read_text(encoding="utf-8")
            newest = (project / "columns" / "column-02-article-2.html").read_text(encoding="utf-8")
            oldest = (project / "columns" / "column-01-article-1.html").read_text(encoding="utf-8")

            self.assertLess(listing.index("테스트 글 2"), listing.index("테스트 글 1"))
            self.assertIn('href="columns/column-02-article-2.html"', listing)
            self.assertIn('href="column-01-article-1.html"', newest)
            self.assertIn('href="../styles.css"', newest)
            self.assertIn('href="../columns.html"', newest)
            self.assertIn('href="column-02-article-2.html"', oldest)
            self.assertFalse((project / "column-02-article-2.html").exists())
            self.assertFalse((project / "column-01-article-1.html").exists())

    def test_generator_splits_seven_columns_into_two_listing_pages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.generate(project, [article(number) for number in range(1, 8)])

            self.assertEqual(result.returncode, 0, result.stderr)
            first_page = (project / "columns.html").read_text(encoding="utf-8")
            second_page = (project / "columns-page-2.html").read_text(encoding="utf-8")

            self.assertIn("테스트 글 7", first_page)
            self.assertIn("테스트 글 2", first_page)
            self.assertNotIn("테스트 글 1", first_page)
            self.assertIn("테스트 글 1", second_page)
            self.assertNotIn("테스트 글 2", second_page)
            self.assertIn('href="columns-page-2.html"', first_page)
            self.assertIn('href="columns.html"', second_page)
            self.assertIn('class="page-link active"', first_page)
            self.assertIn('class="page-link active"', second_page)


if __name__ == "__main__":
    unittest.main(verbosity=2)
