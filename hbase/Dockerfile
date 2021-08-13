#https://www.cnblogs.com/zhi-leaf/p/12092921.html  | https://blog.csdn.net/liuzhoulong/article/details/52056497  | openjdk:8u171-jre-alpine3.8
FROM java:8-jdk
MAINTAINER hbase_2_4_1

ENV HBASE_VERSION=2.4.1
ENV BASE_DIR=/usr/local
ENV HBASE_HOME=${BASE_DIR}/hbase-${HBASE_VERSION}

RUN cd ${BASE_DIR} \
    && curl -fSL "https://mirrors.bfsu.edu.cn/apache/hbase/2.4.1/hbase-2.4.1-bin.tar.gz" -o hbase.tar.gz \
    && tar xfvz hbase.tar.gz \
    && rm -rf hbase.tar.gz

EXPOSE 16010
EXPOSE 8080
EXPOSE 9090

#/usr/local/hbase-1.2.12/bin/hbase-daemon.sh start rest -p 8080
ENTRYPOINT ${HBASE_HOME}/bin/hbase-daemon.sh start rest && ${HBASE_HOME}/bin/hbase-daemon.sh start thrift2 && ${HBASE_HOME}/bin/hbase master start