"""Persist CSV randomization rows with derived sites and stratas."""

from __future__ import annotations

from sqlalchemy.orm import Session

from ..models import RandomizationRecord, Site, Strata
from .randomization_csv import ParsedRow


def persist_csv_randomization(
    db: Session,
    study_id: int,
    parsed_rows: list[ParsedRow],
) -> list[RandomizationRecord]:
    """
    Replace all randomization data for *study_id* from parsed CSV rows.

    Deletes existing randomization records, stratas, and sites for the study,
    then creates sites from unique CSV site values, stratas unique per site,
    and randomization records linked to both. Caller must commit the session.
    """
    db.query(RandomizationRecord).filter(RandomizationRecord.study_id == study_id).delete()
    db.query(Strata).filter(Strata.study_id == study_id).delete()
    db.query(Site).filter(Site.study_id == study_id).delete()

    site_by_name: dict[str, Site] = {}
    for site_name in sorted({row["site"] for row in parsed_rows}):
        site = Site(study_id=study_id, name=site_name)
        db.add(site)
        db.flush()
        site_by_name[site_name] = site

    strata_by_key: dict[tuple[str, str], Strata] = {}
    for site_name, site in site_by_name.items():
        strat_names = sorted(
            {row["strat"] for row in parsed_rows if row["site"] == site_name}
        )
        for strat_name in strat_names:
            strata = Strata(study_id=study_id, site_id=site.id, name=strat_name)
            db.add(strata)
            db.flush()
            strata_by_key[(site_name, strat_name)] = strata

    new_records: list[RandomizationRecord] = []
    for row in parsed_rows:
        site = site_by_name[row["site"]]
        strata = strata_by_key[(row["site"], row["strat"])]
        record = RandomizationRecord(
            study_id=study_id,
            sequence_number=row["sequence_number"],
            kit_code=row["kit_code"],
            treatment_name=row["treatment_name"],
            site_id=site.id,
            strata_id=strata.id,
        )
        db.add(record)
        new_records.append(record)

    return new_records
