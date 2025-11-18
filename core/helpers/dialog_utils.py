import asyncio


async def auto_close_dialog(page, dialog, delay=1.0):
    await asyncio.sleep(delay)
    try:
        page.close(dialog)
        page.update()
    except Exception:
        pass  # Dialog já foi fechado manualmente