import sys

import typer
from typer.testing import CliRunner

from bapy import app

runner = CliRunner()

if __name__ == '__main__':
    runner.invoke(app, sys.argv[1:])
