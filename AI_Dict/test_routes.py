from src.ai_dict.server import app
for route in app.routes:
    print(route.path, route.name)
