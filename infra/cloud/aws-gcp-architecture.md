# Cloud Deployment Architecture

## AWS

- Route53 for DNS
- CloudFront in front of the Next.js frontend
- ALB + EKS for API and worker ingress
- RDS PostgreSQL with read replicas
- ElastiCache Redis for Celery queues and short-lived caches
- S3 for resumes, generated variants, and artifacts
- OpenSearch / CloudWatch / X-Ray for logs, metrics, and traces
- Secrets Manager for credentials

## GCP

- Cloud DNS + Cloud CDN
- GKE for API and worker workloads
- Cloud SQL for PostgreSQL
- Memorystore Redis for queues
- GCS for resumes and generated variants
- Cloud Logging + Cloud Monitoring + Cloud Trace for observability
- Secret Manager for credentials

## Scaling Notes

- Partition Celery queues by tenant cohort and region once global traffic exceeds single-redis comfort limits.
- Keep scraping workers separate from application workers to isolate noisy browser automation from higher-value apply paths.
- Prefer managed PostgreSQL and Redis before self-hosted stateful sets.

