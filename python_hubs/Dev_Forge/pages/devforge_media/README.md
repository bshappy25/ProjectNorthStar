# DevForge Home Reel (Runtime Media)

This folder is used at runtime by the DevForge Home page to store
uploaded images for the **Student Work Reel**.

## Important
- ❌ Do NOT commit student images
- ❌ Do NOT add JPEG/PNG files to the repo
- ✅ Images are uploaded **in-app** by admins only
- ✅ Files persist only on the server filesystem

## Used by
- `pages/home.py`
- Admin-only upload → staged → commit flow

## Deployment Notes
- On ephemeral hosts (e.g. Streamlit Community Cloud),
  images will reset on restart.
- On persistent servers, images remain until deleted in-app.

This folder is intentionally kept empty in the repository.
