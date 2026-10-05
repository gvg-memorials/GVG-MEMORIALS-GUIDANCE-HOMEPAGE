#!/usr/bin/env python3
"""Build the Spanish homepage (es/index.html) from the English one (index.html).

Run from the repo root after any change to index.html:

    python3 scripts/build_es.py

Every English string below must still appear in index.html. If one was edited, the script stops and
names it, so the Spanish page never silently keeps old wording or falls back to English.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SMS_EN = "Hi%20GVG%20Memorials%2C%20I%27d%20like%20help%20with%20a%20memorial."
SMS_ES = "Hola%2C%20GVG%20Memorials.%20Quisiera%20ayuda%20con%20una%20l%C3%A1pida."

# (English, Spanish). Order matters only where one string contains another; longer strings come first.
PAIRS = [
    # --- head ---------------------------------------------------------------------------------------
    ('<html lang="en">', '<html lang="es">'),
    ('<link rel="canonical" href="https://www.gvgmemorials.com/" />',
     '<link rel="canonical" href="https://www.gvgmemorials.com/es/" />'),
    ("<title>GVG Memorials | Headstones and Grave Markers in Oxnard</title>",
     "<title>GVG Memorials | Lápidas y placas para el cementerio en Oxnard</title>"),
    ('content="Family-owned since 1998. GVG Memorials guides Oxnard and Ventura County families through choosing a headstone or grave marker for someone they love, with a free written quote."',
     'content="Negocio familiar desde 1998. GVG Memorials acompaña a las familias de Oxnard y del condado de Ventura a elegir la lápida de un ser querido, con un presupuesto por escrito gratis. Atendemos en español."'),
    ('<meta property="og:title" content="GVG Memorials | Headstones and Grave Markers in Oxnard" />',
     '<meta property="og:title" content="GVG Memorials | Lápidas y placas para el cementerio en Oxnard" />'),
    ('<meta name="twitter:title" content="GVG Memorials | Headstones and Grave Markers in Oxnard" />',
     '<meta name="twitter:title" content="GVG Memorials | Lápidas y placas para el cementerio en Oxnard" />'),
    ("content=\"Family-owned since 1998. We guide you through every choice, check your cemetery's requirements, and give you a free written quote.\"",
     'content="Negocio familiar desde 1998. Le acompañamos en cada decisión, revisamos las reglas de su cementerio y le damos un presupuesto por escrito gratis."'),
    ('<meta property="og:url" content="https://www.gvgmemorials.com/" />',
     '<meta property="og:url" content="https://www.gvgmemorials.com/es/" />'),
    ('<meta property="og:locale" content="en_US" />',
     '<meta property="og:locale" content="es_US" />\n    <meta property="og:locale:alternate" content="en_US" />'),
    ('content="A large gold serif G with GVG Memorials, Oxnard, since 1998, inside it"',
     'content="Una G dorada grande con GVG Memorials, Oxnard, desde 1998, en su interior"'),
    ('"url": "https://www.gvgmemorials.com/",', '"url": "https://www.gvgmemorials.com/es/",'),
    ('"description": "Family-owned Oxnard memorial company, since 1998. Flat granite and bronze memorials, slants, custom uprights, single and companion memorials, granite benches, final dates, and cleaning and restoration."',
     '"description": "Negocio familiar de lápidas en Oxnard desde 1998. Placas planas de granito y de bronce, lápidas inclinadas, lápidas verticales a la medida, lápidas individuales y dobles, bancas de granito, fechas finales, y limpieza y restauración.",\n        "knowsLanguage": ["es", "en"]'),
    ('"name": "Do I need to decide anything before I call?"', '"name": "¿Tengo que decidir algo antes de llamar?"'),
    ("\"text\": \"No. A name and a cemetery are enough to begin. We'll explain the choices and what your cemetery allows.\"",
     '"text": "No. Con un nombre y un cementerio podemos empezar. Le explicamos las opciones y lo que permite su cementerio."'),
    ('"name": "What does a memorial cost?"', '"name": "¿Cuánto cuesta una lápida?"'),
    ("\"text\": \"It depends on the type, size, granite, artwork, and your cemetery's requirements. We give every family a free written quote with every item listed, before anything is decided.\"",
     '"text": "Depende del tipo, el tamaño, el granito, el diseño y las reglas de su cementerio. A cada familia le damos un presupuesto por escrito gratis, con cada cosa detallada, antes de decidir nada."'),
    ('"name": "Should we choose a single or a companion memorial?"', '"name": "¿Conviene una lápida individual o una doble?"'),
    ("\"text\": \"Most families choose a single memorial for their loved one. A companion memorial is for two people, such as a husband and wife. One side is engraved now and the other later, at our shop or at the cemetery, depending on the cemetery's requirements. Any size can be made either way.\"",
     '"text": "La mayoría de las familias elige una lápida individual para su ser querido. La lápida doble es para dos personas, como esposo y esposa. Un lado se graba ahora y el otro después, en nuestro taller o en el cementerio, según las reglas del cementerio. Cualquier tamaño puede hacerse de las dos formas."'),
    ("\"name\": \"Can you add a date to a stone that's already in place?\"", '"name": "¿Pueden agregar una fecha a una lápida que ya está colocada?"'),
    ("\"text\": \"Yes. Send us a photo of the stone and the cemetery name, and we'll explain what's possible.\"",
     '"text": "Sí. Mándenos una foto de la lápida y el nombre del cementerio, y le explicamos qué se puede hacer."'),

    # --- header, menus, contact bar -------------------------------------------------------------------
    ('<a class="skip-link" href="#main-content">Skip to main content</a>',
     '<a class="skip-link" href="#main-content">Saltar al contenido</a>'),
    ('aria-label="Primary navigation"', 'aria-label="Navegación principal"'),
    ('aria-label="GVG Memorials home"', 'aria-label="GVG Memorials, inicio"'),
    ('aria-label="Main navigation"', 'aria-label="Menú principal"'),
    ('aria-label="Mobile navigation"', 'aria-label="Menú"'),
    ('aria-label="Footer navigation"', 'aria-label="Menú del pie de página"'),
    ('aria-label="Open menu"', 'aria-label="Abrir menú"'),
    ('aria-label="Quick contact options"', 'aria-label="Contacto rápido"'),
    ('<a href="#steps">How It Works</a>', '<a href="#steps">Cómo funciona</a>'),
    ('<a href="#granite">Granite</a>', '<a href="#granite">Granito</a>'),
    ('<a href="#gallery">Our Work</a>', '<a href="#gallery">Nuestro trabajo</a>'),
    ('<a href="#family">Our Family</a>', '<a href="#family">Nuestra familia</a>'),
    ('<a href="#questions">Questions</a>', '<a href="#questions">Preguntas</a>'),
    ('<a href="#contact">Contact</a>', '<a href="#contact">Contacto</a>'),
    ('<a class="lang-link" href="/es/" hreflang="es" lang="es">Español</a>',
     '<a class="lang-link" href="/" hreflang="en" lang="en">English</a>'),
    ('<a class="lang-link" href="/es/" hreflang="es" lang="es">En español</a>',
     '<a class="lang-link" href="/" hreflang="en" lang="en">In English</a>'),
    ('<a href="/es/" hreflang="es" lang="es">Español</a>', '<a href="/" hreflang="en" lang="en">English</a>'),
    ('Call (805) 889-3769</a>', 'Llamar al (805) 889-3769</a>'),
    ('Text (805) 889-3769</a>', 'Mandar mensaje al (805) 889-3769</a>'),
    ('<a href="tel:+18058893769">Call</a>', '<a href="tel:+18058893769">Llamar</a>'),
    ('">Text</a>', '">Mensaje</a>'),
    ('<a href="#contact-form">Write</a>', '<a href="#contact-form">Escribir</a>'),

    # --- hero -----------------------------------------------------------------------------------------
    ("<span>Headstones &amp; Grave Markers</span>", "<span>Lápidas y placas</span>"),
    ("<span>Oxnard, California</span>", "<span>Oxnard, California</span>"),
    ("<span>Family owned since 1998</span>", "<span>Negocio familiar desde 1998</span>"),
    ('<h1 id="hero-title">Remember the one you love. <em>Forever.</em></h1>',
     '<h1 id="hero-title">Recuerde a quien tanto ama. <em>Para siempre.</em></h1>'),
    ("<p class=\"hero-sub\">We'll walk with you through every choice, at a pace that feels right for your family.</p>",
     '<p class="hero-sub">Le acompañamos en cada decisión, al paso que su familia necesite.</p>'),
    ('<a class="button button-outline" href="#contact-form">Ask us a question</a>',
     '<a class="button button-outline" href="#contact-form">Háganos una pregunta</a>'),
    ('<p class="hero-es" lang="es">También atendemos en español. <a href="/es/" hreflang="es">Ver esta página en español</a></p>',
     '<p class="hero-es" lang="en">We also help families in English. <a href="/" hreflang="en">Read this page in English</a></p>'),

    # --- slideshow ------------------------------------------------------------------------------------
    ("aria-label=\"Memorials we've made\"", 'aria-label="Lápidas que hemos hecho"'),
    ('aria-roledescription="carousel"', 'aria-roledescription="carrusel"'),
    ("Oxford Gray granite with nature scene artwork", "Granito Oxford Gray con un paisaje de bosque"),
    ("Oxford Gray granite memorial with nature scene artwork by GVG Memorials",
     "Lápida de granito Oxford Gray con un paisaje de bosque, de GVG Memorials"),
    ("Beach scene with palms, hibiscus and an anchor for a husband and wife, by GVG Memorials",
     "Escena de playa con palmeras, hibiscos y un ancla, para esposo y esposa, de GVG Memorials"),
    ("Beach scene with palms, hibiscus and an anchor for a husband and wife",
     "Escena de playa con palmeras, hibiscos y un ancla, para esposo y esposa"),
    ("Carved doves on Blue Pearl granite, up close, by GVG Memorials",
     "Palomas talladas en granito Blue Pearl, de cerca, de GVG Memorials"),
    ("Carved doves on Blue Pearl granite, up close", "Palomas talladas en granito Blue Pearl, de cerca"),
    ("Polished black granite flat memorial with custom scenic artwork by GVG Memorials",
     "Placa de granito negro pulido con un paisaje hecho a la medida, de GVG Memorials"),
    ("Polished black granite with custom scenic artwork", "Granito negro pulido con un paisaje hecho a la medida"),
    ("Blue Pearl granite memorial with a deep-sunk sanded panel by GVG Memorials",
     "Lápida de granito Blue Pearl con un panel hundido y arenado, de GVG Memorials"),
    ("Blue Pearl granite with a deep-sunk sanded panel", "Granito Blue Pearl con un panel hundido y arenado"),
    ("Puritan Rose granite memorial with a stainless steel photo by GVG Memorials",
     "Lápida de granito Puritan Rose con una foto en acero inoxidable, de GVG Memorials"),
    ("Puritan Rose granite with a stainless steel photo", "Granito Puritan Rose con una foto en acero inoxidable"),
    ("Detailed engraving on polished granite by GVG Memorials", "Grabado detallado en granito pulido, de GVG Memorials"),
    ("Standard sunk artwork on polished granite", "Diseño grabado en granito pulido"),
    ("Granite memorial with a color photo and baseball artwork, by GVG Memorials",
     "Lápida de granito con una foto a color y un diseño de béisbol, de GVG Memorials"),
    ("Granite memorial with a color photo and baseball artwork", "Lápida de granito con una foto a color y un diseño de béisbol"),
    ("Mission scene with a color portrait for a husband and wife, by GVG Memorials",
     "Escena de una misión con un retrato a color, para esposo y esposa, de GVG Memorials"),
    ("Mission scene with a color portrait for a husband and wife",
     "Escena de una misión con un retrato a color, para esposo y esposa"),
    ("Blue granite companion memorial with a color portrait, by GVG Memorials",
     "Lápida doble de granito azul con un retrato a color, de GVG Memorials"),
    ("Blue granite companion memorial with a color portrait", "Lápida doble de granito azul con un retrato a color"),
    ("Granite memorial with a color portrait and verse, by GVG Memorials",
     "Lápida de granito con un retrato a color y un verso, de GVG Memorials"),
    ("Granite memorial with a color portrait and verse", "Lápida de granito con un retrato a color y un verso"),
    ("Color portraits, etched photographs and Our Lady of Guadalupe, by GVG Memorials",
     "Retratos a color, fotos grabadas y la Virgen de Guadalupe, de GVG Memorials"),
    ("Color portraits, etched photographs and Our Lady of Guadalupe",
     "Retratos a color, fotos grabadas y la Virgen de Guadalupe"),
    ("Granite memorial with a color photo, a football and a key border, by GVG Memorials",
     "Lápida de granito con una foto a color, un balón de fútbol americano y una greca, de GVG Memorials"),
    ("Granite memorial with a color photo, a football and a key border",
     "Lápida de granito con una foto a color, un balón de fútbol americano y una greca"),
    ('<label for="ask-q" class="sr-only">Ask us anything</label>', '<label for="ask-q" class="sr-only">Pregúntenos lo que quiera</label>'),
    ('placeholder="Try &lsquo;Where do I start?&rsquo;"', 'placeholder="Por ejemplo: &lsquo;¿Por dónde empiezo?&rsquo;"'),
    ('aria-label="Send your question"', 'aria-label="Enviar su pregunta"'),
    ('aria-label="Previous photo"', 'aria-label="Foto anterior"'),
    ('aria-label="Pause photos"', 'aria-label="Pausar fotos"'),
    ('aria-label="Next photo"', 'aria-label="Foto siguiente"'),

    # --- opening note ---------------------------------------------------------------------------------
    ('aria-label="A first word"', 'aria-label="Unas palabras"'),
    ("""              Whether you've lost a parent, a spouse, or a child, we'll guide you through every choice. A name and a
              cemetery are all we need to begin.""",
     """              Ya sea que haya perdido a su papá o su mamá, a su esposo o esposa, o a un hijo, le guiamos en cada
              decisión. Con un nombre y un cementerio podemos empezar."""),
    ("""              We'll check what your cemetery requires, show you real stone, and help you get every name, date, and
              detail right before anything is engraved.""",
     """              Revisamos lo que pide su cementerio, le mostramos piedra de verdad y le ayudamos a que cada nombre,
              fecha y detalle quede bien antes de grabar nada."""),
    ("""              We are a family business, three generations in Oxnard since 1998. We were among the first in the area to
              place a color photograph on a granite memorial, and families rate us 4.8 out of 5. In 2023 we made a
              memorial for our own father, so we know what this moment asks of you.""",
     """              Somos un negocio familiar, tres generaciones en Oxnard desde 1998. Fuimos de los primeros en la zona en
              poner una fotografía a color en una lápida de granito, y las familias nos califican con 4.8 de 5. En
              2023 hicimos la lápida de nuestro propio padre, así que sabemos lo que este momento le pide."""),
    ('<p class="signoff">Jerry Garcia <span>Third generation, GVG Memorials</span></p>',
     '<p class="signoff">Jerry Garcia <span>Tercera generación, GVG Memorials</span></p>'),

    # --- five steps -----------------------------------------------------------------------------------
    ('<span class="chapter-name">How it works</span>', '<span class="chapter-name">Cómo funciona</span>'),
    ('<h2 id="steps-title" class="section-title">Five steps, <em>one at a time</em></h2>',
     '<h2 id="steps-title" class="section-title">Cinco pasos, <em>uno a la vez</em></h2>'),
    ('<p class="kicker">Step one</p>', '<p class="kicker">Paso uno</p>'),
    ("<h3>The cemetery</h3>", "<h3>El cementerio</h3>"),
    ("<p class=\"step-lede\">It decides what's possible, so we begin there.</p>",
     '<p class="step-lede">Decide lo que se puede hacer, así que empezamos ahí.</p>'),
    ("<p>Every cemetery has its own rules about size, material, and what can sit on the grave. Tell us which one, and we'll find out what's allowed. No paperwork? We'll call them for you.</p>",
     "<p>Cada cementerio tiene sus propias reglas sobre el tamaño, el material y lo que se puede poner en la tumba. Díganos cuál es y averiguamos qué está permitido. ¿No tiene los papeles? Nosotros les llamamos.</p>"),
    (">Ask about your cemetery</a>", ">Pregunte por su cementerio</a>"),
    ('<p class="kicker">Step two</p>', '<p class="kicker">Paso dos</p>'),
    ("<h3>The shape</h3>", "<h3>La forma</h3>"),
    ('<p class="step-lede">Flat, slanted, or standing tall.</p>', '<p class="step-lede">Plana, inclinada o de pie.</p>'),
    ("<p>Your cemetery decides which shapes are allowed, and we'll show you only those. A flat marker in granite or bronze rests level with the grass. A slant leans back so it's easy to read, and an upright stands as a traditional headstone. Most honor one person, and a companion leaves room for a husband or wife.</p>",
     "<p>Su cementerio decide qué formas se permiten, y le mostramos solo esas. Una placa plana de granito o de bronce queda al ras del pasto. Una lápida inclinada se recarga hacia atrás para que se lea fácil, y una vertical se levanta como la lápida tradicional. La mayoría honra a una persona, y una doble deja espacio para el esposo o la esposa.</p>"),
    ('<p class="kicker">Step three</p>', '<p class="kicker">Paso tres</p>'),
    ("<h3>The stone and the story</h3>", "<h3>La piedra y la historia</h3>"),
    ('<p class="step-lede">A name, two dates, and something that says who they were.</p>',
     '<p class="step-lede">Un nombre, dos fechas y algo que diga quién fue.</p>'),
    ("<p>See and touch real granite at our shop, in eighteen colors. Choose from 286 designs, or describe what you have in mind and we'll draw it. Where the cemetery allows, we can add a photo portrait or a bronze emblem.</p>",
     "<p>Vea y toque granito de verdad en nuestro taller, en dieciocho colores. Escoja entre 286 diseños, o descríbanos lo que tiene en mente y lo dibujamos. Donde el cementerio lo permite, podemos agregar un retrato con foto o un emblema de bronce.</p>"),
    ('<a class="text-link" href="#granite">See the granite and designs</a>',
     '<a class="text-link" href="#granite">Ver el granito y los diseños</a>'),
    ('<p class="kicker">Step four</p>', '<p class="kicker">Paso cuatro</p>'),
    ("<h3>The quote</h3>", "<h3>El presupuesto</h3>"),
    ('<p class="step-lede">Every cost in writing, before you decide.</p>',
     '<p class="step-lede">Cada costo por escrito, antes de decidir.</p>'),
    ("<p>We write down each item and what it costs, so you can take it home and talk it over. It's free, and you're under no obligation.</p>",
     "<p>Anotamos cada cosa y lo que cuesta, para que se lo lleve a casa y lo platique con su familia. Es gratis y sin ningún compromiso.</p>"),
    (">Ask for a free quote</a>", ">Pida un presupuesto gratis</a>"),
    ('<p class="kicker">Step five</p>', '<p class="kicker">Paso cinco</p>'),
    ("<h3>The proof</h3>", "<h3>La prueba</h3>"),
    ('<p class="step-lede">Nothing is carved until you sign off.</p>',
     '<p class="step-lede">No se graba nada hasta que usted lo apruebe.</p>'),
    ("<p>We draw the whole memorial to scale and send it to you. Read every name and date, share it with family, and ask for any change you want. Once you approve and sign, we begin engraving.</p>",
     "<p>Dibujamos la lápida completa a escala y se la mandamos. Lea cada nombre y fecha, compártala con su familia y pida cualquier cambio que quiera. Cuando usted la aprueba y firma, empezamos a grabar.</p>"),
    ('aria-label="A word from the family"', 'aria-label="Unas palabras de la familia"'),
    ("<p>&ldquo;A memorial is the last thing we make for someone, and the one that stays.&rdquo;</p>",
     "<p>&ldquo;Una lápida es lo último que hacemos por alguien, y lo que permanece.&rdquo;</p>"),
    ("<span>The Garcia family, GVG Memorials</span>", "<span>La familia Garcia, GVG Memorials</span>"),

    # --- granite --------------------------------------------------------------------------------------
    ('<span class="chapter-name">The collection</span>', '<span class="chapter-name">La colección</span>'),
    ('<h2 id="granite-title" class="section-title">Eighteen <em>granite colors</em></h2>',
     '<h2 id="granite-title" class="section-title">Dieciocho <em>colores de granito</em></h2>'),
    ("""              Photographs of the actual stone. Every stone is natural, so ask to see a sample at our shop before you
              decide.""",
     """              Fotografías de la piedra real, con su nombre de catálogo. Cada piedra es natural, así que pida ver una
              muestra en nuestro taller antes de decidir."""),
    ("<h3>A few from our album</h3>", "<h3>Algunos de nuestro álbum</h3>"),
    ("<p class=\"split-note\">286 designs, arranged by subject. If it isn't there, we'll draw it.</p>",
     '<p class="split-note">286 diseños, ordenados por tema. Si no está ahí, lo dibujamos.</p>'),
    ('alt="Sample marker design with a sunflower" /><span>Sunflower</span>',
     'alt="Diseño de muestra con un girasol" /><span>Girasol</span>'),
    ('alt="Sample marker design with Our Lady of Guadalupe" /><span>Guadalupe</span>',
     'alt="Diseño de muestra con la Virgen de Guadalupe" /><span>Guadalupe</span>'),
    ('alt="Sample marker design with a guitar and music notes" /><span>Guitar and music</span>',
     'alt="Diseño de muestra con una guitarra y notas musicales" /><span>Guitarra y música</span>'),
    ('alt="Sample marker design with a rose" /><span>Roses</span>', 'alt="Diseño de muestra con una rosa" /><span>Rosas</span>'),
    ('alt="Sample marker design with a lighthouse" /><span>Lighthouse</span>',
     'alt="Diseño de muestra con un faro" /><span>Faro</span>'),
    ('alt="Sample marker design with an eagle and flag" /><span>Eagle and flag</span>',
     'alt="Diseño de muestra con un águila y la bandera" /><span>Águila y bandera</span>'),

    # --- after you approve ----------------------------------------------------------------------------
    ('<span class="chapter-name">After you approve</span>', '<span class="chapter-name">Después de aprobar</span>'),
    ('<h2 id="after-title" class="section-title">From proof <em>to placement</em></h2>',
     '<h2 id="after-title" class="section-title">De la prueba <em>al cementerio</em></h2>'),
    ("""                We send the approved layout to your cemetery for its records and required review. When the memorial is
                finished, it is installed according to your cemetery's requirements. Most cemeteries set the memorial
                themselves. At Conejo Mountain Memorial Park, we install it ourselves. Either way, we'll tell you what
                to expect at your cemetery.""",
     """                Mandamos el diseño aprobado a su cementerio para sus registros y la revisión que pide. Cuando la lápida
                está terminada, se instala según las reglas de su cementerio. La mayoría de los cementerios la colocan
                ellos mismos. En Conejo Mountain Memorial Park, la instalamos nosotros. En cualquier caso, le decimos
                qué esperar en su cementerio."""),
    ('<h2 class="section-title">How long does it take?</h2>', '<h2 class="section-title">¿Cuánto tiempo tarda?</h2>'),
    ("""                It depends on the cemetery's review, the stone you choose, and the artwork. Once we know your cemetery
                and your choices, we'll give you a clear timeline.""",
     """                Depende de la revisión del cementerio, la piedra que escoja y el diseño. Cuando sepamos su cementerio y
                lo que eligió, le damos fechas claras."""),

    # --- what to bring --------------------------------------------------------------------------------
    ('<span class="chapter-name">Before you visit</span>', '<span class="chapter-name">Antes de su visita</span>'),
    ('<h2 id="bring-title" class="section-title">What to bring, <em>if you have it</em></h2>',
     '<h2 id="bring-title" class="section-title">Qué traer, <em>si lo tiene</em></h2>'),
    ('<p class="step-lede">Bring whatever you have. If something is missing, we can still begin.</p>',
     '<p class="step-lede">Traiga lo que tenga. Si falta algo, de todos modos podemos empezar.</p>'),
    ("<li>The cemetery name, and the section, lot, and space number</li>",
     "<li>El nombre del cementerio, y la sección, el lote y el número de espacio</li>"),
    ("<li>Their full name, as you'd like it engraved</li>", "<li>Su nombre completo, como le gustaría que se grabe</li>"),
    ("<li>Dates of birth and passing</li>", "<li>Las fechas de nacimiento y de fallecimiento</li>"),
    ("<li>Any words, a verse, or a nickname you'd like included</li>",
     "<li>Unas palabras, un verso o un apodo que quiera incluir</li>"),
    ("<li>A photo of them, for a portrait or an image based on something they loved</li>",
     "<li>Una foto de su ser querido, para un retrato o una imagen de algo que amaba</li>"),
    ("<li>Any paperwork from the cemetery</li>", "<li>Cualquier papel del cementerio</li>"),

    # --- gallery --------------------------------------------------------------------------------------
    ('<span class="chapter-name">Our work</span>', '<span class="chapter-name">Nuestro trabajo</span>'),
    ('<h2 id="completed-gallery-title" class="section-title">Crafted <em>with care</em></h2>',
     '<h2 id="completed-gallery-title" class="section-title">Hechas <em>con cariño</em></h2>'),
    ('<p class="split-note">Memorials from our shop. Tap any photo to see it larger.</p>',
     '<p class="split-note">Lápidas de nuestro taller. Toque cualquier foto para verla más grande.</p>'),
    ('aria-label="View larger: ', 'aria-label="Ver más grande: '),
    ("Puritan Rose granite with stainless steel photo", "Granito Puritan Rose con una foto en acero inoxidable"),
    ("Puritan Rose granite memorial with stainless steel photo by GVG Memorials",
     "Lápida de granito Puritan Rose con una foto en acero inoxidable, de GVG Memorials"),
    ("<span>Puritan Rose granite</span>", "<span>Granito Puritan Rose</span>"),
    ("Close detail of engraved granite memorial lettering by GVG Memorials",
     "Detalle de cerca de las letras grabadas en una lápida de granito, de GVG Memorials"),
    ("<span>Engraving detail</span>", "<span>Detalle del grabado</span>"),
    ("Custom polished black granite flat memorial with scenic artwork by GVG Memorials",
     "Placa a la medida de granito negro pulido con un paisaje, de GVG Memorials"),
    ("<span>Custom flat memorial</span>", "<span>Placa plana a la medida</span>"),
    ("<span>Oxford Gray granite</span>", "<span>Granito Oxford Gray</span>"),
    ("<span>Flat granite</span>", "<span>Placa de granito</span>"),
    ("<span>Companion memorial</span>", "<span>Lápida doble</span>"),
    ("Custom upright with an angel sculpture, by GVG Memorials", "Lápida vertical a la medida con la escultura de un ángel, de GVG Memorials"),
    ("Custom upright with an angel sculpture", "Lápida vertical a la medida con la escultura de un ángel"),
    ("<span>Custom upright</span>", "<span>Lápida vertical a la medida</span>"),
    ("Custom upright with Our Lady of Guadalupe, a portrait and vases, by GVG Memorials",
     "Lápida vertical a la medida con la Virgen de Guadalupe, un retrato y floreros, de GVG Memorials"),
    ("Custom upright with Our Lady of Guadalupe, a portrait and vases",
     "Lápida vertical a la medida con la Virgen de Guadalupe, un retrato y floreros"),
    ("Portraits, butterflies and a verse in two languages, by GVG Memorials",
     "Retratos, mariposas y un verso en dos idiomas, de GVG Memorials"),
    ("Portraits, butterflies and a verse in two languages", "Retratos, mariposas y un verso en dos idiomas"),
    ("Red granite memorial with carved swallows and roses, by GVG Memorials",
     "Lápida de granito rojo con golondrinas y rosas talladas, de GVG Memorials"),
    ("Red granite memorial with carved swallows and roses", "Lápida de granito rojo con golondrinas y rosas talladas"),
    ("Bronze companion memorial on a granite base, by GVG Memorials", "Placa doble de bronce sobre una base de granito, de GVG Memorials"),
    ("Bronze companion memorial on a granite base", "Placa doble de bronce sobre una base de granito"),
    ("<span>Flat bronze</span>", "<span>Placa de bronce</span>"),
    ("Bronze companion memorial with a floral border, by GVG Memorials", "Placa doble de bronce con un borde de flores, de GVG Memorials"),
    ("Bronze companion memorial with a floral border", "Placa doble de bronce con un borde de flores"),
    ("Rose granite memorial with carved roses, by GVG Memorials", "Lápida de granito rosa con rosas talladas, de GVG Memorials"),
    ("Rose granite memorial with carved roses", "Lápida de granito rosa con rosas talladas"),
    ("Bronze statue set on a granite monument, by GVG Memorials", "Estatua de bronce sobre un monumento de granito, de GVG Memorials"),
    ("Bronze statue set on a granite monument", "Estatua de bronce sobre un monumento de granito"),
    ("<span>Civic monument</span>", "<span>Monumento cívico</span>"),
    ("Detailed memorial engraving artwork on polished black granite by GVG Memorials",
     "Diseño grabado con detalle en granito negro pulido, de GVG Memorials"),
    ("<span>Detailed engraving</span>", "<span>Grabado detallado</span>"),
    ('aria-expanded="false">See more of our work</button>', 'aria-expanded="false">Ver más de nuestro trabajo</button>'),
    ('aria-label="Close enlarged memorial image"', 'aria-label="Cerrar la imagen ampliada"'),
    ('aria-label="View previous memorial"', 'aria-label="Ver la lápida anterior"'),
    ('aria-label="View next memorial"', 'aria-label="Ver la lápida siguiente"'),
    ('<a class="memorial-viewer-inquiry" href="#contact-form">Ask About a Similar Memorial</a>',
     '<a class="memorial-viewer-inquiry" href="#contact-form">Preguntar por una lápida parecida</a>'),
    ("<h3>What we make</h3>", "<h3>Lo que hacemos</h3>"),
    ("<span>Flat granite and bronze memorials</span>", "<span>Placas planas de granito y de bronce</span>"),
    ("<span>Slants</span>", "<span>Lápidas inclinadas</span>"),
    ("<span>Custom uprights</span>", "<span>Lápidas verticales a la medida</span>"),
    ("<span>Single and companion memorials</span>", "<span>Lápidas individuales y dobles</span>"),
    ("<span>Granite benches</span>", "<span>Bancas de granito</span>"),
    ("<span>Final dates</span>", "<span>Fechas finales</span>"),
    ("<span>Cleaning and restoration</span>", "<span>Limpieza y restauración</span>"),
    ('data-guidance-message="I have an existing memorial and need help adding a date or name, or with cleaning or restoration."',
     'data-guidance-message="Tengo una lápida y necesito ayuda para agregar una fecha o un nombre, o para limpiarla o restaurarla."'),
    ('data-guidance-item="Existing Memorials and Added Lettering"', 'data-guidance-item="Una lápida que ya existe"'),
    ('data-guidance-item="Cemetery requirements"', 'data-guidance-item="Las reglas del cementerio"'),
    ('data-guidance-item="A free written quote"', 'data-guidance-item="Un presupuesto por escrito gratis"'),
    ("<strong>Already have a memorial?</strong>", "<strong>¿Ya tiene una lápida?</strong>"),
    ("<span>If your loved one is joining someone already resting, we can add the final date or a new name. We also clean and restore older stones.</span>",
     "<span>Si su ser querido descansará junto a alguien que ya está ahí, podemos agregar la fecha final o un nombre nuevo. También limpiamos y restauramos lápidas antiguas.</span>"),

    # --- family ---------------------------------------------------------------------------------------
    ('<span class="chapter-name">Our family</span>', '<span class="chapter-name">Nuestra familia</span>'),
    ('<h2 id="family-title" class="section-title">Three generations, <em>serving yours</em></h2>',
     '<h2 id="family-title" class="section-title">Tres generaciones, <em>al servicio de la suya</em></h2>'),
    ('<p class="pull">&ldquo;His vision continues to guide us.&rdquo;</p>',
     '<p class="pull">&ldquo;Su visión nos sigue guiando.&rdquo;</p>'),
    ("<dd>Gerardo Valle Garcia and Gerardo Garcia Jr. founded GVG Memorials in Oxnard.</dd>",
     "<dd>Gerardo Valle Garcia y Gerardo Garcia Jr. fundaron GVG Memorials en Oxnard.</dd>"),
    ("<dt>Firsts</dt><dd>Among the first in the area to place a color photograph on a granite memorial.</dd>",
     "<dt>Pioneros</dt><dd>De los primeros en la zona en poner una fotografía a color en una lápida de granito.</dd>"),
    ("<dt>Today</dt><dd>Jerry Garcia carries the work forward as the third generation, working with carefully selected craftsmen and designers.</dd>",
     "<dt>Hoy</dt><dd>Jerry Garcia continúa el trabajo como la tercera generación, con artesanos y diseñadores escogidos con cuidado.</dd>"),
    ('alt="The memorial GVG made for Gerardo G. Garcia Jr."', 'alt="La lápida que GVG hizo para Gerardo G. Garcia Jr."'),
    ("<figcaption>The memorial we made for him.</figcaption>", "<figcaption>La lápida que hicimos para él.</figcaption>"),

    # --- reviews (the families' own words stay in English, marked as such) -----------------------------
    ('<span class="chapter-name">In their words</span>', '<span class="chapter-name">En sus palabras</span>'),
    ('<h2 id="reviews-title"><span class="sr-only">4.8 </span>out of 5 from families on Google</h2>',
     '<h2 id="reviews-title"><span class="sr-only">4.8 </span>de 5, según las familias en Google</h2>'),
    ('target="_blank" rel="noopener">Read the reviews</a>', 'target="_blank" rel="noopener">Leer las reseñas</a>'),
    ("<blockquote>\n                <p>&ldquo;Jerry was caring", '<blockquote lang="en">\n                <p>&ldquo;Jerry was caring'),
    ("<blockquote>\n                <p>&ldquo;Jerry made the process", '<blockquote lang="en">\n                <p>&ldquo;Jerry made the process'),

    # --- FAQ ------------------------------------------------------------------------------------------
    ('<span class="chapter-name">Questions</span>', '<span class="chapter-name">Preguntas</span>'),
    ('<h2 id="faq-title" class="section-title">Questions <em>families ask</em></h2>',
     '<h2 id="faq-title" class="section-title">Lo que preguntan <em>las familias</em></h2>'),
    ("<summary>Do I need to decide anything before I call?</summary>", "<summary>¿Tengo que decidir algo antes de llamar?</summary>"),
    ("<p>No. A name and a cemetery are enough to begin. We'll explain the choices and what your cemetery allows.</p>",
     "<p>No. Con un nombre y un cementerio podemos empezar. Le explicamos las opciones y lo que permite su cementerio.</p>"),
    ("<summary>What does a memorial cost?</summary>", "<summary>¿Cuánto cuesta una lápida?</summary>"),
    ("<p>It depends on the type, size, granite, artwork, and your cemetery's requirements. We give every family a free written quote with every item listed, before anything is decided.</p>",
     "<p>Depende del tipo, el tamaño, el granito, el diseño y las reglas de su cementerio. A cada familia le damos un presupuesto por escrito gratis, con cada cosa detallada, antes de decidir nada.</p>"),
    ("<summary>Can I see the stone before it's made?</summary>", "<summary>¿Puedo ver la lápida antes de que la hagan?</summary>"),
    ("<p>Yes. You'll see real granite samples at our shop and a full proof drawn to scale. Engraving begins only after you approve and sign the proof.</p>",
     "<p>Sí. Verá muestras de granito de verdad en nuestro taller y una prueba completa dibujada a escala. Solo empezamos a grabar cuando usted aprueba y firma la prueba.</p>"),
    ("<summary>Should we choose a single or a companion memorial?</summary>", "<summary>¿Conviene una lápida individual o una doble?</summary>"),
    ("<p>Most families choose a single memorial for their loved one. A companion memorial is for two people, such as a husband and wife. One side is engraved now and the other later, at our shop or at the cemetery, depending on the cemetery's requirements. Any size can be made either way.</p>",
     "<p>La mayoría de las familias elige una lápida individual para su ser querido. La lápida doble es para dos personas, como esposo y esposa. Un lado se graba ahora y el otro después, en nuestro taller o en el cementerio, según las reglas del cementerio. Cualquier tamaño puede hacerse de las dos formas.</p>"),
    ("<summary>Can you add a date to a stone that's already in place?</summary>",
     "<summary>¿Pueden agregar una fecha a una lápida que ya está colocada?</summary>"),
    ("<p>Yes. Send us a photo of the stone and the cemetery name, and we'll explain what's possible.</p>",
     "<p>Sí. Mándenos una foto de la lápida y el nombre del cementerio, y le explicamos qué se puede hacer.</p>"),

    # --- contact --------------------------------------------------------------------------------------
    ('<span class="chapter-name">Contact</span>', '<span class="chapter-name">Contacto</span>'),
    ("<h2 id=\"contact-title\" class=\"section-title\">Start whenever <em>you're ready</em></h2>",
     '<h2 id="contact-title" class="section-title">Empiece cuando <em>esté listo</em></h2>'),
    ("""                Tell us a little about your loved one and the cemetery, if you know it, and we'll call you back. You
                don't need every detail.""",
     """                Cuéntenos un poco de su ser querido y del cementerio, si lo sabe, y le devolvemos la llamada. No necesita
                tener todos los detalles."""),
    ("""                Hard to talk right now? <a href=\"""", """                ¿Le cuesta hablar en este momento? <a href=\""""),
    (""">Send us a text</a> at the same number. A photo of the
                stone or the cemetery paperwork is a fine way to start.""",
     """>Mándenos un mensaje de texto</a> al mismo número. Una foto
                de la lápida o de los papeles del cementerio es una buena forma de empezar."""),
    (">623 S A Street, Oxnard, CA 93030 <span>Get directions</span></a>",
     ">623 S A Street, Oxnard, CA 93030 <span>Cómo llegar</span></a>"),
    ('aria-label="Office hours"', 'aria-label="Horario"'),
    ("<dt>Monday&ndash;Friday</dt><dd>10 AM&ndash;6 PM</dd>", "<dt>Lunes a viernes</dt><dd>10 a.&nbsp;m. a 6 p.&nbsp;m.</dd>"),
    ("<dt>Saturday</dt><dd>12&ndash;3 PM</dd>", "<dt>Sábado</dt><dd>12 a 3 p.&nbsp;m.</dd>"),
    ("<dt>Sunday</dt><dd>Closed</dd>", "<dt>Domingo</dt><dd>Cerrado</dd>"),
    ('<p class="contact-note">We can meet at our shop or at your home.</p>',
     '<p class="contact-note">Podemos vernos en nuestro taller o en su casa.</p>'),
    (">Schedule a visit</a>", ">Hacer una cita</a>"),
    ('action="/thank-you/"', 'action="/es/gracias/"'),
    ('<input type="hidden" name="language" value="English" />', '<input type="hidden" name="language" value="Spanish" />'),
    ("<label>Do not fill this out: <input", "<label>No llene este campo: <input"),
    ("<h3 class=\"contact-form-title\" id=\"contact-form-title\" tabindex=\"-1\">We'll call you back</h3>",
     '<h3 class="contact-form-title" id="contact-form-title" tabindex="-1">Le devolvemos la llamada</h3>'),
    ("""              Your name and one way to reach you are all we need.
              <span lang="es">También atendemos en español.</span>""",
     """              Solo necesitamos su nombre y una forma de contactarle."""),
    ('<span class="contact-form-context-label">You asked about</span>',
     '<span class="contact-form-context-label">Usted preguntó por</span>'),
    ("aria-expanded=\"false\">Review details</button>", 'aria-expanded="false">Ver detalles</button>'),
    ('<span class="field-label">Your name <span class="field-required-text">Required</span></span>',
     '<span class="field-label">Su nombre <span class="field-required-text">Obligatorio</span></span>'),
    ('data-validation-message="Please enter your name."', 'data-validation-message="Por favor, escriba su nombre."'),
    ("""                  How should we reach you? <span class="field-required-text">Phone or email</span>""",
     """                  ¿Cómo le contactamos? <span class="field-required-text">Teléfono o correo</span>"""),
    ('<span class="field-label">Phone</span>', '<span class="field-label">Teléfono</span>'),
    ('<span class="field-label">Email</span>', '<span class="field-label">Correo electrónico</span>'),
    ('data-validation-message="Please enter a complete email address."',
     'data-validation-message="Por favor, escriba un correo electrónico completo."'),
    ("<summary>Add details or a photo, if you'd like</summary>", "<summary>Agregue detalles o una foto, si quiere</summary>"),
    ('<span class="field-label">What can we help with? <span class="field-optional">(optional)</span></span>',
     '<span class="field-label">¿En qué le podemos ayudar? <span class="field-optional">(opcional)</span></span>'),
    ('<option value="">Choose one</option>', '<option value="">Escoja una opción</option>'),
    ('<option value="Cemetery requirements">Cemetery requirements</option>',
     '<option value="Cemetery requirements">Las reglas del cementerio</option>'),
    ('<option value="Choosing a memorial style">Choosing a memorial</option>',
     '<option value="Choosing a memorial style">Escoger una lápida</option>'),
    ('<option value="Existing memorial or added lettering">Adding a date, or restoring a stone</option>',
     '<option value="Existing memorial or added lettering">Agregar una fecha o restaurar una lápida</option>'),
    ('<option value="Wording, dates, or artwork">Wording, dates, or artwork</option>',
     '<option value="Wording, dates, or artwork">Palabras, fechas o diseño</option>'),
    ('<option value="A free written quote">A free written quote</option>',
     '<option value="A free written quote">Un presupuesto por escrito gratis</option>'),
    ("<option value=\"I am not sure yet\">I'm not sure yet</option>", '<option value="I am not sure yet">Todavía no sé</option>'),
    ('<span class="field-label">Cemetery <span class="field-optional">(if known)</span></span>',
     '<span class="field-label">Cementerio <span class="field-optional">(si lo sabe)</span></span>'),
    ('<span class="field-label">Photo or document <span class="field-optional">(optional)</span></span>',
     '<span class="field-label">Foto o documento <span class="field-optional">(opcional)</span></span>'),
    ("data-file-help>One JPG, PNG, WebP, HEIC, or PDF, up to 8 MB.</span>",
     "data-file-help>Un JPG, PNG, WebP, HEIC o PDF, de hasta 8 MB.</span>"),
    ('<span class="field-label">Message <span class="field-optional">(optional)</span></span>',
     '<span class="field-label">Mensaje <span class="field-optional">(opcional)</span></span>'),
    ("placeholder=\"Their name, the cemetery, or anything you'd like us to know.\"",
     'placeholder="Su nombre, el cementerio o cualquier cosa que quiera contarnos."'),
    ('<button type="submit" class="button button-primary" aria-live="polite">Send</button>',
     '<button type="submit" class="button button-primary" aria-live="polite">Enviar</button>'),
    ("Your information stays with GVG Memorials and is used only to respond.",
     "Su información se queda con GVG Memorials y solo la usamos para responderle."),

    # --- footer and analytics banner ------------------------------------------------------------------
    ("<p>Family owned since 1998</p>", "<p>Negocio familiar desde 1998</p>"),
    ('aria-expanded="false">Analytics choices</button>', 'aria-expanded="false">Opciones de análisis</button>'),
    ('aria-label="Analytics privacy choices"', 'aria-label="Opciones de privacidad"'),
    ("<strong>Help us improve this website</strong>", "<strong>Ayúdenos a mejorar este sitio</strong>"),
    ("<p>Privacy-focused analytics show us which pages and contact options help families. No advertising tracking.</p>",
     "<p>Un análisis respetuoso de su privacidad nos muestra qué páginas y formas de contacto ayudan a las familias. Sin rastreo publicitario.</p>"),
    ("data-analytics-accept>Allow analytics</button>", "data-analytics-accept>Permitir</button>"),
    ("data-analytics-decline>Continue without</button>", "data-analytics-decline>Continuar sin análisis</button>"),

    # --- inline slideshow script ----------------------------------------------------------------------
    ('pause.setAttribute("aria-label", playing ? "Pause photos" : "Play photos");',
     'pause.setAttribute("aria-label", playing ? "Pausar fotos" : "Reproducir fotos");'),
    ('more.textContent = open ? "See more of our work" : "Show fewer";',
     'more.textContent = open ? "Ver más de nuestro trabajo" : "Ver menos";'),
    ('var prompts = ["Where do I start?", "What does my cemetery allow?", "Add a date to a stone", "A portrait on the memorial", "What does a memorial cost?", "A companion for my parents"];',
     'var prompts = ["¿Por dónde empiezo?", "¿Qué permite mi cementerio?", "Agregar una fecha a una lápida", "Un retrato en la lápida", "¿Cuánto cuesta una lápida?", "Una lápida doble para mis papás"];'),
    ('input.placeholder = "Try \\u2018" + prompts[p] + "\\u2019";',
     'input.placeholder = "Por ejemplo: \\u2018" + prompts[p] + "\\u2019";'),
    (SMS_EN, SMS_ES),
]


# Strings on the thank-you page that the homepage list doesn't already cover.
THANK_YOU_PAIRS = [
    ('<html lang="en">', '<html lang="es">'),
    ("<title>Message received | GVG Memorials</title>", "<title>Mensaje recibido | GVG Memorials</title>"),
    ('content="GVG Memorials received your message. We will review your details carefully and respond personally."',
     'content="GVG Memorials recibió su mensaje. Lo leeremos con cuidado y le responderemos personalmente."'),
    ('<a class="skip-link" href="#main-content">Skip to main content</a>',
     '<a class="skip-link" href="#main-content">Saltar al contenido</a>'),
    ('aria-label="Primary navigation"', 'aria-label="Navegación principal"'),
    ('aria-label="GVG Memorials home"', 'aria-label="GVG Memorials, inicio"'),
    ('<a class="brand" href="/"', '<a class="brand" href="/es/"'),
    ('<p class="section-label">Message received</p>', '<p class="section-label">Mensaje recibido</p>'),
    ("<h1>Thank you for reaching out</h1>", "<h1>Gracias por escribirnos</h1>"),
    ("""            We have your message. A member of our family will read it and call or write back personally.""",
     """            Ya tenemos su mensaje. Alguien de nuestra familia lo leerá y le llamará o le escribirá personalmente."""),
    ("<h2 id=\"save-number-title\">We'll call from", '<h2 id="save-number-title">Le llamaremos del'),
    ("<p>Save our number so you'll know it's us when we call, and not a stranger.</p>",
     "<p>Guarde nuestro número para que sepa que somos nosotros cuando llamemos, y no un desconocido.</p>"),
    ('data-analytics-event="save_contact_click">Add us to your contacts</a>',
     'data-analytics-event="save_contact_click">Guardar nuestro número</a>'),
    ('<h2 id="thank-you-next-title">While you wait, if you have them</h2>',
     '<h2 id="thank-you-next-title">Mientras tanto, si los tiene a la mano</h2>'),
    ("<strong>The cemetery</strong>", "<strong>El cementerio</strong>"),
    ("<small>Its name, and the section, lot, and space number from any paperwork.</small>",
     "<small>Su nombre, y la sección, el lote y el número de espacio de cualquier papel.</small>"),
    ("<strong>Their name and dates</strong>", "<strong>Su nombre y sus fechas</strong>"),
    ("<small>Written the way you'd like them engraved.</small>", "<small>Escritos como le gustaría que se graben.</small>"),
    ("<strong>A photo</strong>", "<strong>Una foto</strong>"),
    ("<small>Of them, or of something they loved. There's no rush to find it.</small>",
     "<small>De su ser querido, o de algo que amaba. No hay prisa por encontrarla.</small>"),
    ('<a class="button button-primary" href="tel:+18058893769">Call (805) 889-3769</a>',
     '<a class="button button-primary" href="tel:+18058893769">Llamar al (805) 889-3769</a>'),
    ('<a class="button button-outline" href="/">Return home</a>', '<a class="button button-outline" href="/es/">Volver al inicio</a>'),
    ("<p>Family owned since 1998</p>", "<p>Negocio familiar desde 1998</p>"),
    ("<span>Custom stone memorials planned with patience, clarity, and care.</span>",
     "<span>Lápidas a la medida, planeadas con paciencia, claridad y cariño.</span>"),
    ('aria-label="Get directions to GVG Memorials at 623 S A St, Oxnard, CA 93030"',
     'aria-label="Cómo llegar a GVG Memorials, 623 S A St, Oxnard, CA 93030"'),
    (">Analytics choices</button>", ">Opciones de análisis</button>"),
    ('aria-label="Analytics privacy choices"', 'aria-label="Opciones de privacidad"'),
    ("<strong>Help us improve this website</strong>", "<strong>Ayúdenos a mejorar este sitio</strong>"),
    ("<p>Privacy-focused analytics show us which pages and contact options help families. No advertising tracking.</p>",
     "<p>Un análisis respetuoso de su privacidad nos muestra qué páginas y formas de contacto ayudan a las familias. Sin rastreo publicitario.</p>"),
    ("data-analytics-accept>Allow analytics</button>", "data-analytics-accept>Permitir</button>"),
    ("data-analytics-decline>Continue without</button>", "data-analytics-decline>Continuar sin análisis</button>"),
]

NOTE = "<!-- Generated by scripts/build_es.py from {source}. Edit the English page and that script, not this file. -->"


def translate(source_name, pairs):
    html = (ROOT / source_name).read_text()
    missing = []
    for english, spanish in pairs:
        if english not in html:
            missing.append(english)
            continue
        html = html.replace(english, spanish)
    if missing:
        print(f"These English strings are no longer in {source_name}. Update scripts/build_es.py:\n", file=sys.stderr)
        for english in missing:
            print("  - " + english.strip()[:140], file=sys.stderr)
        sys.exit(1)
    return html.replace("<!doctype html>", "<!doctype html>\n" + NOTE.format(source=source_name), 1)


def write(path, html, count):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"Wrote {path} ({count} strings translated)")


def main():
    html = translate("index.html", PAIRS)
    # The Spanish page lives one folder down, so local files are served from the site root.
    html = re.sub(r'(src|href)="(?!https?:|/|#|tel:|sms:|mailto:|data:)', r'\1="/', html)
    html = re.sub(r'(srcset|data-srcset)="([^"]+)"',
                  lambda m: m.group(1) + '="' + re.sub(r"(^|, )(?!/|https?:)", r"\1/", m.group(2)) + '"', html)
    write("es/index.html", html, len(PAIRS))

    write("es/gracias/index.html", translate("thank-you/index.html", THANK_YOU_PAIRS), len(THANK_YOU_PAIRS))


if __name__ == "__main__":
    main()
