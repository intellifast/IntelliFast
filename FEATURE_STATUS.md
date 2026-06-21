# IntelliFast Product Status

This document is the source of truth for what is complete, partial, missing, or blocked. Update it whenever production behavior changes.

Status key: `DONE`, `PARTIAL`, `IN PROGRESS`, `NOT STARTED`, `BLOCKED BY CONFIG`

Last reviewed: 21 June 2026

## Current priorities

1. Production account and security foundation — **IN PROGRESS**
2. Administrator and operations system — **IN PROGRESS**

## 1. Account security and production foundation — IN PROGRESS

- Implemented locally: verified registration, transactional reset email, CSRF protection, database-backed authentication rate limits, strong password policy, session revocation after password changes, security headers, production cookie mode, verified email changes, signature/size-validated profile photos, Terms, Privacy Policy, central error capture, idempotent schema migrations, consistent backups and password-confirmed deletion.
- Automated foundation tests: passing.
- Deployment dependency: configure Brevo, a verified sender, `APP_ENV`, `APP_BASE_URL` and a stable `SECRET_KEY`; then complete live email and mobile verification.

## 2. Fasting timer — PARTIAL

- Working: start, pause, resume, complete, break, protocols, custom duration, persistence and stage display.
- Missing: prominent remaining time, correct expected end timestamp, target-reached handling, early-completion confirmation, paused-end correction, scheduled start, celebration, persistent achievement event, mood check-in, background/browser notifications.

## 3. History and bulk import — PARTIAL

- Working: list history, manual add, edit, delete, duplicate, basic filters and recurring batch insertion.
- Missing: real calendar and timeline views, data-driven heatmap, duration filter, visibility/reason editing, pagination, CSV upload, preview/edit/remove before import, per-entry outcomes, duplicate detection and rollback.

## 4. Dashboard — PARTIAL

- Working: active fast, weekly summary, recent fasts, basic chart, streak and active-goal preview.
- Missing: complete month/year/lifetime sections, real heatmap, best day/month, consistency score, upcoming reminder, buddy and achievement cards, customisation and component-specific empty states.

## 5. Analytics — PARTIAL

- Working: basic period totals, completion, averages, streak, preferred plan and six-month bars.
- Missing: complete period filters, custom ranges, daily/weekly charts, heatmap, outcome and schedule charts, fasting/eating comparison, best week/month, robust insights, accessible/exportable chart data.

## 6. Streaks and achievements — PARTIAL

- Working: current/longest streak and five computed achievement previews.
- Missing: weekly/monthly streaks, timezone-perfect rules, persisted unlocks and dates, full achievement catalogue, celebrations, share cards, idempotent unlock events and perfect-week/month logic.

## 7. Goals — PARTIAL

- Working: create, calculate simple progress and archive.
- Missing: edit/delete, automatic complete/missed states, restore, date-bounded progress, schedule/custom goals, notifications, history and celebrations.

## 8. Human buddy system — PARTIAL

- Working: invite links, accept, two-buddy limit, summary view and removal.
- Missing: email delivery, reject/cancel/expiry workflows, pending limits, granular privacy, true weekly metrics, recent fasts, notifications and abuse protection.

## 9. AI Buddy — PARTIAL

- Working: personalised chat using active fast, recent fasts, notes, plan, streak and prior conversation; safety prompt and hourly limit.
- Missing: goals/reminders/achievements/buddy context, confirmed app actions, structured recommendations, multiple conversations, granular deletion, stronger moderation, usage controls, provider fallback and admin enable/disable.

## 10. Reminders and notifications — PARTIAL

- Working: reminder records, toggles, in-app notification records.
- Missing: actual scheduler, browser/email delivery, weekday/timezone execution, edit/delete, read state, category preferences, history cleanup.

## 11. Learning resources — PARTIAL

- Working: curated static resources, search, category filter, external links and bookmarks.
- Missing: administrator-managed catalogue, saved-only view, detail pages, link validation, tags, recently viewed, personal recommendations and medical review metadata.

## 12. Reports and exports — PARTIAL

- Working: basic daily/weekly/monthly/yearly summaries, print view and CSV history export.
- Missing: period comparisons, visible goal/achievement sections, stronger insights, PDF, arbitrary date ranges, scheduled delivery, JSON/full-account export and sharing controls.

## 13. Settings and privacy — PARTIAL

- Working: profile fields, password, fasting defaults, reminder records, CSV export, history/account deletion.
- Missing: profile photo, goal/experience editing, complete notification controls, buddy/profile/data visibility, full data request, verified email changes, password-confirmed deletion and optional MFA.

## 14. Administration and operations — IN PROGRESS

- Implemented locally: protected administrator role and CLI promotion, private dashboard, registrations/activity metrics, user search/status/suspension/verified override/confirmed deletion, resource publishing and visibility, AI usage/failure monitoring and kill switch, consistent database backups/downloads, health/uptime, privacy-conscious usage events, error review and append-only administrator audit trail.
- Automated administrator permission and operation tests: passing.
- Deployment dependency: promote the first verified administrator and complete live permission/destructive-action verification.

## Release rule

A feature may be marked `DONE` only when it has persisted server behavior, permission checks, validation, error handling, automated coverage, responsive UI, and successful live verification. Screens that only look complete remain `PARTIAL`.
