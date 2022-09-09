from fastapi import FastAPI


def init_cronjobs(app: FastAPI):
    from .notify_expired_mecidine import setup as expired_setup

    expired_setup(app)




