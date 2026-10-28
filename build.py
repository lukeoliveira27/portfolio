#!/usr/bin/env python3
"""Gera o site em português (raiz) e em inglês (/en): home, páginas de case e currículo.

Uso: python3 build.py          (gera os HTML)
     python3 build.py --pdf    (gera também os currículos em PDF, com o Google Chrome)

Edite os textos aqui, nunca nos .html gerados. Cada texto é um par (português, inglês).
"""
import html
import os
import subprocess
import sys

SITE = "https://lukeoliveira27.github.io/portfolio"
EMAIL = "lucasoliveira270701@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/lucasantosoliveira/"
BEHANCE = "https://www.behance.net/lucasoliveira107"
YOUTUBE = "https://www.youtube.com/@lukizitos"
# Código do GoatCounter (ex.: "lucasoliveira"). Vazio = sem contador de visitas.
GOATCOUNTER = ""
# Depoimentos: lista de (frase_pt, frase_en, nome, cargo_pt, cargo_en). Vazio = seção some.
TESTIMONIALS = []

ROOT = os.path.dirname(os.path.abspath(__file__))
LANG = "pt"


def L(pair):
    """Escolhe o texto do idioma atual."""
    if isinstance(pair, tuple):
        return pair[0] if LANG == "pt" else pair[1]
    return pair


def e(pair):
    return html.escape(L(pair), quote=True)


# ---------------------------------------------------------------- textos gerais

UI = {
    "works": ("Trabalhos", "Work"),
    "about": ("Sobre", "About"),
    "talk": ("Vamos conversar", "Let's talk"),
    "skip": ("Pular para os trabalhos", "Skip to work"),
    "see_case": ("Ver case completo", "See full case"),
    "see_live": ("Ver site no ar", "See it live"),
    "back": ("Todos os trabalhos", "All work"),
    "next": ("Próximo case", "Next case"),
    "role": ("Meu papel", "My role"),
    "deliv": ("Entregas", "Deliverables"),
    "tools": ("Ferramentas", "Tools"),
    "year": ("Ano", "Year"),
    "challenge": ("O desafio", "The challenge"),
    "process": ("O processo", "The process"),
    "result": ("O resultado", "The outcome"),
    "cv": ("Baixar currículo (PDF)", "Download résumé (PDF)"),
    "cv_file": ("curriculo-lucas-oliveira.pdf", "resume-lucas-oliveira.pdf"),
    "pause": ("Pausar vídeo", "Pause video"),
    "play": ("Tocar vídeo", "Play video"),
    "zoom": ("Ampliar", "Enlarge"),
    "close": ("Fechar", "Close"),
    "made": ("feito com muito ☕ e o Eddie no colo", "made with lots of ☕ and Eddie on my lap"),
}


def nav(prefix, home):
    other = "en/" if LANG == "pt" else ""
    # link para a mesma página no outro idioma
    return f"""<header class="nav">
  <a href="{home}#topo" class="nav__name">Lucas Oliveira</a>
  <nav aria-label="{e(('Principal', 'Main'))}">
    <a href="{home}#trabalhos">{e(UI['works'])}</a>
    <a href="{home}#motion">Motion</a>
    <a href="{home}#sobre">{e(UI['about'])}</a>
    <a class="nav__lang" href="{{LANG_SWITCH}}" hreflang="{'en' if LANG == 'pt' else 'pt-BR'}" lang="{'en' if LANG == 'pt' else 'pt-BR'}">{'EN' if LANG == 'pt' else 'PT'}</a>
    <a href="{home}#contato" class="nav__cta">{e(UI['talk'])}</a>
  </nav>
</header>"""


def head(prefix, title, desc, canonical_path, alt_path):
    og = "og.jpg" if LANG == "pt" else "og-en.jpg"
    gc = (f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
          if GOATCOUNTER else "")
    pt_url = SITE + "/" + (canonical_path if LANG == "pt" else alt_path)
    en_url = SITE + "/" + (alt_path if LANG == "pt" else canonical_path)
    return f"""<!doctype html>
<html lang="{'pt-BR' if LANG == 'pt' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}/{canonical_path}">
<link rel="alternate" hreflang="pt-BR" href="{pt_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}/{canonical_path}">
<meta property="og:image" content="{SITE}/assets/img/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;600&family=Caveat:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}styles.css">
{gc}
</head>"""


def foot(prefix):
    return f"""<footer class="foot wrap">
  <span>© 2026 Lucas Oliveira</span>
  <span class="hand">{e(UI['made'])}</span>
</footer>

<dialog class="lightbox" aria-label="{e(UI['zoom'])}">
  <button class="lightbox__close" aria-label="{e(UI['close'])}">×</button>
  <img alt="">
</dialog>

<script>window.I18N = {{ pause: "{e(UI['pause'])}", play: "{e(UI['play'])}", zoom: "{e(UI['zoom'])}" }};</script>
<script src="{prefix}main.js"></script>
</body>
</html>
"""


def video(prefix, name, label, extra=""):
    return (f'<video src="{prefix}assets/video/{name}.mp4" poster="{prefix}assets/img/poster-{name}.webp" '
            f'muted loop playsinline preload="none" aria-label="{e(label)}"{extra}></video>')


def img(prefix, src, alt, extra=""):
    return f'<img src="{prefix}assets/img/{src}" alt="{e(alt)}" loading="lazy"{extra}>'


def browser(url):
    return f'<div class="browser"><span></span><span></span><span></span><b>{url}</b></div>'


# ---------------------------------------------------------------- cases

CASES = [
    {
        "slug": "flowboard",
        "theme": "flow",
        "client": ("Produto autoral · 2026", "Personal product · 2026"),
        "title": "FlowBoard",
        "summary": (
            "Plataforma de gestão de demandas que eu idealizei, desenhei e programei. Nasceu para organizar o time de "
            "Comunicação do Talenses Group e virou produto: board, daily, calendário editorial, planejamentos, portal de "
            "chamados e recursos de foco que cada pessoa liga só se quiser. Também fiz a marca, o design system, o site e os e-mails.",
            "A work management platform I conceived, designed and coded. It started as a way to organise Talenses Group's "
            "Communications team and grew into a product: board, daily, editorial calendar, plans, a request portal and focus "
            "features each person can switch on if they want. I also made the brand, design system, website and emails."),
        "tags": [("Produto", "Product"), ("UI/UX", "UI/UX"), ("Design system", "Design system"), ("Código", "Code")],
        "link": "https://useflowboard.com/",
        "link_label": ("Conhecer o FlowBoard", "Visit FlowBoard"),
        "note": ("use FlowBoard nos seus dias úteis ;)", "useful on every working day ;)"),
        "role": ("Ideia, produto, UX/UI, marca e desenvolvimento", "Concept, product, UX/UI, brand and development"),
        "deliv": ("App web e celular, site, portal de chamados, design system, e-mails do sistema",
                  "Web and mobile app, website, request portal, design system, system emails"),
        "tools": "Figma · React · TypeScript · Replit",
        "cover": ("fb-kanban.webp", ("Board do FlowBoard em kanban", "FlowBoard board in kanban view")),
        "challenge": [
            ("O time de Comunicação atende sete marcas do grupo ao mesmo tempo. Os pedidos chegavam por e-mail, Teams e "
             "conversa de corredor, e ninguém tinha uma visão única do que estava atrasado, em aprovação ou parado.",
             "The Communications team serves seven group brands at once. Requests came in by email, Teams and hallway "
             "chats, and nobody had a single view of what was late, waiting for approval or stuck."),
            ("As ferramentas prontas ou eram genéricas demais, ou viravam mais um sistema para alimentar. Eu queria algo "
             "que organizasse o trabalho sem pesar, inclusive para quem se distrai fácil ou trava na hora de começar.",
             "Off-the-shelf tools were either too generic or became one more system to feed. I wanted something that "
             "organised the work without weighing it down, including for people who get distracted easily or struggle to get started."),
        ],
        "process": [
            {
                "text": [
                    ("Comecei pela demanda como centro de tudo: board, tabela, calendário, daily e projetos são só jeitos "
                     "diferentes de olhar a mesma coisa. Cada nova tela precisa se ligar às demandas, em vez de virar um sistema à parte.",
                     "I started by making the request the centre of everything: board, table, calendar, daily and projects are "
                     "just different ways of looking at the same thing. Every new screen has to connect to requests instead of becoming a separate system."),
                ],
                "figs": [("wide", "fb-daily.webp", ("Daily do time, com as demandas do dia por pessoa", "Team daily, with each person's tasks for the day"))],
            },
            {
                "text": [
                    ("Criei a identidade “grafite e céu”: grafite, azul-céu e bege, com um laranja que aparece só em detalhes "
                     "da marca. As cores de status (verde, âmbar, azul, cinza e vermelho) ficam fixas e nunca se misturam com a marca.",
                     "I created the “graphite and sky” identity: graphite, sky blue and beige, with an orange used only in small brand "
                     "details. Status colours (green, amber, blue, grey and red) are fixed and never mixed with the brand."),
                    ("Tudo virou um design system no Figma, com variáveis de modo claro e escuro espelhando o código.",
                     "Everything became a Figma design system, with light and dark mode variables mirroring the code."),
                ],
                "figs": [("wide", "fb-fundamentos.webp", ("Fundamentos do design system: cores, textos e espaçamentos", "Design system foundations: colours, type and spacing"))],
            },
            {
                "text": [
                    ("Os recursos de foco são opcionais e descritos por situação, sem rótulos: avisos gentis, sugestões, modo "
                     "calmo e leitura confortável. Cada pessoa liga só o que ajuda.",
                     "Focus features are optional and described by situation, without labels: gentle nudges, suggestions, calm "
                     "mode and comfortable reading. Each person switches on only what helps."),
                ],
                "figs": [
                    ("two", "fb-avisos.webp", ("Demanda aberta com avisos gentis e sugestões", "Open task with gentle nudges and suggestions")),
                    ("phone", "fb-foco.webp", ("Configurações de foco e bem-estar no celular", "Focus and wellbeing settings on mobile")),
                ],
            },
        ],
        "result_text": [
            ("Hoje o FlowBoard organiza o dia a dia do time, do pedido que chega até a entrega, e tem site próprio, "
             "planos e e-mails transacionais.",
             "Today FlowBoard runs the team's daily work, from incoming request to delivery, and has its own website, "
             "plans and transactional emails."),
        ],
        "facts": [("7", ("marcas do grupo num só board", "group brands on a single board")),
                  ("120+", ("telas desenhadas no Figma", "screens designed in Figma")),
                  ("11", ("e-mails do sistema", "system emails")),
                  ("2", ("temas: claro e escuro", "themes: light and dark"))],
        "gallery": [
            ("wide", "fb-site.webp", ("Site do FlowBoard", "FlowBoard website"), "useflowboard.com"),
            ("half", "fb-kanban-dark.webp", ("Board no modo escuro", "Board in dark mode"), None),
            ("half", "fb-email.webp", ("E-mail de resumo diário", "Daily digest email"), None),
        ],
    },
    {
        "slug": "board-circle",
        "theme": "board",
        "client": ("Talenses Executive × FTI Consulting · 2026", "Talenses Executive × FTI Consulting · 2026"),
        "title": "Board Circle",
        "summary": (
            "Identidade visual completa para o Board Circle, iniciativa de governança e conselhos. Criei a marca e "
            "desdobrei para o book “Conselho que Gera Valor”, save the date, convite, papelaria do evento de lançamento e o loop de telão.",
            "Full visual identity for Board Circle, a governance and boards initiative. I created the brand and rolled it "
            "out to the book “Conselho que Gera Valor”, save the date, invitation, launch event stationery and the screen loop."),
        "tags": [("Identidade visual", "Visual identity"), ("Editorial", "Editorial"), ("Evento", "Event"), ("Motion", "Motion")],
        "link": None,
        "role": ("Identidade visual, design editorial e peças do evento", "Visual identity, editorial design and event pieces"),
        "deliv": ("Marca, book digital e impresso, convite, save the date, papelaria, loop de telão e posts",
                  "Brand, digital and print book, invitation, save the date, stationery, screen loop and posts"),
        "tools": "Illustrator · InDesign · Photoshop · After Effects",
        "cover": ("bc-convite.webp", ("Convite do Board Circle Experience", "Board Circle Experience invitation")),
        "challenge": [
            ("A Talenses Executive e a FTI Consulting queriam lançar uma iniciativa para conselheiros e executivos de alto "
             "nível. A marca precisava ter a sobriedade de um conselho de administração, sem parecer fria ou burocrática.",
             "Talenses Executive and FTI Consulting wanted to launch an initiative for board members and senior executives. "
             "The brand had to carry the sobriety of a boardroom without feeling cold or bureaucratic."),
            ("Além da marca, era preciso entregar um book de conteúdo e todo o material do evento de lançamento, "
             "em 27 de outubro de 2026, com prazo de gráfica.",
             "Beyond the brand, the job included a content book and every piece for the launch event on 27 October 2026, "
             "all on print deadlines."),
        ],
        "process": [
            {
                "text": [
                    ("A marca combina uma serifa clássica com um símbolo de pontos que formam um círculo. A paleta fica no "
                     "azul-grafite, com dourado em detalhes, e o mesmo padrão de pontos vira grafismo em todas as peças.",
                     "The brand pairs a classic serif with a symbol of dots forming a circle. The palette sits in graphite blue "
                     "with gold accents, and the same dot pattern becomes a graphic device across every piece."),
                ],
                "figs": [("logo", "bc-logo.png", ("Logotipo Board Circle", "Board Circle logo"))],
            },
            {
                "text": [
                    ("O book “Conselho que Gera Valor” tem 24 páginas e passou por 21 versões até a prova de gráfica final. "
                     "Montei um sistema editorial com capítulos numerados, aberturas escuras, destaques de dados e citações.",
                     "The book “Conselho que Gera Valor” has 24 pages and went through 21 versions up to the final press proof. "
                     "I built an editorial system with numbered chapters, dark openers, data highlights and pull quotes."),
                ],
                "figs": [("wide", "bc-book-pages.webp", ("Páginas do book: capa, índice, capítulo e dados", "Book pages: cover, contents, chapter and data"))],
            },
            {
                "text": [
                    ("Para o evento, a identidade foi para o convite (cinco versões), o save the date, os displays de mesa, "
                     "crachás, backdrop, ecobag e a tag do azeite de presente, além do loop animado do telão.",
                     "For the event, the identity went into the invitation (five versions), the save the date, table displays, "
                     "badges, backdrop, tote bag and the gift olive oil tag, plus the animated screen loop."),
                ],
                "figs": [
                    ("third", "bc-std.webp", ("Save the date", "Save the date")),
                    ("third", "bc-ecobag.webp", ("Ecobag", "Tote bag")),
                    ("third", "bc-azeite.webp", ("Porta-azeite", "Olive oil holder")),
                    ("wide", "bc-mesas.webp", ("Displays de mesa de 01 a 06", "Table displays 01 to 06")),
                ],
            },
        ],
        "result_text": [
            ("A marca estreou no evento de lançamento, com uma linguagem visual única do convite ao telão, e o book "
             "segue como material de relacionamento com conselheiros.",
             "The brand debuted at the launch event with one visual language from invitation to big screen, and the book "
             "lives on as a relationship piece for board members."),
        ],
        "facts": [("21", ("versões do book até a gráfica", "book versions up to print")),
                  ("24", ("páginas de conteúdo", "pages of content")),
                  ("5", ("versões do convite", "invitation versions")),
                  ("10+", ("peças para o evento", "pieces for the event"))],
        "video": ("bc-loop", ("Loop animado do telão do evento", "Animated event screen loop")),
        "gallery": [
            ("half", "bc-book-li.webp", ("Divulgação do book no LinkedIn", "Book announcement for LinkedIn"), None),
            ("half", "bc-book-li-v.webp", ("Post vertical do book", "Vertical book post"), None),
        ],
    },
    {
        "slug": "summer-job-moove",
        "theme": "moove",
        "client": ("Mappit × Moove · 2026", "Mappit × Moove · 2026"),
        "title": "Summer Job Moove",
        "summary": (
            "Landing page bilíngue (PT/EN) para o programa de férias da Moove, voltado a brasileiros que estudam no exterior. "
            "Fiz o design, o código, o SEO e o kit de lançamento: e-mails marketing, peças estáticas e motion para redes.",
            "Bilingual (PT/EN) landing page for Moove's summer programme for Brazilians studying abroad. I did the design, "
            "code, SEO and launch kit: marketing emails, static pieces and motion for social."),
        "tags": [("Landing page", "Landing page"), ("Código", "Code"), ("E-mail mkt", "Email"), ("Social + motion", "Social + motion")],
        "link": "https://summerjobmoovelub.com/",
        "role": ("Design, desenvolvimento, SEO e kit de lançamento", "Design, development, SEO and launch kit"),
        "deliv": ("Landing page PT/EN, 2 e-mails, peças de feed, stories e horizontal, motion em 3 formatos",
                  "PT/EN landing page, 2 emails, feed, stories and landscape pieces, motion in 3 formats"),
        "tools": "Figma · HTML/CSS/JS · Replit · After Effects",
        "cover": ("moove-lp-topo.webp", ("Topo da landing page no computador", "Landing page hero on desktop")),
        "challenge": [
            ("A Moove, uma das maiores empresas de lubrificantes da América do Sul, queria atrair estudantes brasileiros "
             "em universidades no exterior para 6 a 8 semanas de imersão nas férias. A Mappit conduz a seleção.",
             "Moove, one of South America's largest lubricant companies, wanted to attract Brazilian students at universities "
             "abroad for a 6 to 8 week summer immersion. Mappit runs the selection."),
            ("O público lê em dois idiomas, decide pelo celular e precisava entender o programa e chegar à inscrição em poucos cliques.",
             "The audience reads in two languages, decides on their phone and needed to understand the programme and reach "
             "the application in a few taps."),
        ],
        "process": [
            {
                "text": [
                    ("Segui o brandbook da Moove (DM Sans, verde-limão e azul oficiais) e organizei a página como uma conversa: "
                     "quem é a Moove, o que é o programa, perfil, o que você ganha, etapas e dúvidas.",
                     "I followed Moove's brandbook (DM Sans, official lime green and blue) and structured the page as a conversation: "
                     "who Moove is, what the programme is, profile, what you get, steps and FAQ."),
                ],
                "figs": [
                    ("two", "moove-lp-07.webp", ("Seção de perfil e benefícios", "Profile and benefits section")),
                    ("phone", "moove-lp-mobile.webp", ("Topo no celular", "Mobile hero")),
                ],
            },
            {
                "text": [
                    ("Programei o site em HTML, CSS e JavaScript puros, com a versão em inglês gerada automaticamente a partir "
                     "da página em português, modo claro e escuro, testes automáticos, cabeçalhos de segurança e links com UTM "
                     "em cada botão para medir de onde vem cada inscrição.",
                     "I coded the site in plain HTML, CSS and JavaScript, with the English version generated automatically from "
                     "the Portuguese page, light and dark mode, automated tests, security headers and UTM links on every button "
                     "to track where each application comes from."),
                ],
                "figs": [("wide", "moove-lp-en.webp", ("Versão em inglês da página", "English version of the page"))],
            },
            {
                "text": [
                    ("O kit de lançamento usa a mesma linguagem: dois e-mails (um para a base e um para estudantes no exterior), "
                     "peças para feed, stories e horizontal, e o motion nos três formatos.",
                     "The launch kit speaks the same language: two emails (one for the general base and one for students abroad), "
                     "feed, stories and landscape pieces, and motion in all three formats."),
                ],
                "figs": [
                    ("third", "moove-feed.webp", ("Post de feed", "Feed post")),
                    ("third", "moove-stories.webp", ("Stories", "Stories")),
                    ("third", "moove-email.webp", ("E-mail de divulgação", "Announcement email")),
                ],
            },
        ],
        "result_text": [
            ("Do briefing da Moove ao site no ar foram sete dias, já com a revisão do cliente incorporada e a página publicada no domínio oficial.",
             "It took seven days from Moove's brief to the live site, client review included, published on the official domain."),
        ],
        "facts": [("7", ("dias do briefing ao site no ar", "days from brief to live site")),
                  ("2", ("idiomas, PT e EN", "languages, PT and EN")),
                  ("11", ("seções na página", "page sections")),
                  ("3", ("formatos de motion", "motion formats"))],
        "video": ("moove-motion", ("Motion de divulgação", "Promo motion")),
        "gallery": [
            ("half", "moove-lp-08.webp", ("Etapas do processo seletivo", "Selection steps"), None),
            ("half", "moove-lp-02.webp", ("Seção Quem é a Moove", "About Moove section"), None),
        ],
    },
    {
        "slug": "panorama-mulheres",
        "theme": "panorama",
        "client": ("Instituto Talenses Group × Insper · 2025–2026", "Instituto Talenses Group × Insper · 2025–2026"),
        "title": "Panorama Mulheres",
        "summary": (
            "Site da pesquisa que acompanha a liderança feminina no Brasil desde 2017. Organizei dados, insights e as edições "
            "numa experiência clara. Também criei o design system e a campanha “Participe!” da 6ª edição.",
            "Website for the study that has tracked women's leadership in Brazil since 2017. I organised data, insights and "
            "past editions into a clear experience, and created the design system and the “Participe!” campaign for the 6th edition."),
        "tags": [("Web design", "Web design"), ("Design system", "Design system"), ("Dados", "Data"), ("Campanha", "Campaign")],
        "link": "https://panoramamulheres.com/",
        "role": ("Web design, design system e campanha", "Web design, design system and campaign"),
        "deliv": ("Site institucional, página de insights, linha do tempo das edições, design system, banner e posts",
                  "Website, insights page, editions timeline, design system, banner and posts"),
        "tools": "Figma · Photoshop · Illustrator",
        "cover": ("pm-site-old.webp", ("Topo do site Panorama Mulheres", "Panorama Mulheres website hero")),
        "challenge": [
            ("O Panorama Mulheres é uma pesquisa do Instituto Talenses Group com o Núcleo de Estudos de Gênero do Insper. "
             "Os dados são ricos, mas estavam espalhados em PDFs e e-books de várias edições.",
             "Panorama Mulheres is a study by Instituto Talenses Group and Insper's Gender Studies Centre. The data is rich, "
             "but it was scattered across PDFs and e-books from several editions."),
            ("O site precisava contar a história da pesquisa, destacar os números certos e convidar empresas a responder e apoiar.",
             "The website had to tell the study's story, surface the right numbers and invite companies to take part and support it."),
        ],
        "process": [
            {
                "text": [
                    ("Organizei a página em camadas: o propósito, a pesquisa em números, os principais insights da edição "
                     "e chamadas claras para baixar, responder e apoiar.",
                     "I layered the page: purpose, the study in numbers, the edition's key insights and clear calls to "
                     "download, respond and support."),
                ],
                "figs": [("wide", "pm-insights.webp", ("Principais insights da edição 2025", "Key insights of the 2025 edition"))],
            },
            {
                "text": [
                    ("A linha do tempo junta as edições desde 2017 e o episódio do C-Talks sobre a pesquisa, para mostrar "
                     "a série histórica como um ativo do Instituto.",
                     "The timeline brings together every edition since 2017 and the C-Talks episode about the study, presenting "
                     "the historical series as an asset of the Institute."),
                ],
                "figs": [
                    ("half", "pm-edicoes.webp", ("Linha do tempo das edições", "Editions timeline")),
                    ("half", "pm-ctalks2.webp", ("Episódio especial do C-Talks", "Special C-Talks episode")),
                ],
            },
            {
                "text": [
                    ("Levei tudo para um design system no Figma, com componentes e variáveis, e usei esse sistema para a "
                     "campanha “Participe!” da 6ª edição.",
                     "I turned it all into a Figma design system with components and variables, and used it for the "
                     "“Participe!” campaign of the 6th edition."),
                ],
                "figs": [
                    ("wide", "pm-participe-1.webp", ("Banner da campanha Participe", "Participe campaign banner")),
                ],
            },
        ],
        "result_text": [
            ("O site virou a casa da pesquisa: reúne a série histórica, os insights da 5ª edição e a porta de entrada "
             "para as empresas participarem da próxima.",
             "The website became the study's home: it holds the historical series, the 5th edition insights and the "
             "entry point for companies to join the next one."),
        ],
        "facts": [("2017", ("início da série histórica", "start of the historical series")),
                  ("310", ("empresas respondentes em 2024", "companies responded in 2024")),
                  ("5ª", ("edição publicada no site", "edition published on the site")),
                  ("6ª", ("edição com campanha “Participe!”", "edition with the “Participe!” campaign"))],
        "gallery": [
            ("half", "pm-participe-2.webp", ("Post da campanha Participe", "Participe campaign post"), None),
            ("half", "pm-hero.webp", ("Primeira versão do topo do site", "Early version of the site hero"), None),
        ],
    },
]


# ---------------------------------------------------------------- home: mosaicos

def bento(c, p):
    s = c["slug"]
    if s == "flowboard":
        return f"""<div class="bento bento--flow">
        <figure class="zoom f-browser">{browser('useflowboard.com/app')}{img(p, 'fb-kanban.webp', ('Board do FlowBoard em kanban, com demandas por status', 'FlowBoard board in kanban view, tasks by status'))}</figure>
        <figure class="zoom f-phone">{img(p, 'fb-mob-board.webp', ('Board do FlowBoard no celular', 'FlowBoard board on mobile'))}</figure>
        <figure class="zoom f-half">{img(p, 'fb-home.webp', ('Home do FlowBoard com a Daily e as prioridades do dia', 'FlowBoard home with the daily and today’s priorities'))}</figure>
        <figure class="zoom f-half">{img(p, 'fb-kanban-dark.webp', ('Board do FlowBoard no modo escuro', 'FlowBoard board in dark mode'))}</figure>
        <figure class="zoom f-browser">{browser('useflowboard.com')}{img(p, 'fb-site.webp', ('Site do FlowBoard: Cada demanda num lugar só', 'FlowBoard website'))}</figure>
        <figure class="zoom f-phone">{img(p, 'fb-mob-daily.webp', ('Daily do FlowBoard no celular', 'FlowBoard daily on mobile'))}</figure>
      </div>"""
    if s == "board-circle":
        return f"""<div class="bento bento--board">
        <figure class="b-logo">{img(p, 'bc-logo.png', ('Logotipo Board Circle', 'Board Circle logo'))}</figure>
        <figure class="b-video">{video(p, 'bc-loop', ('Loop animado do Board Circle para o telão do evento', 'Board Circle animated screen loop'))}</figure>
        <figure class="zoom">{img(p, 'bc-convite.webp', ('Convite do Board Circle Experience', 'Board Circle Experience invitation'))}</figure>
        <figure class="zoom">{img(p, 'bc-std.webp', ('Save the date do Board Circle', 'Board Circle save the date'))}</figure>
        <figure class="zoom b-light">{img(p, 'bc-ecobag.webp', ('Mockup de ecobag preta com a marca Board Circle', 'Black tote bag mockup with the Board Circle brand'))}</figure>
        <figure class="zoom b-wide">{img(p, 'bc-book-li.webp', ('Divulgação do book Conselho que Gera Valor em tablet', 'Book announcement on a tablet'))}</figure>
        <figure class="zoom b-tall">{img(p, 'bc-azeite.webp', ('Mockup de porta-azeite com a marca Board Circle', 'Olive oil holder mockup with the Board Circle brand'))}</figure>
        <figure class="zoom b-strip">{img(p, 'bc-mesas.webp', ('Displays de mesa numerados de 01 a 06', 'Table displays numbered 01 to 06'))}</figure>
      </div>"""
    if s == "summer-job-moove":
        caption = ("Passe suas férias no Brasil e construa seu futuro na Moove ☀️ Inscrições abertas para o Summer Job Moove 2027 em São Paulo, Rio de Janeiro ou Filadélfia.",
                   "Spend your break in Brazil and build your future at Moove ☀️ Applications are open for Summer Job Moove 2027 in São Paulo, Rio de Janeiro or Philadelphia.")
        acts = [("Gostei", "Like"), ("Comentar", "Comment"), ("Compartilhar", "Repost"), ("Enviar", "Send")]
        return f"""<div class="bento bento--moove">
        <figure class="zoom m-browser">{browser('summerjobmoovelub.com')}{img(p, 'moove-lp-topo.webp', ('Topo da landing page Summer Job Moove no computador', 'Summer Job Moove landing page hero on desktop'))}</figure>
        <figure class="zoom m-phone">{img(p, 'moove-lp-mobile.webp', ('Landing page Summer Job Moove no celular', 'Summer Job Moove landing page on mobile'))}</figure>
        <figure class="m-feed">
          <div class="post">
            <header class="post__head">
              <img src="{p}assets/img/mappit-avatar.webp" alt="" width="48" height="48">
              <div><b>Mappit</b><span>{e(('Recrutamento de jovens talentos', 'Early talent recruitment'))}</span><span>1 d · 🌐</span></div>
              <span class="post__follow">+ {e(('Seguir', 'Follow'))}</span>
            </header>
            <p class="post__text">{e(caption)}</p>
            <div class="zoom post__media">{img(p, 'moove-feed.webp', ('Post de feed: Construa seu futuro na Moove', 'Feed post: Build your future at Moove'), ' width="1080" height="1080"')}</div>
            <div class="post__stats" aria-hidden="true"><span><i>👍</i><i>❤️</i><i>👏</i></span></div>
            <div class="post__actions">{''.join(f'<span>{e(a)}</span>' for a in acts)}</div>
          </div>
        </figure>
        <div class="m-stack">
          <figure class="m-video">{video(p, 'moove-motion', ('Motion de divulgação do Summer Job Moove', 'Summer Job Moove promo motion'))}</figure>
          <figure class="zoom m-wide">{img(p, 'moove-lp-08.webp', ('Seção de etapas do processo seletivo', 'Selection steps section'))}</figure>
        </div>
      </div>"""
    return f"""<div class="bento bento--panorama">
        <figure class="zoom p-browser">{browser('panoramamulheres.com')}{img(p, 'pm-site-old.webp', ('Topo do site Panorama Mulheres 2025', 'Panorama Mulheres 2025 website hero'))}</figure>
        <figure class="zoom">{img(p, 'pm-participe-2.webp', ('Post da campanha Participe da 6ª edição', 'Participe campaign post, 6th edition'))}</figure>
        <figure class="zoom">{img(p, 'pm-insights.webp', ('Seção de principais insights da edição 2025', 'Key insights of the 2025 edition'))}</figure>
        <figure class="zoom">{img(p, 'pm-edicoes.webp', ('Linha do tempo das edições desde 2017', 'Editions timeline since 2017'))}</figure>
      </div>"""


def case_intro(c, i, p, case_href):
    tags = "".join(f"<li>{e(t)}</li>" for t in c["tags"])
    link = (f'<a class="link link--muted" href="{c["link"]}" target="_blank" rel="noopener">{e(c.get("link_label", UI["see_live"]))} ↗</a>'
            if c["link"] else "")
    note = f'<p class="hand case__note">{e(c["note"])}</p>' if c.get("note") else ""
    return f"""<div class="case__intro">
        <span class="case__num">{i:02d}</span>
        <div>
          <p class="case__client">{e(c['client'])}</p>
          <h3 class="case__title"><a href="{case_href}">{c['title']}</a></h3>
          <p class="case__text">{e(c['summary'])}</p>
          <ul class="tags">{tags}</ul>
          <div class="case__links"><a class="btn" href="{case_href}">{e(UI['see_case'])} →</a>{link}</div>
          {note}
        </div>
      </div>"""


# ---------------------------------------------------------------- home

TIMELINE = [
    ("2025", ("hoje", "now"), ("Analista de Criação Pleno", "Mid-level Creative Analyst"), "Talenses Group",
     ("Branding e comunicação das marcas do grupo, sites, landing pages, editorial, vídeo e o FlowBoard.",
      "Branding and communication for the group's brands, websites, landing pages, editorial, video and FlowBoard.")),
    ("2023", "2025", ("Analista de Criação Júnior", "Junior Creative Analyst"), "Sat",
     ("UI de landing pages e do novo blog, peças, vídeos e motions, mídia paga e e-mail marketing.",
      "UI for landing pages and the new blog, design, video and motion, paid media and email marketing.")),
    ("2022", "2023", ("Assistente de Criação Júnior", "Junior Creative Assistant"), "Sat",
     ("Conteúdo e vídeo para redes, peças animadas para campanhas, brindes e impressos.",
      "Social content and video, animated campaign pieces, merchandise and print.")),
    ("2021", "2022", ("Estágio em Criação", "Design Intern"), "Sat",
     ("Peças publicitárias, catálogos, folhetos, logotipos e posts.", "Ads, catalogues, flyers, logos and social posts.")),
    ("2020", "2021", ("Editor de Vídeo (estágio)", "Video Editor (intern)"), "Top Produções",
     ("Edição e finalização de vídeos, thumbnails e artes para redes.", "Video editing and finishing, thumbnails and social art.")),
]


def home():
    p = "" if LANG == "pt" else "../"
    hero_title = (
        'Eu desenho <em>marcas</em>, <em>sites</em><br class="br-lg"> e coisas que <span class="hero__move">se mexem</span>.',
        'I design <em>brands</em>, <em>websites</em><br class="br-lg"> and things that <span class="hero__move">move</span>.')
    lead = ("Sou o Lucas, designer de 25 anos. Hoje cuido da comunicação visual do ecossistema Talenses Group: de "
            "identidade de evento a landing page bilíngue, de book impresso a motion para mídia. E nas horas vagas, criei um produto.",
            "I'm Lucas, a 25-year-old designer from São Paulo. I look after the visual communication of the Talenses Group "
            "ecosystem: from event identities to bilingual landing pages, printed books to media motion. On the side, I built a product.")
    brands = ["Talenses Group", "Talenses Executive", "Mappit", "Assigna", "Moove", "Samsung", "UBS", "LiveMode", "Insper", "FTI Consulting"]
    marquee = "".join(f"<span>{b}</span>" for b in brands) + "".join(f'<span aria-hidden="true">{b}</span>' for b in brands)

    cases_html = ""
    for i, c in enumerate(CASES, 1):
        href = f"cases/{c['slug']}.html"
        cases_html += f"""
    <article class="case case--{c['theme']}">
      {case_intro(c, i, p, href)}
      {bento(c, p)}
    </article>
"""

    reel = [
        ("moove-motion", ("Summer Job Moove", "Summer Job Moove"), ("Motion para redes", "Social motion")),
        ("bc-loop", ("Board Circle", "Board Circle"), ("Loop de telão do evento", "Event screen loop")),
        ("radar-header", ("Radar TG", "Radar TG"), ("Header animado de newsletter", "Animated newsletter header")),
    ]
    reel_html = "".join(f"""
        <figure class="reel__item">
          {video(p, v, t)}
          <figcaption><b>{e(t)}</b> {e(d)}</figcaption>
        </figure>""" for v, t, d in reel)

    more = [
        ("samsung.webp", ("Estágio Samsung 2026", "Samsung Internship 2026"), ("Landing page · Mappit", "Landing page · Mappit"), None),
        ("livemode.webp", ("LiveMode Global Experience", "LiveMode Global Experience"), ("Landing page · Copa do Mundo 2026", "Landing page · 2026 World Cup"), None),
        ("ubs.webp", ("Trainee UBS Brasil 2026", "UBS Brazil Trainee 2026"), ("Landing page · Mappit", "Landing page · Mappit"), None),
        ("tg-site.webp", ("Talenses Group", "Talenses Group"), ("Site institucional", "Corporate website"), "https://talensesgroup.com/"),
    ]
    more_html = ""
    for src, t, d, url in more:
        title = (f'<a href="{url}" target="_blank" rel="noopener">{e(t)} ↗</a>' if url else e(t))
        more_html += f"""
      <article class="card">
        <figure class="zoom">{img(p, src, t)}</figure>
        <h3>{title}</h3><p>{e(d)}</p>
      </article>"""

    tl = "".join(f"""
          <li><span class="tl__when">{a}–{L(b)}</span><div><b>{e(r)}</b> · {co}<p>{e(d)}</p></div></li>"""
                 for a, b, r, co, d in TIMELINE)

    testimonials = ""
    if TESTIMONIALS:
        items = "".join(f"""
        <figure class="quote"><blockquote>“{html.escape(L((q_pt, q_en)))}”</blockquote>
          <figcaption><b>{html.escape(n)}</b> {html.escape(L((r_pt, r_en)))}</figcaption></figure>"""
                        for q_pt, q_en, n, r_pt, r_en in TESTIMONIALS)
        testimonials = f"""
  <section class="wrap section quotes" aria-label="{e(('Depoimentos', 'Testimonials'))}">
    <p class="eyebrow">{e(('O que dizem', 'Kind words'))}</p>
    <div class="quotes__grid">{items}</div>
  </section>"""

    cv = f"{p}assets/{L(UI['cv_file'])}"
    path = "" if LANG == "pt" else "en/"
    alt = "en/" if LANG == "pt" else ""
    out = head(p, L(("Lucas Oliveira · Designer", "Lucas Oliveira · Designer")),
               L(("Lucas Oliveira, designer em São Paulo. Identidade visual, sites, landing pages, produto e motion.",
                  "Lucas Oliveira, designer in São Paulo. Visual identity, websites, landing pages, product and motion.")),
               path, alt)
    out += f"""
<body>

<a class="skip" href="#trabalhos">{e(UI['skip'])}</a>

{nav(p, '').replace('{LANG_SWITCH}', ('en/' if LANG == 'pt' else '../'))}

<main id="topo">

  <section class="hero wrap">
    <p class="eyebrow"><span class="dot" aria-hidden="true"></span> {e(('Creative Analyst no Talenses Group · São Paulo', 'Creative Analyst at Talenses Group · São Paulo'))}</p>
    <h1 class="hero__title">{L(hero_title)}</h1>
    <div class="hero__foot">
      <p class="hero__lead">{e(lead)}</p>
      <figure class="hero__photo">
        <img src="{p}assets/img/lucas.webp" alt="{e(('Lucas Oliveira sorrindo e fazendo sinal de paz', 'Lucas Oliveira smiling and making a peace sign'))}" width="800" height="800">
        <figcaption class="hand">{e(('oi! 👋', 'hi! 👋'))}</figcaption>
      </figure>
    </div>
  </section>

  <div class="marquee" aria-label="{e(('Marcas com que trabalhei', 'Brands I have worked with'))}">
    <div class="marquee__track">{marquee}</div>
  </div>

  <section id="trabalhos" class="wrap section">
    <header class="section__head">
      <p class="eyebrow">{e(('Trabalhos selecionados', 'Selected work'))}</p>
      <h2 class="section__title">{L(('Projetos de que <em>me orgulho</em>', 'Projects I’m <em>proud of</em>'))}</h2>
    </header>
{cases_html}
  </section>

  <section id="motion" class="motion">
    <div class="wrap">
      <header class="section__head">
        <p class="eyebrow">Motion</p>
        <h2 class="section__title">{L(('Coisas que <em>se mexem</em>', 'Things that <em>move</em>'))}</h2>
      </header>
      <figure class="showreel">
        {video(p, 'showreel', ('Showreel de motion 2026', 'Motion showreel 2026'))}
        <figcaption><b>Showreel 2026</b> {e(('Shaping the Change, Summer Job Moove e Board Circle · 40s', 'Shaping the Change, Summer Job Moove and Board Circle · 40s'))}</figcaption>
      </figure>
      <div class="reel">{reel_html}
        <figure class="reel__item reel__item--gif">
          {img(p, 'exame-retangulo.gif', ('Banner animado Talenses Group para a Exame', 'Talenses Group animated banner for Exame'))}
          <figcaption><b>Talenses Group × Exame</b> {e(('Banners animados de mídia', 'Animated media banners'))}</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="wrap section">
    <header class="section__head section__head--row">
      <h2 class="section__title section__title--sm">{e(('Mais landing pages & sites', 'More landing pages & websites'))}</h2>
      <a class="link" href="{BEHANCE}" target="_blank" rel="noopener">{e(('Tudo no Behance', 'Everything on Behance'))} ↗</a>
    </header>
    <div class="grid">{more_html}
    </div>
  </section>
{testimonials}
  <section id="sobre" class="wrap section about">
    <div class="about__photos" aria-hidden="true">
      <figure class="polaroid polaroid--a"><img src="{p}assets/img/lucas2.webp" alt="" loading="lazy"><figcaption class="hand">{e(('eu, de touca', 'me, in a beanie'))}</figcaption></figure>
      <figure class="polaroid polaroid--b"><img src="{p}assets/img/eddie.webp" alt="" loading="lazy"><figcaption class="hand">{e(('o Eddie, chefe do estúdio', 'Eddie, head of studio'))}</figcaption></figure>
    </div>
    <div class="about__text">
      <p class="eyebrow">{e(UI['about'])}</p>
      <h2 class="section__title">{L(('Curioso por natureza, <em>detalhista</em> por teimosia.', 'Curious by nature, <em>detail-obsessed</em> by choice.'))}</h2>
      <p>{e(('Sou de São Bernardo do Campo e trabalho como Creative Analyst no Talenses Group, onde atendo um ecossistema inteiro de marcas: Talenses, Talenses Executive, Mappit, Assigna, WEDO, Landtech e o Instituto TG. Isso me fez transitar fácil entre branding, editorial, web e vídeo, muitas vezes no mesmo dia.',
             'I’m from São Bernardo do Campo and work as a Creative Analyst at Talenses Group, serving a whole ecosystem of brands: Talenses, Talenses Executive, Mappit, Assigna, WEDO, Landtech and Instituto TG. That has me moving between branding, editorial, web and video, often on the same day.'))}</p>
      <p>{e(('Fora do trabalho, divido a rotina com o Eddie (que aparece pra pedir carinho no meio das criações) e jogo videogame. Zelda é o favorito, pela forma como tudo nele é pensado nos mínimos detalhes. Tento levar isso pro que eu faço.',
             'Outside work I share my days with Eddie (who shows up for cuddles mid-project) and play video games. Zelda is my favourite, for how every tiny detail is thought through. I try to bring that into what I make.'))}</p>

      <h3 class="about__sub">{e(('Trajetória', 'Experience'))}</h3>
      <ol class="tl">{tl}
      </ol>
      <p class="about__edu">{e(('Formação em design na EBAC, Escola Britânica de Artes Criativas e Tecnologia.', 'Design studies at EBAC, British School of Creative Arts and Technology.'))}</p>

      <div class="skills">
        <div>
          <h3>{e(('Faço', 'I do'))}</h3>
          <ul>{''.join(f'<li>{e(x)}</li>' for x in [('Identidade visual', 'Visual identity'), ('Editorial & impressos', 'Editorial & print'), ('Web design & landing pages', 'Web design & landing pages'), ('UI, produto & design systems', 'UI, product & design systems'), ('Motion & edição de vídeo', 'Motion & video editing'), ('Social media', 'Social media')])}</ul>
        </div>
        <div>
          <h3>{e(('Uso', 'I use'))}</h3>
          <ul>{''.join(f'<li>{e(x)}</li>' for x in ['Figma', 'Photoshop · Illustrator · InDesign', 'After Effects · Premiere', 'Lightroom', ('HTML/CSS/JS · React · Replit', 'HTML/CSS/JS · React · Replit'), ('IA no fluxo criativo', 'AI in the creative workflow')])}</ul>
        </div>
      </div>
      <a class="btn btn--ghost" href="{cv}" download>{e(UI['cv'])} ↓</a>
    </div>
  </section>

  <section id="contato" class="contact">
    <div class="wrap">
      <p class="eyebrow">{e(('Contato', 'Contact'))}</p>
      <h2 class="contact__title">{e(('Tem um projeto em mente?', 'Got a project in mind?'))}<br><a href="mailto:{EMAIL}">{e(('Bora conversar', "Let's talk"))} <span aria-hidden="true">→</span></a></h2>
      <ul class="contact__links">
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn ↗</a></li>
        <li><a href="{BEHANCE}" target="_blank" rel="noopener">Behance ↗</a></li>
        <li><a href="{YOUTUBE}" target="_blank" rel="noopener">YouTube ↗</a></li>
        <li><a href="{cv}" download>{e(UI['cv'])} ↓</a></li>
      </ul>
    </div>
  </section>
</main>

{foot(p)}"""
    return out


# ---------------------------------------------------------------- página de case

def fig(p, kind, src, alt, url=None):
    bar = browser(url) if url else ""
    cls = {"wide": "cf--wide", "half": "cf--half", "two": "cf--two", "third": "cf--third",
           "phone": "cf--phone", "logo": "cf--logo"}[kind]
    zoom = "" if kind == "logo" else " zoom"
    return f'<figure class="cf {cls}{zoom}">{bar}{img(p, src, alt)}<figcaption>{e(alt)}</figcaption></figure>'


def case_page(idx):
    c = CASES[idx]
    nxt = CASES[(idx + 1) % len(CASES)]
    p = "../" if LANG == "pt" else "../../"
    home = "../"
    link = (f'<a class="link" href="{c["link"]}" target="_blank" rel="noopener">{e(c.get("link_label", UI["see_live"]))} ↗</a>'
            if c["link"] else "")
    paras = lambda lst: "".join(f"<p>{e(x)}</p>" for x in lst)
    steps = ""
    for n, step in enumerate(c["process"], 1):
        figs = "".join(fig(p, k, s, a) for k, s, a in step["figs"])
        steps += f"""
      <div class="step">
        <div class="step__text"><span class="step__n">{n:02d}</span>{paras(step['text'])}</div>
        <div class="cf-grid">{figs}</div>
      </div>"""
    facts = "".join(f'<li><b>{n}</b><span>{e(t)}</span></li>' for n, t in c["facts"])
    vid = ""
    if c.get("video"):
        name, label = c["video"]
        vid = f'<figure class="cf cf--wide cf--video">{video(p, name, label)}<figcaption>{e(label)}</figcaption></figure>'
    gallery = "".join(fig(p, k, s, a, u) for k, s, a, u in c["gallery"])
    cover_src, cover_alt = c["cover"]
    path = ("" if LANG == "pt" else "en/") + f"cases/{c['slug']}.html"
    alt_path = ("en/" if LANG == "pt" else "") + f"cases/{c['slug']}.html"

    out = head(p, f"{c['title']} · Lucas Oliveira", L(c["summary"])[:155], path, alt_path)
    out += f"""
<body class="page-case page-case--{c['theme']}">
{nav(p, home).replace('{LANG_SWITCH}', ('../en/cases/' if LANG == 'pt' else '../../cases/') + c['slug'] + '.html')}

<main id="topo">
  <header class="ch wrap">
    <a class="ch__back" href="{home}#trabalhos">← {e(UI['back'])}</a>
    <p class="eyebrow">{e(c['client'])}</p>
    <h1 class="ch__title">{c['title']}</h1>
    <p class="ch__lead">{e(c['summary'])}</p>
    <dl class="ch__meta">
      <div><dt>{e(UI['role'])}</dt><dd>{e(c['role'])}</dd></div>
      <div><dt>{e(UI['deliv'])}</dt><dd>{e(c['deliv'])}</dd></div>
      <div><dt>{e(UI['tools'])}</dt><dd>{e(c['tools'])}</dd></div>
    </dl>
    {link}
  </header>

  <figure class="ch__cover zoom">{img(p, cover_src, cover_alt, ' loading="eager"')}</figure>

  <section class="wrap cs">
    <h2 class="cs__h">{e(UI['challenge'])}</h2>
    <div class="cs__body">{paras(c['challenge'])}</div>
  </section>

  <section class="wrap cs">
    <h2 class="cs__h">{e(UI['process'])}</h2>
    <div class="cs__body cs__body--wide">{steps}
    </div>
  </section>

  <section class="cs-result">
    <div class="wrap">
      <h2 class="cs__h">{e(UI['result'])}</h2>
      <div class="cs__body">{paras(c['result_text'])}</div>
      <ul class="facts">{facts}</ul>
    </div>
  </section>

  <section class="wrap cs cs--gallery">
    <div class="cf-grid">{vid}{gallery}</div>
  </section>

  <a class="next" href="{nxt['slug']}.html">
    <span class="eyebrow">{e(UI['next'])}</span>
    <span class="next__title">{nxt['title']} <span aria-hidden="true">→</span></span>
  </a>
</main>

{foot(p)}"""
    return out


# ---------------------------------------------------------------- currículo

def cv_page():
    exp = "".join(f"""
    <div class="cv-job"><div class="cv-when">{a}–{L(b)}</div><div><b>{e(r)}</b> · {co}<p>{e(d)}</p></div></div>""" for a, b, r, co, d in TIMELINE)
    projects = "".join(f"<li><b>{c['title']}</b>: {e(c['role'])}.</li>" for c in CASES)
    return f"""<!doctype html>
<html lang="{'pt-BR' if LANG == 'pt' else 'en'}"><head><meta charset="utf-8">
<title>{e(('Currículo', 'Résumé'))} · Lucas Oliveira</title>
<style>
@page {{ size: A4; margin: 16mm 16mm; }}
body {{ font: 10.5pt/1.45 "Inter Tight", -apple-system, Helvetica, sans-serif; color: #17150f; margin: 0; }}
h1 {{ font: 400 34pt/1 "Instrument Serif", Georgia, serif; margin: 0 0 4pt; letter-spacing: -.01em; }}
h2 {{ font: 600 8.5pt/1 "Inter Tight", sans-serif; text-transform: uppercase; letter-spacing: .1em; color: #ff4f1a; margin: 18pt 0 8pt; }}
.sub {{ color: #5d574b; font-size: 12pt; margin: 0 0 8pt; }}
.contact {{ display: flex; flex-wrap: wrap; gap: 4pt 14pt; font-size: 9.5pt; color: #5d574b; padding-bottom: 10pt; border-bottom: 1.5pt solid #17150f; }}
.contact a {{ color: inherit; text-decoration: none; }}
p {{ margin: 0 0 6pt; }}
.cv-job {{ display: grid; grid-template-columns: 70pt 1fr; gap: 10pt; margin-bottom: 8pt; break-inside: avoid; }}
.cv-when {{ color: #5d574b; font-variant-numeric: tabular-nums; }}
.cv-job p {{ color: #3d382f; margin-top: 2pt; }}
ul {{ margin: 0; padding-left: 14pt; }} li {{ margin-bottom: 3pt; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18pt; }}
</style>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter+Tight:wght@400;600&display=swap" rel="stylesheet">
</head><body>
<h1>Lucas Oliveira</h1>
<p class="sub">{e(('Designer · Creative Analyst no Talenses Group · São Paulo', 'Designer · Creative Analyst at Talenses Group · São Paulo, Brazil'))}</p>
<div class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{SITE}/{'' if LANG == 'pt' else 'en/'}">{SITE.replace('https://', '')}{'' if LANG == 'pt' else '/en'}</a><a href="{LINKEDIN}">linkedin.com/in/lucasantosoliveira</a><a href="{BEHANCE}">behance.net/lucasoliveira107</a></div>

<h2>{e(('Resumo', 'Summary'))}</h2>
<p>{e(('Designer com mais de 5 anos entre criação, vídeo e digital. Cuido da comunicação visual de um ecossistema de marcas: identidade visual, editorial, sites e landing pages, motion e produto. Desenho no Figma e também programo o que desenho, do site estático ao produto completo.',
       'Designer with 5+ years across creative, video and digital. I look after the visual communication of a whole brand ecosystem: visual identity, editorial, websites and landing pages, motion and product. I design in Figma and also code what I design, from static sites to a full product.'))}</p>

<h2>{e(('Experiência', 'Experience'))}</h2>{exp}

<h2>{e(('Projetos em destaque', 'Selected projects'))}</h2>
<ul>{projects}</ul>

<div class="cols">
  <div><h2>{e(('Competências', 'Skills'))}</h2><p>{e(('Identidade visual · Editorial e impressos · Web design e landing pages · UI, produto e design systems · Motion e edição de vídeo · Social media', 'Visual identity · Editorial and print · Web design and landing pages · UI, product and design systems · Motion and video editing · Social media'))}</p></div>
  <div><h2>{e(('Ferramentas', 'Tools'))}</h2><p>Figma · Photoshop · Illustrator · InDesign · After Effects · Premiere · Lightroom · HTML/CSS/JS · React · Replit</p></div>
</div>

<h2>{e(('Formação', 'Education'))}</h2>
<p>{e(('EBAC, Escola Britânica de Artes Criativas e Tecnologia', 'EBAC, British School of Creative Arts and Technology'))}</p>
</body></html>"""


# ---------------------------------------------------------------- escrita

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    global LANG
    for LANG in ("pt", "en"):
        base = "" if LANG == "pt" else "en/"
        write(base + "index.html", home())
        for i, c in enumerate(CASES):
            write(f"{base}cases/{c['slug']}.html", case_page(i))
        write(f"tools/cv-{LANG}.html", cv_page())
    if "--pdf" in sys.argv:
        chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        for lang, name in (("pt", UI["cv_file"][0]), ("en", UI["cv_file"][1])):
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--virtual-time-budget=4000", f"--print-to-pdf={ROOT}/assets/{name}",
                            f"file://{ROOT}/tools/cv-{lang}.html"], check=True, capture_output=True)
    print("ok")


if __name__ == "__main__":
    main()
