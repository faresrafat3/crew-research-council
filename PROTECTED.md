# PROTECTED — crew-research-council

> **What this file is:** the local declaration of what may never be edited in place here. It is the
> authoritative detail for this project; `~/CONSTITUTION.md` §2 is the umbrella index.
> **Owner:** Fares. **Language:** artifacts English, chat Arabic.
>
> **RECONSTRUCTION — 2026-09-21.** The original was created 2026-09-20, was never `git add`ed, and was
> deleted by a concurrent writer. It is in no commit (`git log --all` → empty) and `git fsck` finds no
> dangling blob, so **these are not the original bytes** (the original was 41 lines / 2375 bytes; its
> hash is unknown because it was never staged). The zones below are the ones the audit trail documents
> — `local/compliance/2026-09-20-gaps.md` §2b and the referent scan in `local/context/` that ran while
> the file still existed — and every path is verified to resolve on disk. **The original's complete
> referent list is not fully recoverable**, so treat this as a floor, not a restoration. It is tracked
> in git from now on (`git ls-files PROTECTED.md`), which is the failure this file now exists to close.

## Protected (do not edit in place)

| Path | Why |
|---|---|
| `RESEARCH-COUNCIL/**` | Research **input**, already ingested by the study — changing it corrupts the study (§2) |
| `RESEARCH-COUNCIL/STATUS.md` | The canonical status record; the repo boundary commit names it as the one that survives |
| `tests/**`, `crew/**`, `harness/**`, `repro/**` | Present on disk and **git-ignored** — one copy, no history, no backup. Deleting or overwriting any of them is unrecoverable. This is the exact failure mode that lost the file you are reading |

## The gate

**None** — there is no build gate in this project. The repository tracks documents: no runner, no
executable surface, no `.json` / `.sh` / `.py` to execute. The written record is the verification, and
`local/scripts/constitution-sweep.sh` files that as a gap rather than pretending prose is a command.

## Safe write-path

`README.md` and the non-council surfaces.

## Local laws that bind any edit here

- The council's own `GOAL.md` law freezes births and team-layer changes while the captain is away.
- "One home per fact": a fact lives in one document; the other side links (`CONSTITUTION.md` §2).
- *The original file's own list is not fully recoverable; the two above are the ones the audit trail
  names.*

## If you believe a protected file must change

Do not edit it. File a new dated document beside it and link the supersession from here.
