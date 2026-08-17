<?php
/**
 * ---------------------------------------------------------------------------
 * NEVIE-GLOBAL SAS — Envoi des formulaires par e-mail (solution alternative)
 * ---------------------------------------------------------------------------
 *
 * Ce fichier est OPTIONNEL. La solution retenue par défaut est Formspree,
 * configurée dans assets/js/main.js : elle ne demande aucun serveur PHP.
 *
 * Utilisez ce script uniquement si votre hébergement exécute PHP et que vous
 * préférez que les e-mails partent de votre propre serveur, sans service tiers.
 *
 * MISE EN PLACE
 * 1. Déposer ce fichier sur l'hébergement, par exemple à la racine du site.
 * 2. Renseigner DESTINATAIRE et EXPEDITEUR ci-dessous.
 *    L'adresse EXPEDITEUR doit appartenir au domaine du site, faute de quoi
 *    la plupart des messageries classeront le message en indésirable.
 * 3. Dans assets/js/main.js, remplacer les deux URL Formspree par :
 *       endpointCession: 'envoi.php',
 *       endpointContact: 'envoi.php',
 *
 * Aucune donnée n'est enregistrée : le script se contente de composer un
 * e-mail et de le transmettre.
 */

declare(strict_types=1);

/* --- Paramètres à renseigner ------------------------------------------- */
const DESTINATAIRE = 'contact@nevie-global.fr';        // Qui reçoit les demandes
const EXPEDITEUR   = 'site@nevie-global.fr';           // Adresse d'envoi technique
const SUJET_PREFIX = '[Site NEVIE-GLOBAL] ';

/* --- Réponse JSON, comme attendu par le script du site ------------------ */
header('Content-Type: application/json; charset=utf-8');

function repondre(int $code, array $corps): void
{
    http_response_code($code);
    echo json_encode($corps, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    repondre(405, ['ok' => false, 'erreur' => 'Méthode non autorisée.']);
}

/* --- Piège à robots : le champ caché doit rester vide ------------------- */
if (!empty($_POST['_gotcha'])) {
    // On renvoie un succès sans rien envoyer : inutile de renseigner le robot.
    repondre(200, ['ok' => true]);
}

/* --- Nettoyage des valeurs --------------------------------------------- */
function nettoyer(string $valeur): string
{
    // Retire les retours à la ligne des valeurs courtes : protège les en-têtes
    // de l'e-mail contre une injection.
    return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $valeur));
}

$champs = [];
foreach ($_POST as $cle => $valeur) {
    if ($cle === '_gotcha' || !is_string($valeur)) {
        continue;
    }
    $champs[nettoyer((string) $cle)] = $cle === 'Message'
        ? trim($valeur)              // le message conserve ses sauts de ligne
        : nettoyer($valeur);
}

/* --- Contrôles minimaux ------------------------------------------------- */
$email = $champs['email'] ?? '';
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    repondre(422, ['ok' => false, 'erreur' => 'Adresse e-mail invalide.']);
}
if (empty($champs['Consentement RGPD'])) {
    repondre(422, ['ok' => false, 'erreur' => 'Consentement manquant.']);
}

/* --- Composition du message -------------------------------------------- */
$estCession = isset($champs['Raison sociale']);
$sujet = SUJET_PREFIX . ($estCession ? 'Dossier de cession' : 'Demande de contact');

$lignes = [];
foreach ($champs as $cle => $valeur) {
    if ($valeur === '') {
        continue;
    }
    $lignes[] = $cle . ' : ' . $valeur;
}
$corps = implode("\n", $lignes)
       . "\n\n-- \nMessage envoyé depuis le formulaire du site NEVIE-GLOBAL SAS.\n";

$entetes = [
    'From: NEVIE-GLOBAL — Site <' . EXPEDITEUR . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
];

$envoye = mail(
    DESTINATAIRE,
    '=?UTF-8?B?' . base64_encode($sujet) . '?=',
    $corps,
    implode("\r\n", $entetes),
    '-f' . EXPEDITEUR
);

if (!$envoye) {
    repondre(500, ['ok' => false, 'erreur' => "L'envoi a échoué."]);
}

repondre(200, ['ok' => true]);
