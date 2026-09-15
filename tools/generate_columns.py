#!/usr/bin/env python3
"""content/columns.json을 바탕으로 columns/ 상세 페이지와 목록 페이지를 생성합니다."""

import argparse
import html
import json
from pathlib import Path

PAGE_SIZE = 6


def esc(value):
    return html.escape(str(value), quote=True)


def display_title(column):
    return " ".join(str(column["title"]).split())


def filename(column):
    return f"column-{int(column['id']):02d}-{column['slug']}.html"


def listing_filename(page_number):
    return "columns.html" if page_number == 1 else f"columns-page-{page_number}.html"


def title_html(column):
    return column.get("title_html") or esc(column["title"]).replace("\n", "<br>")


def site_header(root_prefix):
    return f'''<header class="site-header"><div class="wrap site-header-inner"><a class="brand" href="{root_prefix}index.html"><span class="brand-mark">K</span>노무법인 가람경영컨설팅</a><nav class="nav"><a href="{root_prefix}index.html">홈</a><a href="{root_prefix}about.html">법인소개</a><a href="{root_prefix}services.html">업무분야</a><a href="{root_prefix}subscription.html">기업자문</a><a class="active" href="{root_prefix}columns.html">노무칼럼</a></nav><a class="head-cta" href="{root_prefix}contact.html">상담 신청 →</a><button class="menu-button" aria-label="메뉴"><i></i><i></i><i></i></button></div></header>'''


def column_nav(columns, position):
    links = []
    if position + 1 < len(columns):
        previous = columns[position + 1]
        links.append(f'<a href="{filename(previous)}">← 이전 글<b>{esc(display_title(previous))}</b></a>')
    if position > 0:
        following = columns[position - 1]
        links.append(f'<a href="{filename(following)}">다음 글 →<b>{esc(display_title(following))}</b></a>')
    return f'<nav class="column-nav">{"".join(links)}</nav>' if links else ""


def render_detail(column, columns, position):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(display_title(column))} | 노무법인 가람</title><link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../theme-blue.css"><link rel="stylesheet" href="../column-detail.css"></head><body>
{site_header('../')}
<main><section class="column-hero"><div class="wrap"><a class="column-back" href="../columns.html">← 노무칼럼으로 돌아가기</a><p class="column-kicker">{esc(column["kicker"])} · {int(column["id"]):02d}</p><h1>{title_html(column)}</h1><div class="column-meta"><span>{esc(column["category"])}</span><span>읽는 시간 {int(column["reading_minutes"])}분</span><span>노무법인 가람</span></div></div></section>
<div class="wrap column-layout"><article class="column-body"><p class="lead-copy">{esc(column["lead"])}</p>
{column["body_html"]}
{column_nav(columns, position)}<p class="column-notice">{esc(column["notice"])}</p></article>
<aside class="column-side"><div class="side-card"><small>NEED HELP?</small><h3>{column.get("cta_title_html") or esc(column["cta_title"]).replace(chr(10), "<br>")}</h3><p>{esc(column["cta_text"])}</p><a href="../contact.html">상담 신청 <span>→</span></a></div></aside></div></main>
<footer class="footer"></footer><script src="../script.js"></script></body></html>
'''


def render_pagination(page_number, total_pages):
    if total_pages <= 1:
        return ""

    links = []
    if page_number > 1:
        links.append(f'<a class="page-link page-prev" href="{listing_filename(page_number - 1)}">← 이전</a>')
    for number in range(1, total_pages + 1):
        active = " active" if number == page_number else ""
        links.append(f'<a class="page-link{active}" href="{listing_filename(number)}">{number}</a>')
    if page_number < total_pages:
        links.append(f'<a class="page-link page-next" href="{listing_filename(page_number + 1)}">다음 →</a>')
    return f'<nav class="pagination" aria-label="노무칼럼 페이지">{"".join(links)}</nav>'


def render_listing(page_columns, page_number, total_pages):
    cards = "\n".join(
        f'        <a class="post-link" href="columns/{filename(column)}" aria-label="{esc(display_title(column))} 칼럼 읽기"><article class="post"><p class="type">{esc(column["kicker"])} · {int(column["id"]):02d}</p><h3>{esc(display_title(column))}</h3><p>{esc(column["summary"])}</p><span>칼럼 읽기 <b>→</b></span></article></a>'
        for column in page_columns
    )
    pagination = render_pagination(page_number, total_pages)
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>노무칼럼 | 노무법인 가람</title><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme-blue.css"><link rel="stylesheet" href="column-detail.css"></head><body>
{site_header('')}
<main><section class="subhero"><div class="wrap"><p class="eyebrow">LABOR INSIGHT</p><h1>일하는 모든 순간에<br><span class="highlight">필요한 기준을 나눕니다.</span></h1><p>사업장 운영에 도움이 되는 노동·인사 정보를 쉽게 정리합니다.</p></div></section>
<section class="section wrap"><div class="section-head"><div><p class="eyebrow">LATEST COLUMNS</p><h2>노무칼럼</h2></div><p class="body-copy">실무에서 자주 만나는<br>노무 이슈를 전합니다.</p></div><div class="post-grid">
{cards}
</div>{pagination}</section></main>
<footer class="footer"><div class="wrap footer-grid"><a class="brand" href="index.html"><span class="brand-mark">K</span>노무법인 가람경영컨설팅</a><p>평일 09:00–18:00 · 031-755-0052</p></div></footer><script src="script.js"></script></body></html>
'''


def generate(project):
    data_path = project / "content" / "columns.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    columns = sorted(data["columns"], key=lambda item: int(item["id"]), reverse=True)
    ids = [int(item["id"]) for item in columns]
    if len(ids) != len(set(ids)):
        raise ValueError("칼럼 id는 중복될 수 없습니다.")

    article_dir = project / "columns"
    article_dir.mkdir(exist_ok=True)
    for position, column in enumerate(columns):
        (article_dir / filename(column)).write_text(render_detail(column, columns, position), encoding="utf-8")

    pages = [columns[index:index + PAGE_SIZE] for index in range(0, len(columns), PAGE_SIZE)] or [[]]
    for old_page in project.glob("columns-page-*.html"):
        old_page.unlink()
    for page_number, page_columns in enumerate(pages, start=1):
        (project / listing_filename(page_number)).write_text(
            render_listing(page_columns, page_number, len(pages)), encoding="utf-8"
        )
    print(f"칼럼 {len(columns)}개, 상세 페이지 및 목록 {len(pages)}페이지를 생성했습니다.")


def main():
    parser = argparse.ArgumentParser(description="노무칼럼 HTML 생성기")
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parent.parent, help="content/columns.json이 있는 프로젝트 폴더")
    args = parser.parse_args()
    generate(args.project.resolve())


if __name__ == "__main__":
    main()
