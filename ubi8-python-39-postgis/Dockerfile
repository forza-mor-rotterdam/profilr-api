FROM registry.access.redhat.com/ubi8/python-39

ENV SUMMARY="Ubi8 base image with Proj, GDAL and GEOS preinstalled with cmake from OSGeo"

LABEL summary="$SUMMARY"

USER root

ENV CMAKE_VERSION=3.17.3 \
    PROJ_VERSION=9.1.0 \
    GDAL_VERSION=3.5.2 \
    GEOS_VERSION=3.11.0 \
    INSTALL_DIR=/cmake_tmp

RUN mkdir -p ${INSTALL_DIR} && \
    wget -P ${INSTALL_DIR}/ https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}.tar.gz \
    https://download.osgeo.org/proj/proj-${PROJ_VERSION}.tar.gz \
    https://download.osgeo.org/gdal/CURRENT/gdal-${GDAL_VERSION}.tar.gz \
    https://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2 && \
    tar -zxvf ${INSTALL_DIR}/cmake-${CMAKE_VERSION}.tar.gz -C ${INSTALL_DIR}/ && \
    tar -zxvf ${INSTALL_DIR}/proj-${PROJ_VERSION}.tar.gz -C ${INSTALL_DIR}/ && \
    tar -zxvf ${INSTALL_DIR}/gdal-${GDAL_VERSION}.tar.gz -C ${INSTALL_DIR}/ && \
    tar xvfj ${INSTALL_DIR}/geos-${GEOS_VERSION}.tar.bz2 -C ${INSTALL_DIR}/ && \
    ${INSTALL_DIR}/cmake-${CMAKE_VERSION}/bootstrap && \
    make -I ${INSTALL_DIR}/cmake-${CMAKE_VERSION} && \
    make install -d ${INSTALL_DIR}/cmake-${CMAKE_VERSION} && \
    mkdir ${INSTALL_DIR}/proj-${PROJ_VERSION}/build && \
    cmake ${INSTALL_DIR}/proj-${PROJ_VERSION}/ -B ${INSTALL_DIR}/proj-${PROJ_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/proj-${PROJ_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/proj-${PROJ_VERSION}/build/ --target install && \
    mkdir ${INSTALL_DIR}/gdal-${GDAL_VERSION}/build && \
    cmake ${INSTALL_DIR}/gdal-${GDAL_VERSION}/ -B ${INSTALL_DIR}/gdal-${GDAL_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/gdal-${GDAL_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/gdal-${GDAL_VERSION}/build/  --with-geos=yes --target install && \
    mkdir ${INSTALL_DIR}/geos-${GEOS_VERSION}/build && \
    cmake ${INSTALL_DIR}/geos-${GEOS_VERSION}/ -B ${INSTALL_DIR}/geos-${GEOS_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/geos-${GEOS_VERSION}/build/ && \
    cmake --build ${INSTALL_DIR}/geos-${GEOS_VERSION}/build/ --target install && \
    ldconfig && \
    rm -rf ${INSTALL_DIR}/

ENV GDAL_LIBRARY_PATH=/usr/local/lib64/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/local/lib64/libgeos.so
