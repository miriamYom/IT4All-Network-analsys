import asyncio
import httpx

async def get_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError:
            return None

async def main():
    mac_address = "00:0c:29:9b:ee:14"
    vendor = await get_vendor(mac_address)

    if vendor:
        print(f"Vendor for MAC address {mac_address}: {vendor}")
    else:
        print(f"Vendor information not found for MAC address {mac_address}.")

# Run the main coroutine in the event loop
asyncio.run(main())
