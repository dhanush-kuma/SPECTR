from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Investigator, OrganizerTermsAcceptance, RandomizationRecord, Site, Study


def get_organizer_usage_stats(db: Session, organizer_id: int) -> dict[str, int]:
    study_count = (
        db.query(func.count(Study.id))
        .filter(Study.organizer_id == organizer_id)
        .scalar()
    ) or 0

    active_study_count = (
        db.query(func.count(Study.id))
        .filter(Study.organizer_id == organizer_id, Study.status == "Active")
        .scalar()
    ) or 0

    site_count = (
        db.query(func.count(Site.id))
        .join(Study, Site.study_id == Study.id)
        .filter(Study.organizer_id == organizer_id)
        .scalar()
    ) or 0

    investigator_count = (
        db.query(func.count(Investigator.id))
        .join(Study, Investigator.study_id == Study.id)
        .filter(Study.organizer_id == organizer_id)
        .scalar()
    ) or 0

    total_randomization_records = (
        db.query(func.count(RandomizationRecord.id))
        .join(Study, RandomizationRecord.study_id == Study.id)
        .filter(Study.organizer_id == organizer_id)
        .scalar()
    ) or 0

    assigned_participants = (
        db.query(func.count(RandomizationRecord.id))
        .join(Study, RandomizationRecord.study_id == Study.id)
        .filter(
            Study.organizer_id == organizer_id,
            RandomizationRecord.assigned_patient_id.isnot(None),
        )
        .scalar()
    ) or 0

    return {
        "study_count": study_count,
        "active_study_count": active_study_count,
        "site_count": site_count,
        "investigator_count": investigator_count,
        "total_randomization_records": total_randomization_records,
        "assigned_participants": assigned_participants,
    }


def get_organizer_terms_accepted_at(
    db: Session, organizer_id: int
) -> Optional[datetime]:
    row = (
        db.query(OrganizerTermsAcceptance.accepted_at)
        .filter(OrganizerTermsAcceptance.organizer_id == organizer_id)
        .order_by(OrganizerTermsAcceptance.accepted_at.desc())
        .first()
    )
    return row[0] if row else None


def get_study_summaries_for_organizer(db: Session, organizer_id: int) -> list[dict]:
    studies = (
        db.query(Study)
        .filter(Study.organizer_id == organizer_id)
        .order_by(Study.created_at.desc())
        .all()
    )

    summaries: list[dict] = []
    for study in studies:
        site_count = db.query(Site).filter(Site.study_id == study.id).count()
        investigator_count = (
            db.query(Investigator).filter(Investigator.study_id == study.id).count()
        )
        records_query = db.query(RandomizationRecord).filter(
            RandomizationRecord.study_id == study.id
        )
        total_records = records_query.count()
        assigned = records_query.filter(
            RandomizationRecord.assigned_patient_id.isnot(None)
        ).count()
        summaries.append(
            {
                "id": study.id,
                "title": study.title,
                "protocol_code": study.protocol_code,
                "status": study.status,
                "created_at": study.created_at,
                "site_count": site_count,
                "investigator_count": investigator_count,
                "total_records": total_records,
                "assigned": assigned,
                "unassigned": total_records - assigned,
            }
        )
    return summaries
