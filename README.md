# Portfólio · Lucas Oliveira

Site estático (HTML + CSS + JS), em português (raiz) e inglês (`/en`).

## Editar

Os textos ficam no `build.py`, em pares (português, inglês). Os `.html` são gerados: não edite à mão.

```bash
python3 build.py          # gera home e páginas de case nos dois idiomas
python3 build.py --pdf    # também gera os currículos em PDF (usa o Google Chrome)
python3 -m http.server 8765   # para ver em http://localhost:8765
```

No topo do `build.py`:
- `GOATCOUNTER`: código do contador de visitas (goatcounter.com). Vazio = desligado.
- `TESTIMONIALS`: depoimentos. Lista vazia = seção escondida.

## Estrutura

- `index.html`, `cases/*.html`, `en/...`: páginas geradas
- `styles.css`, `main.js`: visual, animações, pausa dos vídeos e lightbox
- `assets/img`, `assets/video`: mídias otimizadas; `assets/*.pdf`: currículos
- `tools/reel.swift`: monta o showreel; `tools/pdfpages.swift`: renderiza páginas de PDF

Imagens do FlowBoard vêm sempre do Figma "FlowBoard · Telas" (dados fictícios), nunca do app logado.

Publicação: GitHub Pages, branch `main`, pasta raiz.
