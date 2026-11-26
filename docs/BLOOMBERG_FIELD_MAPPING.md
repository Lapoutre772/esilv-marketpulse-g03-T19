# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Live connectivity: **not demonstrated**

The fixture itself declares:

- `sample_kind`: `instructor_approved_fallback_fixture`
- `access_mode`: `approved_sample`
- `is_live_bloomberg_output`: `false`
- Values are illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg historical observations.

> This mapping is based on the instructor-approved fallback fixture.
> It must not be presented later as proof of LIVE Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

Provider identifier != canonical ticker.
The analytical layer (`analytics.py`) only ever receives `AAPL` and `SP500`.

## Inspected inputs

| Series | `role` | `provider_identifier` | `canonical_ticker` | Observations | Period |
|---|---|---|---|---|---|
| Instrument | instrument | AAPL US Equity | AAPL | 21 | 2026-09-01 to 2026-09-30 |
| Benchmark | benchmark | SPX Index | SP500 | 21 | 2026-09-01 to 2026-09-30 |

Both series share exactly the same 21 dates.

## Field mapping

The input keys below are **teaching wrapper keys** defined for the fallback fixture
(see the fixture's own `schema_note`).

Teaching wrapper key != Bloomberg LIVE field mnemonic.

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Teaching wrapper key. ISO string `YYYY-MM-DD`, copied unchanged |
| ticker | series-level `canonical_ticker` (`AAPL US Equity -> AAPL`, `SPX Index -> SP500`) | Application mapping. Not a per-observation field; must be attached to every row |
| open | `open_value` | Teaching wrapper key. Numeric, copied unchanged |
| high | `high_value` | Teaching wrapper key. Numeric, copied unchanged |
| low | `low_value` | Teaching wrapper key. Numeric, copied unchanged |
| close | `close_value` | Teaching wrapper key. Numeric, copied unchanged |
| volume | `volume_value` | Teaching wrapper key. Integer. Always `0` for SPX Index; `0` is kept as-is in the expected output (not converted to null) |

## TD10 handoff

- Access mode: APPROVED_SAMPLE (live connectivity not demonstrated)
- Instrument identifier: `AAPL US Equity` -> canonical `AAPL`
- Benchmark identifier: `SPX Index` -> canonical `SP500`
- Date representation: ISO date string `YYYY-MM-DD` (e.g. `2026-09-01`), no time component, no conversion needed
- Input structure:
  - top-level JSON object with metadata (`sample_kind`, `provider_stage`, `access_mode`, `is_live_bloomberg_output`, `provenance`, `schema_note`)
  - `series`: list of 2 objects, each with `role`, `canonical_ticker`, `provider_identifier`, `observations`
  - `observations`: list of objects with the 6 wrapper keys
- Missing fields: none. Every observation has all 6 keys and no null value
- Special normalization notes:
  - The ticker comes from the series level (`canonical_ticker`), not from the observations: it must be copied onto each canonical row.
  - The Bloomberg identifier (`provider_identifier`) must not appear in canonical rows.
  - Wrapper keys are renamed to the canonical row contract: `date, ticker, open, high, low, close, volume`. Values are not transformed.
  - SPX Index `volume = 0`: an index has no traded volume; analytics must not rely on benchmark volume.
  - 2026-09-07 is absent from both series (US market holiday, Labor Day): no gap filling is expected.
  - Output is a flat list of rows: all AAPL rows (date ascending), then all SP500 rows (date ascending), 42 rows in total.
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`

## Security

No credential, session token or terminal-specific information is stored in this document.
