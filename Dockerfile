FROM python:3.6.4

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY lkmltools ./lkmltools
COPY test ./test
COPY .git ./.git

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt-get update

RUN apt-get install graphviz -y sudo

ENTRYPOINT ["python", "-m", "pytest", "--cov=lkmltools/", "test/"]

