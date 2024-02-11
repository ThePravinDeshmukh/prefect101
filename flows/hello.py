
from prefect import flow, get_run_logger, tags

@flow
def hello(name: str = "Marvin"):
    logger = get_run_logger()
    logger.info(f"Hello, {name}!")

if __name__ == "__main__":
    hello_world.deploy(
        name="my-first-deployment",
        work_pool_name="above-ground",
        image='my_registry/hello_world:demo',
        job_variables={"env": { "EXTRA_PIP_PACKAGES": "boto3" } }
    )