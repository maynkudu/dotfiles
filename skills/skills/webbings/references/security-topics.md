# Security topics to investigate when applicable

Source 7 in [source notes](source-notes.md) lists 20 security topics and displays
advisory or documentation labels. Its historical incidents, affected versions,
attack figures and advertised fixes were not independently verified here.
The table records applicability questions, not confirmed vulnerabilities or
creator-provided remediations. Do not repeat its examples as findings in a project.

Load this only for authorized work involving the relevant technology. Inspect the
actual dependency, deployment and configuration, then consult current official
documentation or the original advisory before proposing a specific remediation.
Follow the dotfiles' documentation lookup and product-specific skill requirements.
No active exploit testing, load test or infrastructure change follows merely from
reading this file.

| Topic named in the reel | Relevant area to inspect |
| --- | --- |
| HTTP/2 Rapid Reset | The deployed proxy/server version, vendor advisory and request-abuse protections. A local UI build cannot establish exposure. |
| Long-username authentication bug | The actual identity-provider advisory, affected versions and complete identifier handling. Do not adopt 52 characters as a universal limit. |
| SAML verification bypass | The provider/library's supported validation and current security updates. Avoid custom assertion validation. |
| OAuth email spoofing | Account binding to verified issuer and stable provider subject; applicable linking and email-verification policy. |
| GraphQL aliases | Authorization and cost/abuse controls that account for the operations inside a request, rather than request count alone. |
| Authentication-code replay | Server-side expiry, consumption and replay handling for the actual code scheme. |
| Regular-expression denial of service | Untrusted input length and potentially unbounded matching cost. Use bounded analysis before any runtime test. |
| JWT algorithm confusion | Allowed algorithms, correct key use and complete claim validation in the actual supported library. |
| Request smuggling | HTTP parsing and framing across the deployed proxy/server chain and applicable vendor fixes. |
| Cache poisoning | Trusted host/header handling, cache keys and isolation of personalized or authorization-dependent responses. |
| Spoofed client-IP headers | The actual trusted proxy boundary. Arbitrary client headers must not establish identity or bypass abuse controls. |
| Database views and row policies | Whether view privileges and execution context preserve the intended data-access policy. Inspect using appropriate test roles. |
| Insecure random tokens | A cryptographically secure platform generator for secrets, with appropriate length, expiry and storage. |
| Timing leakage | Existing supported verification primitives and the complete endpoint's observable behavior. One comparison helper does not prove the endpoint safe. |
| Padding oracle | Supported authenticated encryption and current cryptographic libraries. Avoid designing a custom cipher or padding protocol. |
| Prototype pollution | Untrusted object keys and merge/deserialization paths; current package advisories and safe data structures. |
| Template injection | Whether user content can become executable template source. Keep user data separate from templates. |
| XML external entities | Parser configuration, external-resource access and the supported parser's secure defaults. |
| WebSocket hijacking | Handshake authentication, appropriate origin checks and authorization of subsequent messages. |
| Unicode identity collisions | Consistent identifier normalization, comparison and uniqueness policy without merging distinct accounts or corrupting user-visible names. |

Keep these investigations separate from ordinary visual polish. Record the
technology and evidence that make a topic applicable, the verified remediation
source, any authorized test and its limits. Never label an app secure or vulnerable
because a topic appeared in this reel or passed a visual checklist.
