# NEVIE-GLOBAL SAS — Site institutionnel

Site institutionnel de la holding NEVIE-GLOBAL SAS (Nantes), en dix pages.

**HTML5 / CSS3 / JavaScript natif.** Aucun framework, aucune dépendance à installer,
aucune étape de compilation, aucune base de données. Le contenu du dépôt est le site :
il suffit de copier les fichiers sur un hébergement.

---

## Sommaire

1. [Contenu du dépôt](#1-contenu-du-dépôt)
2. [Mise en ligne](#2-mise-en-ligne)
3. [Connecter les formulaires à n8n](#3-connecter-les-formulaires-à-n8n) — **obligatoire**
4. [À compléter avant la mise en production](#4-à-compléter-avant-la-mise-en-production)
5. [Modifier le contenu](#5-modifier-le-contenu)
6. [Sécurité](#6-sécurité)
7. [Dépendances et licences](#7-dépendances-et-licences)
8. [Sauvegarde et restauration](#8-sauvegarde-et-restauration)
9. [Résultats mesurés](#9-résultats-mesurés)
10. [Périmètre livré et périmètre non livré](#10-périmètre-livré-et-périmètre-non-livré)
11. [Propriété intellectuelle](#11-propriété-intellectuelle)

---

## 1. Contenu du dépôt

### Les dix pages du site

| Fichier | Page |
|---|---|
| `index.html` | 1 — Accueil |
| `le-groupe.html` | 2 — Le Groupe |
| `notre-modele.html` | 3 — Notre Modèle |
| `gouvernance.html` | 4 — Gouvernance |
| `nos-entreprises.html` | 5 — Nos Entreprises / Participations |
| `croissance-acquisitions.html` | 6 — Croissance & Acquisitions |
| `ceder-son-entreprise.html` | 7 — Céder son entreprise (formulaire de cession) |
| `contact.html` | 8 — Contact (formulaire général) |
| `mentions-legales.html` | 9 — Mentions légales |
| `confidentialite-cookies.html` | 10 — Politique de confidentialité + Cookies |

`404.html` complète l'ensemble (page d'erreur, non indexée).

### Le reste

```
assets/
  css/fonts.css                     Déclarations @font-face (Poppins auto-hébergée)
  css/style.css                     Feuille de style unique, commentée, 20 sections
  js/main.js                        Navigation, formulaires, bandeau cookies
  fonts/*.woff2                     Poppins 300/400/500/600, sous-ensembles latin
  img/logo-nevie-global.png|.webp   Logo officiel, marge blanche détourée
  img/logo-nevie-global-original.jpg  Logo tel que transmis, intact
  img/favicon-96.png                Icône d'onglet
  img/og-nevie-global.jpg           Image d'aperçu pour les partages (1200 × 630)

deploiement/
  .htaccess                         Configuration Apache (en-têtes, cache, 404)
  nginx.conf                        Extrait de configuration Nginx
  _headers                          Format Netlify / Cloudflare Pages

outils/                             Outils de maintenance — NON nécessaires au site
  gabarits.py                       En-tête, pied de page et bandeau communs
  construire.py                     Régénère les onze pages
  entetes.py                        Régénère les fichiers de deploiement/

robots.txt   sitemap.xml
```

---

## 2. Mise en ligne

Le site est statique : **aucun serveur applicatif, aucun PHP, aucune base de données**.

1. Copier tout le dépôt à la racine web (`/www`, `/public_html` ou `/htdocs` selon l'hébergeur),
   **sauf** les dossiers `outils/` et `deploiement/`.
2. Déposer à la racine le fichier de configuration correspondant à l'hébergement :
   - Apache (OVH, o2switch, Ionos…) → `deploiement/.htaccess` renommé `.htaccess`
   - Netlify / Cloudflare Pages → `deploiement/_headers`
   - Nginx → inclure `deploiement/nginx.conf` dans le bloc `server{}`
3. Activer HTTPS, puis décommenter les redirections HTTPS et `www` dans `.htaccess`.
4. Vérifier que `index.html` est bien servi à la racine.

### Test en local

```
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000>. Un double-clic sur `index.html` fonctionne aussi,
mais les polices auto-hébergées ne se chargent qu'à travers un serveur.

---

## 3. Connecter les formulaires à n8n

**Sans cette étape, les deux formulaires affichent le message d'échec.** C'est
volontaire : le cahier des charges impose de ne jamais afficher de confirmation
sans accusé de réception réel. Tant qu'aucun webhook n'est renseigné, il n'y a
pas de réception — donc pas de confirmation.

### Étape 1 — renseigner les deux URL

Ouvrir `assets/js/main.js` et remplacer les deux premières valeurs :

```js
var CONFIG = {
  webhookCession: 'https://nevie-global.app.n8n.cloud/webhook/xxxxxxxx',
  webhookContact: 'https://nevie-global.app.n8n.cloud/webhook/yyyyyyyy',
  ...
```

### Étape 2 — régler le nœud Webhook dans n8n

Sur chacun des deux workflows :

| Réglage | Valeur |
|---|---|
| HTTP Method | `POST` |
| Respond | `Immediately` (ou `Using Respond to Webhook node`, en renvoyant un code 200) |
| Options → **Allowed Origins (CORS)** | `https://nevie-global.fr` (ajouter `https://www.nevie-global.fr` si le `www` est servi) |
| Options → **Binary Property** | à activer sur le workflow « cession », pour recevoir la pièce jointe |

> **Le réglage CORS est indispensable.** Sans en-tête `Access-Control-Allow-Origin`,
> le navigateur bloque la lecture de la réponse : le visiteur voit le message
> d'échec alors même que n8n a bien reçu les données. Le site ne peut pas faire
> autrement sans mentir au visiteur.

### Étape 3 — mettre à jour la politique de sécurité

Si le domaine n8n diffère de `https://nevie-global.app.n8n.cloud`, corriger
`DOMAINE_N8N` en haut de `outils/entetes.py`, puis relancer :

```
python3 outils/entetes.py
```

et redéployer le fichier de configuration. La CSP autorise explicitement ce seul
domaine en `connect-src` : un domaine non déclaré serait bloqué.

### Champs transmis

**Formulaire de cession** — `Nom et prénom`, `Fonction`, `Raison sociale`, `SIREN`,
`email`, `Téléphone`, `Localisation`, `Activité`, `Chiffre d'affaires`, `Effectif`,
`Motif de cession`, `Situation de l'entreprise`, `Message`, `piece_jointe` (fichier),
`Consentement — étude du dossier`, `Politique de confidentialité`, plus `origine`
(URL de la page) et `envoye_le` (horodatage ISO).

**Formulaire de contact** — `Nom et prénom`, `Société`, `email`, `Téléphone`,
`Sujet`, `Message`, `Consentement RGPD`, `origine`, `envoye_le`.

Le champ piège `_gotcha` n'est jamais transmis : s'il est rempli, l'envoi est
abandonné côté navigateur.

### Validation côté serveur

Le contrôle du fichier effectué par le site (extension `.pdf` / `.docx` / `.xlsx`,
10 Mo maximum) est un **confort pour le visiteur, pas une sécurité** : un navigateur
peut toujours envoyer autre chose. La validation qui fait foi doit être faite dans
le workflow n8n — vérification du type réel, de la taille, et filtrage anti-spam.
Un site statique ne peut pas garantir cette partie.

---

## 4. À compléter avant la mise en production

| Où | Quoi |
|---|---|
| `assets/js/main.js` | Les deux URL de webhook n8n (voir §3) |
| `mentions-legales.html` | Numéro **SIRET** (dès réception du Kbis définitif) |
| `mentions-legales.html` | **TVA intracommunautaire**, le cas échéant |
| `mentions-legales.html` | **Hébergeur** : raison sociale, adresse et téléphone — mention obligatoire |
| Toutes les pages, `robots.txt`, `sitemap.xml` | Le domaine définitif, si ce n'est pas `https://www.nevie-global.fr` |

Ces emplacements sont signalés dans le code par un commentaire `À COMPLÉTER`
et affichés entre crochets sur la page.

Le SIREN (993 888 841), la dénomination, le capital, le siège et le directeur de la
publication sont déjà renseignés.

### Ce qui n'est volontairement pas affiché

Aucune adresse e-mail ni numéro de téléphone n'apparaît sur le site : le dossier
n'en fournit aucun, et le cahier des charges interdit d'inventer une information.
La page Contact renvoie donc vers son formulaire et l'adresse postale du siège.
Pour afficher une adresse ou un téléphone, il suffit de les communiquer.

---

## 5. Modifier le contenu

### Modifier un texte

Ouvrir le fichier `.html` de la page concernée et modifier le texte entre les
balises. Aucun outil n'est nécessaire.

### Ajouter une entreprise au portefeuille

Dans `nos-entreprises.html`, dupliquer un bloc `<article class="carte fiche">`
et adapter le nom, le pôle, la description et les métadonnées. Le statut se
choisit avec l'une des trois classes de badge :

```html
<span class="badge badge--detenue">Détenue</span>
<span class="badge badge--acquisition">En acquisition</span>
<span class="badge badge--avenir">À venir</span>
```

Reporter ensuite l'aperçu sur `index.html`.

> **Attention au statut.** Une société en cours d'acquisition ne doit jamais être
> présentée comme une filiale ni comme détenue, tant que l'opération n'est pas
> juridiquement finalisée. Chaque fiche « en acquisition » porte une mention
> explicite en ce sens — la conserver.

### En-tête, pied de page et bandeau cookies

Ces trois blocs sont identiques sur les onze pages. Pour les modifier partout à la
fois sans risque d'oubli, éditer `outils/gabarits.py` puis lancer :

```
python3 outils/construire.py   # régénère les onze pages
python3 outils/entetes.py      # régénère deploiement/
```

Ces scripts n'utilisent que la bibliothèque standard de Python 3 — rien à installer.
Ils sont un confort de maintenance : **le site fonctionne sans eux**, et modifier
directement les fichiers `.html` reste parfaitement valable.

---

## 6. Sécurité

Les fichiers de `deploiement/` posent les en-têtes suivants :

| En-tête | Rôle |
|---|---|
| `Content-Security-Policy` | N'autorise que les ressources du site, plus le domaine n8n en `connect-src` et `form-action`. **Ni `unsafe-inline` pour les scripts, ni pour les styles** : le seul script en ligne (données structurées JSON-LD) est autorisé par son empreinte SHA-256. |
| `X-Content-Type-Options: nosniff` | Empêche le navigateur de deviner un type MIME |
| `X-Frame-Options` / `frame-ancestors` | Interdit l'inclusion du site dans une iframe (clickjacking) |
| `Referrer-Policy` | Limite les informations transmises aux sites tiers |
| `Permissions-Policy` | Désactive caméra, micro, géolocalisation, paiement, USB |
| `Strict-Transport-Security` | Impose HTTPS pendant un an |
| `Cross-Origin-Opener-Policy` / `-Resource-Policy` | Isole le site des autres origines |

Ces en-têtes ont été **vérifiés en conditions réelles** : le site a été servi avec
cette configuration exacte et les onze pages ont été chargées sans aucune violation
de CSP, polices et formulaires compris.

### Surface d'attaque

Le site étant purement statique, il n'y a **ni compte administrateur, ni page de
connexion, ni base de données, ni exécution de code côté serveur**. Les protections
contre la force brute, l'injection SQL ou la falsification de requête (CSRF) n'ont
donc pas d'objet ici : il n'existe aucun point d'entrée à protéger. La limitation
de débit et la validation serveur relèvent du workflow n8n, qui est le seul
composant à recevoir des données.

Aucun secret ne figure dans le dépôt. Les URL de webhook n8n ne sont pas des clés
d'API : elles ne donnent accès ni au tableau de bord n8n, ni aux données déjà reçues.

---

## 7. Dépendances et licences

**Aucune bibliothèque, aucun plugin, aucun thème, aucun paquet npm.** Le site
n'utilise ni jQuery, ni Bootstrap, ni Tailwind, ni police d'icônes.

| Ressource | Origine | Licence | Coût |
|---|---|---|---|
| Poppins (4 graisses, woff2) | Indian Type Foundry / Jonny Pinhorn | SIL Open Font License 1.1 — usage commercial autorisé, y compris auto-hébergé | Gratuit |
| Icônes | Dessinées pour ce projet, en SVG inline | Cédées à NEVIE-GLOBAL SAS | — |
| Logo | Fourni par NEVIE-GLOBAL SAS | Propriété de NEVIE-GLOBAL SAS | — |
| Image de partage, favicon | Produites pour ce projet à partir du logo fourni | Cédées à NEVIE-GLOBAL SAS | — |

**Aucune image de banque d'images n'est utilisée**, donc aucune licence à renouveler
et aucun risque de réclamation. Les halos et la grille de fond du hero sont des
dégradés CSS, pas des fichiers.

### Services tiers

| Service | Rôle | Conséquence d'un changement |
|---|---|---|
| n8n (existant, propriété NEVIE-GLOBAL) | Réception des formulaires | Remplacer les deux URL dans `assets/js/main.js` et le domaine dans `outils/entetes.py`, puis régénérer les en-têtes |
| Hébergement statique | Diffusion des fichiers | Recopier les fichiers ailleurs et redéployer la configuration correspondante |

Aucun autre service tiers n'est appelé. En particulier : **pas de Google Fonts,
pas de Google Analytics, pas de CDN, pas de bouton de réseau social.** Aucune donnée
de visiteur ne quitte le site.

---

## 8. Sauvegarde et restauration

Le site ne produisant aucune donnée (ni base, ni fichier téléversé, ni contenu
éditable en ligne), **la sauvegarde du site est le dépôt Git lui-même**. Chaque
version est datée et restaurable.

**Restauration complète — testée :**

```
git clone <url-du-dépôt> nevie-global
cd nevie-global
python3 -m http.server 8000        # vérification locale
# puis copier les fichiers sur l'hébergement
```

Pour revenir à une version antérieure :

```
git log --oneline                  # repérer la version voulue
git checkout <identifiant> -- .    # restaurer les fichiers
```

Les **dossiers de cession reçus** ne transitent pas par le site : ils sont traités
et conservés par le workflow n8n. Leur sauvegarde relève donc de n8n, pas de
l'hébergement du site.

---

## 9. Résultats mesurés

Audit Lighthouse 12, profil **mobile**, sur les onze pages :

| Page | Performance | Accessibilité | Bonnes pratiques | SEO |
|---|---|---|---|---|
| Accueil | 99 | 100 | 100 | 100 |
| Le Groupe | 99 | 100 | 100 | 100 |
| Notre Modèle | 99 | 100 | 100 | 100 |
| Gouvernance | 99 | 100 | 100 | 100 |
| Nos Entreprises | 99 | 100 | 100 | 100 |
| Croissance & Acquisitions | 99 | 100 | 100 | 100 |
| Céder son entreprise | 99 | 100 | 100 | 100 |
| Contact | 99 | 100 | 100 | 100 |
| Mentions légales | 99 | 100 | 100 | 100 |
| Confidentialité & cookies | 99 | 100 | 100 | 100 |
| 404 | 99 | 100 | 100 | 69 |

**Core Web Vitals** — LCP 2,0 s · CLS 0 · TBT de 0 à 90 ms selon la page.

Le 69 en SEO de la page 404 est **volontaire** : elle porte `noindex`, ce que
Lighthouse compte comme un défaut alors que c'est le comportement attendu d'une
page d'erreur.

Ces mesures ont été prises sur un serveur de test local servant déjà les en-têtes de
sécurité de `deploiement/`, mais sans compression ni cache.
Avec la configuration de `deploiement/` (gzip/brotli + cache long sur les assets),
les scores de performance sont supérieurs en production.

### Accessibilité

Objectif WCAG 2.2 niveau AA. Contrastes vérifiés au calcul, pas à l'œil :

- couleur de lien portée à `#3E8BFF` — `#0A6CFF` ne mesurait que 3,93 à 4,31 pour 1
  sur les fonds sombres du site, sous le seuil de 4,5. Le bleu de la charte reste
  utilisé en aplat de bouton, où il porte du texte blanc ;
- texte discret porté à `#928A80` — au minimum 4,95 pour 1 sur les quatre fonds ;
- taille minimale portée à 12,16 px ;
- les liens insérés dans une phrase sont soulignés, pour ne pas reposer sur la seule
  couleur.

Structure sémantique, lien d'évitement, libellés associés à chaque champ, messages
d'erreur reliés au champ concerné, anneau de focus visible, menu mobile pilotable au
clavier (`Échap` referme), hiérarchie de titres continue, respect de la préférence
système « mouvement réduit ».

### Navigateurs

Chrome, Edge, Firefox, Safari (bureau et mobile), versions courantes et deux versions
antérieures. Le JavaScript est écrit en ES5 avec `fetch` et `IntersectionObserver` ;
en l'absence d'`IntersectionObserver`, les contenus s'affichent simplement sans
animation.

---

## 10. Périmètre livré et périmètre non livré

### Livré

Les dix pages et leurs contenus, la charte graphique, le logo officiel, les statuts
de participations, les deux formulaires connectables à n8n avec pièce jointe, le
bandeau cookies Accepter / Refuser / Personnaliser, le référencement technique
(titres, descriptions, canonique, Open Graph, données structurées, `sitemap.xml`,
`robots.txt`, page 404), les en-têtes de sécurité, la documentation et la cession
des droits.

### Non livré

**Le CMS dynamique décrit aux parties 5 et 14 du cahier des charges n'est pas
inclus** : interface d'administration, comptes et mots de passe, matrice de quatre
rôles, gestion des médias, consultation des formulaires reçus, base de données,
sauvegarde quotidienne indépendante avec sept jours de rétention.

Un tel back-office est une application à part entière — authentification, base de
données, hébergement applicatif, sauvegardes — et non un complément au site. Il
suppose aussi des frais récurrents (hébergement applicatif et base) qui n'existent
pas avec un site statique.

Ce qui s'en rapproche dans la présente livraison : ajouter ou modifier une
entreprise se fait en dupliquant un bloc HTML commenté prévu pour cela (voir §5).
C'est une modification de fichier, pas une saisie dans une interface — la
distinction est assumée et signalée.

---

## 11. Propriété intellectuelle

L'intégralité du code source, des contenus, des icônes et des visuels produits dans
le cadre de ce projet est cédée à **NEVIE-GLOBAL SAS**, sans réserve ni restriction
d'usage, après paiement final.

Aucune dépendance propriétaire, aucun composant sous licence restrictive, aucun
service tiers indispensable au fonctionnement du site en dehors de n8n, qui
appartient déjà à NEVIE-GLOBAL SAS.

Le prestataire ne conserve aucun accès actif après validation finale.
