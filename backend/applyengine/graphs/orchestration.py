from __future__ import annotations

from dataclasses import asdict

from applyengine.agents.application_tracking import ApplicationTrackingAgent
from applyengine.agents.cold_outreach import ColdOutreachAgent
from applyengine.agents.interview_preparation import InterviewPreparationAgent
from applyengine.agents.job_discovery import JobDiscoveryAgent
from applyengine.agents.job_matching import JobMatchingAgent
from applyengine.agents.linkedin_networking import LinkedInNetworkingAgent
from applyengine.agents.login_detection import LoginDetectionAgent
from applyengine.agents.mass_application import MassApplicationAgent
from applyengine.agents.profile_analyzer import ProfileAnalyzerAgent
from applyengine.agents.recruiter_finder import RecruiterFinderAgent
from applyengine.agents.resume_optimizer import ResumeOptimizerAgent
from applyengine.graphs.state import WorkflowState
from applyengine.schemas.job import JobRecord


class JobHuntingGraph:
    def __init__(
        self,
        *,
        profile_analyzer: ProfileAnalyzerAgent | None = None,
        resume_optimizer: ResumeOptimizerAgent | None = None,
        job_discovery: JobDiscoveryAgent | None = None,
        job_matching: JobMatchingAgent | None = None,
        mass_application: MassApplicationAgent | None = None,
        login_detection: LoginDetectionAgent | None = None,
        recruiter_finder: RecruiterFinderAgent | None = None,
        cold_outreach: ColdOutreachAgent | None = None,
        linkedin_networking: LinkedInNetworkingAgent | None = None,
        interview_preparation: InterviewPreparationAgent | None = None,
        application_tracking: ApplicationTrackingAgent | None = None,
    ) -> None:
        self.profile_analyzer = profile_analyzer or ProfileAnalyzerAgent()
        self.resume_optimizer = resume_optimizer or ResumeOptimizerAgent()
        self.job_discovery = job_discovery or JobDiscoveryAgent()
        self.job_matching = job_matching or JobMatchingAgent()
        self.mass_application = mass_application or MassApplicationAgent()
        self.login_detection = login_detection or LoginDetectionAgent()
        self.recruiter_finder = recruiter_finder or RecruiterFinderAgent()
        self.cold_outreach = cold_outreach or ColdOutreachAgent()
        self.linkedin_networking = linkedin_networking or LinkedInNetworkingAgent()
        self.interview_preparation = interview_preparation or InterviewPreparationAgent()
        self.application_tracking = application_tracking or ApplicationTrackingAgent()

    def run(self, state: WorkflowState, seed_jobs: list[JobRecord] | None = None) -> WorkflowState:
        state.trace.append("resume_optimizer")
        variants = self.resume_optimizer.optimize(state.profile).payload["variants"]
        state.optimized_resumes = variants if isinstance(variants, dict) else {}

        state.trace.append("job_discovery")
        discovered = self.job_discovery.discover(state.profile, seed_jobs).payload["jobs"]
        state.discovered_jobs = list(discovered) if isinstance(discovered, list) else []

        state.trace.append("job_matching")
        matched = self.job_matching.match(state.profile, state.discovered_jobs).payload["jobs"]
        state.matched_jobs = list(matched) if isinstance(matched, list) else []

        for job in state.matched_jobs:
            state.trace.append(f"decision:{job.id}")
            login_result = self.login_detection.evaluate(job).payload["requires_login"]
            if login_result:
                state.dashboard_queue.append(job)
                continue
            application = self.mass_application.apply(job, state.optimized_resumes).payload["application"]
            state.applications.append(application)
            recruiters = self.recruiter_finder.find(job).payload["recruiters"]
            state.recruiters[job.id] = recruiters if isinstance(recruiters, list) else []
            messages = self.cold_outreach.compose(job, state.recruiters[job.id], state.profile).payload[
                "messages"
            ]
            if isinstance(messages, list):
                state.outreach_messages.extend(messages)
            actions = self.linkedin_networking.build_actions(job, state.recruiters[job.id]).payload["actions"]
            if isinstance(actions, list):
                state.networking_actions.extend(actions)
            brief = self.interview_preparation.prepare(job, state.profile).payload["brief"]
            state.interview_briefs.append(brief if isinstance(brief, dict) else {})

        state.trace.append("application_tracking")
        summary = self.application_tracking.summarize(
            state.applications,
            state.dashboard_queue,
        ).payload["summary"]
        state.tracking_summary = summary if isinstance(summary, dict) else {}
        return state

    @staticmethod
    def state_machine() -> dict[str, object]:
        return {
            "nodes": [
                "profile_analyzer",
                "resume_optimizer",
                "job_discovery",
                "job_matching",
                "decision",
                "mass_application",
                "login_queue",
                "recruiter_finder",
                "cold_outreach",
                "linkedin_networking",
                "interview_preparation",
                "application_tracking",
            ],
            "edges": [
                ("profile_analyzer", "resume_optimizer"),
                ("resume_optimizer", "job_discovery"),
                ("job_discovery", "job_matching"),
                ("job_matching", "decision"),
                ("decision", "mass_application"),
                ("decision", "login_queue"),
                ("mass_application", "recruiter_finder"),
                ("recruiter_finder", "cold_outreach"),
                ("cold_outreach", "linkedin_networking"),
                ("linkedin_networking", "interview_preparation"),
                ("interview_preparation", "application_tracking"),
                ("login_queue", "application_tracking"),
            ],
        }

    @staticmethod
    def snapshot(state: WorkflowState) -> dict[str, object]:
        return asdict(state)

