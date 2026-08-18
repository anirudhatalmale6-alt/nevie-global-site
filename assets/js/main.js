/* ==========================================================================
   NEVIE-GLOBAL SAS — Script principal
   JavaScript natif, sans dépendance ni framework, sans étape de compilation.

   Sommaire
   00. Configuration (webhooks n8n, messages, cookies)
   01. Outils
   02. En-tête : état au défilement
   03. Menu mobile
   04. Apparition des blocs au défilement
   05. Formulaires (validation, pièce jointe, envoi vers n8n)
   06. Bandeau cookies (Accepter / Refuser / Personnaliser)
   07. Année courante dans le pied de page
   ========================================================================== */

(function () {
  'use strict';

  /* ========================================================================
     00. CONFIGURATION
     ------------------------------------------------------------------------
     Les deux formulaires transmettent leurs données au workflow n8n existant
     de NEVIE-GLOBAL. Le site n'enregistre rien : aucune base de données,
     aucun fichier stocké sur l'hébergement.

     À FAIRE AVANT LA MISE EN LIGNE
     ------------------------------
     1. Coller ci-dessous les deux URL de webhook n8n fournies par
        NEVIE-GLOBAL SAS (format https://nevie-global.app.n8n.cloud/webhook/…).

     2. Dans n8n, sur le nœud « Webhook » de chaque workflow :
        • Méthode HTTP ................. POST
        • Respond ...................... « Immediately » ou « Using Respond to
          Webhook node », avec un code 200 en cas de succès.
        • Options → « Allowed Origins (CORS) » ...... https://nevie-global.fr
          (ajouter aussi https://www.nevie-global.fr si le www est servi)

        Ce dernier point est indispensable : sans en-tête CORS, le navigateur
        bloque la réponse et le visiteur voit le message d'échec, même si n8n
        a bien reçu les données. Le site respecte en effet la règle du cahier
        des charges : aucune confirmation n'est affichée sans accusé de
        réception réel (voir partie 6).

     3. Pour recevoir la pièce jointe du dossier de cession, cocher
        « Binary Property » / « Binary Data » sur le nœud Webhook : le fichier
        arrive dans le champ « piece_jointe ».

     Ces URL de webhook ne sont pas des secrets d'API : elles ne donnent accès
     ni au tableau de bord n8n, ni aux données déjà reçues. Elles peuvent donc
     figurer dans le code de la page. La validation de fond (type réel du
     fichier, taille, filtrage anti-spam serveur) reste à faire côté n8n : un
     site statique ne peut pas garantir à lui seul ce que le navigateur envoie.
     ======================================================================== */
  var CONFIG = {
    webhookCession: 'https://nevie-global.app.n8n.cloud/webhook/A_RENSEIGNER_CESSION',
    webhookContact: 'https://nevie-global.app.n8n.cloud/webhook/A_RENSEIGNER_CONTACT',

    // Messages affichés au visiteur (textes validés par NEVIE-GLOBAL SAS)
    succesCession: 'Votre dossier a bien été transmis. Merci pour votre confiance. Nous allons examiner les informations transmises et reviendrons vers vous si votre dossier correspond à nos critères d\'étude.',
    succesContact: 'Votre message a bien été transmis. Nous y répondrons dans les meilleurs délais.',
    echec: 'Votre demande n\'a pas pu être transmise. Veuillez réessayer ou nous écrire directement.',

    // Pièce jointe du dossier de cession
    fichierExtensions: ['pdf', 'docx', 'xlsx'],
    fichierTailleMaxMo: 10,

    // Bandeau cookies
    cleCookies: 'nevie-global.consentement',
    dureeConsentementJours: 180,

    // Délai au-delà duquel l'envoi est considéré comme échoué (ms)
    delaiEnvoiMax: 20000
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

  function avertir(message) {
    if (window.console && window.console.warn) window.console.warn('[NEVIE-GLOBAL] ' + message);
  }

  /* ========================================================================
     02. EN-TÊTE : ÉTAT AU DÉFILEMENT
     L'en-tête devient opaque dès que la page est défilée. Le calcul est
     différé via requestAnimationFrame pour ne pas bloquer le fil de
     défilement (bon pour le score de performance).
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

    // Un clic sur un lien du menu ferme le panneau avant le changement de page
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
    // (le seuil correspond au point de rupture de la feuille de style)
    window.matchMedia('(min-width: 1081px)').addEventListener('change', function (e) {
      if (e.matches) fermer();
    });
  })();

  /* ========================================================================
     04. APPARITION DES BLOCS AU DÉFILEMENT
     Effet volontairement sobre (léger fondu + montée de 16 px).
     Entièrement désactivé si le système demande un mouvement réduit.
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
     05. FORMULAIRES
     Validation côté navigateur, puis transmission au webhook n8n.
     Règle stricte du cahier des charges : le message de confirmation n'est
     affiché QUE si n8n a répondu avec un code de succès. Toute autre issue
     (réseau coupé, CORS non configuré, erreur 500, délai dépassé) affiche le
     message d'échec.
     ======================================================================== */
  (function formulaires() {

    var MESSAGES = {
      requis: 'Ce champ est obligatoire.',
      email: 'Merci de saisir une adresse e-mail valide.',
      telephone: 'Merci de saisir un numéro de téléphone valide.',
      consentement: 'Merci de cocher cette case pour pouvoir envoyer votre demande.',
      fichierType: 'Format non accepté. Formats autorisés : ' + CONFIG.fichierExtensions.join(', ').toUpperCase() + '.',
      fichierTaille: 'Fichier trop volumineux (maximum ' + CONFIG.fichierTailleMaxMo + ' Mo).'
    };

    var REGEX_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
    // Téléphone : chiffres, espaces, points, tirets, parenthèses et préfixe +
    var REGEX_TEL = /^\+?[0-9\s.\-()]{6,25}$/;

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

    // Contrôle de la pièce jointe : extension et poids.
    // Ce contrôle est un confort pour le visiteur, pas une sécurité : la
    // validation qui fait foi est celle du workflow n8n, côté serveur.
    function validerFichier(champ) {
      if (!champ.files || !champ.files.length) { marquerChamp(champ, ''); return true; }

      var fichier = champ.files[0];
      var nom = (fichier.name || '').toLowerCase();
      var extension = nom.indexOf('.') !== -1 ? nom.split('.').pop() : '';

      if (CONFIG.fichierExtensions.indexOf(extension) === -1) {
        marquerChamp(champ, MESSAGES.fichierType);
        return false;
      }
      if (fichier.size > CONFIG.fichierTailleMaxMo * 1024 * 1024) {
        marquerChamp(champ, MESSAGES.fichierTaille);
        return false;
      }
      marquerChamp(champ, '');
      return true;
    }

    // Valide un champ isolé ; renvoie true si le champ est correct
    function validerChamp(champ) {
      if (champ.type === 'file') return validerFichier(champ);

      var valeur = (champ.value || '').trim();

      if (champ.hasAttribute('required') && !valeur) {
        marquerChamp(champ, MESSAGES.requis);
        return false;
      }
      if (champ.type === 'email' && valeur && !REGEX_EMAIL.test(valeur)) {
        marquerChamp(champ, MESSAGES.email);
        return false;
      }
      if (champ.type === 'tel' && valeur && !REGEX_TEL.test(valeur)) {
        marquerChamp(champ, MESSAGES.telephone);
        return false;
      }
      marquerChamp(champ, '');
      return true;
    }

    // Valide le formulaire complet, cases de consentement comprises
    function validerFormulaire(form) {
      var valide = true;

      $$('input:not([type="checkbox"]):not([type="hidden"]), select, textarea', form).forEach(function (champ) {
        if (champ.name === '_gotcha') return;
        if (!validerChamp(champ)) valide = false;
      });

      // Une ou plusieurs cases obligatoires (consentement RGPD, prise de
      // connaissance de la politique de confidentialité)
      $$('input[type="checkbox"][required]', form).forEach(function (case_) {
        var bloc = case_.closest('.champ-consentement');
        var zone = bloc ? $('[data-erreur-consentement]', bloc) : null;
        var ok = case_.checked;
        if (bloc) bloc.classList.toggle('est-invalide', !ok);
        if (zone) zone.textContent = ok ? '' : MESSAGES.consentement;
        if (!ok) valide = false;
      });

      return valide;
    }

    // Affiche le bandeau de retour sous le formulaire
    function afficherRetour(form, type, texte) {
      var zone = $('[data-retour]', form);
      if (!zone) return;
      var icone = type === 'succes' ? '#i-coche' : '#i-alerte';
      zone.className = 'form-retour form-retour--' + type + ' est-visible';
      zone.innerHTML = '<svg class="ico" aria-hidden="true"><use href="' + icone + '"></use></svg><span></span>';
      $('span', zone).textContent = texte;
      // Le message est annoncé aux lecteurs d'écran et amené à l'écran
      zone.setAttribute('tabindex', '-1');
      zone.focus({ preventScroll: false });
    }

    function masquerRetour(form) {
      var zone = $('[data-retour]', form);
      if (zone) { zone.className = 'form-retour'; zone.textContent = ''; }
    }

    // Envoi avec délai maximal : au-delà, on considère n8n indisponible
    function envoyer(url, donnees) {
      var controleur = ('AbortController' in window) ? new AbortController() : null;
      var minuteur = window.setTimeout(function () {
        if (controleur) controleur.abort();
      }, CONFIG.delaiEnvoiMax);

      var options = { method: 'POST', body: donnees };
      if (controleur) options.signal = controleur.signal;

      return fetch(url, options).then(function (reponse) {
        window.clearTimeout(minuteur);
        // Seule une réponse lisible ET en succès vaut accusé de réception.
        // Une réponse « opaque » (CORS absent) n'en est pas une.
        if (reponse.type === 'opaque' || !reponse.ok) {
          throw new Error('HTTP ' + reponse.status);
        }
        return reponse;
      }, function (erreur) {
        window.clearTimeout(minuteur);
        throw erreur;
      });
    }

    // Branche un formulaire sur son webhook
    function brancher(idForm, url, messageSucces) {
      var form = document.getElementById(idForm);
      if (!form) return;

      var bouton = $('button[type="submit"]', form);
      var libelle = bouton ? (bouton.getAttribute('data-libelle') || bouton.textContent.trim()) : '';
      var progression = $('[data-progression]', form);
      var barre = progression ? $('.form-progression__barre', progression) : null;
      var configure = url.indexOf('A_RENSEIGNER') === -1;

      if (!configure) {
        avertir('Webhook n8n non renseigné pour « ' + idForm + ' ». ' +
                'Renseignez CONFIG.webhookCession / CONFIG.webhookContact dans assets/js/main.js. ' +
                'Tant que ce n\'est pas fait, le formulaire affiche le message d\'échec : ' +
                'aucune confirmation n\'est affichée sans accusé de réception réel.');
      }

      // Validation à la volée : on ne signale une erreur qu'après une première
      // sortie de champ, pour ne pas agresser l'utilisateur en cours de saisie.
      $$('input, select, textarea', form).forEach(function (champ) {
        if (champ.name === '_gotcha') return;
        if (champ.type === 'checkbox') return;
        if (champ.type === 'file') {
          champ.addEventListener('change', function () { validerChamp(champ); });
          return;
        }
        champ.addEventListener('blur', function () { validerChamp(champ); });
        champ.addEventListener('input', function () {
          var conteneur = champ.closest('.champ');
          if (conteneur && conteneur.classList.contains('est-invalide')) validerChamp(champ);
        });
      });

      $$('input[type="checkbox"][required]', form).forEach(function (case_) {
        case_.addEventListener('change', function () {
          if (!case_.checked) return;
          var bloc = case_.closest('.champ-consentement');
          if (bloc) {
            bloc.classList.remove('est-invalide');
            var zone = $('[data-erreur-consentement]', bloc);
            if (zone) zone.textContent = '';
          }
        });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        masquerRetour(form);

        if (!validerFormulaire(form)) {
          var premier = $('.est-invalide input, .est-invalide select, .est-invalide textarea', form)
                     || $('.champ-consentement.est-invalide input', form);
          if (premier) premier.focus();
          return;
        }

        // Pot-de-miel : un robot remplit ce champ caché. On interrompt sans
        // rien envoyer et sans lui signaler qu'il a été repéré.
        var piege = form.querySelector('input[name="_gotcha"]');
        if (piege && piege.value) {
          form.reset();
          afficherRetour(form, 'succes', messageSucces);
          return;
        }

        var donnees = new FormData(form);
        donnees.delete('_gotcha');
        // Repères utiles au workflow n8n pour classer la demande
        donnees.append('origine', window.location.href);
        donnees.append('envoye_le', new Date().toISOString());

        if (bouton) { bouton.disabled = true; bouton.textContent = 'Envoi en cours…'; }
        if (progression && barre) {
          progression.classList.add('est-visible');
          barre.style.width = '35%';
        }

        function terminer() {
          if (bouton) { bouton.disabled = false; bouton.textContent = libelle; }
          if (progression && barre) {
            barre.style.width = '100%';
            window.setTimeout(function () {
              progression.classList.remove('est-visible');
              barre.style.width = '0';
            }, 400);
          }
        }

        // Webhook non renseigné : on emprunte exactement le chemin d'échec
        // prévu par le cahier des charges, sans jamais simuler un succès.
        if (!configure) {
          window.setTimeout(function () {
            afficherRetour(form, 'erreur', CONFIG.echec);
            terminer();
            avertir('Envoi non effectué : webhook n8n non configuré.');
          }, 500);
          return;
        }

        envoyer(url, donnees)
          .then(function () {
            form.reset();
            afficherRetour(form, 'succes', messageSucces);
          })
          .catch(function (erreur) {
            afficherRetour(form, 'erreur', CONFIG.echec);
            avertir('Échec de transmission : ' + (erreur && erreur.message ? erreur.message : 'inconnu') +
                    '. Vérifiez que le nœud Webhook n8n autorise l\'origine du site (CORS).');
          })
          .then(terminer, terminer);
      });
    }

    brancher('form-cession', CONFIG.webhookCession, CONFIG.succesCession);
    brancher('form-contact', CONFIG.webhookContact, CONFIG.succesContact);
  })();

  /* ========================================================================
     06. BANDEAU COOKIES — Accepter / Refuser / Personnaliser
     ------------------------------------------------------------------------
     Une seule bannière, sur toutes les pages. Le site n'installe aujourd'hui
     aucun traceur : les polices sont auto-hébergées, il n'y a ni mesure
     d'audience, ni script tiers. « Refuser » correspond donc exactement à
     l'état par défaut du site, et le refus est pleinement effectif.

     Le panneau « Personnaliser » liste les catégories prévues. La catégorie
     « nécessaire » est verrouillée (elle ne couvre que la mémorisation du
     choix lui-même). Les autres sont désactivées par défaut : si une mesure
     d'audience est ajoutée plus tard, il suffira de tester
     window.NEVIE.consentement('mesure') avant de charger le script.
     ======================================================================== */
  (function bandeauCookies() {
    var MS_PAR_JOUR = 86400000;

    // Catégories connues. « necessaire » est toujours vraie.
    var CATEGORIES = ['necessaire', 'mesure', 'preferences'];

    function lireChoix() {
      var brut = stockage.lire(CONFIG.cleCookies);
      if (!brut) return null;

      var donnee;
      try { donnee = JSON.parse(brut); } catch (e) { donnee = null; }
      if (!donnee || !donnee.date || !donnee.categories) {
        stockage.effacer(CONFIG.cleCookies);
        return null;
      }

      // Le choix expire à la durée annoncée dans la politique de confidentialité
      var age = (Date.now() - donnee.date) / MS_PAR_JOUR;
      if (age > CONFIG.dureeConsentementJours || age < 0) {
        stockage.effacer(CONFIG.cleCookies);
        return null;
      }
      return donnee;
    }

    // API publique : permet de conditionner un futur script tiers au consentement
    window.NEVIE = window.NEVIE || {};
    window.NEVIE.consentement = function (categorie) {
      if (categorie === 'necessaire') return true;
      var choix = lireChoix();
      return Boolean(choix && choix.categories && choix.categories[categorie]);
    };

    var bandeau = $('#cookies');
    var relance = $$('[data-rouvrir-cookies]');

    // Le lien « Gérer les cookies » doit fonctionner depuis n'importe quelle
    // page : la bannière est présente partout, il n'y a donc rien à rediriger.
    relance.forEach(function (lien) {
      lien.addEventListener('click', function (e) {
        if (!bandeau) return;      // page sans bannière : on laisse suivre le lien
        e.preventDefault();
        stockage.effacer(CONFIG.cleCookies);
        ouvrirPersonnalisation(false);
        afficher();
      });
    });

    if (!bandeau) return;

    var perso = $('#cookies-perso', bandeau);
    var boutonPerso = $('[data-cookies="personnaliser"]', bandeau);
    var boutonEnregistrer = $('[data-cookies="enregistrer"]', bandeau);

    function enregistrerChoix(categories) {
      stockage.ecrire(CONFIG.cleCookies, JSON.stringify({
        date: Date.now(),
        version: 1,
        categories: categories
      }));
    }

    function toutesCategories(valeur) {
      var res = {};
      CATEGORIES.forEach(function (c) { res[c] = (c === 'necessaire') ? true : valeur; });
      return res;
    }

    function categoriesCochees() {
      var res = { necessaire: true };
      $$('input[data-categorie]', bandeau).forEach(function (input) {
        var nom = input.getAttribute('data-categorie');
        if (nom === 'necessaire') return;
        res[nom] = input.checked;
      });
      return res;
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

    function ouvrirPersonnalisation(ouvert) {
      if (!perso || !boutonPerso) return;
      perso.classList.toggle('est-ouvert', ouvert);
      boutonPerso.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
      if (boutonEnregistrer) boutonEnregistrer.hidden = !ouvert;
    }

    if (boutonPerso) {
      boutonPerso.addEventListener('click', function () {
        ouvrirPersonnalisation(boutonPerso.getAttribute('aria-expanded') !== 'true');
      });
    }

    $$('[data-cookies]', bandeau).forEach(function (bouton) {
      var action = bouton.getAttribute('data-cookies');
      if (action === 'personnaliser') return;

      bouton.addEventListener('click', function () {
        if (action === 'accepter')   enregistrerChoix(toutesCategories(true));
        if (action === 'refuser')    enregistrerChoix(toutesCategories(false));
        if (action === 'enregistrer') enregistrerChoix(categoriesCochees());
        masquer();
        // Aucun script de mesure n'est chargé dans un cas comme dans l'autre :
        // le refus n'a donc rien à désactiver, il est effectif par construction.
      });
    });

    // Affichage uniquement si aucun choix valide n'est enregistré.
    // Léger différé : la bannière ne concurrence pas le premier rendu.
    if (!lireChoix()) {
      window.setTimeout(afficher, 700);
    }
  })();

  /* ========================================================================
     07. ANNÉE COURANTE
     Évite d'avoir à modifier le pied de page chaque 1er janvier.
     ======================================================================== */
  (function anneeCourante() {
    $$('[data-annee]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  })();

})();
