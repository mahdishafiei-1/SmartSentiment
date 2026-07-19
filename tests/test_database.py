import os
import sys
import pytest
from sqlalchemy.exc import IntegrityError

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from database import Reviews, add_new_review

def test_add_new_review_function(db_session):
    new_review = add_new_review(db=db_session, user_name = "مهدی شفیعی", text = "بسیار با کیفیت و عالی", is_buyer= 1, is_expert= 1, star= 5)
    
    assert new_review.id is not None
    assert new_review.star == 5
    assert new_review.text == "بسیار با کیفیت و عالی"

def test_create_review(db_session):
    new_review = Reviews(user_name = "مهدی شفیعی", text = "بسیار با کیفیت و عالی", is_buyer= 1, is_expert= 1, star= 5)

    db_session.add(new_review)
    db_session.commit()
    
    created_review = db_session.query(Reviews).filter_by(user_name="مهدی شفیعی").first()
    
    assert created_review is not None
    assert created_review.id is not None
    assert created_review.star == 5
    assert created_review.is_buyer == 1
    assert created_review.is_expert == 1
    assert created_review.text == "بسیار با کیفیت و عالی"


def test_delete_review(db_session):
    new_review = Reviews(user_name = "مهدی شفیعی", text = "بسیار با کیفیت و عالی", is_buyer= 1, is_expert= 1, star= 5)

    db_session.add(new_review)
    db_session.commit()

    db_session.delete(new_review)
    db_session.commit()
    
    deleted_review = db_session.query(Reviews).filter_by(user_name="مهدی شفیعی").first()
    assert deleted_review is None

def test_update_review(db_session):
    new_review = Reviews(user_name = "مهدی شفیعی", text = "بسیار با کیفیت و عالی", is_buyer= 1, is_expert= 1, star= 5)

    db_session.add(new_review)
    db_session.commit()

    new_review.star = 3
    db_session.commit()
    
    updated_review = db_session.query(Reviews).filter_by(user_name="مهدی شفیعی").first()
    assert updated_review.star == 3

def test_review_requires_username(db_session):
    bad_review = Reviews(
        user_name=None,
        text="بدون نام",
        star=3
    )
    
    db_session.add(bad_review)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
