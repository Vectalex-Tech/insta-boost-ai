# InstaBoost AI (compliant)
Uma app (web) para **criar, embalar e publicar** conteúdo no Instagram com foco em **melhorar a tração inicial orgânica** — sem automações de spam, sem “pods”, sem contornar sistemas.

> ⚠️ Nota importante: esta app **não garante viralização**. Ela otimiza o que controlas: clareza do tema, hook, edição, copy, capa, variantes A/B e um “launch checklist”.
> Publicação e distribuição final dependem do Instagram e do comportamento real do público.

## O que está incluído (MVP funcional)
- Backend **FastAPI** com:
  - Upload de assets (imagem/vídeo/áudio) para armazenamento local (dev)
  - Geração de “packaging” com IA (hooks, texto no ecrã, legenda, CTA, keywords)
  - Jobs assíncronos (Celery + Redis) para “render” com FFmpeg
  - Integração **Instagram Graph API** para publicar (quando elegível)
- Frontend **Next.js**: fluxo simples de “prompt -> upload -> gerar -> render -> publicar”
- Docker Compose para rodar tudo localmente

## Requisitos para publicar via API (Meta)
- Conta **Instagram Professional (Business/Creator)** ligada a uma **Página**.
- App Meta + OAuth + permissões típicas: `pages_show_list`, `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, etc. (ver docs/links).
- Para publicar vídeo, a Meta precisa de um `video_url` **publicamente acessível** (S3/Cloud Storage). Localhost não serve em produção.

Referências (oficiais/Meta):
- Instagram API (Postman/Meta) e permissões necessárias: https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api
- Instagram Platform content publishing: https://developers.facebook.com/docs/instagram-platform/
- Limitações de Reels na API: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/

## Como correr localmente
1) Copia `.env.example` para `.env` e preenche o mínimo.
2) `docker compose up --build`
3) Abre o frontend em `http://localhost:3000`
4) API em `http://localhost:8000/docs`

## Deploy (produção)
- Backend: Render/Fly.io/AWS/GCP + Postgres + Redis
- Assets: S3 (ou equivalente) + URLs públicas (ou presigned com acesso público temporário)
- Frontend: Vercel/Netlify
- OAuth Meta: config em produção (redirect URIs, app review se necessário)

## Estrutura do repositório
- `backend/` FastAPI + Celery worker
- `frontend/` Next.js
- `docker-compose.yml` Orquestração local

## Licença
MIT
