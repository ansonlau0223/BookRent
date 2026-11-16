import asyncio

import httpx


BASE_URL = "http://127.0.0.1:8000"


async def login(
    client: httpx.AsyncClient,
    email: str,
    password: str
):
    response = await client.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]


async def rent_book(
    client: httpx.AsyncClient,
    token: str
):
    return await client.post(
        f"{BASE_URL}/books/121/rentals",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "rentalPeriodDays": 30
        }
    )


async def main():
    async with httpx.AsyncClient() as client:
        token_a = await login(
            client,
            "usera@example.com",
            "string"
        )

        token_b = await login(
            client,
            "userb@example.com",
            "string"
        )

        result_a, result_b = await asyncio.gather(
            rent_book(client, token_a),
            rent_book(client, token_b)
        )

        print(
            "User A:",
            result_a.status_code,
            result_a.text
        )

        print(
            "User B:",
            result_b.status_code,
            result_b.text
        )
        statuses = sorted([
            result_a.status_code,
            result_b.status_code
        ])


        if statuses == [201, 409]:
            print(
                "PASS: only one user rented the last copy."
            )

        else:
            print(
                "FAIL: concurrency protection did not behave as expected."
            )


if __name__ == "__main__":
    asyncio.run(main())