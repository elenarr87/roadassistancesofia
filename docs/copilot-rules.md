# Правила за GitHub Copilot — Visual Studio / проект

Дата: 2026-01-18  
Автор: екип SEO & DevOps  
Актуализация: 2026-01-19 — добавени разширения за governance, performance, accessibility, privacy, security, CI и инструменти за локална валидация

Цел: дефиниране на шаблонни правила за използване на GitHub Copilot при генериране на съдържание и код за проекта. Фокус: максимални SEO & AI оптимизации, PageSpeed ≥ 90, валидни структурирани данни (JSON-LD), и абсолютна липса на SEO канибализъм при създаване на 13 подсайта.

Съдържание
- 1. Общи изисквания
- 2. PageSpeed / Performance (минимум 90)
- 3. JSON-LD йерархия — TEMPLATE & инструкции за екстракция/merge
- 4. ЧЗВ (FAQ) и schema
- 5. Ценова схема и оферти
- 6. Абсолютно избягване на канибализъм при 13 подсайта (subsites)
- 7. Как Copilot да генерира съдържание (шаблон)
- 8. CI / GitHub Actions (примерна стъпка)
- 9. Примери за commit message и branch
- 10. Допълнителни указания за Copilot (изпълнение)
- 11. Governance: content & prompt templates, review и lifecycle
- 12. Accessibility, Privacy & Security
- 13. Monitoring, testing, и observability
- Приложения: примерен JSON-LD, AggregateOffer, препоръчани скриптове и workflow примери
- Чеклист за PR и локални команди

--- 

## 1. Общи изисквания
- Всяка генерирана страница/шаблон трябва да има:
  - уникален `<title>` и `<meta name="description">` (не повтаряйте заглавия/описания).
  - семантичен HTML и валидна H-иерархия (H1 → H2 → H3).
  - `alt` за всички изображения, на български.
  - `<link rel="canonical">` към предпочитания URL.
  - локализация: `lang="bg"` и локализирани мета/структурни текстове.
- Кодировка (Encoding): всички файлове и промени да се записват в UTF-8. При промени чрез PowerShell винаги задавайте явна кодировка в cmdlet-ите, за да избегнете неочаквани символи.

  Примери (PowerShell):
  ```powershell
  # четене със специфична кодировка
  $content = Get-Content -Path .\index.html -Raw -Encoding UTF8
  # запис с UTF-8 (PowerShell 6+ поддържа 'utf8NoBOM')
  Set-Content -Path .\index.html -Value $content -Encoding UTF8
  # алтернатива при писане: Out-File
  $content | Out-File -FilePath .\index.html -Encoding UTF8
  # временна настройка на конзолата към UTF-8 кодова страница
  chcp 65001
  ```

  Забележка: при PowerShell 5.1 `-Encoding UTF8` често записва BOM; ако предпочитате без BOM използвайте PowerShell 6+/Core с `-Encoding utf8NoBOM` или инструмент, който контролира BOM изрично.
- Structured data (JSON-LD): задължително валиден (или валидни) скрипт(ове) — най-вече на `index.html`.
- CI: всеки PR трябва да минава автоматични проверки (Lighthouse, JSON-LD валидатор, duplicate-title checker).
- Copilot винаги да добавя TODO коментар, ако не може да извлече стойности от `index.html` или CMS.
- Забрана за автоматично публикуване на чувствителни/PII данни — използвайте placeholders и маркирайте с TODO.

---

## 2. PageSpeed / Performance (минимум 90)
- Critical CSS inlined; останал CSS зарежда асинхронно (rel="preload" as="style" + onload fallback).
- Снимки: webp/avif, srcset, sizes и `loading="lazy"`.
- Preconnect / dns-prefetch за външни ресурси (fonts, CDN).
- JS: defer/async; минимален initial bundle; code-splitting; SSR/prerender когато е възможно.
- HTTP кеширане, Brotli/gzip, CDN.
- CI job (GitHub Actions) да стартира Lighthouse и да блокира PR при score < 90 (mobile или desktop — според проектната цел).
- Performance budgets: дефинирани в `.lighthouserc` или `performance-budget.json` (max initial JS, max transfer MB, max main-thread ms).
- Fonts: `font-display: swap`, subsetting, system fallback stack.

---

## 3. JSON-LD йерархия — TEMPLATE и инструкции за екстракция/merge
Цел: Copilot автоматично да генерира/вмъква JSON-LD в `index.html` след екстракция на стойности.

Основни принципи:
- Използваме `@context: "https://schema.org"` и `@graph` за множествени взаимносвързани обекти (WebSite, LocalBusiness, WebPage, FAQPage, Offer и т.н.).
- Всеки node има уникален `@id` (URI + #fragment) — за лесни референции.
- AggregateOffer (диапазон цени) да е винаги отделен скрипт.

Инструкции за Copilot (екстракция и вмъкване)
1. Парсни локално `index.html` и извлечи (ако съществуват): title, meta description, canonical, телефон, адрес, основно изображение (`og:image`/hero img), списък с обслужвани зони (area-served), базови цени (min price) и ценови ставки на км.
2. Ако някое поле липсва — остави placeholder и добави коментар `/* TODO: fill from index.html or CMS */`.
3. Вмъкни/обнови в `index.html` един основен JSON-LD `<script type="application/ld+json">` с `@graph` (WebSite, LocalBusiness, WebPage) и след това отделен `<script type="application/ld+json">` с AggregateOffer (lowPrice=40, highPrice=500, currency=EUR).
4. Постави скриптовете в `<head>` (предпочитано) или преди `</body>`; увери се, че са валидни JSON.

Пример (съкратен шаблон — адаптирай чрез екстракция)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "WebSite", "@id": "https://example.com/#website", "url": "https://example.com/", "name": "Име" },
    { "@type": "LocalBusiness", "@id": "https://example.com/#organization", "name": "Име", "telephone": "+359..." },
    { "@type": "WebPage", "@id": "https://example.com/#homepage", "url": "https://example.com/", "isPartOf": { "@id": "https://example.com/#website" } }
  ]
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://example.com/#price-range",
  "name": "Диапазон цени",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": 40,
    "highPrice": 500,
    "priceCurrency": "EUR"
  }
}
</script>
```

Бележки при merge:
- Ако в `index.html` вече има JSON-LD:
  - ако има `@graph` — добави missing nodes или актуализирай чрез референции (`@id`),
  - не презаписвай основен блок без одобрение; винаги прави backup/коментар.
- Валидация: Google Rich Results Test + локален JSON-LD валидатор в CI.

---

## 4. ЧЗВ (FAQ) и schema
- Генерирай `FAQPage` JSON-LD, използвайки въпроси/отговори от `index.html` (ако има) или шаблонни въпроси.
- Поставяй `FAQPage` в `@graph` или като отделен скрипт и свързвай `WebPage.mainEntity` към `FAQPage.@id`.
- `mainEntity` трябва да е масив от `Question` обекти. CI да валидира тази структура.

---

## 5. Ценова схема и оферти
- Базова минимална цена в шаблона: 40 EUR; максимална цена: 500 EUR.
- Ако офертите са на км — използвайте `UnitPriceSpecification` с numeric `price` и `minPrice`.
- В JSON-LD офертите да съдържат `priceCurrency: "EUR"`. CI да валидира `lowPrice ≤ highPrice`.
- Всеки `Offer` да има уникален `@id`.

Пример за Offer node (със UnitPriceSpecification):
```json
{
  "@type": "Offer",
  "@id": "https://example.com/#offer-light-vehicle",
  "name": "Репатрак услуги - Леки МПС",
  "priceCurrency": "EUR",
  "priceSpecification": {
    "@type": "UnitPriceSpecification",
    "price": 0.80,
    "priceCurrency": "EUR",
    "unitText": "km",
    "minPrice": 40
  },
  "availability": "https://schema.org/InStock"
}
```

---

## 6. Абсолютно избягване на канибализъм при 13 подсайта (subsites)
Checklist (задължително за всеки подсайт/subdomain/subfolder):
- Уникален primary keyword и вторични keywords — запис в `content-plan.json`.
- Уникален `<title>` и `<meta description>`; автоматичен duplicate-title checker в CI.
- Canonical: ако подсайт е mirror, задайте canonical към предпочитания URL.
- robots.txt & sitemap.xml за всеки подсайт/гранулирана sitemap стратегия.
- Тематична и гео разделеност: всеки подсайт покрива строго определена гео/нишова тема.
- URL шаблон: `/ {region}/{service}/{slug}`.
- Content frontmatter (YAML/JSON) да съдържа: `primary_keyword`, `geo_scope`, `canonical`, `template_version`.
- CI: similarity check (shingling или cosine sim на текст), блокиране при similarity > конфигурируем threshold.

---

## 7. Как Copilot да генерира съдържание (шаблон)
- Branch suggestion: `feature/copilot/content-{page-slug}`
- Commit message suggestion: `chore(content): add {page-slug} content + json-ld`
- Структура за съдържание:
  - unique title (≤ 60 chars)
  - meta description (150–160 chars)
  - H1 (primary keyword)
  - Intro (50–100 words)
  - H2: услуги / предимства / как работи
  - H3: ценова таблица / FAQ
  - CTA: телефон + link to booking
  - JSON-LD insertion point: коментар `<!-- JSON-LD: insert here -->` в head
- Copilot prompts: дефинирайте и съхранявайте шаблони за prompt-ове в `/docs/copilot-prompts.md`. В PR описанието посочвайте кой prompt е използван и кои стойности са извлечени автоматично.

---

## 8. CI / GitHub Actions (примерна стъпка)
Примерен job `.github/workflows/lighthouse-and-schema.yml` (съкратено описание):
- checkout
- setup-node
- serve static site / use preview URL
- run lighthouse-ci (mobile & desktop) assert score >= 90 per categories (Performance, Accessibility, Best Practices, SEO)
- validate JSON-LD (npm script: `node scripts/validate-jsonld.js`)
- duplicate-title/content checker
- axe-core accessibility checks

Примерни npm scripts:
- "ci:test:perf": "lhci autorun --config=./.lighthouserc.js"
- "ci:test:jsonld": "node scripts/validate-jsonld.js"

(Конкретни workflow и скриптове са в Приложенията/Артефактите).

---

## 9. Примери за commit message и branch
- Branch: `feature/copilot/jsonld-price-range`  
- Commit: `feat(json-ld): add aggregate priceRange (40-500 EUR) and base @graph template`  
- PR title: `Добавяне: Copilot правила и JSON-LD шаблони — priceRange + homepage schema`

---

## 10. Допълнителни указания за Copilot (изпълнение)
- Винаги добавяй TODO placeholders, когато информация липсва (напр. email).
- Преди merge: ръчна проверка от SEO специалист за заглавия/каноникал/ключови думи.
- Не публикувай чувствителни данни; използвай placeholders.
- Логвайте в PR описание кои стойности са извлечени от `index.html` и кои са placeholders.

---

## 11. Governance: content & prompt templates, review и lifecycle
- Content lifecycle: ревизия на съдържание на всеки 6 месеца; frontmatter полета: `last_reviewed`, `content_owner`, `content_tier`.
- Content-plan: централен `content-plan.json` с всички pages/subsites/owners/keywords.
- Pre-commit hooks: lint, prettier, simple duplicate-title static check.
- PR template (задължително): checklist (duplicate-title, JSON-LD validate, Lighthouse report, accessibility report, content owner sign-off).
- Prompt governance: всички Copilot prompts да се съхраняват и версионират в `/docs/copilot-prompts.md`. Всеки PR с Copilot съдържание да посочва използвания prompt.

---

## 12. Accessibility, Privacy & Security
Accessibility:
- Даваме приоритет на WCAG 2.1 AA: color contrast ≥ 4.5:1, keyboard navigation, visible focus indicators.
- Автоматични тестове: `axe-core` run в CI и отчет; блокиране при критични проблеми.
- Skip-to-content link; landmark roles; aria-labels за сложни UI компоненти.

Privacy & GDPR:
- Consent management за analytics; блокиране на tracking докато consent не е даден.
- Никакво автоматично инжектиране на PII от Copilot — placeholders и TODO задължително.
- Log retention & preview URLs: не съхранявайте чувствителни данни.

Security:
- Задължителни security headers: CSP (report-uri), HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
- Secrets via GitHub Secrets; rotate keys периодично.
- Dependency scanning: Dependabot + SCA.
- Не включвайте API keys/credentials в публични файлове или JSON-LD.

---

## 13. Monitoring, testing, и observability
- Search Console / Bing Webmaster: автоматични проверки и alerting за coverage/schema errors.
- SEO monitoring: periodic rank tracking за primary keywords, alert при drop > X positions.
- Error & uptime: Sentry/Datadog for front-end errors; uptime checks за критични страници.
- Broken link checker: CI или scheduled job.
- Visual regression: Percy / Playwright snapshot testing.
- E2E smoke tests: критични flows (контакт, booking, CTA).

---

## Приложения / Препоръчани артефакти (за локална работа)
1. Обновен Markdown с правилата (този файл).
2. scripts/validate-jsonld.js — Node скрипт (парсва index.html, валидира JSON-LD структури, numeric checks).
3. scripts/extract-jsonld.js — Node помощен скрипт (генерира draft JSON-LD попълнен от извлечени стойности).
4. Примерен updated-index.html (шаблон) — включва `<!-- JSON-LD: insert here -->` и draft JSON-LD с TODO placeholders.
5. .github/workflows/lighthouse-and-schema.yml — примерен workflow (за по-къснa употреба).
6. docs/copilot-prompts.md — събира всички дефинирани prompt шаблони.
7. README.md — кратко ръководство за локално изпълнение (инсталация и команди).

Примерни локални команди
- npm init -y
- npm i jsdom ajv axios minimist
- node scripts/extract-jsonld.js --input=./index.html --output=./draft-jsonld.json
- node scripts/validate-jsonld.js --input=./index.html
- npx lhci autorun --config=./.lighthouserc.js

---

## Чеклист за PR (задължителен)
- [ ] Duplicate title check (всички title са уникални).
- [ ] JSON-LD валидирано успешно (`node scripts/validate-jsonld.js`).
- [ ] Lighthouse report (Performance, Accessibility, Best Practices, SEO ≥ 90).
- [ ] Accessibility axe report (без критични проблеми).
- [ ] Content owner review и sign-off.
- [ ] Content frontmatter записан в `content-plan.json`.
- [ ] Всички placeholders и TODO са описани в PR description.
- [ ] Ако е променен `@graph` — snapshot/backup на предишния JSON-LD е приложен.

---

Финални бележки:
- Този документ е основен шаблон. Локалните CI скриптове и скриптовете за екстракция/валидация трябва да се имплементират в `scripts/` и да следват указанията тук.
- За всяка автоматична промяна, генерирана от Copilot, изисквайте ръчно одобрение преди публикуване на production.
