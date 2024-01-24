from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from helpers import handleNewURL, handle_short_url, getHits

router = APIRouter()

@router.post("/shorten-url")
def shorten_url(new_url: str):
    short_url = "https://shorter-link.fly.dev/"
    short_url += handleNewURL(new_url)
    return {"short_url": short_url}

@router.get("/{short_url}")
def redirect_to_original(short_url: str):
        original_url = handle_short_url(short_url)
        if original_url:
            return RedirectResponse(url=original_url, status_code=302)
        else:
            raise HTTPException(status_code=404, detail="URL not found")
    
@router.get("/{short_url}/stats")
def get_hits(short_url: str):
    url_object = getHits(short_url)
    if url_object:
        print("original url: ", url_object.original_url, "short url:", url_object.short_url)
        return {f"hits for {url_object.short_url}": url_object.hits}
    else:
        print("Error, short url not found")
        raise HTTPException(status_code=404, detail="URL not found")