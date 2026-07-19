import os
import sys
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from database import Base 


src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(root_path, ".env")
load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope="function")
def page():
    chrome_path = os.getenv("CHROME_EXECUTABLE_PATH")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=chrome_path
        )
        page = browser.new_page()
        yield page
        browser.close()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
