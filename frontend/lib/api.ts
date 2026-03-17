export type DashboardSnapshot = {
  metrics: {
    applications_per_day: number;
    response_rate: number;
    interview_rate: number;
  };
  sections: {
    applications_sent: number;
    pending: number;
    login_required: number;
    interviews: number;
    recruiter_responses: number;
  };
};

const fallbackSnapshot: DashboardSnapshot = {
  metrics: {
    applications_per_day: 742,
    response_rate: 0.118,
    interview_rate: 0.027
  },
  sections: {
    applications_sent: 742,
    pending: 119,
    login_required: 84,
    interviews: 20,
    recruiter_responses: 31
  }
};

export async function getDashboardSnapshot(userId = "demo-user"): Promise<DashboardSnapshot> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!baseUrl) {
    return fallbackSnapshot;
  }

  try {
    const response = await fetch(`${baseUrl}/api/v1/dashboard/${userId}`, {
      next: { revalidate: 30 }
    });
    if (!response.ok) {
      return fallbackSnapshot;
    }
    return (await response.json()) as DashboardSnapshot;
  } catch {
    return fallbackSnapshot;
  }
}

