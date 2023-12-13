from dagster import asset, AssetExecutionContext, AssetIn, Definitions, define_asset_job, AssetSelection, ScheduleDefinition
from typing import List

@asset(group_name='get_started')
def my_first_asset(context: AssetExecutionContext):
    """
    This is my first asset for testing purpose
    """
    print('Hello. This is my first asset')
    context.log.info('this is a log message')
    return [1, 2, 3]

# @asset(deps=[my_first_asset])
# def my_second_asset(context:AssetExecutionContext):
#     """
#     This is my second asset 
#     """
#     data = [4, 5, 6]
#     context.log.info(f"Output data is {data}")
#     return data

@asset(ins={"upstream": AssetIn(key="my_first_asset")}, group_name='get_started')
def my_second_asset(context:AssetExecutionContext, upstream: List):
    """
    This is my second asset 
    """
    data = upstream + [4, 5, 6]
    context.log.info(f"Output data is {data}")
    return data

@asset(
    ins={
        "first_upstream": AssetIn("my_first_asset"),
        "second_upstream": AssetIn("my_second_asset"),
    },
    group_name='get_started'
)
def my_third_asset(
    context: AssetExecutionContext, first_upstream: List, second_upstream: List
):
    """
    This is our third asset
    """
    data = {
        "first_asset": first_upstream,
        "second_asset": second_upstream,
        "third_asset": second_upstream + [7, 8],
    }
    context.log.info(f"Output data is: {data}")
    return data

defs = Definitions(
    assets = [my_first_asset, my_second_asset, my_third_asset],
    jobs=[
        define_asset_job(
            name='hello_dagster_job',
            selection=AssetSelection.groups('get_started')
        )
    ],
    schedules=[
        ScheduleDefinition(
            name='hello_dagster_schedule',
            job_name='hello_dagster_job',
            cron_schedule='* * * * *'
        )
    ]
)