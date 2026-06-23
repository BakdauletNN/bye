import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_openapi_is_available():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        response = await client.get('/openapi.json')
        assert response.status_code == 200
        assert response.json().get('openapi', '').startswith('3.')


@pytest.mark.asyncio
async def test_login_requires_credentials():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        response = await client.post('/auth/login', json={'username': '', 'password': ''})
        assert response.status_code in (400, 401, 422)


@pytest.mark.asyncio
async def test_get_students_requires_admin():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        response = await client.get('/students')
        assert response.status_code in (401, 422, 403)
