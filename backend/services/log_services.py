def analyze_log(log_text: str):
    log_lower = log_text.lower()

    if "timeout" in log_lower or "database" in log_lower:
        return {
            "incident_type": "Database / Service Timeout",
            "severity": "high",
            "likely_root_cause": "The application may be unable to reach a downstream service or database within the expected time.",
            "recommended_commands": [
                "Check application logs",
                "Check database connectivity",
                "Review recent deployments",
                "Check API latency metrics"
            ],
            "next_steps": [
                "Verify if the database is healthy",
                "Check connection pool usage",
                "Confirm network connectivity",
                "Review timeout and retry configuration"
            ]
        }

    if "crashloopbackoff" in log_lower or "pod" in log_lower:
        return {
            "incident_type": "Kubernetes Pod Failure",
            "severity": "critical",
            "likely_root_cause": "A Kubernetes workload may be repeatedly crashing due to bad configuration, missing environment variables, or application startup failure.",
            "recommended_commands": [
                "kubectl get pods",
                "kubectl describe pod <pod-name>",
                "kubectl logs <pod-name>",
                "kubectl get events --sort-by=.metadata.creationTimestamp"
            ],
            "next_steps": [
                "Check container logs",
                "Validate environment variables",
                "Review readiness and liveness probes",
                "Check recent image or config changes"
            ]
        }

    if "terraform" in log_lower or "state lock" in log_lower:
        return {
            "incident_type": "Terraform / Infrastructure Error",
            "severity": "medium",
            "likely_root_cause": "Terraform may be blocked by a state lock, backend issue, or configuration mismatch.",
            "recommended_commands": [
                "terraform init",
                "terraform plan",
                "terraform state list",
                "terraform force-unlock <LOCK_ID>"
            ],
            "next_steps": [
                "Check if another Terraform process is running",
                "Verify backend configuration",
                "Review state lock details",
                "Avoid force-unlock unless you are sure no deployment is active"
            ]
        }

    return {
        "incident_type": "Unknown",
        "severity": "low",
        "likely_root_cause": "The log does not match known incident patterns yet.",
        "recommended_commands": [
            "Collect more logs",
            "Check recent deployments",
            "Review service metrics"
        ],
        "next_steps": [
            "Add more log examples",
            "Improve detection rules",
            "Escalate if issue affects users"
        ]
    }