# Tadashii Frontend

The Tadashii frontend is a Vue 3 application for finding anime by mood, theme, or story preference. A user describes what they feel like watching, and the app presents AI-ranked recommendations from the Tadashii FastAPI backend.

## Features

- Natural-language anime search
- Random prompt suggestions with **Surprise me**
- Responsive recommendation cards and detailed result modals
- Match explanations, anime metadata, MyAnimeList links, and trailer lookup
- Animated loading screen with anime quotes cached in the browser for 24 hours
- Dark, light, and zen themes with saved preferences and matching favicons
- Responsive layouts for desktop and mobile
- Optional local mock recommendation data for UI development

## Tech Stack

- [Vue 3](https://vuejs.org/) with the Composition API
- [Vite](https://vite.dev/)
- [GSAP](https://gsap.com/) for animation
- [Phosphor Icons](https://phosphoricons.com/)

## Prerequisites

- Node.js `22.18+` or `24.12+`
- npm
- The Tadashii backend running locally, unless mock data is enabled

## Getting Started

From the `frontend` directory, install the dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Vite will print the local URL, which is usually `http://localhost:5173`.

### Connect to the backend

During local development, Vite proxies requests beginning with `/api` to:

```text
http://localhost:8000
```

Run the backend on that port from the repository root:

```powershell
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Alternatively, create `frontend/.env.local` and point the frontend directly at a backend running on another port:

```env
VITE_API_BASE_URL=http://127.0.0.1:8002
```

Restart the Vite development server after changing an environment file.

## Available Scripts

```powershell
npm run dev      # Start the Vite development server
npm run build    # Create an optimized production build in dist/
npm run preview  # Preview the production build locally
npm run format   # Format files under src/ with Prettier
```

## Application Flow

1. The user submits a natural-language prompt from the home screen.
2. The frontend sends the prompt to `POST /api/recommend`.
3. A loading view displays anime quotes while the backend builds recommendations.
4. The API response is normalized into frontend card data and displayed in a responsive grid.
5. Selecting a card opens a details modal and requests its trailer from `GET /api/anime/{mal_id}/trailer`.

The quote loader uses `GET /api/quotes/list` and caches valid quotes in `localStorage` for 24 hours.

## Project Structure

```text
frontend/
|-- public/                 Static assets
|-- src/
|   |-- api/client.js       Backend API client and mock-data switch
|   |-- assets/             Global styles and images
|   |-- components/common/  Shared UI components
|   |-- coposables/         Theme and anime-quote state
|   |-- data/               Surprise prompts and mock recommendations
|   |-- views/              Home and recommendation result views
|   |-- App.vue             Main application state and search flow
|   `-- main.js             Vue entry point
|-- index.html
|-- package.json
`-- vite.config.js          Vite plugins, aliases, and development proxy
```

> The `coposables` directory name is intentional in the current codebase. Keep imports aligned with it if it is renamed later.

## API Configuration

The frontend reads one optional environment variable:

| Variable | Purpose | Default |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Absolute backend URL used before every API path | Empty; requests use the current origin and the development proxy |

The frontend expects these backend endpoints:

| Method | Endpoint | Use |
| --- | --- | --- |
| `POST` | `/api/recommend` | Generate recommendations from a prompt |
| `GET` | `/api/anime/{mal_id}/trailer` | Fetch a trailer URL for a selected anime |
| `GET` | `/api/quotes/list` | Load quotes for the recommendation loading screen |

To develop the interface without the backend, set `USE_MOCK_DATA` to `true` in `src/api/client.js`. Recommendation and trailer requests will then use `src/data/mockRecommendations.js`; quote requests still require the backend.

## Production Build

Create and test a production build with:

```powershell
npm run build
npm run preview
```

The generated files are written to `dist/`. For deployment, either serve the frontend and API from the same origin or set `VITE_API_BASE_URL` to the public backend URL before running the build.

## Related Documentation

See [`../backend/README.md`](../backend/README.md) for backend configuration, API response shapes, and the recommendation pipeline.
