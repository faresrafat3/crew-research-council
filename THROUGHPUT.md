# THROUGHPUT — TOC constitution (from Goldratt's The Goal)

Goal: gated-shipped missions, compounded. Balance flow, not capacity.

## T / I / OE (logged weekly)

- **T (Throughput)** = DONE-DONE mission value per week. Only gated + compounded missions count, owner-rated 1/3/5. Not starts, not builds, not PRs opened.
- **I (Inventory)** = everything stuck in the chain: live probes + uncut plans + unbuilt cuts + ungated builds + uncompounded lessons. Past spend with zero value until gated.
- **OE (Operating Expense)** = tokens + owner review minutes + coordination time per week.
- Health: T up, I down, OE flat. Kill-a-stalled beats finish-a-mediocre, every time.
- Weekly line: `T=__pts/__missions | I=__ open (__ pre-razor) | OE=__tok + __owner-min`.

## The constraint (drum)

- **Drum: @razor** (visited 2x per mission, holds veto — constraint by construction). **Standby drum: @gate.**
- Re-vote WEEKLY from queue data (@coach): biggest sustained queue wins the drum. 5 straight days of gate-queue > razor-queue = drum moves. No re-vote, no truth.
- An hour saved anywhere except the drum is a mirage. Only razor-minutes count.

## Drum-Buffer-Rope

- Drum = razor cadence for the week (published: e.g. 6 cuts = 4x Cut-1 + 2x Cut-2). Nothing else sets pace.
- Buffers (small, visible, BEFORE the constraint): B1 pre-Cut-1 = 2 ready plans; B2 pre-Cut-2 = 1 finished build; B3 pre-Gate = 3 missions, 48h expiry. Full buffer = upstream STOPS and helps the constraint, never pushes.
- Rope (owned by @firstmate): release a bet / start evidence ONLY on a free B1 slot; start a build ONLY on a free B2 slot. Razor idle + buffers empty = rope failed → one expedite same-day. Buffers chronically full = rope ignored → freeze all releases until drain to 1.
- Expiry: 72h pre-razor, 48h pre-gate — then auto-kill or return-to-@edge. Buffers never become warehouses.

## WIP limits (protect the constraint, not fairness)

edge 3 live probes TOTAL (the rope) · scout 2 packs/probe · architect 2 plans awaiting Cut-1 · razor 2 in Cut-1 + 1 in Cut-2 · ship 2 (1 active + 1 standby; idle ship is protective capacity — tooling/debt, never new missions) · gate 3 w/ 48h SLA · coach 2 uncompounded.

## Station metrics (constraint-service only)

@edge by razor-accept rate · @ship by gate-pass rate · never by starts. No station metric except how it serves the drum.

## Inertia warning

Exploit rules sunset when @razor overrides them >30% of the time. Old drum/buffers/metrics die the day the drum moves. If T stalls 2 weeks, you are optimizing a non-constraint.
