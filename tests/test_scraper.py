import os
import sys
import pytest
from unittest.mock import patch

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from database import Reviews
from playwright.sync_api import Page
from scraper import extract_and_save_comments


def test_extract_and_save_comments(page: Page, db_session):
    mock_html = """
    <div id="commentSection">
        <article class="br-list-vertical-no-padding-200">
            <p class="text-body1-strong-compact">مهدی شفیعی</p>
            <p class="text-body-1 text-neutral-900">بسیار با کیفیت و عالی</p>
            <p class="inline-block text-caption-strong">خریدار</p>
            <div>صاحب‌نظر</div>
            <div class="absolute inset-0 overflow-hidden" style="width: 100%;">
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

    with patch("scraper.get_db", return_value=iter([db_session])):
        extract_and_save_comments(page, page_number=1)
    
    saved_review = db_session.query(Reviews).filter_by(user_name="مهدی شفیعی").first()
    
    try:
        assert saved_review is not None
        assert saved_review.text == "بسیار با کیفیت و عالی"
        assert saved_review.is_buyer == 1
        assert saved_review.is_expert == 1
        assert saved_review.star == 5

    finally:
        if saved_review:
            db_session.delete(saved_review)
            db_session.commit()