# INTERLEET — Frontend UI Build Plan

A production-quality, multi-page SaaS UI for an engineering practice platform. Frontend-only with mocked data. Restrained, developer-focused style inspired by GitHub, Linear, Vercel, Notion, Stripe — no neon, no cyberpunk.

## Stack

- TanStack Start (default Lovable web app scaffold)
- Tailwind CSS + shadcn/ui
- Recharts (analytics), Lucide icons, Framer Motion (subtle transitions)
- Monaco Editor (`@monaco-editor/react`) for the code workspace
- All data mocked in `src/lib/mock/` — no backend in this pass

## Design System

Defined as semantic HSL tokens in `index.css` + `tailwind.config.ts`:

- **Neutrals:** charcoal bg `#0B0D10`, panel `#111418`, border `#1F242B`, muted `#8B95A1`, text `#E6EAF0`
- **Accents:** blue `#3B82F6` primary, indigo `#6366F1`, green `#22C55E` success, red `#EF4444` danger, amber `#F59E0B` warning
- **Type:** Inter (UI) + JetBrains Mono (code). Scale 12/13/14/16/20/24/32/48.
- **Surfaces:** 1px soft borders, low-opacity shadows, 8/12px radii.
- **Motion:** 150–250ms ease-out; hover lift on cards, fade dropdowns, sidebar width transition.
- Dark default, light mode toggle.

## Routes

```text
/                            Landing (12 sections)
/login  /signup  /forgot     Auth
/app/dashboard               User dashboard
/app/challenges              List + filters
/app/challenges/:id          Detail
/app/editor/:id              Monaco workspace
/app/interviews              AI interview list
/app/interviews/live         Live interview
/app/interviews/:id/report   Feedback report
/app/system-design           System design library
/app/leaderboard             Rankings
/app/profile/:username       Public profile
/app/settings                Settings
/recruiter                   Recruiter dashboard
/admin                       Admin panel
```

## Shared Components

- `layout/` AppShell, Sidebar (collapsible → icon rail → mobile drawer), Topbar, Footer
- `ui/` shadcn primitives (Button, Card, Tabs, Dialog, Dropdown, Tooltip, Toast, Table, Pagination, Badge, Skeleton, EmptyState)
- `charts/` Line, Radar, Bar, ProgressRing
- `domain/` ChallengeCard, DifficultyPill, DomainTag, RankRow, SkillBar, ActivityItem, AIMessageBubble

## Page Highlights

- **Landing:** sticky minimal navbar, hero with in-page dashboard mock (real components, not an image), stats strip, problem statement, feature grid, AI interview + system design previews, 6 domain cards, leaderboard preview, recruiter verification, testimonials, footer.
- **Dashboard:** XP/rank/streak/accuracy cards, domain radar, weekly activity chart, recommended challenges, activity timeline, badges row.
- **Challenges:** search + filter rail (domain, difficulty, tags, time), grid/list toggle.
- **Editor:** three-pane VS Code-style — file explorer, Monaco with tabs + language picker, right/bottom panel for problem, terminal, tests. Run/Submit in topbar.
- **AI Interview Live:** conversation column, mic control, live transcript, timer, progress steps, confidence meter.
- **Feedback Report:** four score cards, skill radar, strengths/weaknesses, recommendations, progress chart.
- **System Design:** category cards (Scalability, Caching, DB, Load Balancing, Distributed Systems, Infra) with topic lists.
- **Leaderboard:** Global / Weekly / Friends tabs; ranked table with avatar, rating, XP, badges, delta.
- **Profile:** banner with avatar/rating/rank; tabs Overview/Challenges/Interviews/Projects/Badges; contribution heatmap.
- **Recruiter:** candidate search, comparison table, verified skill badges, candidate drawer.
- **Admin:** Challenges/Users/Contests/Reports tables with row actions + analytics overview.

## Responsiveness

- Sidebar: full → icon rail <1024px → drawer <768px
- Tables collapse to stacked cards on mobile
- Editor: tabbed explorer/code/terminal on mobile
- Touch targets ≥40px

## Build Order

1. Scaffold web app, design tokens, AppShell
2. Landing page
3. Auth pages
4. Dashboard + chart components
5. Challenges list + detail
6. Code editor
7. AI interview live + feedback report
8. System design, Leaderboard, Profile
9. Recruiter, Admin, Settings
10. Responsive + motion polish, empty/loading states

## Out of Scope (this pass)

Real backend, auth, code execution, AI calls. All interactions visual/mocked — Lovable Cloud + real AI can come next.
