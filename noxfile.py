import nox


@nox.session
def tests_coverage(session):
    """ Install all requirements, run pytest.
    """
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.install("coverage")
    session.run("coverage", "run",  "-m",  "--omit=.nox/*", "pytest")
    session.run("coverage", "report", "--fail-under=85", "--show-missing")
    session.run("coverage", "erase")

@nox.session
def black_check(session):
    """ Install black and test if the linting is correct.
    """
    session.install("black")
    session.run("black", "--check", "--diff", "tests", "scrape")