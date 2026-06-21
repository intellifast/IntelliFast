# IntelliFast Product Status

This document is the source of truth for what is complete, partial, missing, or blocked. Update it whenever production behavior changes.

Status key: `DONE`, `PARTIAL`, `IN PROGRESS`, `READY FOR DEPLOYMENT`, `NOT STARTED`, `BLOCKED BY CONFIG`

Last reviewed: 21 June 2026

## Current priorities

1. Fasting timer completion — **READY FOR DEPLOYMENT**
2. Reminders and notifications — **READY FOR DEPLOYMENT**
3. History and bulk import — **READY FOR DEPLOYMENT**

## 1. Account security and production foundation — IN PROGRESS

- Implemented locally: verified registration, transactional reset email, CSRF protection, database-backed authentication rate limits, strong password policy, session revocation after password changes, security headers, production cookie mode, verified email changes, signature/size-validated profile photos, Terms, Privacy Policy, central error capture, idempotent schema migrations, consistent backups and password-confirmed deletion.
- Automated foundation tests: passing.
- Deployment dependency: configure Brevo, a verified sender, `APP_ENV`, `APP_BASE_URL` and a stable `SECRET_KEY`; then complete live email and mobile verification.

## 2. Fasting timer — READY FOR DEPLOYMENT

- Implemented: immediate and scheduled starts, start-now/cancel controls, prominent remaining time, corrected expected end including pauses, persisted target-reached event, idempotent achievement notification, confirmed early completion, pause/resume, mood check-in, notes/reasons, browser target alerts and responsive controls.
- Automated timer workflow and regression tests: passing. Awaiting live deployment and mobile verification before `DONE`.

## 3. History and bulk import — READY FOR DEPLOYMENT

- Implemented: editable timeline, data-driven monthly calendar, date/status/plan/duration/note filters, visibility and reason editing, pagination, recurring insertion, CSV upload, row-level preview/edit/remove selection, validation, duplicate detection, per-batch outcomes and transactional database rollback.
- Automated history, filtering, pagination and CSV workflow tests: passing. Awaiting live deployment and mobile verification before `DONE`.

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

- Working: personalised chat using active fast, recent fasts, notes, plan, streak and prior conversation; safety prompt, hourly abuse limit, five-message monthly default, per-user recurring allowances, current-month administrator grants, user-visible remaining quota, failure-safe accounting and administrator enable/disable.
- Missing: goals/reminders/achievements/buddy context, confirmed app actions, structured recommendations, multiple conversations, granular deletion, stronger moderation and provider fallback.

## 10. Reminders and notifications — READY FOR DEPLOYMENT

- Implemented: timezone/weekday scheduler, authenticated external scheduler endpoint, server CLI dispatcher, Brevo email delivery, live in-app polling, browser permission and alerts, add/edit/delete/toggle, read state, delivery-channel choice, idempotent sends and old-history cleanup.
- Automated dispatch/idempotence/email/edit/delete tests: passing. Deployment still requires a private `CRON_SECRET` and one-minute scheduler; then live email and mobile browser verification before `DONE`.

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
