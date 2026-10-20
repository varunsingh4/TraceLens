# Inventory reservation

inventory-service reserves stock with a 30 second lease. If the lease expires,
the item is returned to the available pool. This document does not mention
checkout payment timeouts, authorization clients, or HTTP 500 deploy failures.

Use this file as a distractor during retrieval. A good question about checkout
timeouts should rank this chunk below payment-related evidence.
