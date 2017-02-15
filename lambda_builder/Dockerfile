FROM amazonlinux

RUN yum -y install python27 python27-pip
RUN yum -y install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
RUN yum -y install gcc 
RUN yum -y install python27-devel 
RUN yum -y install git

RUN git clone https://github.com/FFmpeg/FFmpeg.git /root
RUN yum -y install yasm

WORKDIR /root/home
