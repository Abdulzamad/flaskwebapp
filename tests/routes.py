import sys
sys.path.append('../cook-book')
from app import app
from dotenv import load_dotenv
import pytest

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv("../.env")

# minimal checkup if website is working or not 
def test_routes_get():
    urls = ["/" , "/recipes" ,"/login" , "/register" ]
    load_dotenv("../.env")
    app.testing =True
    for url in urls:
        response = app.test_client().get(url)
        assert response.status_code == 200 

def test_routes_post():
    urls = ["/login" , "/register" ]
    load_dotenv("../.env")
    app.testing =True
    for url in urls:
        response = app.test_client().post(url)
        assert response.status_code == 200