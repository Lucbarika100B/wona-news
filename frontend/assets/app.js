/* Wona.news frontend logic. Vanilla JS. No framework. */
(function () {
  "use strict";

  // ----------------------------------------------------------------------------
  // i18n: chrome translations. Article content stays in source language.
  // ----------------------------------------------------------------------------
  const I18N = {
    fr: {
      "ribbon.tagline": "Reclaiming the African narrative, one story at a time.",
      "ribbon.cta": "Notre mission",
      "brand.tagline": "Intelligence médiatique africaine",

      "nav.news": "Actualités",
      "nav.perspectives": "Perspectives",
      "nav.blindspots": "Angles morts",
      "nav.mission": "Mission",

      "search.placeholder": "Rechercher",

      "btn.donate": "Faire un don",
      "btn.subscribe": "S'abonner",

      "topics.label": "En tendance",

      "briefing.title": "Briefing du jour",

      "perspectives.eyebrow": "Cinq perspectives africaines",
      "perspectives.all": "Toutes les perspectives",
      "perspectives.panelTitle": "Perspectives africaines",

      "stories.headline": "À la une",
      "stories.aria": "Histoires",
      "stories.empty": "Aucune histoire ne correspond à vos filtres.",
      "stories.featured": "À la une",
      "stories.allFilter": "Toutes",

      "blindspot.title": "Angles morts",
      "blindspot.tag": "Sous-couvert",
      "blindspot.lede": "Les histoires que les fils dominants oublient de raconter.",
      "blindspot.empty": "Aucun angle mort détecté aujourd'hui.",
      "blindspot.concentration": "Concentration",

      "donate.title": "Soutenir Wona",
      "donate.tag": "Indépendant",
      "donate.lede": "Wona.news est sans publicité, sans investisseur, sans agenda externe. Votre soutien nous garde libres.",
      "donate.allocation.title": "Où va votre contribution",
      "donate.allocation.compute": "Calcul & modèles : améliorer la classification des perspectives et la qualité des résumés.",
      "donate.allocation.coverage": "Couverture des sources : intégrer plus de médias locaux et de langues sous-représentées.",
      "donate.allocation.features": "Priorités des contributeurs : développer en priorité les fonctionnalités les plus demandées.",
      "donate.tier1": "un café",
      "donate.tier2": "un mois",
      "donate.tier3": "soutien",
      "donate.custom": "Choisir un autre montant →",

      "about.title": "À propos de Wona",
      "about.copy": "Wona.news contextualise l'actualité du continent et de la diaspora à travers des grilles de lecture africaines. Pas de gauche, pas de droite. Des perspectives nées ici.",
      "about.cta": "Lire le manifeste",

      "mission.eyebrow": "Notre engagement",
      "mission.headline": "Reprendre le récit africain.<br />Le contextualiser. Le diffuser.",
      "mission.body": "Wona.news aggrège des sources africaines et internationales, produit des résumés courts et lisibles, et révèle l'orientation idéologique de chaque récit à travers cinq perspectives africaines. Pas une plateforme contre, une plateforme depuis.",
      "mission.cta": "Soutenir le projet →",

      "subscribe.title": "Le briefing Wona, chaque matin.",
      "subscribe.body": "Recevez chaque matin une synthèse de l'actualité africaine, contextualisée et classée par perspective.",
      "subscribe.placeholder": "vous@example.com",

      "footer.brandTagline": "Plateforme d'intelligence médiatique africaine.",
      "footer.platform": "Plateforme",
      "footer.support": "Soutenir",
      "footer.method": "Méthode",
      "footer.contact": "Contact",
      "footer.manifesto": "Manifeste",
      "footer.methodology": "Méthodologie",
      "footer.sources": "Sources",
      "footer.newsletter": "S'abonner à la newsletter",
      "footer.tagline": "Indépendant. Continental. Diasporique.",

      "floating.support": "Soutenir",

      "story.unclassified": "Non classé",
      "story.sources": "source",
      "story.sourcesPlural": "sources",
      "story.loadFailed": "Impossible de charger les histoires. Vérifiez data/articles.json.",

      "time.lessThanHour": "il y a < 1h",
      "time.hours": "il y a {n}h",
      "time.days": "il y a {n}j",
    },

    en: {
      "ribbon.tagline": "Reclaiming the African narrative, one story at a time.",
      "ribbon.cta": "Our mission",
      "brand.tagline": "African media intelligence",

      "nav.news": "News",
      "nav.perspectives": "Perspectives",
      "nav.blindspots": "Blindspots",
      "nav.mission": "Mission",

      "search.placeholder": "Search",

      "btn.donate": "Donate",
      "btn.subscribe": "Subscribe",

      "topics.label": "Trending",

      "briefing.title": "Today's briefing",

      "perspectives.eyebrow": "Five African perspectives",
      "perspectives.all": "All perspectives",
      "perspectives.panelTitle": "African perspectives",

      "stories.headline": "Top stories",
      "stories.aria": "Stories",
      "stories.empty": "No stories match your filters.",
      "stories.featured": "Featured",
      "stories.allFilter": "All",

      "blindspot.title": "Blindspots",
      "blindspot.tag": "Underreported",
      "blindspot.lede": "Stories the dominant feeds forget to tell.",
      "blindspot.empty": "No blindspots detected today.",
      "blindspot.concentration": "Concentration",

      "donate.title": "Support Wona",
      "donate.tag": "Independent",
      "donate.lede": "Wona.news has no ads, no investors, no external agenda. Your support keeps us free.",
      "donate.allocation.title": "Where your support goes",
      "donate.allocation.compute": "Compute & models: better perspective classification and summary quality.",
      "donate.allocation.coverage": "Source coverage: integrating more local outlets and underrepresented languages.",
      "donate.allocation.features": "Contributor priorities: building the features supporters request most.",
      "donate.tier1": "a coffee",
      "donate.tier2": "a month",
      "donate.tier3": "patron",
      "donate.custom": "Choose another amount →",

      "about.title": "About Wona",
      "about.copy": "Wona.news contextualizes news from the continent and the diaspora through African frameworks. Not left, not right. Perspectives born here.",
      "about.cta": "Read the manifesto",

      "mission.eyebrow": "Our commitment",
      "mission.headline": "Reclaim the African narrative.<br />Contextualize it. Spread it.",
      "mission.body": "Wona.news aggregates African and international sources, produces short readable summaries, and reveals the ideological orientation of each story through five African perspectives. Not a platform against, a platform from.",
      "mission.cta": "Support the project →",

      "subscribe.title": "The Wona briefing, every morning.",
      "subscribe.body": "Get a daily synthesis of African news, contextualized and classified by perspective.",
      "subscribe.placeholder": "you@example.com",

      "footer.brandTagline": "African media intelligence platform.",
      "footer.platform": "Platform",
      "footer.support": "Support",
      "footer.method": "Method",
      "footer.contact": "Contact",
      "footer.manifesto": "Manifesto",
      "footer.methodology": "Methodology",
      "footer.sources": "Sources",
      "footer.newsletter": "Subscribe to newsletter",
      "footer.tagline": "Independent. Continental. Diasporic.",

      "floating.support": "Support",

      "story.unclassified": "Unclassified",
      "story.sources": "source",
      "story.sourcesPlural": "sources",
      "story.loadFailed": "Failed to load stories. Check data/articles.json.",

      "time.lessThanHour": "< 1h ago",
      "time.hours": "{n}h ago",
      "time.days": "{n}d ago",
    },
  };

  function t(key) {
    const dict = I18N[STATE.lang] || I18N.fr;
    return dict[key] !== undefined ? dict[key] : key;
  }

  function applyTranslations() {
    const lang = STATE.lang;
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.dataset.i18n;
      const value = I18N[lang] && I18N[lang][key];
      if (value !== undefined) el.textContent = value;
    });
    document.querySelectorAll("[data-i18n-html]").forEach(el => {
      const key = el.dataset.i18nHtml;
      const value = I18N[lang] && I18N[lang][key];
      if (value !== undefined) el.innerHTML = value;
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.dataset.i18nPlaceholder;
      const value = I18N[lang] && I18N[lang][key];
      if (value !== undefined) el.placeholder = value;
    });
    document.querySelectorAll("[data-i18n-aria-label]").forEach(el => {
      const key = el.dataset.i18nAriaLabel;
      const value = I18N[lang] && I18N[lang][key];
      if (value !== undefined) el.setAttribute("aria-label", value);
    });

    // Language toggle button: show the OTHER language as the call-to-switch
    const toggle = document.getElementById("lang-toggle");
    if (toggle) {
      const current = toggle.querySelector(".lang-current");
      const other = toggle.querySelector(".lang-other");
      if (current && other) {
        current.textContent = lang.toUpperCase();
        other.textContent = (lang === "fr" ? "EN" : "FR");
      }
    }
  }

  function setLanguage(lang) {
    if (!I18N[lang]) return;
    STATE.lang = lang;
    try { localStorage.setItem("wona.lang", lang); } catch (e) { /* ignore */ }
    applyTranslations();
    paint();
  }

  function getInitialLang() {
    try {
      const saved = localStorage.getItem("wona.lang");
      if (saved && I18N[saved]) return saved;
    } catch (e) { /* ignore */ }
    const browser = (navigator.language || "fr").slice(0, 2).toLowerCase();
    return I18N[browser] ? browser : "fr";
  }

  // ----------------------------------------------------------------------------
  // Data sources
  // ----------------------------------------------------------------------------
  const API_BASE = (typeof window !== "undefined" && window.WONA_API_URL) || null;
  const DATA_URL = API_BASE ? `${API_BASE}/articles` : "data/articles.json";
  const ORIENT_URL = API_BASE ? `${API_BASE}/orientations` : "data/orientations.json";

  const STATE = {
    stories: [],
    orientations: [],
    activeOrientation: null,
    activeTopic: null,
    searchQuery: "",
    lang: "fr",
  };

  // ----------------------------------------------------------------------------
  // Fetch
  // ----------------------------------------------------------------------------
  async function fetchJSON(url) {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`Fetch failed: ${url} (${response.status})`);
    return response.json();
  }

  // ----------------------------------------------------------------------------
  // Helpers
  // ----------------------------------------------------------------------------
  function orientationById(id) {
    return STATE.orientations.find(o => o.id === id);
  }

  function orientationName(o) {
    if (!o) return "";
    return STATE.lang === "en" ? (o.name_en || o.name_fr) : (o.name_fr || o.name_en);
  }

  function orientationDesc(o) {
    if (!o) return "";
    return STATE.lang === "en" ? (o.description_en || o.description_fr || "") : (o.description_fr || o.description_en || "");
  }

  function formatDate(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    const locale = STATE.lang === "en" ? "en-US" : "fr-FR";
    return d.toLocaleDateString(locale, { day: "numeric", month: "long" });
  }

  function relativeTime(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    const diffH = (Date.now() - d.getTime()) / 36e5;
    if (diffH < 1) return t("time.lessThanHour");
    if (diffH < 24) return t("time.hours").replace("{n}", Math.floor(diffH));
    const diffD = Math.floor(diffH / 24);
    return t("time.days").replace("{n}", diffD);
  }

  function escapeHTML(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // ----------------------------------------------------------------------------
  // Rendering: orientation bar
  // ----------------------------------------------------------------------------
  function renderOrientationBar(orientations, opts = {}) {
    const showLabels = opts.showLabels !== false;
    const sorted = Object.entries(orientations || {}).sort((a, b) => b[1] - a[1]);

    if (sorted.length === 0) {
      return `
        <div class="orientation-bar">
          <div class="orientation-bar-track" style="background:var(--sand-200);">
            <div class="orientation-bar-segment" style="width:100%;background:var(--sand-300);"></div>
          </div>
          ${showLabels ? `<div class="orientation-labels"><span class="orientation-label" style="color:var(--ink-soft);font-style:italic;">${escapeHTML(t("story.unclassified"))}</span></div>` : ""}
        </div>`;
    }

    const total = sorted.reduce((sum, [, v]) => sum + v, 0) || 1;

    const segments = sorted.map(([id, value]) => {
      const meta = orientationById(id);
      const color = meta ? meta.color : "var(--ink-soft)";
      const pct = ((value / total) * 100).toFixed(1);
      const name = orientationName(meta) || id;
      return `<div class="orientation-bar-segment"
        style="width:${pct}%;background:${color};"
        title="${escapeHTML(name)} ${pct}%"></div>`;
    }).join("");

    const labels = showLabels ? sorted.slice(0, 3).map(([id, value]) => {
      const meta = orientationById(id);
      const color = meta ? meta.color : "var(--ink-soft)";
      const name = orientationName(meta) || id;
      const pct = Math.round((value / total) * 100);
      return `<span class="orientation-label">
        <span class="orientation-label-dot" style="background:${color}"></span>
        ${escapeHTML(name)} ${pct}%
      </span>`;
    }).join("") : "";

    return `
      <div class="orientation-bar">
        <div class="orientation-bar-track">${segments}</div>
        ${showLabels ? `<div class="orientation-labels">${labels}</div>` : ""}
      </div>`;
  }

  // ----------------------------------------------------------------------------
  // Rendering: media fallback when image missing or fails
  // ----------------------------------------------------------------------------
  function renderMediaFallback(story) {
    const sources = story.sources || [];
    const initials = sources.length
      ? (sources[0].logo_initials || sources[0].name.slice(0, 2)).toUpperCase()
      : "W";
    return `<div class="media-fallback"><span class="media-fallback-mark">${escapeHTML(initials)}</span></div>`;
  }

  // ----------------------------------------------------------------------------
  // Rendering: story card
  // ----------------------------------------------------------------------------
  function renderStoryCard(story, index = 0) {
    const sources = story.sources || [];
    const primaryUrl = sources[0] && sources[0].url ? sources[0].url : null;

    const sourcePills = sources.slice(0, 3).map(src => {
      const inner = `
        <span class="source-pill-mark">${escapeHTML(src.logo_initials || src.name.slice(0, 2).toUpperCase())}</span>
        ${escapeHTML(src.name)}
      `;
      return src.url
        ? `<a href="${escapeHTML(src.url)}" target="_blank" rel="noopener noreferrer" class="source-pill">${inner}</a>`
        : `<span class="source-pill">${inner}</span>`;
    }).join("");

    const blindspotClass = story.blindspot ? "is-blindspot" : "";
    const mediaContent = story.image_url
      ? `<img src="${escapeHTML(story.image_url)}" alt="" loading="lazy" onerror="this.parentElement.innerHTML=this.dataset.fallback" data-fallback='${renderMediaFallback(story).replace(/'/g, "&apos;")}' />`
      : renderMediaFallback(story);

    const sourceLabel = sources.length === 1 ? t("story.sources") : t("story.sourcesPlural");

    const titleEl = primaryUrl
      ? `<a href="${escapeHTML(primaryUrl)}" target="_blank" rel="noopener noreferrer" class="story-title-link"><h3 class="story-title">${escapeHTML(story.title)}</h3></a>`
      : `<h3 class="story-title">${escapeHTML(story.title)}</h3>`;

    const mediaLink = primaryUrl
      ? `<a href="${escapeHTML(primaryUrl)}" target="_blank" rel="noopener noreferrer" class="story-media-link" aria-hidden="true" tabindex="-1">${mediaContent}</a>`
      : mediaContent;

    return `
      <article class="story-card ${blindspotClass}" style="animation-delay:${index * 60}ms">
        <div class="story-media">${mediaLink}</div>
        <div class="story-body">
          <div class="story-meta">
            ${sourcePills}
            <span class="source-count">${sources.length} ${sourceLabel} · ${relativeTime(story.published_at)}</span>
          </div>
          ${titleEl}
          <p class="story-summary">${escapeHTML(story.summary || "")}</p>
          ${renderOrientationBar(story.orientations || {})}
        </div>
      </article>`;
  }

  // ----------------------------------------------------------------------------
  // Rendering: featured story
  // ----------------------------------------------------------------------------
  function renderFeatured(story) {
    if (!story) return "";
    const sources = story.sources || [];
    const primaryUrl = sources[0] && sources[0].url ? sources[0].url : null;

    const sourcePills = sources.slice(0, 4).map(src => {
      const inner = `
        <span class="source-pill-mark">${escapeHTML(src.logo_initials || src.name.slice(0, 2).toUpperCase())}</span>
        ${escapeHTML(src.name)}
      `;
      return src.url
        ? `<a href="${escapeHTML(src.url)}" target="_blank" rel="noopener noreferrer" class="source-pill">${inner}</a>`
        : `<span class="source-pill">${inner}</span>`;
    }).join("");

    const featuredEyebrow = escapeHTML(t("stories.featured"));
    const mediaContent = story.image_url
      ? `<img src="${escapeHTML(story.image_url)}" alt="" onerror="this.parentElement.innerHTML='<span class=\\'featured-eyebrow\\'>${featuredEyebrow}</span>'+this.dataset.fallback" data-fallback='${renderMediaFallback(story).replace(/'/g, "&apos;")}' />`
      : renderMediaFallback(story);

    const mediaLink = primaryUrl
      ? `<a href="${escapeHTML(primaryUrl)}" target="_blank" rel="noopener noreferrer" class="story-media-link" aria-hidden="true" tabindex="-1">${mediaContent}</a>`
      : mediaContent;

    const titleEl = primaryUrl
      ? `<a href="${escapeHTML(primaryUrl)}" target="_blank" rel="noopener noreferrer" class="story-title-link"><h2 class="featured-title">${escapeHTML(story.title)}</h2></a>`
      : `<h2 class="featured-title">${escapeHTML(story.title)}</h2>`;

    return `
      <div class="featured-media">
        <span class="featured-eyebrow">${featuredEyebrow}</span>
        ${mediaLink}
      </div>
      <div class="featured-body">
        <div class="story-meta" style="margin-bottom:16px">${sourcePills}</div>
        ${titleEl}
        <p class="featured-summary">${escapeHTML(story.summary || "")}</p>
        ${renderOrientationBar(story.orientations || {})}
      </div>`;
  }

  // ----------------------------------------------------------------------------
  // Rendering: briefing list
  // ----------------------------------------------------------------------------
  function renderBriefing(stories) {
    return stories.slice(0, 6).map(s => {
      const sources = s.sources || [];
      const url = sources[0] && sources[0].url;
      const inner = `<span class="briefing-title">${escapeHTML(s.title)}</span>`;
      return url
        ? `<li><a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer" class="briefing-link">${inner}</a></li>`
        : `<li>${inner}</li>`;
    }).join("");
  }

  // ----------------------------------------------------------------------------
  // Rendering: orientation legend (clickable filters with descriptions)
  // ----------------------------------------------------------------------------
  function renderOrientationLegend() {
    return STATE.orientations
      .filter(o => !o.secondary)
      .map(o => `
        <li>
          <button type="button" class="legend-item" data-orientation="${escapeHTML(o.id)}">
            <span class="orientation-swatch" style="background:${o.color}"></span>
            <span class="legend-text">
              <span class="legend-name">${escapeHTML(orientationName(o))}</span>
              <span class="legend-desc">${escapeHTML(orientationDesc(o) || "")}</span>
            </span>
          </button>
        </li>
      `).join("");
  }

  // ----------------------------------------------------------------------------
  // Rendering: dropdown items (Perspectives menu)
  // ----------------------------------------------------------------------------
  function renderDropdownItems() {
    return STATE.orientations
      .filter(o => !o.secondary)
      .map(o => {
        const desc = orientationDesc(o);
        const truncated = desc.length > 70 ? desc.slice(0, 70) + "…" : desc;
        return `
        <button type="button" class="dropdown-item" data-orientation="${escapeHTML(o.id)}">
          <span class="dropdown-dot" style="background:${o.color}"></span>
          <span class="dropdown-item-text">
            <span class="dropdown-item-name">${escapeHTML(orientationName(o))}</span>
            <span class="dropdown-item-desc">${escapeHTML(truncated)}</span>
          </span>
        </button>
      `;
      }).join("");
  }

  // ----------------------------------------------------------------------------
  // Rendering: blindspot panel
  // ----------------------------------------------------------------------------
  function renderBlindspots(stories) {
    const blindspots = stories.filter(s => s.blindspot);
    if (blindspots.length === 0) {
      return `<p class="panel-lede" style="color:rgba(247,241,229,0.5);font-style:italic;">${escapeHTML(t("blindspot.empty"))}</p>`;
    }
    const concentrationLabel = escapeHTML(t("blindspot.concentration"));
    return blindspots.slice(0, 3).map(s => {
      const score = Math.round((s.blindspot_score || 0) * 100);
      const sources = s.sources || [];
      const url = sources[0] && sources[0].url;
      const titleHtml = `<h4 class="blindspot-card-title">${escapeHTML(s.title)}</h4>`;
      const titleEl = url
        ? `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer" class="blindspot-card-link">${titleHtml}</a>`
        : titleHtml;
      return `
        <div class="blindspot-card">
          ${titleEl}
          ${s.blindspot_note ? `<p class="blindspot-card-note">${escapeHTML(s.blindspot_note)}</p>` : ""}
          <div class="blindspot-coverage">
            <span>${concentrationLabel} ${score}%</span>
            <div class="blindspot-bar"><div class="blindspot-bar-fill" style="width:${score}%"></div></div>
          </div>
        </div>`;
    }).join("");
  }

  // ----------------------------------------------------------------------------
  // Topic chips
  // ----------------------------------------------------------------------------
  function collectTopics(stories) {
    const counts = {};
    stories.forEach(s => (s.themes || []).forEach(t => {
      counts[t] = (counts[t] || 0) + 1;
    }));
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([t]) => t);
  }

  function renderTopicChips(topics) {
    if (topics.length === 0) {
      const fallback = ["AfCFTA", "Diaspora", "Sahel", "Climat", "Tech", "Souveraineté"];
      return fallback.map(t => `<button class="topic-chip" data-topic="${escapeHTML(t.toLowerCase())}">${escapeHTML(t)}</button>`).join("");
    }
    return topics.map(t => `<button class="topic-chip" data-topic="${escapeHTML(t)}">${escapeHTML(t)}</button>`).join("");
  }

  // ----------------------------------------------------------------------------
  // Orientation filters above the grid
  // ----------------------------------------------------------------------------
  function renderFilters() {
    const all = `<button class="filter-chip" data-orientation="">${escapeHTML(t("stories.allFilter"))}</button>`;
    const chips = STATE.orientations
      .filter(o => !o.secondary)
      .map(o => `<button class="filter-chip" data-orientation="${escapeHTML(o.id)}">${escapeHTML(orientationName(o))}</button>`)
      .join("");
    return all + chips;
  }

  // ----------------------------------------------------------------------------
  // Filter logic
  // ----------------------------------------------------------------------------
  function getFilteredStories() {
    let result = STATE.stories;
    if (STATE.activeOrientation) {
      result = result.filter(s => (s.orientations || {})[STATE.activeOrientation]);
    }
    if (STATE.activeTopic) {
      result = result.filter(s => (s.themes || []).includes(STATE.activeTopic));
    }
    if (STATE.searchQuery) {
      const q = STATE.searchQuery.toLowerCase();
      result = result.filter(s =>
        (s.title || "").toLowerCase().includes(q) ||
        (s.summary || "").toLowerCase().includes(q) ||
        (s.sources || []).some(src => src.name.toLowerCase().includes(q))
      );
    }
    return result;
  }

  // ----------------------------------------------------------------------------
  // Top-level rendering
  // ----------------------------------------------------------------------------
  function paint() {
    const filtered = getFilteredStories();

    const featured = filtered.find(s => !s.blindspot) || filtered[0];
    const featuredEl = document.getElementById("featured-story");
    if (featuredEl) featuredEl.innerHTML = featured ? renderFeatured(featured) : "";

    const rest = filtered.filter(s => !featured || s.id !== featured.id);
    const grid = document.getElementById("story-grid");
    if (grid) grid.innerHTML = rest.map((s, i) => renderStoryCard(s, i)).join("");

    const empty = document.getElementById("empty-state");
    if (empty) empty.hidden = filtered.length > 0;

    const briefing = document.getElementById("briefing-list");
    if (briefing) briefing.innerHTML = renderBriefing(STATE.stories);

    const dateEl = document.getElementById("briefing-date");
    if (dateEl) dateEl.textContent = formatDate(new Date().toISOString());

    const blindspotList = document.getElementById("blindspot-list");
    if (blindspotList) blindspotList.innerHTML = renderBlindspots(STATE.stories);

    const legendEl = document.getElementById("orientation-legend");
    if (legendEl) legendEl.innerHTML = renderOrientationLegend();

    const filtersEl = document.getElementById("orientation-filters");
    if (filtersEl) filtersEl.innerHTML = renderFilters();

    const dropdownEl = document.getElementById("perspectives-items");
    if (dropdownEl) dropdownEl.innerHTML = renderDropdownItems();

    syncOrientationActiveState();

    const topicEl = document.getElementById("topic-chips");
    if (topicEl) topicEl.innerHTML = renderTopicChips(collectTopics(STATE.stories));
  }

  function syncOrientationActiveState() {
    const active = STATE.activeOrientation || "";
    document.querySelectorAll("[data-orientation]").forEach(el => {
      if ((el.dataset.orientation || "") === active) {
        el.classList.add("is-active");
      } else {
        el.classList.remove("is-active");
      }
    });
  }

  function setActiveOrientation(orientation, opts = {}) {
    const next = orientation || null;
    STATE.activeOrientation = (STATE.activeOrientation === next) ? null : next;
    paint();

    if (opts.scroll !== false) {
      const target = document.getElementById("stories");
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function closeAllDropdowns() {
    document.querySelectorAll(".nav-dropdown.is-open").forEach(d => {
      d.classList.remove("is-open");
      const toggle = d.querySelector("[aria-expanded]");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    });
  }
  function toggleDropdown(dropdownEl) {
    const isOpen = dropdownEl.classList.contains("is-open");
    closeAllDropdowns();
    if (!isOpen) {
      dropdownEl.classList.add("is-open");
      const toggle = dropdownEl.querySelector("[aria-expanded]");
      if (toggle) toggle.setAttribute("aria-expanded", "true");
    }
  }

  // ----------------------------------------------------------------------------
  // Event wiring
  // ----------------------------------------------------------------------------
  function wireEvents() {
    document.addEventListener("click", (e) => {
      const langBtn = e.target.closest("#lang-toggle");
      if (langBtn) {
        e.preventDefault();
        setLanguage(STATE.lang === "fr" ? "en" : "fr");
        return;
      }

      const toggle = e.target.closest("#perspectives-toggle");
      if (toggle) {
        e.preventDefault();
        const dropdown = toggle.closest(".nav-dropdown");
        if (dropdown) toggleDropdown(dropdown);
        return;
      }

      const orientationEl = e.target.closest("[data-orientation]");
      if (orientationEl) {
        e.preventDefault();
        setActiveOrientation(orientationEl.dataset.orientation || null);
        closeAllDropdowns();
        return;
      }

      const topicChip = e.target.closest(".topic-chip");
      if (topicChip) {
        const topic = topicChip.dataset.topic || null;
        STATE.activeTopic = (STATE.activeTopic === topic) ? null : topic;
        document.querySelectorAll(".topic-chip").forEach(c => c.classList.remove("is-active"));
        if (STATE.activeTopic) topicChip.classList.add("is-active");
        paint();
        return;
      }

      if (!e.target.closest(".nav-dropdown")) {
        closeAllDropdowns();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeAllDropdowns();
    });

    const search = document.getElementById("search-input");
    if (search) {
      let timer;
      search.addEventListener("input", (e) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
          STATE.searchQuery = e.target.value.trim();
          paint();
        }, 180);
      });
    }
  }

  // ----------------------------------------------------------------------------
  // Boot
  // ----------------------------------------------------------------------------
  async function boot() {
    STATE.lang = getInitialLang();

    try {
      const [articlesData, orientationsData] = await Promise.all([
        fetchJSON(DATA_URL),
        fetchJSON(ORIENT_URL),
      ]);
      STATE.stories = articlesData.stories || [];
      STATE.orientations = orientationsData.orientations || [];
      applyTranslations();
      paint();
      wireEvents();
    } catch (err) {
      console.error("Boot failed:", err);
      applyTranslations();
      const grid = document.getElementById("story-grid");
      if (grid) {
        grid.innerHTML = `<div class="empty-state">${escapeHTML(t("story.loadFailed"))}</div>`;
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();