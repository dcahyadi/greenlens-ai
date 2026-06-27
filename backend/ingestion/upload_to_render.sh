#!/bin/bash
# Upload pre-built ChromaDB + documents to Render persistent disk
#
# Usage:
#   1. Run locally first: cd backend && python ingestion/indexer.py
#   2. Get SSH address from Render Dashboard → greenlens-api → Shell tab
#   3. export RENDER_SSH=ssh-xxxx@ssh.singapore.render.com
#   4. ./backend/ingestion/upload_to_render.sh

RENDER_SSH="${RENDER_SSH:-YOUR_RENDER_SSH_ADDRESS}"

if [ "$RENDER_SSH" = "YOUR_RENDER_SSH_ADDRESS" ]; then
  echo "❌ Set RENDER_SSH first: export RENDER_SSH=ssh-xxxx@ssh.singapore.render.com"
  exit 1
fi

echo "=== GreenLens — Uploading to Render disk ==="
echo "Target: $RENDER_SSH:/data"
echo ""

echo "📄 Uploading PDFs..."
rsync -avz --progress \
  data/documents/ "${RENDER_SSH}:/data/documents/"

echo ""
echo "🗄️  Uploading ChromaDB..."
rsync -avz --progress \
  backend/chroma_db/ "${RENDER_SSH}:/data/chroma_db/"

echo ""
echo "✅ Done! Verify with:"
echo "   ls /data/documents/ && ls /data/chroma_db/"
