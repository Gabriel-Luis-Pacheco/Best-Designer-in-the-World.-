# Privacy, data rights, trust and consent as UX

Activate when personal data, identity, voice recordings, analytics/cookies, emails, payments, children or sensitive information materially affect the task. This is product guidance, NOT legal advice, LGPD/GDPR certification or a replacement for a security audit. Validate current law, jurisdiction and internal policy with responsible experts.

## Design commitments
- Ask only for necessary information; give a contextual, truthful explanation of permissions and meaningful decline where applicable.
- Distinguish service-essential behavior from optional marketing and analytics. Avoid deceptive defaults, bundled opt-ins, fake expiry and hidden exits.
- Expose accurate account, profile, notification, export/delete request and marketing preference routes when supported; do not simulate capabilities that do not exist.
- Make retention, deletion, data location or sharing claims only when policies and actual implementation support them. A confirmation screen does not prove deletion from backups or queued services.
- Avoid leaking secrets, personal records or account existence in public error messages. Browser-hidden elements and cosmetic locks do not enforce access.
- For AI/media inputs: clarify microphone/camera permissions, recording/transcription, uncertain output, stop controls and privacy expectations.
- Trust marks, ratings and activity notices must have real source/provenance; never fake customer stories, legal certification or popularity.

## Contextual test table

| Surface | Real question |
|---|---|
| Cookie/analytics choice | Does opt-out actually persist and suppress optional collection? |
| Roles/profile | Can an unauthorized user or another tenant access this personal data? |
| Voice/AI | Can the user stop capture? Is storage/use disclosed accurately? |
| Checkout | Are renewal, cancellation, price and identity expectations truthful? |
| Forms/email | Is contact purpose clear and can a person stop messages? |
| Data rights | Is request/status/recovery real, with an identified owner? |
| Young or vulnerable audiences | Has responsible owner reviewed age, consent and manipulative-mechanic risks? |

For each promise record its authority (policy/provider/backend), UI route, consent/decline, relevant role and actual test. Missing evidence is UNKNOWN. Front-end disclosure alone cannot prove compliant processing, server authorization, encryption, RLS or retention.
