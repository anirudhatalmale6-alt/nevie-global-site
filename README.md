# NEVIE-GLOBAL SAS — Site institutionnel

Site vitrine institutionnel de NEVIE-GLOBAL SAS, holding française basée à Nantes.

Site **statique** : HTML5 / CSS3 / JavaScript natif. Aucun CMS, aucune base de données,
aucun framework, aucune dépendance externe à installer. Il suffit de déposer les fichiers
sur n'importe quel hébergement web.

---

## 1. Contenu du dépôt

```
index.html                          Page principale (navigation ancrée, défilement fluide)
mentions-legales.html               Mentions légales
politique-de-confidentialite.html   Politique de confidentialité et cookies
favicon.svg                         Icône de l'onglet (emblème « N »)
robots.txt                          Indexation
sitemap.xml                         Plan du site pour les moteurs
assets/
  css/fonts.css                     Déclarations @font-face (Poppins auto-hébergée)
  css/style.css                     Feuille de style unique et commentée
  js/main.js                        Navigation, formulaires, bandeau cookies
  fonts/*.woff2                     Poppins 300/400/500/600, sous-ensembles latin
  img/embleme-n.svg                 Emblème « N »
  img/og-nevie-global.jpg           Image d'aperçu pour les partages (1200 × 630)
php/envoi.php                       Alternative PHP à Formspree (optionnelle)
```

---

## 2. Mise en ligne

Le site est purement statique : **aucun serveur applicatif n'est requis**.

1. Copier l'intégralité du dossier à la racine web de l'hébergement
   (`/www`, `/public_html`, `/htdocs` selon l'hébergeur).
2. Vérifier que `index.html` se trouve bien à la racine.
3. Activer HTTPS (certificat Let's Encrypt, inclus chez la quasi-totalité des hébergeurs).

Le site fonctionne également tel quel sur GitHub Pages, Netlify, Vercel, Cloudflare Pages
ou tout stockage objet servant des fichiers statiques.

### Test en local

```
python3 -m http.server 8000
```
puis ouvrir <http://localhost:8000>. Un simple double-clic sur `index.html` fonctionne
aussi, mais les polices auto-hébergées ne se chargent qu'à travers un serveur.

---

## 3. Activer l'envoi des formulaires (obligatoire avant mise en ligne)

Les deux formulaires (« Céder son entreprise » et « Contact ») envoient un e-mail
**sans base de données**. Tant que la configuration n'est pas faite, ils fonctionnent en
mode démonstration : la validation et le message de confirmation s'affichent, mais aucun
e-mail n'est réellement envoyé (un avertissement apparaît dans la console du navigateur).

### Solution retenue : Formspree

1. Créer un compte gratuit sur <https://formspree.io> avec l'adresse e-mail qui doit
   recevoir les demandes.
2. Créer deux formulaires, par exemple « Cession » et « Contact ». Formspree fournit pour
   chacun une URL de la forme `https://formspree.io/f/xxxxxxxx`.
3. Ouvrir `assets/js/main.js` et remplacer les deux valeurs en haut du fichier :

   ```js
   var CONFIG = {
     endpointCession: 'https://formspree.io/f/xxxxxxxx',
     endpointContact: 'https://formspree.io/f/yyyyyyyy',
     ...
   ```

4. Valider l'adresse de réception depuis l'e-mail envoyé par Formspree, puis tester un
   envoi réel depuis le site en ligne.

> L'identifiant Formspree est une **donnée publique**, visible dans le code de la page.
> Ce n'est pas un secret et aucune clé d'API privée n'est utilisée : le dépôt ne contient
> donc aucune information confidentielle.

### Alternative : script PHP (si l'hébergement exécute PHP)

Voir `php/envoi.php`. Renseigner `DESTINATAIRE` et `EXPEDITEUR` dans le fichier, le déposer
à la racine, puis remplacer les deux endpoints par `'envoi.php'` dans `assets/js/main.js`.
L'adresse d'expédition doit appartenir au domaine du site pour éviter le classement en
courrier indésirable.

---

## 4. À compléter avant la mise en production

| Où | Quoi |
|---|---|
| `index.html`, `mentions-legales.html`, `politique-de-confidentialite.html`, `robots.txt`, `sitemap.xml` | Remplacer `https://www.nevie-global.fr/` par le domaine définitif (balises `canonical`, Open Graph, plan du site) |
| `assets/js/main.js` | Les deux endpoints Formspree (voir §3) |
| `index.html` — section Contact | L'adresse e-mail affichée (`contact@nevie-global.fr` est une valeur provisoire) |
| `mentions-legales.html` | SIREN / SIRET, numéro RCS Nantes, TVA intracommunautaire, coordonnées de l'hébergeur |

Ces emplacements sont signalés dans le code par un commentaire `À COMPLÉTER` ou
`À REMPLACER`.

---

## 5. Choix techniques

**Poppins auto-hébergée.** Les polices sont servies depuis le site (`assets/fonts/`,
format woff2, sous-ensembles latin et latin-ext uniquement). Aucune requête n'est adressée
à Google Fonts : l'adresse IP des visiteurs n'est transmise à aucun tiers — position la
plus sûre au regard du RGPD — et une connexion réseau est économisée au chargement.

**Aucun traceur.** Le site n'installe ni cookie publicitaire, ni outil de mesure
d'audience. Le bouton « Refuser » de la bannière est donc pleinement effectif : il
correspond exactement à l'état par défaut. Le choix est mémorisé dans le `localStorage`
du navigateur sous la clé `nevie-global.consentement`, avec une validité de 180 jours,
conformément à ce qu'annonce la politique de confidentialité. Le lien « Gérer les
cookies » en pied de page permet de revenir sur son choix à tout moment.

**Icônes en sprite SVG inline.** Toutes les icônes sont définies une seule fois dans la
page, sans police d'icônes ni fichier externe : aucune requête supplémentaire et aucun
décalage de mise en page pendant le chargement.

**Performance.** Deux feuilles de style, un script en `defer`, aucune image bloquante,
préchargement des deux graisses visibles immédiatement. Le décalage cumulé de mise en
page (CLS) mesuré est de 0.

**Accessibilité.** Structure sémantique (`header`, `main`, `section`, `footer`), lien
d'évitement, libellés associés à chaque champ, messages d'erreur reliés au champ concerné,
anneau de focus visible, menu mobile pilotable au clavier (`Échap` referme), respect de la
préférence système « mouvement réduit ».

**Statuts des participations.** Les statuts sont affichés strictement selon le cahier des
charges : NEVIE-GLOBAL LIMITED est « Détenue », TECHNIFLOC-DIFFUSION est « En acquisition »
— les termes « filiale » et « détenue » ne lui sont jamais appliqués, et une mention
explicite précise que la société n'est à ce jour ni détenue, ni intégrée au périmètre du
groupe. Les quatre pôles annoncés sont marqués « À venir », sans société nommée.

---

## 6. Résultats mesurés

Audit Lighthouse en profil **mobile** sur la page d'accueil :

| Catégorie | Score |
|---|---|
| Performance | 98 |
| Accessibilité | 100 |
| Bonnes pratiques | 100 |
| SEO | 100 |

CLS 0 · TBT 20 ms · LCP 2,0 s (mesuré sur un serveur de test local sans compression ;
les scores de performance sont supérieurs sur un hébergement réel, où gzip/brotli et la
mise en cache des fichiers statiques sont actifs).

---

## 7. Compatibilité navigateurs

Chrome, Edge, Firefox, Safari (desktop et mobile), versions courantes et deux versions
antérieures. Le JavaScript est écrit en ES5 avec `fetch` et `IntersectionObserver` ;
en l'absence d'`IntersectionObserver`, les contenus s'affichent simplement sans animation.

---

## 8. Propriété intellectuelle

L'intégralité du code source, des contenus et de l'identité visuelle produits dans le
cadre de ce projet est cédée à NEVIE-GLOBAL SAS, sans réserve ni restriction d'usage.
