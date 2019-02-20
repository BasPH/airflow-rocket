# Airflow Rocket

To setup the development environment, create a Conda environment from the `environment.yml`:

```bash
conda env create -f environment.yml
```

## Useful commands

The Makefile contains a number of useful targets for development. Run `make ci` to run the entire CI pipeline. 

## Testing

Tests require Docker installed to run.

## Tools used

This project uses:

- [Pylint](https://www.pylint.org) for linting
- [Black](https://github.com/ambv/black) for formatting
- [Pytest](https://pytest.org) for testing
- [Misspell](https://github.com/client9/misspell) for finding typos
