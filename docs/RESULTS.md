# Observed outcome

- Actual event: November 14, 2026, California.
- Guests independently joined the local Wi-Fi, captured, and downloaded photos.
- Photo capture/download did not require continuous operation by an attendant, based on onsite observation.
- Guests independently requested one 4×6-inch sheet per visit, selecting up to four session photos. In the event configuration, booth20 submitted print jobs directly via CUPS (`lp -d selphy`) to the Canon SELPHY CP1500 on the PhotoBooth Wi-Fi network, with manual printing and approval disabled. Other printing modes remain available in the code.
- According to the author's firsthand recollection, guest-requested physical printing operated during the event. Approximately 30–40 sheets of photographic paper were brought, and none remained unused at the end. This is a rough paper-stock observation; the exact number of successfully completed printed sheets cannot be established from it.
- Reported project parts cost: **US$501**, excluding development labor and operating expenses.

Further session and verified print totals are pending investigation of retained storage and available event records. CUPS job acceptance, queue status and estimated paper use should not be mistaken for a measured total of physically completed prints. The event printing path was CUPS (`lp -d selphy`) over PhotoBooth Wi-Fi; exact throughput and uptime metrics were not logged here.
