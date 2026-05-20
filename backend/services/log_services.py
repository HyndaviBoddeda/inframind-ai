def analyze_log(log_text: str):
    log_lower = log_text.lower()

    if "timeout" in log_lower or "database" in log_lower:
        return {
            "incident_type": "Database / Service Timeout",
            "severity": "high",
            "likely_root_cause": "Database connectivity issue",
            "recommended_commands": [
                "Check application logs",
                "Check database connectivity"
            ],
            "next_steps": [
                "Review timeout configuration"
            ]
        }

    if "cpu" in log_lower or "usage exceeded" in log_lower:
        return {
            "incident_type": "High CPU Usage",
            "severity": "high",
            "likely_root_cause": "Application consuming excessive CPU",
            "recommended_commands": [
                "top",
                "htop"
            ],
            "next_steps": [
                "Review scaling"
            ]
        }

    if "disk" in log_lower or "no space left" in log_lower:
        return {
            "incident_type": "Disk Capacity Issue",
            "severity": "high",
            "likely_root_cause": "Disk utilization exceeded capacity",
            "recommended_commands": [
                "df -h"
            ],
            "next_steps": [
                "Free storage"
            ]
        }

    return {
        "incident_type": "Unknown",
        "severity": "low",
        "likely_root_cause": "Unknown issue",
        "recommended_commands": [],
        "next_steps": []
    }
