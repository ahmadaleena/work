from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from helpers import handleNewURL, handle_short_url, originalURLExists
from urllib.parse import unquote

def configure_routes(app):
    @app.post("/shorten-url")
    def shorten_url(new_url: str):
        short_url = handleNewURL(new_url)
        return {"short_url": short_url}

    @app.get("/{short_url}")
    def redirect_to_original(short_url: str):
            original_url = handle_short_url(short_url)
            if original_url:
                return RedirectResponse(url=original_url, status_code=302)
            else:
                raise HTTPException(status_code=404, detail="URL not found")
            
    @app.get("/{original_url:path}")
    def get_hits(original_url: str):
        new_original_url = unquote(original_url)
        original_url = originalURLExists(new_original_url)
        if original_url:
            print("original url: ", original_url.original_url)
            return {f"hits for {original_url.original_url}": original_url.hits}
        else:
            print("Error, original_url not found")
            raise HTTPException(status_code=404, detail="URL not found")