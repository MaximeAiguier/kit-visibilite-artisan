/* Gabarit du kit : menu mobile, consentement cookies, suivi Google Ads (après accord), formulaire de devis. */
(function () {
  "use strict";
  var S = window.SUIVI || {};
  var CLE = "consentement-mesure";

  // Menu mobile
  var bouton = document.querySelector(".menu-bouton");
  var nav = document.getElementById("navigation");
  if (bouton && nav) {
    bouton.addEventListener("click", function () {
      var ouvert = nav.classList.toggle("ouverte");
      bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
  }

  // Consentement (le suivi Google Ads n'est chargé qu'après "Accepter").
  // Le choix est redemandé au bout de 6 mois (recommandation CNIL).
  var DUREE_CHOIX = 182 * 24 * 3600 * 1000;
  function lire() {
    try {
      var brut = localStorage.getItem(CLE);
      if (!brut) return null;
      var c = JSON.parse(brut);
      if (!c || !c.t || Date.now() - c.t > DUREE_CHOIX) return null;
      return c.v;
    } catch (e) { return null; }
  }
  function ecrire(v) { try { localStorage.setItem(CLE, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {} }
  var gtagCharge = false;
  function chargerGtag() {
    if (gtagCharge || !S.id) return;
    gtagCharge = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    // Mode Consentement v2 de Google : mesure des demandes acceptée par le visiteur,
    // aucune personnalisation publicitaire (c'est ce qu'annonce le bandeau).
    window.gtag("consent", "default", {
      ad_storage: "granted", ad_user_data: "granted",
      ad_personalization: "denied", analytics_storage: "denied"
    });
    window.gtag("js", new Date());
    window.gtag("config", S.id);
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(S.id);
    document.head.appendChild(s);
  }
  function conversion(label) {
    if (!label || !S.id || lire() !== "oui" || typeof window.gtag !== "function") return;
    window.gtag("event", "conversion", { send_to: S.id + "/" + label });
  }
  var bandeau = document.getElementById("cookies");
  if (S.id) {
    if (lire() === "oui") chargerGtag();
    else if (lire() !== "non" && bandeau) bandeau.hidden = false;
    document.addEventListener("click", function (e) {
      var c = e.target.closest("[data-consentement]");
      if (!c) return;
      var v = c.getAttribute("data-consentement");
      if (v === "choisir") { if (bandeau) bandeau.hidden = false; return; }
      ecrire(v);
      if (bandeau) bandeau.hidden = true;
      if (v === "oui") chargerGtag();
    });
  }

  // Clic sur le numéro de téléphone
  document.querySelectorAll('a[href^="tel:"]').forEach(function (a) {
    a.addEventListener("click", function () { conversion(S.labelTel); });
  });

  // Formulaire de devis (Formspree, envoi sans quitter la page)
  var form = document.getElementById("form-devis");
  if (form) {
    var zone = document.getElementById("form-message");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = "Envoi en cours…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) {
          if (r.ok) {
            conversion(S.labelForm);
            form.hidden = true;
            zone.className = "message-form message-ok";
            zone.textContent = form.getAttribute("data-confirmation");
            zone.hidden = false;
            zone.focus();
          } else { throw new Error("statut " + r.status); }
        })
        .catch(function () {
          btn.disabled = false;
          btn.textContent = "Envoyer ma demande";
          zone.className = "message-form message-erreur";
          zone.textContent = form.getAttribute("data-erreur");
          zone.hidden = false;
        });
    });
  }
})();
