from pydantic import BaseModel

class RecommendRequest(BaseModel):
    prompt: str


class TrailerResponse(BaseModel):
    mal_id: int
    trailer_url: str | None = None
    title_japanese: str | None = None


class AnimeQuote(BaseModel):
    content: str
    character: str
    anime: str


class QuoteListResponse(BaseModel):
    anime: str
    quotes: list[AnimeQuote]


#alright so we need 2 models, our tadashii shape(animecandidate) and our final result
#clean factual data from jikan and ai

class AnimeCandidate(BaseModel):
    mal_id: int
    url: str | None = None

    title: str
    title_english: str | None = None
    title_japanese: str | None = None
    title_synonyms: list[str] = []

    type: str | None = None
    source: str | None = None
    episodes: int | None = None
    status: str | None = None
    airing: bool | None = None

    synopsis: str | None = None
    background: str | None = None

    season: str | None = None
    year: int | None = None
    rating: str | None = None
    score: float | None = None

    genres: list[str] = []
    explicit_genres: list[str] = []
    themes: list[str] = []
    demographics: list[str] = []
    studios: list[str] = []

    image: str | None = None
    trailer_url: str | None = None

    data_source: str = "jikan"

    
    
#final result form 
class RecommendationResult(BaseModel):
    anime: AnimeCandidate
    match_score: int
    reason: str
    emotion_tags: list[str] = []

