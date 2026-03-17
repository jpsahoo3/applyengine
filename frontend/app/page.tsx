import { DashboardShell } from "@/components/dashboard-shell";
import { getDashboardSnapshot } from "@/lib/api";

export default async function HomePage() {
  const snapshot = await getDashboardSnapshot();
  return <DashboardShell snapshot={snapshot} />;
}

