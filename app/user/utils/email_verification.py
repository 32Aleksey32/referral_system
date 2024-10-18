import httpx

from app.errors import CustomError
from app.settings import HUNTER_API_KEY


async def verify_email_via_hunter(email: str):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return None

        data = response.json()

        # Возвращаем ответ для доменов .ru без дополнительных проверок
        email_domain = email.split('@')[-1]
        if email_domain.endswith('.ru'):
            return data

        if data['data']['result'] != 'deliverable':
            raise CustomError('Введенный email не действителен или не подлежит проверке.', status_code=422)

        return data
