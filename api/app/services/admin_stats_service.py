from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import project_repository, transaction_repository
from app.schemas.admin import DashboardOverviewOut, ProjectActivityOut, StatusBreakdown


def _breakdown(counts: dict[str, int]) -> StatusBreakdown:
    return StatusBreakdown(**{k: v for k, v in counts.items() if k in StatusBreakdown.model_fields})


async def get_overview(db: AsyncSession) -> DashboardOverviewOut:
    total = await transaction_repository.count_total(db)
    by_status = await transaction_repository.count_by_status(db)
    by_type = await transaction_repository.count_by_type(db)
    projects = await project_repository.list_all(db)

    return DashboardOverviewOut(
        total_transactions=total,
        total_projects=len(projects),
        active_projects=sum(1 for p in projects if p.status.value == "active"),
        by_status=_breakdown(by_status),
        by_type=by_type,
    )


async def get_activity_by_project(db: AsyncSession) -> list[ProjectActivityOut]:
    projects = await project_repository.list_all(db)
    raw_counts = await transaction_repository.count_by_project_and_status(db)

    per_project: dict[str, dict[str, int]] = {}
    for project_id, status_value, count in raw_counts:
        per_project.setdefault(str(project_id), {})[status_value] = count

    results = []
    for project in projects:
        counts = per_project.get(str(project.id), {})
        results.append(
            ProjectActivityOut(
                project_id=project.id,
                project_name=project.name,
                project_slug=project.slug,
                total_transactions=sum(counts.values()),
                by_status=_breakdown(counts),
            )
        )
    return results
