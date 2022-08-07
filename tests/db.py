import sys
sys.path.append('../cook-book')
from app import app 
from app.models import Recipe , User 
from dotenv import load_dotenv
import pytest

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv("../.env")

# minimal checkup if website is working or not 
def test_db_connectivity():
    # sample query running
    try:
        Recipe.query.all()
        User.query.all()
        assert True
    except Exception as e:
        
        assert False
    
