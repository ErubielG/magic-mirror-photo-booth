# Recovering event statistics

Do not erase or alter the Pi's event media before backing it up. The application stores captured JPEGs in `~/fotos/` and, when framing is enabled, additional originals in `~/fotos/originales/`. Print sheets can have names beginning `hoja-`.

Count unique captured filenames from the main photo folder **excluding print-sheet composites**. Do not add originals to that count, because originals and framed photographs may represent the same capture. Check file timestamps to isolate the November 14, 2026 event, if metadata was preserved.

Print requests and pickup numbers were retained in an **in-memory** `cola`, so they may be unavailable after service restart. In manual mode, a 'ready' job does not confirm a physical page was printed. Verify physical print totals against operator notes, printer records if accessible, or remaining paper/consumables with appropriate uncertainty.

The read-only inventory script in `tools/photo_inventory.py` prints candidate counts without modifying files.
