#!/usr/bin/env python3
"""
Génère les onze pages HTML du site NEVIE-GLOBAL SAS.

Les textes proviennent intégralement du cahier des charges et du document
« Textes du site » fournis par NEVIE-GLOBAL SAS. Aucune information juridique,
financière, historique ou commerciale n'a été ajoutée.

Usage :  python3 outils/construire.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gabarits import page, DOMAINE  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ===========================================================================
# Données structurées : décrivent l'organisation aux moteurs de recherche.
# Elles ne reprennent que des informations fournies par le client.
# ===========================================================================
JSON_LD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "NEVIE-GLOBAL SAS",
    "legalName": "NEVIE-GLOBAL SAS",
    "url": "%s/",
    "logo": "%s/assets/img/logo-nevie-global.png",
    "description": "Holding entrepreneuriale française constituant progressivement un portefeuille diversifié d'entreprises par acquisitions et reprises.",
    "foundingLocation": { "@type": "Place", "name": "Nantes, France" },
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "2 Place Jean V, bureau 3",
      "postalCode": "44000",
      "addressLocality": "Nantes",
      "addressCountry": "FR"
    },
    "identifier": { "@type": "PropertyValue", "name": "SIREN", "value": "993888841" },
    "subOrganization": {
      "@type": "Organization",
      "name": "NEVIE-GLOBAL LIMITED",
      "url": "https://nevie-global.com/",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "61 Bridge Street",
        "addressLocality": "Kington",
        "postalCode": "HR5 3DJ",
        "addressCountry": "GB"
      }
    }
  }
  </script>
""" % (DOMAINE, DOMAINE)


# ===========================================================================
# PAGE 1 — ACCUEIL
# ===========================================================================
ACCUEIL = """
<!-- ===================== HERO ===================== -->
<section class="hero">
  <div class="hero__fond" aria-hidden="true"></div>
  <div class="hero__grille" aria-hidden="true"></div>

  <div class="conteneur">
    <div class="hero__contenu">
      <p class="eyebrow">Société holding — Nantes, France</p>

      <h1 class="hero__titre">
        Un groupe. Des entreprises.
        <span class="ligne-or">Une vision de <em>long terme</em>.</span>
      </h1>

      <p class="hero__chapo">
        NEVIE-GLOBAL construit progressivement un portefeuille diversifié d'entreprises
        indépendantes dans l'industrie, les services, la technologie et l'artisanat.
      </p>

      <div class="hero__actions">
        <a class="btn btn--primaire" href="le-groupe.html">
          Découvrir le groupe
          <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
        </a>
        <a class="btn btn--secondaire" href="ceder-son-entreprise.html">Vous cédez votre entreprise&nbsp;?</a>
      </div>
    </div>

    <!-- Repères : simple décompte de ce qui figure dans la page « Nos entreprises ».
         Aucun chiffre d'affaires, aucune donnée financière n'est avancée. -->
    <ul class="hero__reperes">
      <li class="repere">
        <span class="repere__val">1</span>
        <span class="repere__lib">Filiale détenue</span>
      </li>
      <li class="repere">
        <span class="repere__val">1</span>
        <span class="repere__lib">Acquisition en cours</span>
      </li>
      <li class="repere">
        <span class="repere__val">4</span>
        <span class="repere__lib">Pôles à venir</span>
      </li>
      <li class="repere">
        <span class="repere__val">FR&nbsp;·&nbsp;UK</span>
        <span class="repere__lib">Implantations</span>
      </li>
    </ul>
  </div>
</section>

<!-- ===================== LE GROUPE (résumé) ===================== -->
<section class="section section--alt">
  <div class="conteneur">
    <div class="groupe__grille">

      <div class="groupe__texte reveal">
        <p class="eyebrow">Le groupe</p>
        <h2 class="u-titre-2">Une holding entrepreneuriale française</h2>
        <p class="u-mt-s">
          <strong>NEVIE-GLOBAL SAS</strong> est une holding entrepreneuriale française qui identifie,
          reprend et accompagne des entreprises dans des secteurs volontairement diversifiés.
          Notre approche privilégie la continuité&nbsp;: chaque entreprise qui rejoint le groupe
          conserve son nom, son identité et son savoir-faire.
        </p>

        <ul class="liste-marquee">
          <li>Une holding de gouvernance, de stratégie et d'acquisitions.</li>
          <li>Des entreprises qui gardent leur nom et leur autonomie opérationnelle.</li>
          <li>Une construction progressive, pôle après pôle.</li>
        </ul>

        <p class="u-mt-l">
          <a class="lien-fleche" href="le-groupe.html">
            En savoir plus sur le groupe
            <svg class="ico" aria-hidden="true"><use href="#i-fleche-droite"></use></svg>
          </a>
        </p>
      </div>

      <!-- Gouvernance : résumé, la page dédiée donne le détail -->
      <div class="reveal">
        <p class="eyebrow">Gouvernance</p>
        <div class="gouvernance">

          <article class="carte dirigeant">
            <span class="dirigeant__initiales" aria-hidden="true">EV</span>
            <div>
              <h3 class="dirigeant__nom">Elisa Varinot</h3>
              <p class="dirigeant__role">Présidente — co-fondatrice</p>
            </div>
          </article>

          <article class="carte dirigeant">
            <span class="dirigeant__initiales" aria-hidden="true">EV</span>
            <div>
              <h3 class="dirigeant__nom">Emmanuel Varinot</h3>
              <p class="dirigeant__role">Directeur Général — co-fondateur</p>
            </div>
          </article>

          <dl class="carte encart-siege">
            <dt>Siège social</dt>
            <dd>2 Place Jean V, bureau 3<br>44000 Nantes, France</dd>
            <dt>Forme juridique</dt>
            <dd>Société par actions simplifiée (SAS)</dd>
          </dl>

        </div>

        <p class="u-mt-m">
          <a class="lien-fleche" href="gouvernance.html">
            Voir la gouvernance
            <svg class="ico" aria-hidden="true"><use href="#i-fleche-droite"></use></svg>
          </a>
        </p>
      </div>

    </div>
  </div>
</section>

<!-- ===================== PORTEFEUILLE (aperçu) ===================== -->
<section class="section">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Portefeuille</p>
      <h2>Nos entreprises</h2>
      <p class="chapo">
        Le portefeuille se construit pôle par pôle. Le statut de chaque société est
        indiqué sans ambiguïté&nbsp;: détenue, en cours d'acquisition, ou pôle annoncé.
      </p>
    </div>

    <div class="poles">
      <div class="poles__nommes">

        <article class="carte entite reveal">
          <div class="entite__tete">
            <div>
              <p class="entite__pole">Pôle Technologie</p>
              <h3 class="entite__nom">NEVIE-GLOBAL LIMITED</h3>
            </div>
            <span class="badge badge--detenue">Détenue</span>
          </div>
          <p class="entite__desc">
            Filiale technologique du groupe, basée au Royaume-Uni.
            IA, automatisation, wearables premium, blockchain.
          </p>
          <div class="entite__pied">
            <a class="lien-fleche" href="https://nevie-global.com" target="_blank" rel="noopener noreferrer">
              Visiter le site
              <svg class="ico" aria-hidden="true"><use href="#i-externe"></use></svg>
              <span class="sr-only">(nouvelle fenêtre)</span>
            </a>
          </div>
        </article>

        <article class="carte entite entite--acquisition reveal">
          <div class="entite__tete">
            <div>
              <p class="entite__pole">Pôle Textile / Industrie</p>
              <h3 class="entite__nom">TECHNIFLOC-DIFFUSION</h3>
            </div>
            <span class="badge badge--acquisition">En acquisition</span>
          </div>
          <p class="entite__desc">
            Entreprise spécialisée dans le flocage et l'ennoblissement textile, basée à Issoudun.
            Acquisition en cours par NEVIE-GLOBAL SAS.
          </p>
          <div class="entite__pied">
            <!-- Statut : mention explicite, conformément au cahier des charges. -->
            <p class="entite__note">
              Opération en cours&nbsp;: l'entreprise n'est à ce jour ni détenue,
              ni intégrée au périmètre du groupe.
            </p>
          </div>
        </article>

      </div>

      <div class="carte avenir reveal">
        <div class="avenir__tete">
          <h3 class="avenir__titre">Pôles à venir</h3>
          <span class="badge badge--avenir">À venir</span>
        </div>
        <ul class="avenir__liste">
          <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-usine"></use></svg>Fonderie</li>
          <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-feuille"></use></svg>Pompes funèbres</li>
          <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-voiture"></use></svg>Garage automobile</li>
          <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-outils"></use></svg>Mécanique générale</li>
        </ul>
        <p class="avenir__note">
          Pôles annoncés, sans société nommée à ce stade. D'autres secteurs pourront
          s'ajouter au fil de nos acquisitions.
        </p>
      </div>
    </div>

    <p class="u-mt-xl" class="reveal">
      <a class="btn btn--secondaire" href="nos-entreprises.html">
        Voir toutes nos entreprises
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </p>

  </div>
</section>

<!-- ===================== STRATÉGIE DE CROISSANCE ===================== -->
<section class="section section--alt">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Croissance &amp; acquisitions</p>
      <h2>Se développer par la reprise d'entreprises</h2>
      <p class="chapo">
        NEVIE-GLOBAL se développe par croissance organique et par acquisitions d'entreprises —
        reprises classiques, reprises progressives, ou opérations à prix symbolique selon le
        contexte de transmission.
      </p>
    </div>

    <div class="croissance__grille">

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-loupe"></use></svg></div>
        <h3 class="axe__titre">Sourcing et analyse</h3>
        <p class="axe__desc">
          Identification par sourcing direct, réseaux professionnels et plateformes
          spécialisées, puis analyse de l'activité, du marché et du contexte de transmission.
        </p>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-poignee"></use></svg></div>
        <h3 class="axe__titre">Modalités de reprise</h3>
        <p class="axe__desc">
          Acquisition classique, reprise progressive, crédit-vendeur, prix symbolique dans
          certains contextes, ou opérations liées à des procédures judiciaires.
        </p>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-horloge"></use></svg></div>
        <h3 class="axe__titre">Logique de portefeuille</h3>
        <p class="axe__desc">
          Une logique de long terme, pas de court terme. Les secteurs peuvent être différents&nbsp;;
          il n'existe pas nécessairement de synergie commerciale entre les entreprises.
        </p>
      </article>

    </div>

    <!-- Appel à l'action « Céder son entreprise » -->
    <div class="bande-cta reveal">
      <div>
        <h3>Vous envisagez de céder votre entreprise&nbsp;?</h3>
        <p>
          Nous étudions les opportunités de reprise dans différents secteurs et situations.
        </p>
      </div>
      <a class="btn btn--or" href="ceder-son-entreprise.html">
        Présenter mon entreprise
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>

  </div>
</section>

<!-- ===================== CONTACT (résumé) ===================== -->
<section class="section">
  <div class="conteneur">
    <div class="suite reveal">
      <div>
        <p class="suite__lib">Contact</p>
        <p class="suite__titre">Une question sur NEVIE-GLOBAL ou son portefeuille&nbsp;?</p>
      </div>
      <a class="btn btn--primaire" href="contact.html">
        Contactez-nous
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>
  </div>
</section>
"""


# ===========================================================================
# PAGE 2 — LE GROUPE
# ===========================================================================
LE_GROUPE = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Le Groupe</span>
    </nav>
    <h1>Le Groupe</h1>
    <p class="page-hero__chapo">
      Une holding entrepreneuriale construisant progressivement un portefeuille
      diversifié d'entreprises.
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="groupe__grille">

      <div class="groupe__texte reveal">
        <p class="eyebrow">Notre histoire</p>
        <h2 class="u-titre-2">Fondée à Nantes</h2>
        <p class="u-mt-s">
          NEVIE-GLOBAL SAS a été fondée à Nantes par <strong>Elisa et Emmanuel Varinot</strong>,
          avec la volonté de bâtir un groupe industriel diversifié capable de reprendre et
          développer des entreprises françaises dans la durée.
        </p>

        <p class="eyebrow u-mt-xxl" >Notre vision</p>
        <p>
          Nous considérons chaque entreprise comme une réalité propre, avec son histoire,
          ses équipes, ses savoir-faire et ses enjeux. Notre ambition est de construire
          progressivement un groupe diversifié capable d'accompagner durablement les
          entreprises qui rejoignent son portefeuille.
        </p>
      </div>

      <div class="reveal">
        <p class="eyebrow">Gouvernance</p>
        <div class="gouvernance">

          <article class="carte dirigeant">
            <span class="dirigeant__initiales" aria-hidden="true">EV</span>
            <div>
              <h3 class="dirigeant__nom">Elisa Varinot</h3>
              <p class="dirigeant__role">Présidente</p>
            </div>
          </article>

          <article class="carte dirigeant">
            <span class="dirigeant__initiales" aria-hidden="true">EV</span>
            <div>
              <h3 class="dirigeant__nom">Emmanuel Varinot</h3>
              <p class="dirigeant__role">Directeur Général, co-fondateur</p>
            </div>
          </article>

        </div>
        <p class="u-mt-m">
          <a class="lien-fleche" href="gouvernance.html">
            Rôles et approche de gouvernance
            <svg class="ico" aria-hidden="true"><use href="#i-fleche-droite"></use></svg>
          </a>
        </p>
      </div>

    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Notre philosophie</p>
      <h2>Quatre principes de conduite</h2>
    </div>

    <div class="philo">

      <article class="carte philo__item reveal">
        <div class="philo__ico"><svg class="ico" aria-hidden="true"><use href="#i-boussole"></use></svg></div>
        <h3 class="philo__titre">Entrepreneurial</h3>
        <p class="philo__desc">Des décisions pragmatiques et orientées vers l'action.</p>
      </article>

      <article class="carte philo__item reveal">
        <div class="philo__ico"><svg class="ico" aria-hidden="true"><use href="#i-horloge"></use></svg></div>
        <h3 class="philo__titre">Long terme</h3>
        <p class="philo__desc">
          Une approche privilégiant la construction progressive plutôt que la logique
          de court terme.
        </p>
      </article>

      <article class="carte philo__item reveal">
        <div class="philo__ico"><svg class="ico" aria-hidden="true"><use href="#i-couches"></use></svg></div>
        <h3 class="philo__titre">Diversification</h3>
        <p class="philo__desc">
          Des entreprises et secteurs différents au sein d'un portefeuille
          volontairement diversifié.
        </p>
      </article>

      <article class="carte philo__item reveal">
        <div class="philo__ico"><svg class="ico" aria-hidden="true"><use href="#i-bouclier"></use></svg></div>
        <h3 class="philo__titre">Continuité</h3>
        <p class="philo__desc">
          Préserver les savoir-faire, les équipes et les identités lorsque cela est pertinent.
        </p>
      </article>

    </div>

  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="suite reveal">
      <div>
        <p class="suite__lib">Page suivante</p>
        <p class="suite__titre">Notre Modèle — acquérir, structurer, développer</p>
      </div>
      <a class="btn btn--primaire" href="notre-modele.html">
        Découvrir le modèle
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>
  </div>
</section>
"""


# ===========================================================================
# PAGE 3 — NOTRE MODÈLE
# ===========================================================================
ETAPES = [
    ("01", "Sourcing", "i-loupe",
     "Nous identifions des entreprises susceptibles de rejoindre le groupe par sourcing "
     "direct, réseaux professionnels et plateformes spécialisées."),
    ("02", "Analyse", "i-graphique",
     "Nous évaluons l'activité, le marché, la situation financière, l'effectif, les actifs, "
     "le dirigeant, le contexte de transmission et le potentiel de développement."),
    ("03", "Reprise", "i-poignee",
     "Selon la situation : acquisition classique, reprise progressive, crédit-vendeur, prix "
     "symbolique dans certains contextes, ou opérations liées à des procédures judiciaires."),
    ("04", "Intégration", "i-couches",
     "L'entreprise conserve son nom, son identité, son expertise et son fonctionnement "
     "opérationnel. L'intégration est progressive."),
    ("05", "Gouvernance", "i-engrenage",
     "Mutualisation possible du pilotage, de la gestion, de la structuration et des fonctions "
     "support, selon les besoins de chaque entreprise."),
    ("06", "Développement", "i-graphique",
     "Consolider, structurer, moderniser, développer, accompagner."),
    ("07", "Long terme", "i-horloge",
     "Une logique de portefeuille, pas une logique de court terme. Les secteurs de nos "
     "entreprises peuvent être différents ; il n'existe pas nécessairement de synergie "
     "commerciale entre elles."),
]


def _etapes_html():
    blocs = []
    for numero, titre, _ico, desc in ETAPES:
        blocs.append(f"""      <li class="etape reveal">
        <span class="etape__num" aria-hidden="true">{numero}</span>
        <h2 class="etape__titre">{titre}</h2>
        <p class="etape__desc">{desc}</p>
      </li>""")
    return "\n".join(blocs)


NOTRE_MODELE = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Notre Modèle</span>
    </nav>
    <h1>Acquérir. Structurer. Développer.</h1>
    <p class="page-hero__chapo">
      Une approche de reprise adaptée à chaque situation, du premier contact
      au développement dans la durée.
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">

    <ol class="modele__etapes">
__ETAPES__
    </ol>

    <div class="modele__synthese reveal">
      <span class="ico-bloc" aria-hidden="true">
        <svg class="ico" width="20" height="20"><use href="#i-couches"></use></svg>
      </span>
      <p>
        Chaque entreprise reprise conserve son nom, son identité et son savoir-faire.
        La holding apporte la gouvernance, la structuration et les moyens de développement —
        elle ne se substitue pas à l'entreprise.
      </p>
    </div>

  </div>
</section>

<section class="section section--alt">
  <div class="conteneur">
    <div class="suite reveal">
      <div>
        <p class="suite__lib">Page suivante</p>
        <p class="suite__titre">Nos entreprises et participations</p>
      </div>
      <a class="btn btn--primaire" href="nos-entreprises.html">
        Voir le portefeuille
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>
  </div>
</section>
""".replace("__ETAPES__", _etapes_html())


# ===========================================================================
# PAGE 4 — GOUVERNANCE
# ===========================================================================
GOUVERNANCE = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Gouvernance</span>
    </nav>
    <h1>Gouvernance</h1>
    <p class="page-hero__chapo">
      Une direction resserrée, une gouvernance claire.
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">

    <!-- Cartes en version texte seule : aucune photo n'est fournie et aucun
         emplacement n'est réservé pour en accueillir une (cf. cahier des charges). -->
    <div class="direction">

      <article class="carte direction__carte reveal">
        <p class="direction__role">Présidente</p>
        <h2 class="direction__nom">Elisa Varinot</h2>
        <p class="direction__texte">
          Co-fondatrice de NEVIE-GLOBAL SAS.
        </p>
      </article>

      <article class="carte direction__carte reveal">
        <p class="direction__role">Directeur Général</p>
        <h2 class="direction__nom">Emmanuel Varinot</h2>
        <p class="direction__texte">
          Co-fondateur de NEVIE-GLOBAL SAS. 20 ans d'expérience en opérations industrielles
          (agroalimentaire, ferroviaire, aéronautique, plasturgie).
        </p>
      </article>

    </div>

  </div>
</section>

<section class="section section--alt">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Notre approche</p>
      <h2>Trois principes de gouvernance</h2>
    </div>

    <div class="croissance__grille">

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-boussole"></use></svg></div>
        <h3 class="axe__titre">Entrepreneuriale</h3>
        <p class="axe__desc">Décisions rapides et pragmatiques.</p>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-couches"></use></svg></div>
        <h3 class="axe__titre">Décentralisée</h3>
        <p class="axe__desc">Les entreprises conservent leur identité et leur expertise.</p>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-utilisateurs"></use></svg></div>
        <h3 class="axe__titre">Responsable</h3>
        <p class="axe__desc">
          Une attention particulière portée aux équipes et à la continuité des entreprises.
        </p>
      </article>

    </div>

    <div class="carte encart-siege reveal u-mt-xl u-max-520" >
      <dl class="u-m-0">
        <dt>Siège social</dt>
        <dd>2 Place Jean V, bureau 3 — 44000 Nantes, France</dd>
        <dt>Forme juridique</dt>
        <dd>Société par actions simplifiée (SAS)</dd>
        <dt>Directeur de la publication</dt>
        <dd>Emmanuel Varinot, Directeur Général</dd>
      </dl>
    </div>

  </div>
</section>
"""


# ===========================================================================
# PAGE 5 — NOS ENTREPRISES / PARTICIPATIONS
# ===========================================================================
NOS_ENTREPRISES = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Nos Entreprises</span>
    </nav>
    <h1>Nos entreprises</h1>
    <p class="page-hero__chapo">
      Découvrez les entreprises détenues, en cours d'acquisition et les pôles à venir du groupe.
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">

    <!-- ---------- Pôle Technologie ---------- -->
    <div class="section-tete reveal u-mb-l" >
      <p class="eyebrow">Pôle Technologie</p>
      <h2 class="u-titre-3">Entreprise détenue</h2>
    </div>

    <article class="carte fiche reveal">
      <div class="fiche__tete">
        <div>
          <p class="fiche__pole">Pôle Technologie</p>
          <h3 class="fiche__nom">NEVIE-GLOBAL LIMITED</h3>
        </div>
        <span class="badge badge--detenue">Détenue</span>
      </div>

      <p class="fiche__desc">
        Filiale technologique du groupe, basée au Royaume-Uni.
        IA, automatisation, wearables premium, blockchain.
      </p>

      <dl class="fiche__meta">
        <div><dt>Pôle</dt><dd>Technologie</dd></div>
        <div><dt>Statut</dt><dd>Détenue</dd></div>
        <div><dt>Localisation</dt><dd>Kington, Royaume-Uni</dd></div>
        <div><dt>Site internet</dt><dd>nevie-global.com</dd></div>
      </dl>

      <!-- Les activités opérationnelles restent au niveau de la filiale : elles sont
           renvoyées vers son propre site, jamais présentées comme celles de la holding. -->
      <div class="fiche__pied">
        <a class="btn btn--secondaire" href="https://nevie-global.com" target="_blank" rel="noopener noreferrer">
          Visiter le site
          <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-externe"></use></svg>
          <span class="sr-only">(nouvelle fenêtre)</span>
        </a>
        <p class="entite__note">
          Les offres, produits et technologies de NEVIE-GLOBAL LIMITED sont présentés
          exclusivement sur son propre site.
        </p>
      </div>
    </article>

    <!-- ---------- Pôle Textile / Industrie ---------- -->
    <div class="section-tete reveal u-bloc-suivant" >
      <p class="eyebrow">Pôle Textile / Industrie</p>
      <h2 class="u-titre-3">Acquisition en cours</h2>
    </div>

    <article class="carte fiche fiche--acquisition reveal">
      <div class="fiche__tete">
        <div>
          <p class="fiche__pole">Pôle Textile / Industrie</p>
          <h3 class="fiche__nom">TECHNIFLOC-DIFFUSION</h3>
        </div>
        <span class="badge badge--acquisition">En acquisition</span>
      </div>

      <p class="fiche__desc">
        Entreprise spécialisée dans le flocage et l'ennoblissement textile, basée à Issoudun.
        Acquisition en cours par NEVIE-GLOBAL SAS.
      </p>

      <dl class="fiche__meta">
        <div><dt>Pôle</dt><dd>Textile / Industrie</dd></div>
        <div><dt>Statut</dt><dd>En cours d'acquisition</dd></div>
        <div><dt>Localisation</dt><dd>Issoudun, France</dd></div>
        <div><dt>Activité</dt><dd>Flocage et ennoblissement textile</dd></div>
      </dl>

      <div class="fiche__pied">
        <!-- Mention imposée par le cahier des charges : tant que l'opération n'est pas
             juridiquement finalisée, l'entreprise n'est ni une filiale, ni détenue. -->
        <p class="entite__note">
          Opération en cours&nbsp;: l'entreprise n'est à ce jour ni détenue, ni intégrée
          au périmètre du groupe. Le statut sera mis à jour lorsque l'acquisition sera
          juridiquement finalisée.
        </p>
      </div>
    </article>

    <!-- ---------- Pôles à venir ---------- -->
    <div class="section-tete reveal u-bloc-suivant" >
      <p class="eyebrow">Pôles à venir</p>
      <h2 class="u-titre-3">Secteurs identifiés, sans société nommée</h2>
    </div>

    <div class="carte avenir reveal">
      <div class="avenir__tete">
        <h3 class="avenir__titre">Quatre pôles annoncés</h3>
        <span class="badge badge--avenir">À venir</span>
      </div>
      <ul class="avenir__liste">
        <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-usine"></use></svg>Fonderie — Industrie</li>
        <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-feuille"></use></svg>Pompes funèbres — Services</li>
        <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-voiture"></use></svg>Garage automobile — Automobile</li>
        <li class="avenir__item"><svg class="ico" aria-hidden="true"><use href="#i-outils"></use></svg>Mécanique générale — Industrie</li>
      </ul>
      <p class="avenir__note">
        Aucune fiche détaillée n'est publiée tant qu'aucune société n'est nommée.
        D'autres secteurs pourront s'ajouter au fil de nos acquisitions.
      </p>
    </div>

  </div>
</section>

<section class="section section--alt">
  <div class="conteneur">
    <div class="bande-cta reveal u-mt-0" >
      <div>
        <h3>Votre entreprise pourrait rejoindre l'un de ces pôles</h3>
        <p>
          Nous étudions les opportunités de reprise dans différents secteurs et situations.
        </p>
      </div>
      <a class="btn btn--or" href="ceder-son-entreprise.html">
        Présenter mon entreprise
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>
  </div>
</section>
"""


# ===========================================================================
# PAGE 6 — CROISSANCE & ACQUISITIONS
# ===========================================================================
CROISSANCE = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Croissance &amp; Acquisitions</span>
    </nav>
    <h1>Une stratégie de développement par acquisitions</h1>
    <p class="page-hero__chapo">
      NEVIE-GLOBAL développe son portefeuille par croissance organique, mais également par
      acquisitions et reprises d'entreprises. Cette dimension est au cœur de notre stratégie.
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">

    <div class="ceder__grille">

      <div class="reveal">
        <div class="critere-bloc">
          <h2>Ce que nous recherchons</h2>
          <ul class="puces">
            <li>Entreprises avec un potentiel de continuité, de transformation ou de développement.</li>
            <li>Secteurs : industrie, technologie, artisanat, services.</li>
            <li>
              Situations variées : transmission classique, départ en retraite, reprise progressive,
              procédures judiciaires.
            </li>
          </ul>
        </div>

        <div class="critere-bloc">
          <h2>Notre approche</h2>
          <p class="u-texte-doux">
            Nous privilégions une entrée progressive dans les entreprises que nous reprenons,
            en nous adaptant à chaque situation plutôt qu'en imposant un schéma unique.
          </p>
        </div>

        <p class="avertissement">
          Chaque dossier est étudié au cas par cas. Aucun prix, aucun délai et aucune reprise
          ne sont garantis à ce stade.
        </p>
      </div>

      <div class="reveal">
        <div class="croissance__grille u-une-colonne" >

          <article class="carte axe">
            <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-cible"></use></svg></div>
            <h3 class="axe__titre">Secteurs étudiés</h3>
            <div class="etiquettes">
              <span class="etiquette">Industrie</span>
              <span class="etiquette">Technologie</span>
              <span class="etiquette">Artisanat</span>
              <span class="etiquette">Services</span>
            </div>
          </article>

          <article class="carte axe">
            <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-poignee"></use></svg></div>
            <h3 class="axe__titre">Modalités envisagées</h3>
            <div class="etiquettes">
              <span class="etiquette">Acquisition classique</span>
              <span class="etiquette">Reprise progressive</span>
              <span class="etiquette">Crédit-vendeur</span>
              <span class="etiquette">Prix symbolique</span>
              <span class="etiquette">Procédures judiciaires</span>
            </div>
          </article>

        </div>
      </div>

    </div>

    <div class="bande-cta reveal">
      <div>
        <h3>Vous envisagez de céder votre entreprise&nbsp;?</h3>
        <p>Présentez-nous votre dossier : nous l'étudions et revenons vers vous.</p>
      </div>
      <a class="btn btn--or" href="ceder-son-entreprise.html">
        Présenter mon entreprise
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>

  </div>
</section>
"""


# ===========================================================================
# PAGE 7 — CÉDER SON ENTREPRISE (avec le formulaire de cession)
# ===========================================================================
CEDER = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Céder son entreprise</span>
    </nav>
    <h1>Vous envisagez de céder votre entreprise&nbsp;?</h1>
    <p class="page-hero__chapo">
      Nous étudions les opportunités de reprise progressive, les transmissions classiques
      et certaines situations particulières.
    </p>
    <div class="page-hero__actions">
      <a class="btn btn--primaire" href="#formulaire">
        Présenter mon entreprise
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Ce que nous étudions</p>
      <h2>Secteurs, zones et situations</h2>
    </div>

    <div class="croissance__grille">

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-cible"></use></svg></div>
        <h3 class="axe__titre">Secteurs</h3>
        <p class="axe__desc">Industrie, Technologie, Artisanat, Services, et autres secteurs selon opportunités.</p>
        <div class="etiquettes">
          <span class="etiquette">Industrie</span>
          <span class="etiquette">Technologie</span>
          <span class="etiquette">Artisanat</span>
          <span class="etiquette">Services</span>
        </div>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-globe"></use></svg></div>
        <h3 class="axe__titre">Zone géographique</h3>
        <p class="axe__desc">
          France (hors Île-de-France et régions trop au sud en priorité), ainsi que Belgique,
          Suisse, Canada-Québec, Allemagne.
        </p>
      </article>

      <article class="carte axe reveal">
        <div class="axe__ico"><svg class="ico" aria-hidden="true"><use href="#i-document"></use></svg></div>
        <h3 class="axe__titre">Situations étudiées</h3>
        <div class="etiquettes">
          <span class="etiquette">Départ à la retraite</span>
          <span class="etiquette">Cession classique</span>
          <span class="etiquette">Reprise progressive</span>
          <span class="etiquette">Difficultés</span>
          <span class="etiquette">Sauvegarde</span>
          <span class="etiquette">Redressement judiciaire</span>
          <span class="etiquette">Liquidation judiciaire</span>
          <span class="etiquette">Autres à étudier</span>
        </div>
      </article>

    </div>

  </div>
</section>

<section class="section section--alt">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Notre processus</p>
      <h2>Six étapes, sans engagement</h2>
    </div>

    <ol class="parcours reveal">
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">1</span>
        <div>
          <h3 class="parcours__titre">Vous nous présentez votre entreprise</h3>
          <p class="parcours__desc">Via le formulaire ci-dessous, en quelques minutes.</p>
        </div>
      </li>
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">2</span>
        <div>
          <h3 class="parcours__titre">Nous analysons votre dossier</h3>
          <p class="parcours__desc">Activité, marché, situation, contexte de transmission.</p>
        </div>
      </li>
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">3</span>
        <div>
          <h3 class="parcours__titre">Nous échangeons avec vous</h3>
          <p class="parcours__desc">Un premier échange pour comprendre votre projet.</p>
        </div>
      </li>
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">4</span>
        <div>
          <h3 class="parcours__titre">Nous approfondissons lorsque le dossier est pertinent</h3>
          <p class="parcours__desc">Analyse détaillée et rencontre.</p>
        </div>
      </li>
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">5</span>
        <div>
          <h3 class="parcours__titre">Nous étudions une solution de reprise adaptée</h3>
          <p class="parcours__desc">Le montage est construit à partir de votre situation.</p>
        </div>
      </li>
      <li class="parcours__etape">
        <span class="parcours__num" aria-hidden="true">6</span>
        <div>
          <h3 class="parcours__titre">Les modalités sont définies au cas par cas</h3>
          <p class="parcours__desc">Aucun schéma unique n'est imposé.</p>
        </div>
      </li>
    </ol>

    <p class="avertissement reveal u-max-70" >
      Votre dossier est étudié après réception des informations nécessaires.
      Aucun délai ni prix n'est promis à ce stade, et aucune reprise n'est garantie.
    </p>

  </div>
</section>

<!-- ===================== FORMULAIRE DE CESSION ===================== -->
<section class="section" id="formulaire">
  <div class="conteneur">

    <div class="section-tete reveal">
      <p class="eyebrow">Formulaire</p>
      <h2>Présenter mon entreprise</h2>
      <p class="chapo">
        Les champs marqués d'un astérisque sont obligatoires. Vous pouvez joindre un
        document de présentation si vous en disposez.
      </p>
    </div>

    <div class="carte form-bloc reveal">
      <form id="form-cession" novalidate>
        <div class="form-grille">

          <!-- Piège à robots : invisible pour un humain, souvent rempli par un script.
               Le formulaire s'interrompt alors sans rien transmettre. -->
          <div class="pot-de-miel" aria-hidden="true">
            <label for="cession-site">Ne pas remplir</label>
            <input type="text" id="cession-site" name="_gotcha" tabindex="-1" autocomplete="off">
          </div>

          <div class="champ">
            <label for="cession-nom">Nom et prénom <span class="requis" aria-hidden="true">*</span></label>
            <input type="text" id="cession-nom" name="Nom et prénom" autocomplete="name" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-fonction">Fonction <span class="requis" aria-hidden="true">*</span></label>
            <input type="text" id="cession-fonction" name="Fonction" autocomplete="organization-title"
                   placeholder="Dirigeant, associé…" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-societe">Raison sociale <span class="requis" aria-hidden="true">*</span></label>
            <input type="text" id="cession-societe" name="Raison sociale" autocomplete="organization" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-siren">SIREN</label>
            <input type="text" id="cession-siren" name="SIREN" inputmode="numeric" placeholder="9 chiffres">
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-email">Adresse e-mail <span class="requis" aria-hidden="true">*</span></label>
            <input type="email" id="cession-email" name="email" autocomplete="email" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-tel">Téléphone <span class="requis" aria-hidden="true">*</span></label>
            <input type="tel" id="cession-tel" name="Téléphone" autocomplete="tel" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-lieu">Localisation <span class="requis" aria-hidden="true">*</span></label>
            <input type="text" id="cession-lieu" name="Localisation" placeholder="Ville, département ou pays" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-activite">Activité <span class="requis" aria-hidden="true">*</span></label>
            <input type="text" id="cession-activite" name="Activité" placeholder="Secteur, métier principal" required>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-ca">Chiffre d'affaires annuel</label>
            <input type="text" id="cession-ca" name="Chiffre d'affaires" placeholder="Ordre de grandeur, en euros">
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-effectif">Effectif</label>
            <input type="text" id="cession-effectif" name="Effectif" placeholder="Nombre de salariés">
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-motif">Motif de cession <span class="requis" aria-hidden="true">*</span></label>
            <select id="cession-motif" name="Motif de cession" required>
              <option value="">Sélectionner…</option>
              <option>Départ à la retraite</option>
              <option>Cession classique</option>
              <option>Reprise progressive souhaitée</option>
              <option>Réorientation du dirigeant</option>
              <option>Autre</option>
            </select>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ">
            <label for="cession-situation">Situation de l'entreprise <span class="requis" aria-hidden="true">*</span></label>
            <select id="cession-situation" name="Situation de l'entreprise" required>
              <option value="">Sélectionner…</option>
              <option>En activité — situation saine</option>
              <option>En activité — difficultés</option>
              <option>Procédure de sauvegarde</option>
              <option>Redressement judiciaire</option>
              <option>Liquidation judiciaire</option>
              <option>Autre situation à étudier</option>
            </select>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ champ--plein">
            <label for="cession-message">Votre message <span class="requis" aria-hidden="true">*</span></label>
            <textarea id="cession-message" name="Message" rows="5" required
                      placeholder="Présentez votre entreprise, votre projet de cession et le calendrier envisagé."></textarea>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <div class="champ champ--plein champ-fichier">
            <label for="cession-fichier">Document de présentation (facultatif)</label>
            <input type="file" id="cession-fichier" name="piece_jointe"
                   accept=".pdf,.docx,.xlsx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                   aria-describedby="cession-fichier-aide">
            <p class="champ__aide" id="cession-fichier-aide">
              Formats acceptés : PDF, DOCX, XLSX — 10 Mo maximum. Le document est transmis
              directement au système interne de NEVIE-GLOBAL&nbsp;: il n'est stocké nulle part
              sur ce site et n'est accessible par aucune adresse publique.
            </p>
            <p class="champ__erreur" data-erreur role="alert"></p>
          </div>

          <!-- Consentements RGPD — volontairement NON pré-cochés -->
          <div class="champ-consentement">
            <input type="checkbox" id="cession-consentement" name="Consentement — étude du dossier"
                   value="Oui" required>
            <label for="cession-consentement">
              J'accepte que les informations transmises soient utilisées pour l'étude de mon
              projet de cession. <span class="requis" aria-hidden="true">*</span>
            </label>
            <p class="champ__erreur" data-erreur-consentement role="alert"></p>
          </div>

          <div class="champ-consentement">
            <input type="checkbox" id="cession-politique" name="Politique de confidentialité"
                   value="Lue et acceptée" required>
            <label for="cession-politique">
              J'ai pris connaissance de la
              <a href="confidentialite-cookies.html">politique de confidentialité</a>.
              <span class="requis" aria-hidden="true">*</span>
            </label>
            <p class="champ__erreur" data-erreur-consentement role="alert"></p>
          </div>

          <div class="form-pied">
            <p class="mention-confidentialite">
              <svg class="ico" aria-hidden="true"><use href="#i-cadenas"></use></svg>
              <span>
                Les informations et documents transmis dans le cadre d'une démarche de cession
                sont traités de manière confidentielle, sous réserve des obligations légales
                applicables.
              </span>
            </p>
            <button class="btn btn--primaire" type="submit" data-libelle="Transmettre mon dossier">
              Transmettre mon dossier
            </button>
          </div>

          <div class="form-progression" data-progression aria-hidden="true">
            <span class="form-progression__barre"></span>
          </div>

          <div class="form-retour" data-retour role="status" aria-live="polite"></div>

        </div>
      </form>
    </div>

  </div>
</section>
"""


# ===========================================================================
# PAGE 8 — CONTACT
# ===========================================================================
CONTACT = """
<section class="page-hero">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <nav class="ariane" aria-label="Fil d'Ariane">
      <a href="index.html">Accueil</a>
      <span class="sep" aria-hidden="true">/</span>
      <span aria-current="page">Contact</span>
    </nav>
    <h1>Contact</h1>
    <p class="page-hero__chapo">
      Une question concernant NEVIE-GLOBAL ou son portefeuille&nbsp;?
    </p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="contact__grille">

      <div class="reveal">
        <div class="coordonnees">

          <div class="coordonnee">
            <svg class="ico" aria-hidden="true"><use href="#i-immeuble"></use></svg>
            <div>
              <p class="coordonnee__lib">Raison sociale</p>
              <p class="coordonnee__val">NEVIE-GLOBAL SAS</p>
            </div>
          </div>

          <div class="coordonnee">
            <svg class="ico" aria-hidden="true"><use href="#i-broche"></use></svg>
            <div>
              <p class="coordonnee__lib">Siège social</p>
              <p class="coordonnee__val">
                2 Place Jean V, bureau 3<br>
                44000 Nantes, France
              </p>
            </div>
          </div>

          <div class="coordonnee">
            <svg class="ico" aria-hidden="true"><use href="#i-globe"></use></svg>
            <div>
              <p class="coordonnee__lib">Filiale technologique</p>
              <p class="coordonnee__val">
                <a href="https://nevie-global.com" target="_blank" rel="noopener noreferrer">
                  nevie-global.com
                </a>
              </p>
            </div>
          </div>

        </div>

        <div class="suite u-mt-m" >
          <div>
            <p class="suite__lib">Transmission</p>
            <p class="suite__titre u-t-normal" >Vous souhaitez céder votre entreprise&nbsp;?</p>
          </div>
          <a class="btn btn--or" href="ceder-son-entreprise.html">
            Accéder au formulaire dédié
            <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
          </a>
        </div>
      </div>

      <div class="carte form-bloc reveal">
        <form id="form-contact" novalidate>
          <div class="form-grille">

            <div class="pot-de-miel" aria-hidden="true">
              <label for="contact-site">Ne pas remplir</label>
              <input type="text" id="contact-site" name="_gotcha" tabindex="-1" autocomplete="off">
            </div>

            <div class="champ">
              <label for="contact-nom">Nom et prénom <span class="requis" aria-hidden="true">*</span></label>
              <input type="text" id="contact-nom" name="Nom et prénom" autocomplete="name" required>
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <div class="champ">
              <label for="contact-societe">Société</label>
              <input type="text" id="contact-societe" name="Société" autocomplete="organization">
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <div class="champ">
              <label for="contact-email">Adresse e-mail <span class="requis" aria-hidden="true">*</span></label>
              <input type="email" id="contact-email" name="email" autocomplete="email" required>
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <div class="champ">
              <label for="contact-tel">Téléphone</label>
              <input type="tel" id="contact-tel" name="Téléphone" autocomplete="tel">
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <div class="champ champ--plein">
              <label for="contact-sujet">Sujet <span class="requis" aria-hidden="true">*</span></label>
              <select id="contact-sujet" name="Sujet" required>
                <option value="">Sélectionner…</option>
                <option>Le groupe et son portefeuille</option>
                <option>Partenariat</option>
                <option>Investisseurs et banques</option>
                <option>Candidature</option>
                <option>Presse</option>
                <option>Autre</option>
              </select>
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <div class="champ champ--plein">
              <label for="contact-message">Votre message <span class="requis" aria-hidden="true">*</span></label>
              <textarea id="contact-message" name="Message" rows="5" required></textarea>
              <p class="champ__erreur" data-erreur role="alert"></p>
            </div>

            <!-- Consentement RGPD — volontairement NON pré-coché -->
            <div class="champ-consentement">
              <input type="checkbox" id="contact-consentement" name="Consentement RGPD" value="Oui" required>
              <label for="contact-consentement">
                J'accepte que les informations transmises soient utilisées pour traiter ma
                demande, conformément à la
                <a href="confidentialite-cookies.html">politique de confidentialité</a>.
                <span class="requis" aria-hidden="true">*</span>
              </label>
              <p class="champ__erreur" data-erreur-consentement role="alert"></p>
            </div>

            <div class="form-pied">
              <p class="mention-confidentialite">
                <svg class="ico" aria-hidden="true"><use href="#i-cadenas"></use></svg>
                <span>
                  Vos informations sont destinées à NEVIE-GLOBAL SAS exclusivement et ne sont
                  transmises à aucun tiers.
                </span>
              </p>
              <button class="btn btn--primaire" type="submit" data-libelle="Envoyer le message">
                Envoyer le message
              </button>
            </div>

            <div class="form-progression" data-progression aria-hidden="true">
              <span class="form-progression__barre"></span>
            </div>

            <div class="form-retour" data-retour role="status" aria-live="polite"></div>

          </div>
        </form>
      </div>

    </div>
  </div>
</section>
"""


# ===========================================================================
# PAGE 9 — MENTIONS LÉGALES
# ===========================================================================
MENTIONS = """
<section class="page-legale">
  <div class="conteneur">

    <a class="retour-accueil" href="index.html">
      <svg class="ico" aria-hidden="true"><use href="#i-fleche-gauche"></use></svg>
      Retour à l'accueil
    </a>

    <h1>Mentions légales</h1>
    <p class="maj">Dernière mise à jour : août 2026</p>

    <h2>1. Éditeur du site</h2>
    <dl>
      <div><dt>Dénomination sociale</dt><dd>NEVIE-GLOBAL SAS</dd></div>
      <div><dt>Forme juridique</dt><dd>Société par actions simplifiée (SAS)</dd></div>
      <div><dt>Capital social</dt><dd>50 € (500 actions de 0,10 €)</dd></div>
      <div><dt>Siège social</dt><dd>2 Place Jean V, bureau 3 — 44000 Nantes, France</dd></div>
      <div><dt>SIREN</dt><dd>993 888 841 — RCS Nantes</dd></div>
      <!-- À COMPLÉTER : numéro SIRET dès réception du Kbis définitif -->
      <div><dt>SIRET</dt><dd>[à compléter dès réception du Kbis définitif]</dd></div>
      <!-- À COMPLÉTER : numéro de TVA intracommunautaire, s'il y a lieu -->
      <div><dt>TVA intracommunautaire</dt><dd>[à compléter, le cas échéant]</dd></div>
      <div><dt>Présidente</dt><dd>Elisa Varinot</dd></div>
      <div><dt>Directeur Général</dt><dd>Emmanuel Varinot</dd></div>
    </dl>

    <h2>2. Directeur de la publication</h2>
    <p>Emmanuel Varinot, Directeur Général de NEVIE-GLOBAL SAS.</p>

    <h2>3. Hébergement</h2>
    <!-- À COMPLÉTER : raison sociale, adresse et téléphone de l'hébergeur retenu.
         La loi impose de faire figurer ces informations. -->
    <dl>
      <div><dt>Hébergeur</dt><dd>[à compléter selon l'hébergement retenu]</dd></div>
      <div><dt>Adresse</dt><dd>[à compléter]</dd></div>
      <div><dt>Téléphone</dt><dd>[à compléter]</dd></div>
    </dl>

    <h2>4. Objet du site</h2>
    <p>
      Le présent site est le site institutionnel de la holding NEVIE-GLOBAL SAS. Il a pour
      objet de présenter le groupe, sa gouvernance, son modèle, son portefeuille de
      participations et sa démarche d'acquisition. Il ne constitue ni un site marchand,
      ni une offre de vente de produits ou de services.
    </p>
    <p>
      Les informations publiées ne constituent ni une offre de souscription, ni un conseil
      en investissement, ni une sollicitation d'achat ou de vente de titres.
    </p>

    <h2>5. Statut des participations</h2>
    <p>
      Les sociétés présentées dans la rubrique « Nos entreprises » sont accompagnées d'un
      statut explicite. Une société signalée <strong>« en cours d'acquisition »</strong> n'est,
      à la date de publication, ni détenue ni intégrée au périmètre du groupe&nbsp;: l'opération
      correspondante n'est pas juridiquement finalisée. Les pôles signalés
      <strong>« à venir »</strong> ne correspondent à aucune société détenue à ce jour.
    </p>
    <p>
      NEVIE-GLOBAL LIMITED (Royaume-Uni) est une entité distincte, disposant de son propre
      site internet. Les produits, technologies et offres commerciales de cette société ne
      sont pas ceux de NEVIE-GLOBAL SAS.
    </p>

    <h2>6. Propriété intellectuelle</h2>
    <p>
      L'ensemble des contenus de ce site (textes, images, logo, structure et mise en forme)
      est la propriété de NEVIE-GLOBAL SAS, sauf mention contraire. Toute reproduction,
      représentation, adaptation ou exploitation, totale ou partielle, sans autorisation
      écrite préalable est interdite.
    </p>
    <p>
      La marque et le logo NEVIE-GLOBAL sont la propriété de NEVIE-GLOBAL SAS.
    </p>

    <h2>7. Liens externes</h2>
    <p>
      Ce site comporte des liens vers des sites tiers, notamment celui de NEVIE-GLOBAL
      LIMITED. NEVIE-GLOBAL SAS n'exerce aucun contrôle sur leur contenu et décline toute
      responsabilité à leur égard.
    </p>

    <h2>8. Données personnelles et cookies</h2>
    <p>
      Le traitement des données transmises via les formulaires du site et l'usage des cookies
      sont décrits dans la
      <a href="confidentialite-cookies.html">politique de confidentialité et cookies</a>.
    </p>

    <h2>9. Responsabilité</h2>
    <p>
      NEVIE-GLOBAL SAS s'efforce d'assurer l'exactitude des informations publiées, mais ne
      peut garantir qu'elles soient exemptes d'erreur ou d'omission. Les informations sont
      susceptibles d'évoluer, en particulier le statut des participations.
    </p>

    <h2>10. Droit applicable</h2>
    <p>
      Le présent site est soumis au droit français. Tout litige relatif à son utilisation
      relève de la compétence des tribunaux français.
    </p>

  </div>
</section>
"""


# ===========================================================================
# PAGE 10 — POLITIQUE DE CONFIDENTIALITÉ + COOKIES
# ===========================================================================
CONFIDENTIALITE = """
<section class="page-legale">
  <div class="conteneur">

    <a class="retour-accueil" href="index.html">
      <svg class="ico" aria-hidden="true"><use href="#i-fleche-gauche"></use></svg>
      Retour à l'accueil
    </a>

    <h1>Politique de confidentialité et cookies</h1>
    <p class="maj">Dernière mise à jour : août 2026</p>

    <p class="u-mt-l">
      NEVIE-GLOBAL SAS attache une importance particulière à la protection des données
      qui lui sont confiées, en particulier dans le cadre d'un projet de cession
      d'entreprise. La présente politique décrit quelles données sont collectées,
      pourquoi, pendant combien de temps, et comment exercer vos droits.
    </p>

    <h2>1. Responsable du traitement</h2>
    <dl>
      <div><dt>Responsable</dt><dd>NEVIE-GLOBAL SAS</dd></div>
      <div><dt>Adresse</dt><dd>2 Place Jean V, bureau 3 — 44000 Nantes, France</dd></div>
      <div><dt>Contact</dt><dd>Via la <a href="contact.html">page Contact</a> du site</dd></div>
    </dl>

    <h2>2. Données collectées</h2>
    <p>Aucune donnée n'est collectée par la simple consultation du site. Les seules données
      collectées sont celles que vous saisissez volontairement dans l'un des deux formulaires.</p>

    <h3>Formulaire de contact</h3>
    <ul>
      <li>Nom et prénom, société (facultatif)</li>
      <li>Adresse e-mail, téléphone (facultatif)</li>
      <li>Sujet et contenu du message</li>
    </ul>

    <h3>Formulaire de cession d'entreprise</h3>
    <ul>
      <li>Identité et fonction : nom, prénom, fonction exercée</li>
      <li>Coordonnées : adresse e-mail, téléphone</li>
      <li>Informations sur l'entreprise : raison sociale, SIREN, localisation, activité,
        chiffre d'affaires, effectif</li>
      <li>Contexte : motif de cession, situation de l'entreprise, message libre</li>
      <li>Document de présentation joint, le cas échéant</li>
    </ul>

    <h2>3. Finalité et base légale</h2>
    <div class="table-wrap">
      <table class="table-legale">
        <caption class="sr-only">Finalités des traitements et bases légales correspondantes</caption>
        <thead>
          <tr><th scope="col">Traitement</th><th scope="col">Finalité</th><th scope="col">Base légale</th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Formulaire de contact</td>
            <td>Répondre à votre demande</td>
            <td>Consentement (art. 6.1.a RGPD)</td>
          </tr>
          <tr>
            <td>Formulaire de cession</td>
            <td>Étudier votre dossier de cession et échanger avec vous</td>
            <td>Consentement et mesures précontractuelles (art. 6.1.a et 6.1.b RGPD)</td>
          </tr>
          <tr>
            <td>Mémorisation du choix cookies</td>
            <td>Ne pas réafficher la bannière à chaque page</td>
            <td>Intérêt légitime — respect de votre choix</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>4. Destinataires</h2>
    <p>
      Les données sont destinées à <strong>NEVIE-GLOBAL SAS exclusivement</strong>. Elles ne
      sont ni vendues, ni louées, ni communiquées à des tiers à des fins commerciales.
      <strong>Aucune donnée n'est transférée hors de l'Union européenne.</strong>
    </p>
    <p>
      Le site est statique et ne dispose d'aucune base de données&nbsp;: les informations
      saisies sont transmises directement au système interne de NEVIE-GLOBAL SAS et ne sont
      à aucun moment enregistrées sur le serveur qui héberge ce site.
    </p>

    <h2>5. Durée de conservation</h2>
    <ul>
      <li><strong>Demandes de contact</strong> : le temps nécessaire au traitement de la demande,
        puis suppression.</li>
      <li><strong>Dossiers de cession</strong> : le temps nécessaire à l'étude du dossier et aux
        échanges qui en découlent, puis suppression.</li>
      <li><strong>Choix relatif aux cookies</strong> : 6 mois (180 jours). Passé ce délai, la
        bannière vous est de nouveau présentée.</li>
    </ul>

    <h2>6. Confidentialité des dossiers de cession</h2>
    <p>
      Les informations et documents transmis dans le cadre d'une démarche de cession sont
      traités de manière confidentielle, sous réserve des obligations légales applicables.
      Les documents joints ne sont stockés sur aucun espace public et ne sont accessibles
      par aucune adresse web.
    </p>

    <h2>7. Vos droits</h2>
    <p>
      Conformément au Règlement général sur la protection des données, vous disposez d'un
      droit d'accès, de rectification, d'effacement, d'opposition, de limitation du
      traitement et de portabilité de vos données, ainsi que du droit de retirer votre
      consentement à tout moment.
    </p>
    <p>
      Pour exercer ces droits, contactez NEVIE-GLOBAL SAS via la
      <a href="contact.html">page Contact</a> ou par courrier à l'adresse du siège social.
    </p>
    <p>
      Si vous estimez, après nous avoir contactés, que vos droits ne sont pas respectés,
      vous pouvez adresser une réclamation à la CNIL — 3 place de Fontenoy, TSA 80715,
      75334 Paris Cedex 07 — <a href="https://www.cnil.fr" target="_blank" rel="noopener noreferrer">www.cnil.fr</a>.
    </p>

    <h2>8. Cookies</h2>
    <p>
      Ce site utilise uniquement les cookies techniques nécessaires à son fonctionnement.
      Vous pouvez accepter, refuser ou personnaliser leur utilisation via la bannière
      affichée lors de votre première visite.
    </p>
    <p>
      Il n'installe <strong>aucun outil de mesure d'audience</strong>, aucun cookie
      publicitaire et aucun bouton de réseau social. Les polices de caractères sont
      hébergées sur le site lui-même&nbsp;: aucune requête n'est adressée à un service tiers
      et votre adresse IP n'est transmise à personne.
    </p>

    <div class="table-wrap">
      <table class="table-legale">
        <caption class="sr-only">Éléments enregistrés dans votre navigateur</caption>
        <thead>
          <tr>
            <th scope="col">Nom</th><th scope="col">Type</th>
            <th scope="col">Finalité</th><th scope="col">Durée</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>nevie-global.consentement</td>
            <td>Stockage local (localStorage)</td>
            <td>Mémorise votre choix afin de ne pas réafficher la bannière</td>
            <td>6 mois</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>Effet du bouton « Refuser »</h3>
    <p>
      Comme aucun traceur n'est chargé par défaut, refuser revient exactement à l'état
      initial du site&nbsp;: <strong>le refus est pleinement effectif et n'entraîne aucune
      dégradation</strong> de la navigation. Seul votre choix est mémorisé, afin de ne pas
      vous présenter la bannière à chaque page.
    </p>

    <h3>Modifier votre choix</h3>
    <p>
      Vous pouvez revenir sur votre décision à tout moment en cliquant sur
      <a href="#" data-rouvrir-cookies>Gérer les cookies</a>, en bas de chaque page.
      L'option « Personnaliser » de la bannière permet d'accepter ou de refuser
      catégorie par catégorie.
    </p>

    <h2>9. Sécurité</h2>
    <p>
      Le site est diffusé en HTTPS. Les données saisies dans les formulaires transitent
      chiffrées. Le site ne conservant aucune donnée, il ne constitue pas un point de
      stockage susceptible d'être compromis.
    </p>

    <h2>10. Modification de la présente politique</h2>
    <p>
      Cette politique peut être mise à jour pour tenir compte d'évolutions légales ou
      techniques. La date de dernière mise à jour figure en haut de la page.
    </p>

  </div>
</section>
"""


# ===========================================================================
# PAGE 404
# ===========================================================================
ERREUR_404 = """
<section class="erreur">
  <div class="page-hero__fond" aria-hidden="true"></div>
  <div class="conteneur">
    <p class="erreur__code" aria-hidden="true">404</p>
    <h1>Cette page n'existe pas</h1>
    <p>
      L'adresse demandée est introuvable. Elle a peut-être été déplacée, ou comporte
      une erreur de saisie.
    </p>
    <div class="page-hero__actions">
      <a class="btn btn--primaire" href="index.html">
        Retour à l'accueil
        <svg class="ico" aria-hidden="true" width="14" height="14"><use href="#i-fleche-droite"></use></svg>
      </a>
      <a class="btn btn--secondaire" href="nos-entreprises.html">Voir nos entreprises</a>
      <a class="btn btn--secondaire" href="contact.html">Nous contacter</a>
    </div>
  </div>
</section>
"""


# ===========================================================================
# Assemblage et écriture des fichiers
# ===========================================================================
PAGES = [
    ("index.html",
     "NEVIE-GLOBAL SAS — Holding entrepreneuriale française",
     "NEVIE-GLOBAL SAS, holding française basée à Nantes, construit progressivement un "
     "portefeuille diversifié d'entreprises dans l'industrie, les services, la technologie "
     "et l'artisanat.",
     ACCUEIL, JSON_LD),

    ("le-groupe.html",
     "Le Groupe — NEVIE-GLOBAL SAS",
     "Histoire, vision et philosophie de NEVIE-GLOBAL SAS, holding entrepreneuriale "
     "fondée à Nantes par Elisa et Emmanuel Varinot.",
     LE_GROUPE, ""),

    ("notre-modele.html",
     "Notre Modèle — NEVIE-GLOBAL SAS",
     "Sourcing, analyse, reprise, intégration, gouvernance et développement : la mécanique "
     "de la holding NEVIE-GLOBAL, étape par étape.",
     NOTRE_MODELE, ""),

    ("gouvernance.html",
     "Gouvernance — NEVIE-GLOBAL SAS",
     "Elisa Varinot, Présidente, et Emmanuel Varinot, Directeur Général : direction et "
     "approche de gouvernance de NEVIE-GLOBAL SAS.",
     GOUVERNANCE, ""),

    ("nos-entreprises.html",
     "Nos Entreprises et participations — NEVIE-GLOBAL SAS",
     "Portefeuille de NEVIE-GLOBAL SAS par pôle : NEVIE-GLOBAL LIMITED (détenue), "
     "TECHNIFLOC-DIFFUSION (en cours d'acquisition) et les pôles à venir.",
     NOS_ENTREPRISES, ""),

    ("croissance-acquisitions.html",
     "Croissance & Acquisitions — NEVIE-GLOBAL SAS",
     "Stratégie de développement par acquisitions et reprises d'entreprises : critères "
     "recherchés, secteurs étudiés et approche de NEVIE-GLOBAL SAS.",
     CROISSANCE, ""),

    ("ceder-son-entreprise.html",
     "Céder son entreprise — NEVIE-GLOBAL SAS",
     "Vous envisagez de céder votre entreprise ? Secteurs et situations étudiés par "
     "NEVIE-GLOBAL SAS, processus et formulaire de présentation de dossier.",
     CEDER, ""),

    ("contact.html",
     "Contact — NEVIE-GLOBAL SAS",
     "Contacter NEVIE-GLOBAL SAS, holding basée au 2 Place Jean V, bureau 3, "
     "44000 Nantes : formulaire et coordonnées.",
     CONTACT, ""),

    ("mentions-legales.html",
     "Mentions légales — NEVIE-GLOBAL SAS",
     "Mentions légales du site institutionnel de NEVIE-GLOBAL SAS : éditeur, directeur de "
     "la publication, hébergeur et propriété intellectuelle.",
     MENTIONS, ""),

    ("confidentialite-cookies.html",
     "Politique de confidentialité et cookies — NEVIE-GLOBAL SAS",
     "Données collectées, finalités, durées de conservation, droits RGPD et gestion des "
     "cookies sur le site de NEVIE-GLOBAL SAS.",
     CONFIDENTIALITE, ""),
]


def main():
    ecrits = []

    for fichier, titre, description, corps, extra in PAGES:
        html = page(fichier, titre, description, corps, extra_head=extra)
        chemin = os.path.join(RACINE, fichier)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(html)
        ecrits.append(fichier)

    # La page 404 ne doit pas être indexée
    html = page("404.html", "Page introuvable — NEVIE-GLOBAL SAS",
                "La page demandée est introuvable sur le site de NEVIE-GLOBAL SAS.",
                ERREUR_404, sans_index=True)
    with open(os.path.join(RACINE, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)
    ecrits.append("404.html")

    for nom in ecrits:
        taille = os.path.getsize(os.path.join(RACINE, nom))
        print("  %-34s %6.1f ko" % (nom, taille / 1024))
    print("\n%d pages générées." % len(ecrits))


if __name__ == "__main__":
    main()
