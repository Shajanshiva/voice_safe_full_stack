from backend.main import app

print("--- REGISTERED ROUTES ---")
for route in app.routes:
    # Most interesting: check for APIRoute instances
    if hasattr(route, "path"):
        methods = getattr(route, "methods", [])
        print(f"{list(methods)} {route.path}")
print("-------------------------")
