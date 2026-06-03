# Pinned, reproducible container for the n=26 circle-packing run (Task 02/03).
#
# OpenEvolve requires an OpenAI-compatible API; no key is baked in. For the local
# path (Task 03) the endpoint is host Ollama, reached at
# http://host.docker.internal:11434/v1 with a dummy key set in the run config.
#
# Reproducibility pins:
#   - Base image is pinned BY DIGEST (not a floating tag).
#   - OpenEvolve is installed at an exact commit SHA.
#   - Python deps are frozen in requirements.lock.txt (to be generated at build).
#
# Base image digest resolved locally on 2026-06-02 via:
#   docker buildx imagetools inspect python:3.12-slim-bookworm
FROM python:3.12-slim-bookworm@sha256:93ab4b7fa528b25124c97bcc755415e60eb671a86b4dbe0328df2fe2d1c1193d

# Pin the OpenEvolve dependency at the SHA selected in Task 01.
ARG OPENEVOLVE_REPO=https://github.com/codelion/openevolve
ARG OPENEVOLVE_SHA=80945ed82886d5c4ff2f3d22436765d50cb61266

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Clone and pin OpenEvolve. The tree is treated as a dependency; the example we
# adapt is copied into /work, not edited in place.
RUN git clone "${OPENEVOLVE_REPO}" openevolve \
    && cd openevolve \
    && git checkout "${OPENEVOLVE_SHA}" \
    && git rev-parse HEAD > /opt/OPENEVOLVE_SHA.txt

RUN pip install --upgrade pip \
    && pip install ./openevolve \
    && pip freeze > /opt/requirements.lock.txt

WORKDIR /work
# The independent evaluator is copied in so a result can be re-checked in-container.
COPY independent_evaluator.py /work/independent_evaluator.py

# Output is written to a mounted directory; the host only reads results back.
VOLUME ["/work/output"]

# No API key is stored in the image. Supply at runtime, e.g.:
#   docker run --rm \
#     -e OPENAI_API_KEY -e OPENAI_BASE_URL \
#     -v ${PWD}/output:/work/output \
#     circle-packing:pinned <run-command>
CMD ["python", "-c", "print('Container ready. Provide run command + LLM env at runtime.')"]
