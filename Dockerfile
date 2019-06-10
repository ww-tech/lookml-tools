FROM python:3.6.4


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY lkmltools ./lkmltools
COPY test ./test

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt-get update

RUN apt-get install graphviz -y sudo

# install node and the lookml-parser
RUN apt-get install -y sudo
RUN sudo apt-get install -y curl
RUN sudo curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
RUN sudo apt-get install -y nodejs
RUN sudo npm install -g lookml-parser

ENTRYPOINT ["python", "-m", "pytest", "--cov=lkmltools/", "test/"]

