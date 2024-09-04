##################
# base stage
# setting up shared environment variables
##################
FROM python:3.12.0-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.0 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

##################
# base stage
# building dependencies and create virtual environment
##################
FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # for installing poetry
        curl \
        # for building python deps
        build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
COPY poetry.lock pyproject.toml ./

# install poetry
RUN poetry install --no-dev

##################
# runner stage
# running as production environment
##################

FROM python-base as runner

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY . /app/

WORKDIR /app

RUN useradd --create-home --shell /bin/sh --uid 1001 --user-group user1

COPY --chown=user1 . /app

USER user1

CMD ["uvicorn", "fs_store.main:app", "--host", "0.0.0.0", "--port", "8000"]
