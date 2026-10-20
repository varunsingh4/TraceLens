# Payments timeout runbook

checkout-service calls payments-service synchronously during POST /api/checkout.

Default client timeout is 2500ms. If payments-service p95 latency exceeds that,
checkout returns 500 with IllegalStateException: PaymentAuthorizationClient timed out.

Mitigations:
1. Check payments-service CPU and DB pool saturation.
2. Confirm the checkout client timeout was not lowered in a recent release.
3. If payments is healthy, look for a missing retry or circuit breaker on authorize().
4. Incident owners should compare the failing release tag against the previous known-good tag.
