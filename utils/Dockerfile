FROM aiboot/r-minimal:4.5.1

RUN installr -d -t "curl-dev" httr2

RUN echo -e 'PKG_CFLAGS+=-fopenmp\nPKG_LIBS+=-fopenmp\n' >> /tmp/Makevars && \
    R_MAKEVARS_USER=/tmp/Makevars \
    installr -a "libgomp zlib" -t "openmp-dev zlib-dev" -d data.table && \
    rm /tmp/Makevars

RUN ldd /usr/local/lib/R/library/data.table/libs/data_table.so 2> /dev/null || true

WORKDIR /app

ENV KAGGLE_USERNAME=#KAGGLE_USERNAME#
ENV KAGGLE_KEY=#KAGGLE_KEY#

COPY get_images.r .

ENTRYPOINT ["R", "-e", "source('/app/get_images.r')"]

# docker build -t images .
# docker run -v "$(pwd):/app/images" images
