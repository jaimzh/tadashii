<script setup>
const promptExamples = [
  'An underdog story with satisfying character growth',
  'Something like Naruto, but do not recommend Naruto because I have seen it',
  'A relaxing slice-of-life anime with adult characters and little drama',
]

const questions = [
  {
    question: 'Why might I recognize a title under a different name?',
    answer:
      'Anime can have English, Romaji, and native Japanese titles. Open a result to see the available alternate names without changing the title shown on the result card.',
  },
  {
    question: 'Why are there ten recommendations?',
    answer:
      'Tadashii currently returns up to ten ranked recommendations. This keeps the list focused and avoids filling the final positions with weak matches.',
  },
  {
    question: 'Where is my Watch Later list stored?',
    answer:
      'Watch Later is stored locally in this browser. It is fast and does not require an account, but clearing browser storage or switching devices will not preserve the list.',
  },
  {
    question: 'Why did a search fail or take longer than usual?',
    answer:
      'Recommendations depend on external AI and anime-data services. A temporary 503 means the AI service is unavailable, while a 429 means the request limit was reached. Waiting briefly and trying again usually resolves either case.',
  },
]
</script>

<template>
  <main class="help-view">
    <header class="help-header">
      <p class="eyebrow">Guide</p>
      <h1>Help & information</h1>
      <p class="lede">
        Tadashii turns a natural-language description into a focused list of anime,
        with a match score and a reason for every recommendation.
      </p>
    </header>

    <section class="help-section" aria-labelledby="search-heading">
      <div class="section-number">01</div>
      <div class="section-content">
        <h2 id="search-heading">Describe what you actually want</h2>
        <p>
          Include the mood, story, character journey, genre, or pacing you care about.
          You can also name anime you liked and explicitly exclude titles you have seen.
        </p>
        <div class="examples">
          <p v-for="example in promptExamples" :key="example">“{{ example }}”</p>
        </div>
      </div>
    </section>

    <section class="help-section" aria-labelledby="results-heading">
      <div class="section-number">02</div>
      <div class="section-content">
        <h2 id="results-heading">Understand the results</h2>
        <p>
          The match score measures fit with your request—not general popularity or the
          MyAnimeList rating. Open a card for the full synopsis, alternate titles,
          airing information, trailer, and the option to save it for later.
        </p>
      </div>
    </section>

    <section class="help-section" aria-labelledby="recommendation-heading">
      <div class="section-number">03</div>
      <div class="section-content">
        <h2 id="recommendation-heading">How recommendations are made</h2>
        <p>
          Tadashii understands your intent, searches anime metadata through Jikan,
          removes unsuitable entries, and asks Gemini to rank a balanced shortlist.
          Franchise diversity helps prevent seasons and spin-offs from crowding out
          distinct recommendations.
        </p>
      </div>
    </section>

    <section class="help-section" aria-labelledby="future-heading">
      <div class="section-number">04</div>
      <div class="section-content">
        <h2 id="future-heading">What could come next</h2>
        <p>
          Tadashii is currently focused on anime, but its recommendation experience
          could grow in a few useful directions.
        </p>
        <ul class="future-list">
          <li>
            <strong>More kinds of stories</strong>
            <span>Discover cartoons and live-action series alongside anime.</span>
          </li>
          <li>
            <strong>Where to watch</strong>
            <span>Explore region-aware recommendations from services such as Netflix and Prime Video.</span>
          </li>
          <li>
            <strong>Recommendation feedback</strong>
            <span>Mark suggestions as helpful, irrelevant, or already seen so future rankings can better reflect your preferences.</span>
          </li>
        </ul>
        <p class="future-note">
          These are ideas being explored rather than confirmed release commitments.
        </p>
      </div>
    </section>

    <section class="faq" aria-labelledby="faq-heading">
      <p class="eyebrow">Common questions</p>
      <h2 id="faq-heading">A few useful details</h2>
      <div class="faq-list">
        <details v-for="item in questions" :key="item.question">
          <summary>{{ item.question }}</summary>
          <p>{{ item.answer }}</p>
        </details>
      </div>
    </section>

    <footer class="about-note">
      <strong>About the data</strong>
      <p>
        Anime facts come from MyAnimeList data provided through Jikan Edge. AI-generated
        scores and explanations are recommendations, not factual ratings. Tadashii does
        not host or stream anime.
      </p>
    </footer>
  </main>
</template>

<style scoped>
.help-view {
  width: min(100%, 820px);
  margin: 0 auto;
  padding: 3.5rem 0 5rem;
}

.help-header {
  max-width: 680px;
  margin-bottom: 4rem;
}

.eyebrow {
  margin-bottom: 0.45rem;
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

h1 {
  color: var(--text-main);
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 1.05;
  letter-spacing: -0.04em;
}

.lede {
  max-width: 62ch;
  margin-top: 1rem;
  color: var(--text-muted);
  font-size: var(--font-size-md);
}

.help-section {
  display: grid;
  grid-template-columns: 2.5rem minmax(0, 1fr);
  gap: 1.25rem;
  padding: 2rem 0;
  border-top: 1px solid var(--border-color);
}

.section-number {
  padding-top: 0.15rem;
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
}

.section-content h2,
.faq h2 {
  color: var(--text-main);
  font-size: var(--font-size-xl);
  line-height: 1.25;
}

.section-content > p,
.about-note p {
  max-width: 68ch;
  margin-top: 0.65rem;
  color: var(--text-muted);
}

.examples {
  display: grid;
  gap: 0.55rem;
  margin-top: 1.1rem;
}

.future-list {
  display: grid;
  gap: 0.9rem;
  margin-top: 1.2rem;
  list-style: none;
}

.future-list li {
  display: grid;
  gap: 0.15rem;
  padding-left: 0.9rem;
  border-left: 2px solid color-mix(in srgb, var(--accent) 45%, transparent);
}

.future-list strong {
  color: var(--text-main);
  font-size: var(--font-size-sm);
}

.future-list span,
.future-note {
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.section-content .future-note {
  margin-top: 1.25rem;
  font-size: var(--font-size-xs);
}

.examples p {
  padding-left: 0.9rem;
  border-left: 2px solid color-mix(in srgb, var(--accent) 55%, transparent);
  color: var(--text-main);
  font-size: var(--font-size-sm);
}

.faq {
  padding-top: 3.5rem;
}

.faq-list {
  margin-top: 1.25rem;
  border-top: 1px solid var(--border-color);
}

details {
  border-bottom: 1px solid var(--border-color);
}

summary {
  padding: 1.15rem 2rem 1.15rem 0;
  color: var(--text-main);
  font-weight: 600;
  cursor: pointer;
}

details p {
  max-width: 68ch;
  padding: 0 0 1.25rem;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.about-note {
  margin-top: 3.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  color: var(--text-main);
}

.about-note strong,
.about-note p {
  font-size: var(--font-size-sm);
}

@media (max-width: 600px) {
  .help-view {
    padding: 2.5rem 0 4rem;
  }

  .help-header {
    margin-bottom: 2.5rem;
  }

  .help-section {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>
