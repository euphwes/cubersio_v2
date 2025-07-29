from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cubersio.types import EventSlug

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_GLOBAL_SORT_ORDER = [
    # Weekly NxN
    EventSlug.EVENT_333,
    EventSlug.EVENT_222,
    EventSlug.EVENT_444,
    EventSlug.EVENT_555,
    EventSlug.EVENT_666,
    EventSlug.EVENT_777,
    # Weekly other
    EventSlug.SKEWB,
    EventSlug.PYRA,
    EventSlug.MEGA,
    EventSlug.FTO,
    EventSlug.SQ1,
    EventSlug.CLOCK,
    EventSlug.FMC,
    EventSlug.EVENT_3OH,
    # Weekly blind events
    EventSlug.EVENT_3BLD,
    EventSlug.EVENT_4BLD,
    EventSlug.EVENT_5BLD,
    EventSlug.MBLD,
    # Bonus
    EventSlug.KILO,
    EventSlug.MIRROR,
    EventSlug.REDI,
    EventSlug.DINO,
    EventSlug.REX,
    EventSlug.FIFTEEN,
    EventSlug.RELAY_234,
    EventSlug.EVENT_223,
    EventSlug.EVENT_332,
    EventSlug.EVENT_334,
    EventSlug.EVENT_335,
    EventSlug.EVENT_888,
    EventSlug.EVENT_999,
    EventSlug.EVENT_10X,
    EventSlug.BICUBE,
]


@app.get("/")
def read_root():
    return {
        "events": sorted(
            EventSlug,
            key=lambda slug: _GLOBAL_SORT_ORDER.index(slug),
        )
    }
