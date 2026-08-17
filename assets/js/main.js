/* ==========================================================================
   NEVIE-GLOBAL SAS — Script principal
   JavaScript natif, sans dépendance ni framework.

   Sommaire
   00. Configuration (endpoints des formulaires)
   01. Outils
   02. En-tête : état au défilement
   03. Menu mobile
   04. Lien de navigation actif selon la section visible
   05. Apparition des blocs au défilement
   06. Formulaires (validation + envoi e-mail)
   07. Bandeau cookies
   08. Année courante dans le pied de page
   ========================================================================== */

(function () {
  'use strict';

  /* ========================================================================
     00. CONFIGURATION
     ------------------------------------------------------------------------
     Les deux formulaires envoient un e-mail via Formspree : pas de base de
     données, pas de serveur à maintenir, aucune donnée conservée sur le site.

     À FAIRE AVANT LA MISE EN LIGNE
     1. Créer un compte gratuit sur https://formspree.io avec l'adresse e-mail
        qui doit recevoir les messages.
     2. Créer deux formulaires : « Cession » et « Contact ».
     3. Coller ci-dessous les deux URL fournies (format :
        https://formspree.io/f/xxxxxxxx).

     L'identifiant Formspree est une donnée publique, pas un secret : il figure
     dans le code de la page. Aucune clé d'API privée n'est utilisée.

     Tant que les valeurs ci-dessous ne sont pas remplacées, les formulaires
     fonctionnent en mode démonstration : la validation et le message de
     confirmation s'affichent normalement, mais aucun e-mail n'est envoyé.
     ======================================================================== */
  var CONFIG = {
    endpointCession: 'https://formspree.io/f/REMPLACER_ID_CESSION',
    endpointContact: 'https://formspree.io/f/REMPLACER_ID_CONTACT',

    // Message de confirmation affiché après un envoi réussi
    messageSuccesCession: 'Votre dossier a bien été transmis, nous l\'étudions.',
    messageSuccesContact: 'Votre message a bien été transmis. Nous vous répondons rapidement.',
    messageErreur: 'L\'envoi a échoué. Merci de réessayer dans quelques instants, ou de nous écrire directement à contact@nevie-global.fr.',

    // Clé de stockage du choix « cookies » dans le navigateur
    cleCookies: 'nevie-global.consentement',

    // Durée de validité du choix, en jours (cohérente avec la politique de
    // confidentialité : passé ce délai, la bannière est réaffichée).
    dureeConsentementJours: 180
  };

  /* ========================================================================
     01. OUTILS
     ======================================================================== */
  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  // L'utilisateur a-t-il demandé un mouvement réduit au niveau du système ?
  var mouvementReduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Le localStorage peut être indisponible (navigation privée, réglages stricts).
  // On l'encapsule pour ne jamais casser la page.
  var stockage = {
    lire: function (cle) {
      try { return window.localStorage.getItem(cle); } catch (e) { return null; }
    },
    ecrire: function (cle, valeur) {
      try { window.localStorage.setItem(cle, valeur); } catch (e) { /* ignoré */ }
    },
    effacer: function (cle) {
      try { window.localStorage.removeItem(cle); } catch (e) { /* ignoré */ }
    }
  };

  /* ========================================================================
     02. EN-TÊTE : ÉTAT AU DÉFILEMENT
     L'en-tête devient opaque dès que la page est défilée.
     Le calcul est différé via requestAnimationFrame pour éviter de bloquer
     le fil de défilement (bon pour le score de performance).
     ======================================================================== */
  (function enteteAuDefilement() {
    var entete = $('#entete');
    if (!entete) return;

    var enAttente = false;

    function majEtat() {
      entete.classList.toggle('est-defile', window.scrollY > 12);
      enAttente = false;
    }

    window.addEventListener('scroll', function () {
      if (enAttente) return;
      enAttente = true;
      window.requestAnimationFrame(majEtat);
    }, { passive: true });

    majEtat();
  })();

  /* ========================================================================
     03. MENU MOBILE
     ======================================================================== */
  (function menuMobile() {
    var burger = $('#burger');
    var nav = $('#nav');
    if (!burger || !nav) return;

    function ouvrir() {
      nav.classList.add('est-ouvert');
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Fermer le menu');
      document.body.classList.add('menu-ouvert');
    }

    function fermer() {
      nav.classList.remove('est-ouvert');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Ouvrir le menu');
      document.body.classList.remove('menu-ouvert');
    }

    burger.addEventListener('click', function () {
      if (nav.classList.contains('est-ouvert')) { fermer(); } else { ouvrir(); }
    });

    // Un clic sur un lien du menu ferme le panneau avant le défilement
    $$('a', nav).forEach(function (lien) {
      lien.addEventListener('click', fermer);
    });

    // Échap ferme le menu et redonne le focus au bouton
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('est-ouvert')) {
        fermer();
        burger.focus();
      }
    });

    // Repasser en affichage large referme le panneau resté ouvert
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) {
      if (e.matches) fermer();
    });
  })();

  /* ========================================================================
     04. LIEN DE NAVIGATION ACTIF
     Un IntersectionObserver suit la section visible : pas d'écouteur de
     défilement, donc aucun calcul de position à chaque pixel.
     ======================================================================== */
  (function navigationActive() {
    var liens = $$('.nav__lien[href^="#"]');
    if (!liens.length || !('IntersectionObserver' in window)) return;

    var parSection = {};
    var sections = [];

    liens.forEach(function (lien) {
      var section = document.getElementById(lien.getAttribute('href').slice(1));
      if (!section) return;
      parSection[section.id] = lien;
      sections.push(section);
    });

    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) return;
        liens.forEach(function (l) { l.classList.remove('est-actif'); });
        var actif = parSection[entree.target.id];
        if (actif) actif.classList.add('est-actif');
      });
    }, {
      // La section est considérée « courante » quand elle occupe la bande
      // centrale de l'écran, sous l'en-tête fixe.
      rootMargin: '-45% 0px -50% 0px',
      threshold: 0
    });

    sections.forEach(function (s) { observateur.observe(s); });
  })();

  /* ========================================================================
     05. APPARITION DES BLOCS AU DÉFILEMENT
     Effet volontairement sobre (léger fondu + montée de 16px).
     Désactivé si le système demande un mouvement réduit.
     ======================================================================== */
  (function apparitions() {
    var blocs = $$('.reveal');
    if (!blocs.length) return;

    if (mouvementReduit || !('IntersectionObserver' in window)) {
      blocs.forEach(function (b) { b.classList.add('est-vu'); });
      return;
    }

    var observateur = new IntersectionObserver(function (entrees, obs) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) return;
        entree.target.classList.add('est-vu');
        // On cesse d'observer : l'animation ne se rejoue pas au retour
        obs.unobserve(entree.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    blocs.forEach(function (b) { observateur.observe(b); });
  })();

  /* ========================================================================
     06. FORMULAIRES
     Validation côté client puis envoi vers Formspree (fetch + JSON).
     Aucune donnée n'est conservée par le site.
     ======================================================================== */
  (function formulaires() {

    var MESSAGES = {
      requis: 'Ce champ est obligatoire.',
      email: 'Merci de saisir une adresse e-mail valide.',
      consentement: 'Merci de cocher cette case pour pouvoir envoyer votre demande.'
    };

    var REGEX_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

    // Affiche ou efface le message d'erreur d'un champ
    function marquerChamp(champ, message) {
      var conteneur = champ.closest('.champ');
      if (!conteneur) return;
      var zone = $('[data-erreur]', conteneur);
      conteneur.classList.toggle('est-invalide', Boolean(message));
      if (zone) zone.textContent = message || '';
      if (message) {
        champ.setAttribute('aria-invalid', 'true');
      } else {
        champ.removeAttribute('aria-invalid');
      }
    }

    // Valide un champ isolé ; renvoie true si le champ est correct
    function validerChamp(champ) {
      var valeur = (champ.value || '').trim();

      if (champ.hasAttribute('required') && !valeur) {
        marquerChamp(champ, MESSAGES.requis);
        return false;
      }
      if (champ.type === 'email' && valeur && !REGEX_EMAIL.test(valeur)) {
        marquerChamp(champ, MESSAGES.email);
        return false;
      }
      marquerChamp(champ, '');
      return true;
    }

    // Valide le formulaire complet, y compris la case RGPD
    function validerFormulaire(form) {
      var valide = true;

      $$('input:not([type="checkbox"]):not([type="hidden"]), select, textarea', form).forEach(function (champ) {
        if (champ.name === '_gotcha') return;
        if (!validerChamp(champ)) valide = false;
      });

      var consentement = $('input[type="checkbox"][required]', form);
      var zoneConsentement = $('[data-erreur-consentement]', form);
      if (consentement) {
        var blocConsentement = consentement.closest('.champ-consentement');
        var ok = consentement.checked;
        if (blocConsentement) blocConsentement.classList.toggle('est-invalide', !ok);
        if (zoneConsentement) zoneConsentement.textContent = ok ? '' : MESSAGES.consentement;
        if (!ok) valide = false;
      }

      return valide;
    }

    // Affiche le bandeau de retour sous le formulaire
    function afficherRetour(form, type, texte) {
      var zone = $('[data-retour]', form);
      if (!zone) return;
      var icone = type === 'succes' ? '#i-coche' : '#i-alerte';
      zone.className = 'form-retour form-retour--' + type + ' est-visible';
      zone.innerHTML =
        '<svg class="ico" aria-hidden="true"><use href="' + icone + '"></use></svg><span></span>';
      $('span', zone).textContent = texte;
    }

    function masquerRetour(form) {
      var zone = $('[data-retour]', form);
      if (zone) { zone.className = 'form-retour'; zone.textContent = ''; }
    }

    // Branche un formulaire sur son endpoint
    function brancher(idForm, endpoint, messageSucces) {
      var form = document.getElementById(idForm);
      if (!form) return;

      var bouton = $('button[type="submit"]', form);
      var libelle = bouton ? (bouton.getAttribute('data-libelle') || bouton.textContent.trim()) : '';
      var modeDemo = endpoint.indexOf('REMPLACER_') !== -1;

      // Validation à la volée : on ne signale une erreur qu'après une première
      // sortie de champ, pour ne pas agresser l'utilisateur en cours de saisie.
      $$('input, select, textarea', form).forEach(function (champ) {
        if (champ.name === '_gotcha' || champ.type === 'checkbox') return;
        champ.addEventListener('blur', function () { validerChamp(champ); });
        champ.addEventListener('input', function () {
          var conteneur = champ.closest('.champ');
          if (conteneur && conteneur.classList.contains('est-invalide')) validerChamp(champ);
        });
      });

      var consentement = $('input[type="checkbox"][required]', form);
      if (consentement) {
        consentement.addEventListener('change', function () {
          var bloc = consentement.closest('.champ-consentement');
          var zone = $('[data-erreur-consentement]', form);
          if (consentement.checked) {
            if (bloc) bloc.classList.remove('est-invalide');
            if (zone) zone.textContent = '';
          }
        });
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        masquerRetour(form);

        if (!validerFormulaire(form)) {
          var premier = $('.est-invalide input, .est-invalide select, .est-invalide textarea', form)
                     || $('.champ-consentement.est-invalide input', form);
          if (premier) premier.focus();
          return;
        }

        // Pot-de-miel : un robot remplit ce champ caché. On simule un succès
        // pour ne pas lui indiquer qu'il a été détecté, sans rien envoyer.
        var piege = form.querySelector('input[name="_gotcha"]');
        if (piege && piege.value) {
          form.reset();
          afficherRetour(form, 'succes', messageSucces);
          return;
        }

        if (bouton) { bouton.disabled = true; bouton.textContent = 'Envoi en cours…'; }

        // Mode démonstration : tant que l'endpoint Formspree n'est pas
        // renseigné, on affiche le parcours complet sans appel réseau.
        if (modeDemo) {
          window.setTimeout(function () {
            form.reset();
            afficherRetour(form, 'succes', messageSucces);
            if (bouton) { bouton.disabled = false; bouton.textContent = libelle; }
            if (window.console) {
              console.warn('[NEVIE-GLOBAL] Mode démonstration : renseignez l\'endpoint Formspree dans assets/js/main.js pour activer l\'envoi réel.');
            }
          }, 600);
          return;
        }

        var donnees = new FormData(form);

        fetch(endpoint, {
          method: 'POST',
          body: donnees,
          headers: { Accept: 'application/json' }
        })
          .then(function (reponse) {
            if (!reponse.ok) throw new Error('HTTP ' + reponse.status);
            form.reset();
            afficherRetour(form, 'succes', messageSucces);
          })
          .catch(function () {
            afficherRetour(form, 'erreur', CONFIG.messageErreur);
          })
          .then(function () {
            if (bouton) { bouton.disabled = false; bouton.textContent = libelle; }
          });
      });
    }

    brancher('form-cession', CONFIG.endpointCession, CONFIG.messageSuccesCession);
    brancher('form-contact', CONFIG.endpointContact, CONFIG.messageSuccesContact);
  })();

  /* ========================================================================
     07. BANDEAU COOKIES
     Une seule bannière. « Accepter » et « Refuser » enregistrent tous deux le
     choix : la bannière ne réapparaît pas. Le site n'installe aucun traceur,
     donc « Refuser » n'a rien à désactiver — c'est l'état par défaut.
     ======================================================================== */
  (function bandeauCookies() {
    var bandeau = $('#cookies');
    if (!bandeau) return;

    var boutons = $$('[data-cookies]', bandeau);
    var relance = $$('[data-rouvrir-cookies]');

    var MS_PAR_JOUR = 86400000;

    // Lit le choix enregistré et le considère expiré au-delà de la durée
    // annoncée dans la politique de confidentialité.
    function choixEnregistre() {
      var brut = stockage.lire(CONFIG.cleCookies);
      if (!brut) return null;

      var donnee;
      try { donnee = JSON.parse(brut); } catch (e) { donnee = null; }
      if (!donnee || !donnee.choix || !donnee.date) {
        stockage.effacer(CONFIG.cleCookies);
        return null;
      }

      var age = (Date.now() - donnee.date) / MS_PAR_JOUR;
      if (age > CONFIG.dureeConsentementJours || age < 0) {
        stockage.effacer(CONFIG.cleCookies);
        return null;
      }
      return donnee.choix;
    }

    function enregistrerChoix(choix) {
      stockage.ecrire(CONFIG.cleCookies, JSON.stringify({ choix: choix, date: Date.now() }));
    }

    function afficher() {
      bandeau.classList.add('est-affiche');
      // Deux images successives pour que la transition d'entrée se joue
      window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
          bandeau.classList.add('est-visible');
        });
      });
    }

    function masquer() {
      bandeau.classList.remove('est-visible');
      if (mouvementReduit) {
        bandeau.classList.remove('est-affiche');
        return;
      }
      window.setTimeout(function () { bandeau.classList.remove('est-affiche'); }, 620);
    }

    // Arrivée depuis « Gérer les cookies » d'une page légale (index.html?cookies=1)
    var demandeReouverture = window.location.search.indexOf('cookies=1') !== -1;
    if (demandeReouverture) {
      stockage.effacer(CONFIG.cleCookies);
      // On nettoie l'URL pour ne pas rouvrir la bannière à chaque rechargement
      if (window.history && window.history.replaceState) {
        window.history.replaceState({}, '', window.location.pathname);
      }
    }

    // Affichage uniquement si aucun choix valide n'est enregistré
    if (!choixEnregistre()) {
      // Léger différé : la bannière ne concurrence pas l'affichage initial
      window.setTimeout(afficher, demandeReouverture ? 120 : 700);
    }

    boutons.forEach(function (bouton) {
      bouton.addEventListener('click', function () {
        var choix = bouton.getAttribute('data-cookies'); // « accepter » ou « refuser »
        enregistrerChoix(choix);
        masquer();
        // Aucun script de mesure n'est chargé dans les deux cas :
        // le refus est donc pleinement effectif.
      });
    });

    // Lien « Gérer les cookies » du pied de page : rouvre la bannière
    relance.forEach(function (lien) {
      lien.addEventListener('click', function (e) {
        e.preventDefault();
        stockage.effacer(CONFIG.cleCookies);
        afficher();
      });
    });
  })();

  /* ========================================================================
     08. ANNÉE COURANTE
     Évite d'avoir à modifier le pied de page chaque 1er janvier.
     ======================================================================== */
  (function anneeCourante() {
    $$('[data-annee]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  })();

})();
