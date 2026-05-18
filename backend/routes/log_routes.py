from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.log_models import LogRequest
from models.incident import Incident
from services.log_services import analyze_log
from database import get_db

router = APIRouter()


def format_incident(incident: Incident):
    return {
        "id": incident.id,
        "log_text": incident.log_text,
        "incident_type": incident.incident_type,
        "severity": incident.severity,
        "status": incident.status
    }


@router.post("/analyze-log")
def analyze(request: LogRequest, db: Session = Depends(get_db)):
    result = analyze_log(request.log_text)

    incident = Incident(
        log_text=request.log_text,
        incident_type=result.get("incident_type"),
        severity=result.get("severity"),
        status="open"
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return {
        "incident_id": incident.id,
        "analysis": result,
        "status": incident.status
    }


@router.get("/incidents")
def get_incidents(
    severity: str | None = None,
    incident_type: str | None = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)

    if severity:
        query = query.filter(Incident.severity == severity)

    if incident_type:
        query = query.filter(
            Incident.incident_type.contains(incident_type)
        )

    incidents = query.limit(limit).all()

    return {
        "count": len(incidents),
        "incidents": [
            format_incident(incident)
            for incident in incidents
        ]
    }


@router.get("/incidents/{incident_id}")
def get_incident_by_id(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {
            "error": "Incident not found"
        }

    return format_incident(incident)


@router.put("/incidents/{incident_id}/status")
def update_incident_status(
    incident_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        return {
            "error": "Incident not found"
        }

    allowed_statuses = [
        "open",
        "investigating",
        "resolved"
    ]

    if status not in allowed_statuses:
        return {
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }

    incident.status = status

    db.commit()
    db.refresh(incident)

    return {
        "message": "Incident status updated",
        "incident": format_incident(incident)
    }


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()

    return {
        "total_incidents": len(incidents),
        "severity_counts": {
            "critical": len(
                [i for i in incidents if i.severity == "critical"]
            ),
            "high": len(
                [i for i in incidents if i.severity == "high"]
            ),
            "medium": len(
                [i for i in incidents if i.severity == "medium"]
            ),
            "low": len(
                [i for i in incidents if i.severity == "low"]
            )
        },
        "status_counts": {
            "open": len(
                [i for i in incidents if i.status == "open"]
            ),
            "investigating": len(
                [i for i in incidents if i.status == "investigating"]
            ),
            "resolved": len(
                [i for i in incidents if i.status == "resolved"]
            )
        }
    }