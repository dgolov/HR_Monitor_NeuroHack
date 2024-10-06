import os.path
from datetime import datetime
from pathlib import Path

import pandas as pd
import xlsxwriter
from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.api.v1.deps import repo_dep
from src.database.models import HireTimeMetrics
from src.repositiry.repo import Repository
from src.schema import schemas


router = APIRouter(prefix="/reports")



@router.get("/{metric_by_hr}")
async def get_task(
        metric_by_hr: str | None = None,
        hr_names: str | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        repository: Repository = repo_dep,
):
    report_directory = "./reports"
    filename = f'./{metric_by_hr}_{start}_{end}.xlsx'
    full_filepath = os.path.join(report_directory, filename)

    all_metrics = {
        'screen-time': repository.get_screen_time_data,
        'hire-quality': repository.get_hire_quality_data,
        'hire-time': repository.get_hire_time_data,
        'owner-satisfaction': repository.get_owner_satisfaction,
        'vacancy-cost': repository.get_vacancy_cost_data,
        'vacancy-cost-comparison': repository.get_vacancy_cost_comparison_data,
    }
    method = all_metrics.get(metric_by_hr)
    if not method:
        return 400, 'Not found'

    if hr_names:
        user_names = hr_names.split(',')
    else:
        user_names = None

    metrics = await method(recruiter_name=user_names, date_start=start, date_end=end)
    data_dicts = [{
        "id": d.id,
        "recruiter_name": d.recruiter_name,
        "month": d.month,
        "value": d.value
    } for d in metrics]

    df = pd.DataFrame(data_dicts)
    pivot_df = df.pivot(index='month', columns='recruiter_name', values='value')
    pivot_df.to_excel(full_filepath)

    return FileResponse(full_filepath, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename=filename)



