import pytest
from black import main as main_black
from invoke import context, task
from isort.main import main as import_sort


@task
def isort(c, path="."):
    # type: (context.Context, str) -> None
    import_sort([path])


@task
def black(c, path="."):
    # type: (context.Context, str) -> None
    main_black(path)


@task
def format(c, path="."):
    # type: (context.Context, str) -> None
    isort(c, path)
    black(c, path)


@task
def test(c, path="."):
    # type: (context.Context, str) -> None
    pytest.main([path])


@task
def retest(c, path="."):
    # type: (context.Context, str) -> None
    pytest.main([path, "--lf"])
