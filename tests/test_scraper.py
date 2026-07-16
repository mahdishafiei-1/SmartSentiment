import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from scraper import extract_and_print_comments
import pytest
from playwright.sync_api import Page


def test_extract_and_print_comments(page: Page, capsys):
    mock_html = """
    <div id="commentSection">
        <article class="br-list-vertical-no-padding-200">
            <p class="text-body1-strong-compact">مهدی شفیعی</p>
            <p class="text-body-1 text-neutral-900">بسیار با کیفیت و عالی</p>
            <p class="inline-block text-caption-strong">خریدار</p>
            <div>صاحب‌نظر</div>
            <div>
                <img src="/statics/img/svg/star-fill.svg" />
                <img src="/statics/img/svg/star-fill.svg" />
                <img src="/statics/img/svg/star-fill.svg" />
                <img src="/statics/img/svg/star-fill.svg" />
                <img src="/statics/img/svg/star-fill.svg" />
            </div>
        </article>
    </div>
    """

    page.set_content(mock_html)
    
    extract_and_print_comments(page, page_number=1)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Name: مهدی شفیعی" in output
    assert "Text: بسیار با کیفیت و عالی" in output
    assert "Is buyer: 1" in output
    assert "Is expert: 1" in output
    assert "Star: 5" in output
