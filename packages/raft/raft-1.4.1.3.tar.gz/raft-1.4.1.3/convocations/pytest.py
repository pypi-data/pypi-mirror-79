"""
Pytest-using variant of testing.py. Will eventually replace the latter.
"""

from raft import task


@task
def test(
    c,
    verbose=True,
    color=True,
    capture="sys",
    module=None,
    k=None,
    x=False,
    opts="",
    pty=True,
):
    """
    Run pytest with given options.

    :param bool verbose:
        Whether to run tests in verbose mode.

    :param bool color:
        Whether to request colorized output (typically only works when
        ``verbose=True``.)

    :param str capture:
        What type of stdout/err capturing pytest should use. Defaults to
        ``sys`` since pytest's own default, ``fd``, tends to trip up
        subprocesses trying to detect PTY status. Can be set to ``no`` for no
        capturing / useful print-debugging / etc.

    :param str module:
        Select a specific test module to focus on, e.g. ``main`` to only run
        ``tests/main.py``. (Note that this is a specific idiom aside from the
        use of ``-o '-k pattern'``.) Default: ``None``.

    :param str k:
        Convenience passthrough for ``pytest -k``, i.e. test selection.
        Default: ``None``.

    :param bool x:
        Convenience passthrough for ``pytest -x``, i.e. fail-fast. Default:
        ``False``.

    :param str opts:
        Extra runtime options to hand to ``pytest``.

    :param bool pty:
        Whether to use a pty when executing pytest. Default: ``True``.
    """
    # TODO: really need better tooling around these patterns
    # TODO: especially the problem of wanting to be configurable, but
    # sometimes wanting to override one's config via kwargs; and also needing
    # non-None defaults in the kwargs to inform the parser (or have to
    # configure it explicitly...?)
    flags = []
    if verbose:
        flags.append("--verbose")
    if color:
        flags.append("--color=yes")
    flags.append("--capture={0}".format(capture))
    if opts is not None:
        flags.append(opts)
    if k is not None and not ("-k" in opts if opts else False):
        flags.append("-k '{}'".format(k))
    if x and not ("-x" in opts if opts else False):
        flags.append("-x")
    modstr = ""
    if module is not None:
        modstr = " tests/{}.py".format(module)
    c.run("pytest {}{}".format(" ".join(flags), modstr), pty=pty)


@task(help=test.help)
def integration(
    c,
    opts=None,
    pty=True,
    x=False,
    k=None,
    verbose=True,
    color=True,
    capture="sys",
    module=None,
):
    """
    Run the integration test suite. May be slow!

    See ``pytest.test`` for description of most arguments.
    """
    opts = opts or ""
    opts += " integration/"
    if module is not None:
        opts += "{}.py".format(module)
    test(
        c,
        opts=opts,
        pty=pty,
        x=x,
        k=k,
        verbose=verbose,
        color=color,
        capture=capture,
    )


@task
def coverage(c, report="term", opts="", tester=None):
    """
    Run pytest with coverage enabled.

    Assumes the ``pytest-cov`` pytest plugin is installed.

    :param str report:
        Coverage report style to use. If 'html', will also open in browser.

    :param str opts:
        Extra runtime opts to pass to pytest.

    :param tester:
        Specific test task object to raft. If ``None`` (default), uses this
        module's local `test`.
    """
    opts += "--cov --no-cov-on-fail --cov-report={0}".format(report)
    # TODO: call attached suite's test(), not the one in here, if they differ
    (tester or test)(c, opts=opts)
    if report == "html":
        c.run("open htmlcov/index.html")
