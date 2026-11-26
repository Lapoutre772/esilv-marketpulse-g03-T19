# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Mode change: the session was first set to LIVE and switched to APPROVED_SAMPLE with instructor approval (2026-11-26).
- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` is cited by TD09 but was not available in the team repository. This mapping follows the TD09 and TD10 lab sheets and the fixture's schema note.
- Live connectivity: not demonstrated
- Provenance: illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg historical observations.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The provider identifier is not the canonical ticker. MarketPulse analytics receive only `AAPL` and `SP500`.

## Input inspection

| Observation | AAPL US Equity | SPX Index |
|---|---|---|
| Date representation | String, `YYYY-MM-DD` | String, `YYYY-MM-DD` |
| Period | 2026-09-01 to 2026-09-30 | 2026-09-01 to 2026-09-30 |
| Observations | 21 | 21 |
| Missing values | None | None |
| Volume | Non-zero on all observations | `0` on all observations |

Available keys in each observation: `observation_date`, `open_value`, `high_value`, `low_value`, `close_value`, `volume_value`.

Data structure: a JSON object with a `series` list. Each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Available, kept as `YYYY-MM-DD` |
| ticker | series `canonical_ticker` | Application mapping: AAPL or SP500 |
| open | `open_value` | Available, convert to float |
| high | `high_value` | Available, convert to float |
| low | `low_value` | Available, convert to float |
| close | `close_value` | Available, convert to float |
| volume | `volume_value` | Available, convert to int |

Teaching wrapper key != Bloomberg LIVE field mnemonic.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: `AAPL US Equity` (canonical `AAPL`)
- Benchmark identifier: `SPX Index` (canonical `SP500`)
- Date representation: `YYYY-MM-DD` string
- Input structure: `series[]`, then `observations[]`; select a series by `provider_identifier`
- Missing fields: none
- Special normalization notes: the JSON mixes integers and decimals, so convert prices to float; keep the SP500 volume of `0` as provided; provider identifiers stay inside the provider boundary
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json` (42 rows)
