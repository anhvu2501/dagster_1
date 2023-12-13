from dagster import asset, AssetExecutionContext

@asset
def my_first_asset(context: AssetExecutionContext):
    """
    This is my first asset for testing purpose
    """
    print('Hello. This is my first asset')
    context.log.info('this is a log message')
    return [1, 2, 3]

@asset(deps=[my_first_asset])
def my_second_asset(context:AssetExecutionContext):
    """
    This is my second asset 
    """
    data = [4, 5, 6]
    context.log.info(f"Output data is {data}")
    return data