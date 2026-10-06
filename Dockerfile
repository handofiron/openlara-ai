FROM lscr.io/linuxserver/baseimage-selkies:ubuntu-noble

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libx11-6 \
        libgl1 \
        libpulse0 \
        libasound2 \
        libstdc++6 \
        libgcc-s1 \
        mesa-utils \
        mesa-utils-extra \
        intel-gpu-tools \
        xterm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY root/ /

RUN chmod +x /custom-cont-init.d/10-openlara-autostart \
    && mkdir -p \
        /defaults/autostart \
        /opt/openlara \
        /config/openlara

ENV OPENLARA_GAME_DIR=/game \
    OPENLARA_SAVE_DIR=/config/openlara \
    LIBGL_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri \
    MESA_LOADER_DRIVER_OVERRIDE=iris
