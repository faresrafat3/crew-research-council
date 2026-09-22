# adaptive-fleet-discovery

Hypothesis: runtime model discovery + latency-ranked binding outperforms
static model lists for a free-tier fleet — zero human edits when
providers ship or retire models.

Design (source: dspy-lab/programs/adaptive_fleet.py):
1. GET /v1beta/openai/models — the live roster (never a hardcoded list)
2. non-chat families filtered by pattern (tts/image/embed/veo/live/...)
3. every candidate probed with a real completion; choices-envelope
   sanity check (a 200 with an error body is NOT alive)
4. role binding: task=cheapest lite, reflection=strongest gemini
   (pro-first), agent=flash non-lite — by family then measured latency
5. 1h cache TTL; static list kept as last-resort fallback only

Evidence 2026-09-22:
- adaptive_cache_2026-09-22.json: 10 models alive latency-ranked
- gemini-3.6-flash was DISCOVERED (absent from every prior config)
- agent task bound models/gemini-flash-lite-latest: 2 steps, 4.9 s
- closed loop: bind -> ask 17*23 -> 391 correct
