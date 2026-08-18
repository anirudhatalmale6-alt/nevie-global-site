#!/usr/bin/env python3
"""
Génère les fichiers de configuration d'hébergement (en-têtes de sécurité,
compression, cache, page 404, redirections) pour les trois cas les plus
courants : Apache, Nginx et les plateformes de type Netlify / Cloudflare Pages.

La politique de sécurité de contenu (CSP) est stricte : ni « unsafe-inline »
pour les scripts, ni pour les styles. Le seul script en ligne du site est le
bloc de données structurées JSON-LD de l'accueil ; son empreinte SHA-256 est
calculée ici et insérée dans la directive script-src. Ce fichier est donc
régénéré automatiquement à chaque construction du site.

Usage :  python3 outils/entetes.py   (appelé aussi par outils/construire.py)
"""

import base64
import hashlib
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "deploiement")

# Domaine du webhook n8n : le formulaire y envoie ses données, la CSP doit
# donc l'autoriser explicitement en connect-src.
DOMAINE_N8N = "https://nevie-global.app.n8n.cloud"


def empreintes_scripts_inline():
    """Empreintes SHA-256 de tous les scripts en ligne présents dans les pages."""
    empreintes = set()
    for nom in sorted(os.listdir(RACINE)):
        if not nom.endswith(".html"):
            continue
        html = open(os.path.join(RACINE, nom), encoding="utf-8").read()
        for corps in re.findall(r"<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>", html, re.S):
            somme = hashlib.sha256(corps.encode("utf-8")).digest()
            empreintes.add("'sha256-" + base64.b64encode(somme).decode() + "'")
    return sorted(empreintes)


def csp():
    scripts = " ".join(["'self'"] + empreintes_scripts_inline())
    return "; ".join([
        "default-src 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "script-src " + scripts,
        "style-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self' " + DOMAINE_N8N,
        "form-action 'self' " + DOMAINE_N8N,
        "upgrade-insecure-requests",
    ])


ENTETES = [
    ("Content-Security-Policy", None),  # rempli dynamiquement
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"),
    ("X-Frame-Options", "DENY"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
    ("Cross-Origin-Resource-Policy", "same-origin"),
    ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
]


def liste_entetes(valeur_csp):
    return [(nom, valeur_csp if nom == "Content-Security-Policy" else val)
            for nom, val in ENTETES]


APACHE = """# ===========================================================================
# NEVIE-GLOBAL SAS — configuration Apache
# À déposer à la racine web (fichier .htaccess).
#
# Généré par outils/entetes.py — ne pas modifier à la main : régénérer.
# ===========================================================================

# --- Page d'erreur --------------------------------------------------------
ErrorDocument 404 /404.html

# --- HTTPS et domaine canonique -------------------------------------------
# Décommenter après la mise en place du certificat, en adaptant le domaine.
<IfModule mod_rewrite.c>
  RewriteEngine On
  # RewriteCond %{HTTPS} !=on
  # RewriteRule ^ https://www.nevie-global.fr%{REQUEST_URI} [L,R=301]
  # RewriteCond %{HTTP_HOST} !^www\\. [NC]
  # RewriteRule ^ https://www.nevie-global.fr%{REQUEST_URI} [L,R=301]
</IfModule>

# --- En-têtes de sécurité -------------------------------------------------
<IfModule mod_headers.c>
__ENTETES_APACHE__
  # Le cache long ne s'applique qu'aux fichiers versionnables
  <FilesMatch "\\.(css|js|woff2|png|jpg|webp|svg|ico)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  # Les pages HTML doivent être revalidées : le contenu évolue
  <FilesMatch "\\.html$">
    Header set Cache-Control "public, max-age=0, must-revalidate"
  </FilesMatch>
</IfModule>

# --- Compression ----------------------------------------------------------
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml \\
                                application/javascript application/json \\
                                image/svg+xml application/xml
</IfModule>
<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/css text/plain text/xml \\
                                        application/javascript application/json \\
                                        image/svg+xml application/xml
</IfModule>

# --- Types MIME -----------------------------------------------------------
<IfModule mod_mime.c>
  AddType font/woff2 .woff2
  AddType image/webp .webp
</IfModule>

# --- Indexation des répertoires interdite ---------------------------------
Options -Indexes
"""


NGINX = """# ===========================================================================
# NEVIE-GLOBAL SAS — extrait de configuration Nginx
# À inclure dans le bloc server{} du domaine.
#
# Généré par outils/entetes.py — ne pas modifier à la main : régénérer.
# ===========================================================================

root /var/www/nevie-global;
index index.html;

error_page 404 /404.html;

# --- En-têtes de sécurité -------------------------------------------------
__ENTETES_NGINX__

# --- Compression ----------------------------------------------------------
gzip on;
gzip_vary on;
gzip_min_length 512;
gzip_types text/plain text/css text/xml application/javascript application/json image/svg+xml;

# --- Cache ----------------------------------------------------------------
location ~* \\.(css|js|woff2|png|jpg|jpeg|webp|svg|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location ~* \\.html$ {
    add_header Cache-Control "public, max-age=0, must-revalidate";
}

# --- URL sans extension : /contact sert contact.html ----------------------
location / {
    try_files $uri $uri.html $uri/ =404;
}
"""


HEADERS_PLATEFORME = """# ===========================================================================
# NEVIE-GLOBAL SAS — fichier _headers
# Format reconnu par Netlify et Cloudflare Pages.
# À déposer à la racine du site publié.
#
# Généré par outils/entetes.py — ne pas modifier à la main : régénérer.
# ===========================================================================

/*
__ENTETES_PLATEFORME__

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
"""


def main():
    os.makedirs(SORTIE, exist_ok=True)
    entetes = liste_entetes(csp())

    apache = "\n".join('  Header always set %s "%s"' % (n, v) for n, v in entetes)
    nginx = "\n".join('add_header %s "%s" always;' % (n, v) for n, v in entetes)
    plateforme = "\n".join("  %s: %s" % (n, v) for n, v in entetes)

    fichiers = {
        ".htaccess": APACHE.replace("__ENTETES_APACHE__", apache),
        "nginx.conf": NGINX.replace("__ENTETES_NGINX__", nginx),
        "_headers": HEADERS_PLATEFORME.replace("__ENTETES_PLATEFORME__", plateforme),
    }

    for nom, contenu in fichiers.items():
        with open(os.path.join(SORTIE, nom), "w", encoding="utf-8") as f:
            f.write(contenu)
        print("  deploiement/%-14s %5.1f ko" % (nom, len(contenu) / 1024))

    print("\nEmpreintes de scripts en ligne autorisées :")
    for e in empreintes_scripts_inline():
        print("  " + e)


if __name__ == "__main__":
    main()
