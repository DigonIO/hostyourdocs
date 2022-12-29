FROM archlinux:base-20221225.0.113672

RUN echo 'Server = https://archive.archlinux.org/repos/2022/12/28/$repo/os/$arch' > /etc/pacman.d/mirrorlist

RUN pacman -Syy
RUN pacman -S zsh python python-pip mariadb gcc --noconfirm

RUN chsh -s /usr/bin/zsh root

RUN pacman -Q -s python
RUN pacman -Q -s mariadb

RUN useradd app

RUN mkdir /app
RUN mkdir /data
RUN chown app:app /data

COPY setup.py /app
COPY src /app
COPY LICENSE /app

RUN pip install /app

USER app
EXPOSE 8080
CMD ["python", "-m", "hyd.backend"]