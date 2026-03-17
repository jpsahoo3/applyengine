import { DashboardSnapshot } from "@/lib/api";

type DashboardShellProps = {
  snapshot: DashboardSnapshot;
};

const metricCards = [
  {
    key: "applications_per_day",
    label: "Applications / Day",
    suffix: ""
  },
  {
    key: "response_rate",
    label: "Response Rate",
    suffix: "%"
  },
  {
    key: "interview_rate",
    label: "Interview Rate",
    suffix: "%"
  }
] as const;

const sectionCards = [
  { key: "applications_sent", label: "Applications Sent" },
  { key: "pending", label: "Pending" },
  { key: "login_required", label: "Login Required" },
  { key: "interviews", label: "Interviews" },
  { key: "recruiter_responses", label: "Recruiter Responses" }
] as const;

function renderMetricValue(snapshot: DashboardSnapshot, key: keyof DashboardSnapshot["metrics"]) {
  const value = snapshot.metrics[key];
  if (key === "applications_per_day") {
    return Math.round(value).toString();
  }
  return `${(value * 100).toFixed(1)}`;
}

export function DashboardShell({ snapshot }: DashboardShellProps) {
  return (
    <main className="grain min-h-screen px-5 py-6 md:px-10 md:py-8">
      <div className="mx-auto max-w-7xl">
        <section className="mb-6 rounded-[2rem] border border-[var(--panel-border)] bg-[var(--panel)] p-6 shadow-panel backdrop-blur md:p-10">
          <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
            <div className="max-w-3xl">
              <p className="mb-2 text-sm uppercase tracking-[0.32em] text-[var(--secondary)]">
                Autonomous Job Ops
              </p>
              <h1 className="font-display text-4xl font-semibold tracking-tight md:text-6xl">
                ApplyEngine control plane for high-volume AI job execution
              </h1>
            </div>
            <div className="rounded-[1.5rem] border border-[var(--panel-border)] bg-stone-950 px-5 py-4 text-stone-50">
              <p className="text-xs uppercase tracking-[0.28em] text-stone-400">Cluster Status</p>
              <p className="mt-2 font-display text-2xl">4 worker pools online</p>
              <p className="mt-1 text-sm text-stone-300">Targeting 1M+ applications/day</p>
            </div>
          </div>
        </section>

        <section className="mb-6 grid gap-4 md:grid-cols-3">
          {metricCards.map((card) => (
            <article
              key={card.key}
              className="rounded-[1.75rem] border border-[var(--panel-border)] bg-white/70 p-6 shadow-panel backdrop-blur"
            >
              <p className="text-sm uppercase tracking-[0.22em] text-stone-500">{card.label}</p>
              <p className="mt-4 font-display text-5xl font-semibold">
                {renderMetricValue(snapshot, card.key)}
                <span className="ml-1 text-xl text-[var(--accent)]">{card.suffix}</span>
              </p>
              <div className="mt-5 h-2 rounded-full bg-stone-200">
                <div
                  className="h-2 rounded-full bg-[var(--accent)]"
                  style={{
                    width:
                      card.key === "applications_per_day"
                        ? "82%"
                        : `${Math.max(8, Math.min(100, snapshot.metrics[card.key] * 100))}%`
                  }}
                />
              </div>
            </article>
          ))}
        </section>

        <section className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {sectionCards.map((card, index) => (
              <article
                key={card.key}
                className="rounded-[1.75rem] border border-[var(--panel-border)] bg-[var(--panel)] p-5 shadow-panel backdrop-blur transition-transform duration-300 ease-out hover:-translate-y-1"
                style={{ animationDelay: `${index * 90}ms` }}
              >
                <p className="text-sm uppercase tracking-[0.18em] text-stone-500">{card.label}</p>
                <p className="mt-3 font-display text-4xl font-semibold text-[var(--foreground)]">
                  {snapshot.sections[card.key]}
                </p>
              </article>
            ))}
          </div>

          <aside className="rounded-[1.75rem] border border-[var(--panel-border)] bg-stone-950 p-6 text-stone-100 shadow-panel">
            <p className="text-sm uppercase tracking-[0.24em] text-stone-400">Runbook</p>
            <ul className="mt-5 space-y-4 text-sm text-stone-300">
              <li>Scraping workers fan out across LinkedIn, Indeed, Naukri, Wellfound, RemoteOK, Greenhouse, Lever, and Workday.</li>
              <li>Matching workers score semantic fit, skill overlap, and ATS keyword coverage before any application task is enqueued.</li>
              <li>Application workers handle applyable jobs while login-gated listings are diverted to a dashboard queue for supervised takeover.</li>
              <li>Outreach workers find recruiters, draft cold emails, and schedule LinkedIn connection actions off the same job context.</li>
            </ul>
          </aside>
        </section>
      </div>
    </main>
  );
}

