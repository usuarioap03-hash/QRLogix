import requests
import os
from github import Github

# Config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = "usuarioap03-hash"
REPO_NAME = "hosting"
FILE_PATH = "index.html"
BRANCH = "main"

# 1. Obtener URL pública de ngrok
resp = requests.get("http://127.0.0.1:4040/api/tunnels")
data = resp.json()
url = data["tunnels"][0]["public_url"]
print(f"✅ URL pública ngrok: {url}")

# 2. Preparar nuevo contenido de index.html
nuevo_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QRLogix - Redirección</title>
    <script>
        const BASE_URL = "{url}";
        const params = new URLSearchParams(window.location.search);
        const punto = params.get("punto");

        if (punto) {{
            window.location.href = `${{BASE_URL}}/scan/punto${{punto}}`;
        }} else {{
            document.write("⚠️ No se especificó ningún punto.");
        }}
    </script>
</head>
<body>
    <h1>Redirigiendo...</h1>
</body>
</html>
"""

# 3. Conectar a GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_user(GITHUB_USER).get_repo(REPO_NAME)

# 4. Obtener archivo actual
contents = repo.get_contents(FILE_PATH, ref=BRANCH)

# 5. Actualizar archivo
repo.update_file(
    path=FILE_PATH,
    message=f"Actualizar túnel a {url}",
    content=nuevo_html,
    sha=contents.sha,
    branch=BRANCH
)

print("🚀 index.html actualizado en GitHub Pages")