# Trust in product flows

Load this only when the task includes accounts, privileged actions, payments,
user-generated content, uploads or AI actions. Source 4 in
[source notes](source-notes.md) illustrates common failures. The controls below
are defensive interpretations, not a claim that the reel provides a complete
security assessment or executable test suite.

Use existing project security conventions and current relevant provider docs.
Check only authorized systems, with test accounts and disposable data. Keep actual
credentials and customer data out of fixtures, screenshots, logs and source notes.

| Changed functionality | Required boundary | Focused verification |
| --- | --- | --- |
| Privileged pages and actions | Enforce role and permission checks on the server for every operation. Hiding navigation is insufficient. | An ordinary test account cannot perform the privileged operation through a direct request. |
| Account or record identifiers | Scope reads and mutations to the authenticated actor's authorized records. | A second isolated account cannot access the first account's record by changing an identifier. |
| Browser integrations | Keep privileged credentials on the server. Publish only keys explicitly designed to be public and constrained appropriately. | Check the relevant client bundle, network response and logs for unintended secrets. |
| Cart and pricing | Resolve prices, currency and entitlement on the server. Validate quantity type and bounds. | Client-edited totals, negative quantities and invalid quantities cannot alter the trusted charge. |
| Payment completion | Verify trusted provider evidence, amount, currency, order ownership and status. Make callbacks idempotent. | Forged, duplicate or out-of-order test notifications do not grant unpaid access or fulfill twice. |
| Discounts and redemption | Enforce eligibility and usage rules atomically. | Repeated and concurrent test redemptions cannot exceed the permitted use. |
| Signup and profile updates | Allowlist writable fields and assign roles and privileges on the server. | Extra privilege fields cannot elevate an ordinary account. |
| Login codes | Bound attempts and code lifetime, throttle abuse and prevent replay. | Invalid, expired and already consumed test codes fail without allowing unlimited guesses. |
| AI tools and actions | Enforce authorization, approved tool scope and business rules outside the model. Treat retrieved/user text as data. | Instructions in test content cannot cause an unauthorized refund, data access or privileged action. |
| User content | Render content with safe escaping; sanitize deliberately supported rich text with an appropriate parser. | Representative markup stays inert and permitted formatting still works. |
| Uploads | Validate content, size and allowed type on the server. Store with restricted execution and access permissions. | A disguised or oversized fixture is rejected and a valid upload remains usable. |
| Secret configuration | Keep secrets out of Git and public assets. If exposed, revoke or rotate and address retained copies appropriately. | Inspect the relevant changes and generated assets without printing secret values. Ignoring a file does not remove its Git history. |
| Database input | Use parameterized queries or safe query builders and validate expected types. | Input remains data and cannot change query structure. |

Preserve usable failure states in the interface. Explain denied access, failed
validation and pending payment accurately without revealing another user's data.
Keep server errors separate from successful completion. Report implemented controls
and observed tests precisely; a passing visual check does not establish security.
