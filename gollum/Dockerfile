#https://github.com/gollum/gollum/wiki/Gollum-via-Docker, 2021-2-6  docker run -v `pwd`:/wiki -p 4567:80 gollum

FROM ruby:2.7
RUN apt-get -y update && apt-get -y install libicu-dev cmake git && rm -rf /var/lib/apt/lists/*
RUN gem install github-linguist
RUN gem install gollum
RUN gem install org-ruby  # optional
WORKDIR /wiki
ENTRYPOINT ["gollum", "--port", "80"]
EXPOSE 80