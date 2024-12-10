from invoke import task


@task
def run_dev(c):
    c.run("poetry run fastapi dev server", pty=True)
