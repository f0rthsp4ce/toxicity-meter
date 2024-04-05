FROM mambaorg/micromamba:1 as build
COPY --chown=$MAMBA_USER:$MAMBA_USER conda.yml /tmp/
RUN micromamba install -y -n base -f /tmp/conda.yml && \
    micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY --chown=$MAMBA_USER:$MAMBA_USER models-preload.py /tmp/
RUN python3 /tmp/models-preload.py

FROM gcr.io/distroless/base-debian12:nonroot

COPY --from=build /opt/conda /opt/conda
COPY --from=build /home/mambauser/.cache /home/nonroot/.cache
COPY tg-bot.py /home/nonroot/

WORKDIR /home/nonroot
ENTRYPOINT ["/opt/conda/bin/python", "tg-bot.py"]