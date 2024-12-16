from invoke import task


@task
def run_dev(c):
    c.run("poetry run fastapi dev server", pty=True)


@task
def run_production(c):
    c.run("poetry run fastapi run server", pty=True)
