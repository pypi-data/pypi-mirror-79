import fastapi

class AppClient:
    def __init__(self, router, middleware=None):
        self.app = fastapi.FastAPI()
        self.app.include_router(router)

        self.middleware = middleware

    def _add_middleware(self):
        if self.middleware:
            self.app.middleware("http")(self.middleware)

    def get_app(self):
        self._add_middleware()
        return self.app
