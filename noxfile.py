import nox


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    pyproject = nox.project.load_toml()
    deps = nox.project.dependency_groups(pyproject, "test")
    session.install("-e.", *deps)
    session.run("pytest", *session.posargs)


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("ruff")
    session.run("ruff", "check", ".")
