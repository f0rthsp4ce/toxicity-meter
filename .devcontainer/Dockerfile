FROM mcr.microsoft.com/devcontainers/anaconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY conda.yml /tmp/conda-tmp/environment.yml
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    direnv \
    && /bin/bash -c "echo 'eval \"\$(direnv hook bash)\"' >> ~/.bashrc"
# XXX: this should use dev containers' auto UID discovery. This hardcodes UID to 1001.
RUN sudo -u vscode /bin/sh -c 'curl -L https://nixos.org/nix/install | sh -s -- --no-daemon' \
    && chown -R 1001 /nix
RUN mkdir -p /home/vscode/.config/nix \
    && echo "experimental-features = nix-command flakes" > /home/vscode/.config/nix/nix.conf