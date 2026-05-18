def analyze_log(log_text: str):
    log_lower = log_text.lower()

    # Database issues
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

    # Kubernetes issues
    if "crashloopbackoff" in log_lower or "pod" in log_lower:
        return {
            "incident_type": "Kubernetes Pod Failure",
            "severity": "critical",
            "likely_root_cause": "A Kubernetes workload may be repeatedly crashing.",
            "recommended_commands": [
                "kubectl get pods",
                "kubectl describe pod <pod-name>",
                "kubectl logs <pod-name>"
            ],
            "next_steps": [
                "Check container logs",
                "Validate environment variables",
                "Review probes"
            ]
        }

    # Terraform issues
    if "terraform" in log_lower or "state lock" in log_lower:
        return {
            "incident_type": "Terraform / Infrastructure Error",
            "severity": "medium",
            "likely_root_cause": "Terraform backend or state issue.",
            "recommended_commands": [
                "terraform init",
                "terraform state list",
                "terraform force-unlock <LOCK_ID>"
            ],
            "next_steps": [
                "Review state lock details",
                "Check backend configuration"
            ]
        }

    # CPU issues
    if "cpu" in log_lower or "usage exceeded" in log_lower:
        return {
            "incident_type": "High CPU Usage",
            "severity": "high",
            "likely_root_cause": "Application process or workload consuming excessive CPU.",
            "recommended_commands": [
                "top",
                "htop",
                "kubectl top pod",
                "Check monitoring dashboards"
            ],
            "next_steps": [
                "Identify high CPU processes",
                "Check recent deployments",
                "Review scaling strategy"
            ]
        }

    # Memory issues
    if "memory" in log_lower or "outofmemory" in log_lower:
        return {
            "incident_type": "Memory Pressure",
            "severity": "high",
            "likely_root_cause": "Application may be leaking memory or workload exceeds limits.",
            "recommended_commands": [
                "free -m",
                "kubectl top pod",
                "Check memory dashboards"
            ],
            "next_steps": [
                "Review memory consumption",
                "Check memory limits",
                "Restart affected services if needed"
            ]
        }

    # Authentication failures
    if "authentication" in log_lower or "unauthorized" in log_lower:
        return {
            "incident_type": "Authentication Failure",
            "severity": "medium",
            "likely_root_cause": "Invalid credentials or token issues.",
            "recommended_commands": [
                "Review auth logs",
                "Check token expiration",
                "Validate IAM permissions"
            ],
            "next_steps": [
                "Verify credentials",
                "Review access configuration"
            ]
        }

    # Network issues
    if "network" in log_lower or "latency" in log_lower:
        return {
            "incident_type": "Network Latency",
            "severity": "medium",
            "likely_root_cause": "Network connectivity degradation.",
            "recommended_commands": [
                "ping",
                "traceroute",
                "Check network dashboards"
            ],
            "next_steps": [
                "Check packet loss",
                "Review network configuration"
            ]
        }

    # Disk issues
    if "disk" in log_lower or "no space left" in log_lower:
        return {
            "incident_type": "Disk Capacity Issue",
            "severity": "high",
            "likely_root_cause": "Disk utilization exceeded available capacity.",
            "recommended_commands": [
                "df -h",
                "du -sh *"
            ],
            "next_steps": [
                "Remove unnecessary files",
                "Increase storage"
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
            "Escalate if issue affects users"
        ]
    }