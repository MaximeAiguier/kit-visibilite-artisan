// Test du site généré dans un vrai navigateur (Playwright + Chromium).
// Usage : node tests/test_navigateur.js <url_de_base> [--complet]
//   --complet : site publiable (réalisations, mentions légales, suivi Google Ads attendus)
const { chromium, devices } = require('playwright');

const base = process.argv[2].replace(/\/$/, '');
const complet = process.argv.includes('--complet');
let echecs = 0;
const ok = (cond, msg) => { console.log((cond ? '  OK   ' : '  ÉCHEC ') + msg); if (!cond) echecs++; };

async function contexte(b, opts) {
  const ctx = await b.newContext(opts);
  const appels = { gtag: 0, posts: [] };
  await ctx.route('**/*', async (route) => {
    const url = route.request().url();
    if (url.startsWith(base)) return route.continue();
    if (url.includes('googletagmanager.com')) { appels.gtag++; return route.fulfill({ status: 200, contentType: 'text/javascript', body: '' }); }
    if (url.includes('formspree.io')) {
      appels.posts.push(route.request().postData() || '');
      const statut = ctx._statutFormulaire || 200;
      return route.fulfill({ status: statut, contentType: 'application/json', body: statut === 200 ? '{"ok":true}' : '{"error":"limit"}' });
    }
    return route.abort();
  });
  return { ctx, appels };
}

(async () => {
  const b = await chromium.launch();
  const pages = ['index.html', 'contact.html', 'a-propos.html', 'confidentialite.html'];
  const { ctx: mob, appels } = await contexte(b, { ...devices['iPhone SE'] });
  const p = await mob.newPage();
  const erreursJs = [];
  p.on('pageerror', (e) => erreursJs.push(e.message));

  console.log('Mobile (iPhone SE)');
  await p.goto(base + '/index.html');
  const liens = await p.$$eval('a[href]', (as) => as.map((a) => a.getAttribute('href')));
  const pagesSite = [...new Set(liens.filter((h) => /^[a-z0-9-]+\.html$/.test(h)))];
  for (const f of new Set([...pages, ...pagesSite])) {
    const r = await p.goto(base + '/' + f);
    ok(r.status() === 200, `${f} s'ouvre`);
    const larg = await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
    ok(larg, `${f} : pas de défilement horizontal`);
    const barre = await p.isVisible('.barre-mobile a[href^="tel:"]');
    ok(barre, `${f} : bouton « Appeler » visible en bas d'écran`);
    const ld = await p.$$eval('script[type="application/ld+json"]', (s) => s.map((x) => x.textContent));
    let valide = ld.length > 0;
    const tels = new Set();
    for (const t of ld) {
      try { const j = JSON.parse(t); (Array.isArray(j) ? j : [j]).forEach((o) => o.telephone && tels.add(o.telephone)); } catch (e) { valide = false; }
    }
    ok(valide, `${f} : données structurées lisibles`);
    ok(tels.size === 1, `${f} : un seul numéro dans les données structurées`);
    const imgs = await p.$$eval('img', (is) => is.map((i) => ({ src: i.src, ok: i.complete ? i.naturalWidth > 0 : true, alt: i.alt })));
    ok(imgs.every((i) => i.alt), `${f} : toutes les images ont une description`);
  }
  ok(erreursJs.length === 0, 'aucune erreur JavaScript' + (erreursJs.length ? ' : ' + erreursJs.join(' | ') : ''));

  console.log('Formulaire de devis');
  await p.goto(base + '/contact.html');
  ok(await p.isVisible('select#source[required]'), 'champ « Comment nous avez-vous connu ? » présent et obligatoire');
  const nbOptions = await p.$$eval('#source option', (o) => o.length);
  ok(nbOptions >= 10, `liste des origines proposée (${nbOptions} choix)`);
  await p.click('button[type="submit"]');
  await p.waitForTimeout(300);
  ok(appels.posts.length === 0, 'formulaire vide : rien n\'est envoyé');
  await p.fill('#nom', 'Client Test');
  await p.fill('#telephone', '0600000001');
  await p.fill('#commune', 'Commune Test');
  await p.selectOption('#source', 'google-annonce');
  await p.check('input[name="accord"]');
  if (complet) {
    // Consentement accepté avant l'envoi pour vérifier la conversion
    ok(appels.gtag === 0, 'aucune balise Google chargée avant accord');
    ok(await p.isVisible('#cookies'), 'bandeau cookies affiché');
    await p.click('[data-consentement="oui"]');
    await p.waitForTimeout(200);
    ok(appels.gtag === 1, 'balise Google chargée après « Accepter »');
    const consent = await p.evaluate(() => JSON.stringify((window.dataLayer || []).find((a) => a[0] === 'consent') || []));
    ok(/"ad_user_data":"granted"/.test(consent) && /"ad_personalization":"denied"/.test(consent), 'signaux de consentement envoyés à Google (mode Consentement v2)');
    const choix = await p.evaluate(() => JSON.parse(localStorage.getItem('consentement-mesure')));
    ok(choix && choix.v === 'oui' && choix.t > 0, 'choix daté (redemandé au bout de 6 mois)');
  }
  await p.click('button[type="submit"]');
  await p.waitForSelector('#form-message:not([hidden])');
  const msg = await p.textContent('#form-message');
  ok(appels.posts.length === 1 && appels.posts[0].includes('google-annonce'), 'demande envoyée avec son origine');
  ok(/bien reçu/.test(msg), 'confirmation affichée : « ' + msg.trim() + ' »');
  if (complet) {
    const dl = await p.evaluate(() => JSON.stringify(window.dataLayer || []));
    ok(dl.includes('labelForm'), 'conversion « formulaire » envoyée à Google Ads');
    await p.goto(base + '/index.html');
    await p.click('.barre-mobile a[href^="tel:"]', { noWaitAfter: true }).catch(() => {});
    const dl2 = await p.evaluate(() => JSON.stringify(window.dataLayer || []));
    ok(dl2.includes('labelTel'), 'conversion « clic sur le numéro » envoyée à Google Ads');
  }

  console.log('Formulaire saturé (limite Formspree)');
  const { ctx: mob2 } = await contexte(b, { ...devices['iPhone SE'] });
  mob2._statutFormulaire = 429;
  const p2 = await mob2.newPage();
  await p2.goto(base + '/contact.html');
  await p2.fill('#nom', 'X'); await p2.fill('#telephone', '0600000002'); await p2.fill('#commune', 'Y');
  await p2.selectOption('#source', 'facebook'); await p2.check('input[name="accord"]');
  await p2.click('button[type="submit"]');
  await p2.waitForSelector('#form-message:not([hidden])');
  ok(/Appelez-nous/.test(await p2.textContent('#form-message')), 'message d\'erreur avec le numéro à appeler');

  if (complet) {
    const { ctx: c4, appels: a4 } = await contexte(b, { ...devices['iPhone SE'] });
    const p4 = await c4.newPage();
    await p4.goto(base + '/index.html');
    await p4.evaluate(() => localStorage.setItem('consentement-mesure', JSON.stringify({ v: 'oui', t: Date.now() - 200 * 86400000 })));
    await p4.goto(base + '/index.html');
    ok(a4.gtag === 0 && (await p4.isVisible('#cookies')), 'accord de plus de 6 mois : bandeau redemandé, aucune balise chargée');
  }

  if (!complet) {
    const { ctx: c3, appels: a3 } = await contexte(b, { ...devices['iPhone SE'] });
    const p3 = await c3.newPage();
    await p3.goto(base + '/index.html');
    if (await p3.isVisible('#cookies')) {
      await p3.click('[data-consentement="non"]');
      await p3.goto(base + '/contact.html');
      ok(a3.gtag === 0 && !(await p3.isVisible('#cookies')), 'refus des cookies respecté (aucune balise chargée)');
    }
  }

  console.log('Ordinateur (1280 px)');
  const { ctx: bureau } = await contexte(b, { viewport: { width: 1280, height: 800 } });
  const d = await bureau.newPage();
  await d.goto(base + '/index.html');
  ok(!(await d.isVisible('.barre-mobile')), 'barre mobile masquée sur ordinateur');
  ok(await d.isVisible('.entete-tel'), 'numéro cliquable visible dans l\'en-tête');
  ok(await d.isVisible('nav#navigation'), 'menu visible');

  await b.close();
  console.log(echecs ? `\n${echecs} ÉCHEC(S)` : '\nTous les tests navigateur sont OK.');
  process.exit(echecs ? 1 : 0);
})();
