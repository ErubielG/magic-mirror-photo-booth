# Recovering event statistics

Do not erase or alter the Pi's event media before backing it up. The application stores captured JPEGs in `~/fotos/` and, when framing is enabled, additional originals in `~/fotos/originales/`. Print sheets can have names beginning `hoja-`.

Count unique captured filenames from the main photo folder **excluding print-sheet composites**. Do not add originals to that count, because originals and framed photographs may represent the same capture. Check file timestamps to isolate the November 14, 2026 event, if metadata was preserved.

Print requests and pickup numbers were retained in an **in-memory** `cola`, so they may be unavailable after service restart. The code supports automatic CUPS dispatch as well as optional approval and a separate manual print fallback. A queue status of 'ready', or successful acceptance by CUPS, does not by itself verify a physical sheet was delivered. The author recalls approximately 30–40 sheets of photo paper taken to the event and none unused afterward; treat this only as an approximate paper-consumption observation, not an independently verified successful print total. Reconcile counts against operator notes, printer records if accessible, and remaining supplies with appropriate uncertainty.

The read-only inventory script in `tools/photo_inventory.py` prints candidate counts without modifying files.
