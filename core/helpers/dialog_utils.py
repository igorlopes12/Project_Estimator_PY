"""core/helpers/dialog_utils.py

Small dialog helper utilities for the Flet UI.
Currently provides an async helper to auto-close dialogs after a delay.
"""

import asyncio


async def auto_close_dialog(page, dialog, delay=1.0):
    """Close the given Flet dialog after a delay (non-blocking).

    Args:
        page: Flet page instance where the dialog was opened.
        dialog: The dialog object to close.
        delay: Seconds to wait before closing the dialog.
    """
    await asyncio.sleep(delay)
    try:
        page.close(dialog)
        page.update()
    except Exception:
        pass  # Dialog was already closed manually
