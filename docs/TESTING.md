# Testing and verification

The author's engineering portfolio reports **293 automated checks** against mocked camera and virtual printer behavior, headless-browser screenshot checks, and a 12-second load simulation with 50 simulated clients (about 101 status requests/s, zero observed errors, and 2 ms median status-endpoint response on a development machine). Adaptive polling reduced offered load to about 32 requests/s.

These numbers are reported historical development results, **not** benchmarks measured on the Raspberry Pi. The original 293-check harness was not provided and is not included in this repository. The tests in `tests/` are separate lightweight static checks and do not reproduce the original test suite.

Before deployment, test camera initialization/recovery, guest session isolation, iOS Safari handoff, Wi-Fi captive portal, physical print handoff and disconnected power/restore behavior on the actual Raspberry Pi.
