# Changelog

## [0.2.1] - 2026-01-31
- Hardened exception handling end-to-end, validating target URLs, catching user interrupts cleanly, and surfacing friendly error messaging.
- Added scan statistics summary (requests, hits, redirects, soft-404s, errors) to highlight outcomes even when scans are halted early.
- Filtered WAF detections further to discard payload echoes and return only meaningful vendor signals while persisting results.

## [0.2.0] - 2026-01-31
- Hardened directory enumeration to avoid redirect false positives by inspecting redirect chains and soft-404 signatures when evaluating responses.
- Added rotating user-agents, accept-language headers, and optional proxy pool (via `MANDORA_PROXIES`) to diversify scan traffic and improve resilience.
- Persisted richer scan results, recording status codes and classification notes in depth files for clearer follow-up analysis.
- Enhanced WAF detection to summarise only confirmed matches, deduplicate signals, and capture vendor context while keeping output readable.

## [0.1.0] - 2024-01-01
- Initial public release featuring baseline wordlist-based directory brute forcing and WAF detection bootstrap.
