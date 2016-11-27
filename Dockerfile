# 5MB linux image with python
FROM jfloff/alpine-python:3.4-slim
MAINTAINER Martin Tomik <mtomik@live.com>
ENV PYTHONUNBUFFERED 1

# add needed package list to root dir ( to be visible for entrypoint.sh )
COPY *.txt /

# alpine bug fix
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

# run loading dependencies
RUN /entrypoint.sh

##5 defining compilers
ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++


RUN apk update && apk upgrade && apk --update add linux-headers

##6 opencv3
RUN mkdir /opt && cd /opt && \
  wget https://github.com/opencv/opencv/archive/3.1.0.zip && \
  wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip && \
  unzip 3.1.0.zip && \
  unzip opencv_contrib.zip && \
  cd /opt/opencv-3.1.0 && \
  mkdir build && \
  cd build && \
  cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_FFMPEG=NO \
    -D WITH_IPP=NO  \
    -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-3.1.0/modules \
    -D WITH_OPENEXR=NO .. && \
     make  && \
     make install

# move created opencv python lib to original place
RUN cd /usr/local/lib/python3.4/site-packages/ && \
     mv  cv2.cpython-34m.so /usr/lib/python3.4/site-packages/cv2.so

RUN mkdir /code
# set work dir to our code directory
WORKDIR /code

# copy project to the WORKDIR directory
COPY . .


# Clean APK cache
RUN rm -rf /var/cache/apk/*

EXPOSE 8000
# 0.0.0.0:8000 for prod server
CMD ["python","manage.py","runserver","0.0.0.0:8000"]