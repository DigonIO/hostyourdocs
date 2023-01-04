FROM registry.gitlab.com/digonio/images/hostyourdocs-base:c05cb9bb

COPY setup.py /app
COPY src /app
COPY LICENSE /app

RUN pip install /app

USER app
EXPOSE 8000
CMD ["python", "-m", "hyd.backend"]