from fastapi import FastAPI


app = FastAPI(debug=True)


def setup(setup_app: FastAPI):

    from app.controllers.auth.auth import router as auth_router
    from app.controllers.user.user import router as user_router
    from app.infrastructure.postgresql.database import create_tables

    create_tables()


    setup_app.include_router(auth_router)
    setup_app.include_router(user_router)


setup(app)
