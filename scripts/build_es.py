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
SMS_EN = "Hi%2C%20I%27d%20like%20help%20with%20a%20headstone."
SMS_ES = "Hola%2C%20GVG%20Memorials.%20Quisiera%20ayuda%20con%20una%20l%C3%A1pida."

# (English, Spanish). Order matters only where one string contains another; longer strings come first.
PAIRS = [
    # --- head ---------------------------------------------------------------------------------------
    ('<html lang="en">', '<html lang="es">'),
    ('<link rel="canonical" href="https://www.gvgmemorials.com/" />',
     '<link rel="canonical" href="https://www.gvgmemorials.com/es/" />'),
    ('<title>Headstones and Grave Markers in Oxnard | GVG Memorials</title>',
     '<title>Lápidas y placas para el cementerio en Oxnard | GVG Memorials</title>'),
    ('content="Headstones and grave markers for Oxnard and Ventura County families, from the Garcia family since 1998. Free written quote. Se habla español."',
     'content="Lápidas y placas para familias de Oxnard y del condado de Ventura, de la familia Garcia desde 1998. Presupuesto por escrito gratis. Atendemos en español."'),
    ('<meta property="og:title" content="Headstones and Grave Markers in Oxnard | GVG Memorials" />',
     '<meta property="og:title" content="Lápidas y placas para el cementerio en Oxnard | GVG Memorials" />'),
    ('<meta name="twitter:title" content="Headstones and Grave Markers in Oxnard | GVG Memorials" />',
     '<meta name="twitter:title" content="Lápidas y placas para el cementerio en Oxnard | GVG Memorials" />'),
    ("content=\"Family-owned since 1998. We guide you through every choice, check your cemetery's requirements, and give you a free written quote.\"",
     'content="Negocio familiar desde 1998. Le acompañamos en cada decisión, revisamos las reglas de su cementerio y le damos un presupuesto por escrito gratis."'),
    ('<meta property="og:url" content="https://www.gvgmemorials.com/" />',
     '<meta property="og:url" content="https://www.gvgmemorials.com/es/" />'),
    ('<meta property="og:locale" content="en_US" />',
     '<meta property="og:locale" content="es_US" />\n    <meta property="og:locale:alternate" content="en_US" />'),
    ('content="A large gold serif G with GVG Memorials, Oxnard, since 1998, inside it"',
     'content="Una G dorada grande con GVG Memorials, Oxnard, desde 1998, en su interior"'),
    ('"url": "https://www.gvgmemorials.com/",', '"url": "https://www.gvgmemorials.com/es/",'),
    ('"description": "Family-owned Oxnard memorial company, since 1998. Flat granite and bronze markers, slant markers, custom uprights, single and companion memorials, granite benches, final dates on existing stones, and cleaning and restoration."',
     '"description": "Negocio familiar de lápidas en Oxnard desde 1998. Placas planas de granito y de bronce, lápidas inclinadas, lápidas verticales a la medida, lápidas individuales y dobles, bancas de granito, fechas finales en lápidas existentes, y limpieza y restauración.",\n        "knowsLanguage": ["es", "en"]'),
    ('"name": "Do I need to decide anything before I call?"', '"name": "¿Tengo que decidir algo antes de llamar?"'),
    ('"text": "No. Call when you\'re ready, and we\'ll explain the choices and what your cemetery allows."',
     '"text": "No. Llame cuando esté listo, y le explicamos las opciones y lo que permite su cementerio."'),
    ('"name": "What does a memorial cost?"', '"name": "¿Cuánto cuesta una lápida?"'),
    ("\"text\": \"It depends on the type, size, granite, artwork, and your cemetery's requirements. We give every family a free written quote with every item listed, before anything is decided.\"",
     '"text": "Depende del tipo, el tamaño, el granito, el diseño y las reglas de su cementerio. A cada familia le damos un presupuesto por escrito gratis, con cada cosa detallada, antes de decidir nada."'),
    ('"name": "Should we choose a single or a companion memorial?"', '"name": "¿Conviene una lápida individual o una doble?"'),
    ('"text": "Most families choose a single memorial. A companion is for two people, such as a husband and wife: one side is engraved now and the other later, at our shop or at the cemetery, as the cemetery allows. Any size can be made either way."',
     '"text": "La mayoría de las familias elige una lápida individual. La doble es para dos personas, como esposo y esposa: un lado se graba ahora y el otro después, en nuestro taller o en el cementerio, según lo permita el cementerio. Cualquier tamaño puede hacerse de las dos formas."'),
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
    ('<a href="#granite">Granite &amp; Designs</a>',
     '<a href="#granite">Granito y diseños</a>'),
    ('<a href="#gallery">Our Work</a>', '<a href="#gallery">Galería</a>'),
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
    ('<p class="hero-kicker">Oxnard, California · <span>Family-owned since 1998</span></p>',
     '<p class="hero-kicker">Oxnard, California · <span>Negocio familiar desde 1998</span></p>'),
    ('<h1 id="hero-title">Headstones made with care, <em>for the one you love.</em></h1>',
     '<h1 id="hero-title">Lápidas hechas con cariño, <em>para quien tanto ama.</em></h1>'),
    ('<p class="hero-sub">Tell us their name and the cemetery, and we\'ll take it from there, at your family\'s pace, with a free written quote.</p>',
     '<p class="hero-sub">Díganos su nombre y el cementerio, y nosotros nos encargamos del resto, al paso de su familia, con un presupuesto por escrito gratis.</p>'),
    ('<p class="hero-proof"><a href="#reviews">Rated 4.8 out of 5 by families on Google</a></p>',
     '<p class="hero-proof"><a href="#reviews">Calificación de 4.8 de 5 según las familias en Google</a></p>'),
    ('<a class="button button-outline" href="#contact-form">Ask us a question</a>',
     '<a class="button button-outline" href="#contact-form">Háganos una pregunta</a>'),
    ('<p class="hero-es" lang="es">También atendemos en español. <a href="/es/" hreflang="es">Ver esta página en español</a></p>',
     '<p class="hero-es" lang="en">We also help families in English. <a href="/" hreflang="en">Read this page in English</a></p>'),

    # --- slideshow ------------------------------------------------------------------------------------

    # --- opening note ---------------------------------------------------------------------------------
    ('aria-label="A first word"', 'aria-label="Unas palabras"'),
    ("              Choosing a memorial for someone you love is deeply personal. You don't need to have a design in mind or\n              all the answers before we talk. We'll take the time to listen, understand what matters to your family, and\n              help you create something that reflects their life.",
     '              Elegir una lápida para alguien que ama es algo muy personal. No necesita tener un diseño en mente ni\n              todas las respuestas antes de hablar con nosotros. Nos tomaremos el tiempo de escucharle, entender lo que\n              es importante para su familia y ayudarle a crear algo que refleje su vida.'),
    ("              We'll confirm your cemetery's requirements, show you granite samples, and prepare a layout for you to\n              review. Nothing is engraved until you've checked every name, date, and detail and approved the final\n              design.",
     '              Confirmamos las reglas de su cementerio, le mostramos muestras de granito y preparamos un diseño para que\n              lo revise. No se graba nada hasta que usted haya revisado cada nombre, fecha y detalle, y aprobado el\n              diseño final.'),
    ('              We are a three-generation family business that has served our community since 1998. We were among the\n              first in the area to offer color photographs on granite memorials, giving families a way to make each\n              tribute more personal by preserving the familiar face of someone they love.',
     '              Somos un negocio familiar de tres generaciones que sirve a nuestra comunidad desde 1998. Fuimos de los\n              primeros en la zona en ofrecer fotografías a color en lápidas de granito, para que cada familia pudiera\n              hacer su homenaje más personal conservando el rostro de su ser querido.'),
    ('<p class="signoff">Jerry Garcia <span>Third generation, GVG Memorials</span></p>',
     '<p class="signoff">Jerry Garcia <span>Tercera generación, GVG Memorials</span></p>'),

    # --- five steps -----------------------------------------------------------------------------------
    ('<h2 id="steps-title" class="section-title" data-reveal>Five steps, one at a time</h2>',
     '<h2 id="steps-title" class="section-title" data-reveal>Cinco pasos, uno a la vez</h2>'),
    ('<h3>Start with the cemetery</h3>',
     '<h3>Empiece por el cementerio</h3>'),
    ("<p class=\"step-lede\">It decides what's possible, so we begin there.</p>",
     '<p class="step-lede">Decide lo que se puede hacer, así que empezamos ahí.</p>'),
    ("<p>Every cemetery has its own rules about size, material, and what can sit on the grave. Tell us which one, and we'll find out what's allowed.</p>",
     '<p>Cada cementerio tiene sus propias reglas sobre el tamaño, el material y lo que se puede poner en la tumba. Díganos cuál es y averiguamos qué está permitido.</p>'),
    (">Ask about your cemetery</a>", ">Pregunte por su cementerio</a>"),
    ('<h3>Choose the shape</h3>',
     '<h3>Elija la forma</h3>'),
    ('<p class="step-lede">Flat, slanted, or standing tall.</p>', '<p class="step-lede">Plana, inclinada o de pie.</p>'),
    ("<p>We'll show you only the shapes your cemetery allows. A flat marker rests level with the grass, in granite or bronze. A slant leans back so it's easy to read. An upright is the traditional standing headstone. Most are for one person, and a companion has room for two.</p>",
     '<p>Le mostramos solo las formas que permite su cementerio. Una placa plana queda al ras del pasto, en granito o en bronce. Una lápida inclinada se recarga hacia atrás para que se lea fácil. Una vertical es la lápida tradicional de pie. La mayoría son para una persona, y una doble tiene espacio para dos.</p>'),
    ('<h3>Make it theirs</h3>',
     '<h3>Hágala suya</h3>'),
    ('<p class="step-lede">A name, two dates, and something that says who they were.</p>',
     '<p class="step-lede">Un nombre, dos fechas y algo que diga quién fue.</p>'),
    ("<p>Visit our shop to see and touch granite samples, browse our designs, or share your ideas, and we'll create a custom layout. You can add a photo, portrait, or bronze emblem where your cemetery allows.</p>",
     '<p>Visite nuestro taller para ver y tocar muestras de granito, ver nuestros diseños o compartir sus ideas, y le preparamos un diseño a la medida. Puede agregar una foto, un retrato o un emblema de bronce donde su cementerio lo permita.</p>'),
    ('<a class="text-link" href="#granite">See the granite and designs</a>',
     '<a class="text-link" href="#granite">Ver el granito y los diseños</a>'),
    ('<h3>Get your quote</h3>',
     '<h3>Reciba su presupuesto</h3>'),
    ('<p class="step-lede">Every cost in writing, before you decide.</p>',
     '<p class="step-lede">Cada costo por escrito, antes de decidir.</p>'),
    ("<p>We'll provide a free written quote with a clear breakdown of costs. There's no obligation to order.</p>",
     '<p>Le damos un presupuesto por escrito gratis, con cada costo detallado. No hay ninguna obligación de ordenar.</p>'),
    (">Ask for a free quote</a>", ">Pida un presupuesto gratis</a>"),
    ('<h3>Approve the proof</h3>',
     '<h3>Apruebe el diseño</h3>'),
    ('<p class="step-lede">Nothing is carved until you sign and approve the final layout.</p>',
     '<p class="step-lede">No se graba nada hasta que usted firme y apruebe el diseño final.</p>'),
    ("<p>We draw the whole memorial to scale and send it to you. Read every name and date, share it with family, and ask for any change you want. Once you approve and sign, we begin engraving.</p>",
     "<p>Dibujamos la lápida completa a escala y se la mandamos. Lea cada nombre y fecha, compártala con su familia y pida cualquier cambio que quiera. Cuando usted la aprueba y firma, empezamos a grabar.</p>"),
    ('aria-label="A word from the family"', 'aria-label="Unas palabras de la familia"'),
    ("<p>&ldquo;A memorial is the last thing we make for someone, and the one that stays.&rdquo;</p>",
     "<p>&ldquo;Una lápida es lo último que hacemos por alguien, y lo que permanece.&rdquo;</p>"),
    ("<span>The Garcia family, GVG Memorials</span>", "<span>La familia Garcia, GVG Memorials</span>"),

    # --- granite --------------------------------------------------------------------------------------
    ('<h2 id="granite-title" class="section-title">Seventeen granite colors</h2>',
     '<h2 id="granite-title" class="section-title">Diecisiete colores de granito</h2>'),
    ('              Every stone is natural, so ask to see a sample at our shop before you decide.',
     '              Cada piedra es natural, así que pida ver una muestra en nuestro taller antes de decidir.'),
    ("<h3>A few from our album</h3>", "<h3>Algunos de nuestro álbum</h3>"),
    ('<p class="section-note">Designs, arranged by subject. If it isn\'t there, we\'ll draw it.</p>',
     '<p class="section-note">Diseños ordenados por tema. Si no está ahí, lo dibujamos.</p>'),
    ('alt="Sample marker design with a sunflower" /><span>Sunflower</span>',
     'alt="Diseño de muestra con un girasol" /><span>Girasol</span>'),
    ('alt="Sample marker design with Our Lady of Guadalupe" /><span>Our Lady of Guadalupe</span>',
     'alt="Diseño de muestra con la Virgen de Guadalupe" /><span>Virgen de Guadalupe</span>'),
    ('alt="Sample marker design with a guitar and music notes" /><span>Guitar and music</span>',
     'alt="Diseño de muestra con una guitarra y notas musicales" /><span>Guitarra y música</span>'),
    ('alt="Sample marker design with a rose" /><span>Roses</span>', 'alt="Diseño de muestra con una rosa" /><span>Rosas</span>'),
    ('alt="Sample marker design with a lighthouse" /><span>Lighthouse</span>',
     'alt="Diseño de muestra con un faro" /><span>Faro</span>'),
    ('alt="Sample marker design with an eagle and flag" /><span>Eagle and flag</span>',
     'alt="Diseño de muestra con un águila y la bandera" /><span>Águila y bandera</span>'),

    # --- after you approve ----------------------------------------------------------------------------
    ("<h3>After you approve</h3>", "<h3>Después de aprobar</h3>"),
    ("                We send the approved layout to your cemetery for its review. Most cemeteries set the memorial\n                themselves; at Conejo Mountain Memorial Park, we install it ourselves. Either way, we'll tell you what\n                to expect.",
     '                Enviamos el diseño aprobado a su cementerio para su revisión. La mayoría de los cementerios colocan la\n                lápida ellos mismos; en Conejo Mountain Memorial Park, la instalamos nosotros. De cualquier forma, le\n                diremos qué esperar.'),
    ("<h3>How long does it take?</h3>", "<h3>¿Cuánto tiempo tarda?</h3>"),
    ("""                It depends on the cemetery's review, the stone you choose, and the artwork. Once we know your cemetery
                and your choices, we'll give you a clear timeline.""",
     """                Depende de la revisión del cementerio, la piedra que escoja y el diseño. Cuando sepamos su cementerio y
                lo que eligió, le damos fechas claras."""),

    # --- what to bring --------------------------------------------------------------------------------
    ("<h3>What to bring, if you have it</h3>", "<h3>Qué traer, si lo tiene</h3>"),
    ('<p class="bring-note">Bring what you have. If something is missing, we can still begin.</p>',
     '<p class="bring-note">Traiga lo que tenga. Si falta algo, de todos modos podemos empezar.</p>'),
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
    ('<h2 id="completed-gallery-title" class="section-title">Recent work</h2>',
     '<h2 id="completed-gallery-title" class="section-title">Trabajos recientes</h2>'),
    ('<p class="section-note">Memorials from our shop. Tap any photo to see it larger.</p>',
     '<p class="section-note">Lápidas de nuestro taller. Toque cualquier foto para verla más grande.</p>'),
    ('aria-label="View larger: ', 'aria-label="Ver más grande: '),
    ('Custom monument with a marble Our Lady of Guadalupe sculpture, a portrait and granite flower vases',
     'Monumento a la medida con una escultura de mármol de la Virgen de Guadalupe, un retrato y floreros de granito'),
    ('Palms, hibiscus and an anchor on a beach scene for a husband and wife',
     'Palmeras, hibiscos y un ancla en una escena de playa, para esposo y esposa'),
    ('Mission scene with a color portrait for a husband and wife',
     'Escena de una misión con un retrato a color, para esposo y esposa'),
    ('Blue granite companion memorial with a color portrait',
     'Lápida doble de granito azul con un retrato a color'),
    ('Deep-sunk sanded panel with carved swallows and roses',
     'Panel hundido y arenado con golondrinas y rosas talladas'),
    ('Puritan Rose granite with a stainless steel portrait',
     'Granito Puritan Rose con un retrato en acero inoxidable'),
    ('Ventura County Fallen Firefighter Memorial Expansion',
     'Ampliación del Monumento a los Bomberos Caídos del Condado de Ventura'),
    ('Oxford Gray granite with a pine forest and an eagle',
     'Granito Oxford Gray con un bosque de pinos y un águila'),
    ('Portraits, butterflies and a verse in two languages',
     'Retratos, mariposas y un verso en dos idiomas'),
    ('Polished black granite with custom scenic artwork',
     'Granito negro pulido con un paisaje hecho a la medida'),
    ('Blue Pearl granite with a deep-sunk sanded panel',
     'Granito Blue Pearl con un panel hundido y arenado'),
    ('Custom-shaped color photo and baseball artwork',
     'Foto a color con forma a la medida y un diseño de béisbol'),
    ('Bronze companion memorial with a floral border',
     'Placa doble de bronce con un borde de flores'),
    ('Bronze companion memorial on a granite base',
     'Placa doble de bronce sobre una base de granito'),
    ('A color photo, a football and a key border',
     'Una foto a color, un balón de fútbol americano y una greca'),
    ('Custom upright with an angel sculpture',
     'Lápida vertical a la medida con la escultura de un ángel'),
    ('Engraved artwork on polished granite',
     'Diseño grabado en granito pulido'),
    ('Color portraits, etched photographs',
     'Retratos a color, fotos grabadas'),
    ('Carved doves on Blue Pearl granite',
     'Palomas talladas en granito Blue Pearl'),
    ('Rose granite with carved roses',
     'Granito rosa con rosas talladas'),
    ('A color portrait with a verse',
     'Un retrato a color con un verso'),
    (', by GVG Memorials"',
     ', de GVG Memorials"'),
    ("<span>Puritan Rose granite</span>", "<span>Granito Puritan Rose</span>"),
    ("<span>Engraving detail</span>", "<span>Detalle del grabado</span>"),
    ("<span>Custom flat memorial</span>", "<span>Placa plana a la medida</span>"),
    ("<span>Flat granite</span>", "<span>Placa de granito</span>"),
    ("<span>Companion memorial</span>", "<span>Lápida doble</span>"),
    ("<span>Custom upright</span>", "<span>Lápida vertical a la medida</span>"),
    ("<span>Flat bronze</span>", "<span>Placa de bronce</span>"),
    ("<span>Civic monument</span>", "<span>Monumento cívico</span>"),
    ("<span>Detailed engraving</span>", "<span>Grabado detallado</span>"),
    ('aria-expanded="false">See more of our work</button>', 'aria-expanded="false">Ver más de nuestro trabajo</button>'),
    ('aria-label="Close enlarged memorial image"', 'aria-label="Cerrar la imagen ampliada"'),
    ('aria-label="View previous memorial"', 'aria-label="Ver la lápida anterior"'),
    ('aria-label="View next memorial"', 'aria-label="Ver la lápida siguiente"'),
    ('<a class="memorial-viewer-inquiry" href="#contact-form">Ask about a memorial like this</a>',
     '<a class="memorial-viewer-inquiry" href="#contact-form">Preguntar por una lápida como esta</a>'),
    ('<h3>What we create</h3>',
     '<h3>Lo que creamos</h3>'),
    ('<li>Flat granite and bronze markers</li>',
     '<li>Placas planas de granito y de bronce</li>'),
    ('<li>Slant markers</li>',
     '<li>Lápidas inclinadas</li>'),
    ("<li>Custom uprights</li>", "<li>Lápidas verticales a la medida</li>"),
    ("<li>Single and companion memorials</li>", "<li>Lápidas individuales y dobles</li>"),
    ("<li>Granite benches</li>", "<li>Bancas de granito</li>"),
    ('<li>Final dates on existing stones</li>',
     '<li>Fechas finales en lápidas existentes</li>'),
    ("<li>Cleaning and restoration</li>", "<li>Limpieza y restauración</li>"),
    ('data-guidance-message="I have an existing memorial and need help adding a date or name, or with cleaning or restoration."',
     'data-guidance-message="Tengo una lápida y necesito ayuda para agregar una fecha o un nombre, o para limpiarla o restaurarla."'),
    ('data-guidance-item="Existing Memorials and Added Lettering"', 'data-guidance-item="Una lápida que ya existe"'),
    ('data-guidance-item="Cemetery requirements"', 'data-guidance-item="Las reglas del cementerio"'),
    ('data-guidance-item="A free written quote"', 'data-guidance-item="Un presupuesto por escrito gratis"'),
    ('<strong>Already have a headstone?</strong>',
     '<strong>¿Ya tiene una lápida?</strong>'),
    ("<span>If your loved one is joining someone already resting, we can add the final date or a new name. We also clean and restore older stones.</span>",
     "<span>Si su ser querido descansará junto a alguien que ya está ahí, podemos agregar la fecha final o un nombre nuevo. También limpiamos y restauramos lápidas antiguas.</span>"),

    # --- reviews (the families' own words stay in English, marked as such) -----------------------------
    ('<h2 id="reviews-title"><span class="sr-only">4.8 </span>out of 5 from families on Google</h2>',
     '<h2 id="reviews-title"><span class="sr-only">4.8 </span>de 5, según las familias en Google</h2>'),
    ('target="_blank" rel="noopener">Read the reviews</a>', 'target="_blank" rel="noopener">Leer las reseñas</a>'),
    ("<blockquote>\n                <p>&ldquo;Jerry was caring", '<blockquote lang="en">\n                <p>&ldquo;Jerry was caring'),
    ("<blockquote>\n                <p>&ldquo;Jerry made the process", '<blockquote lang="en">\n                <p>&ldquo;Jerry made the process'),

    # --- FAQ ------------------------------------------------------------------------------------------
    ('<h2 id="faq-title" class="section-title">Questions families ask</h2>',
     '<h2 id="faq-title" class="section-title">Lo que preguntan las familias</h2>'),
    ("<summary>Do I need to decide anything before I call?</summary>", "<summary>¿Tengo que decidir algo antes de llamar?</summary>"),
    ("<p>No. Call when you're ready, and we'll explain the choices and what your cemetery allows.</p>",
     '<p>No. Llame cuando esté listo, y le explicamos las opciones y lo que permite su cementerio.</p>'),
    ("<summary>What does a memorial cost?</summary>", "<summary>¿Cuánto cuesta una lápida?</summary>"),
    ("<p>It depends on the type, size, granite, artwork, and your cemetery's requirements. We give every family a free written quote with every item listed, before anything is decided.</p>",
     "<p>Depende del tipo, el tamaño, el granito, el diseño y las reglas de su cementerio. A cada familia le damos un presupuesto por escrito gratis, con cada cosa detallada, antes de decidir nada.</p>"),
    ("<summary>Can I see the stone before it's made?</summary>", "<summary>¿Puedo ver la lápida antes de que la hagan?</summary>"),
    ("<p>Yes. You'll see real granite samples at our shop and a full proof drawn to scale. Engraving begins only after you approve and sign the proof.</p>",
     "<p>Sí. Verá muestras de granito de verdad en nuestro taller y una prueba completa dibujada a escala. Solo empezamos a grabar cuando usted aprueba y firma la prueba.</p>"),
    ("<summary>Should we choose a single or a companion memorial?</summary>", "<summary>¿Conviene una lápida individual o una doble?</summary>"),
    ('<p>Most families choose a single memorial. A companion is for two people, such as a husband and wife: one side is engraved now and the other later, at our shop or at the cemetery, as the cemetery allows. Any size can be made either way.</p>',
     '<p>La mayoría de las familias elige una lápida individual. La doble es para dos personas, como esposo y esposa: un lado se graba ahora y el otro después, en nuestro taller o en el cementerio, según lo permita el cementerio. Cualquier tamaño puede hacerse de las dos formas.</p>'),
    ('Do you install the memorial?',
     '¿Ustedes instalan la lápida?'),
    ("Most cemeteries set the memorial themselves. At Conejo Mountain Memorial Park, we install it ourselves. Either way, we'll tell you what to expect at your cemetery.",
     'La mayoría de los cementerios colocan la lápida ellos mismos. En Conejo Mountain Memorial Park, la instalamos nosotros. De cualquier forma, le diremos qué esperar en su cementerio.'),
    ("<summary>Can you add a date to a stone that's already in place?</summary>",
     "<summary>¿Pueden agregar una fecha a una lápida que ya está colocada?</summary>"),
    ("<p>Yes. Send us a photo of the stone and the cemetery name, and we'll explain what's possible.</p>",
     "<p>Sí. Mándenos una foto de la lápida y el nombre del cementerio, y le explicamos qué se puede hacer.</p>"),

    # --- contact --------------------------------------------------------------------------------------
    ("<h2 id=\"contact-title\" class=\"section-title\">Start whenever <em>you're ready</em></h2>",
     '<h2 id="contact-title" class="section-title">Empiece cuando <em>esté listo</em></h2>'),
    ("                Tell us a little about your loved one and the cemetery, and we'll call you back. You don't need every\n                detail.",
     '                Cuéntenos un poco sobre su ser querido y el cementerio, y le llamamos. No necesita tener todos los\n                detalles.'),
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
    ('data-file-help>One photo or PDF, up to 8 MB.</span>',
     'data-file-help>Una foto o un PDF, de hasta 8 MB.</span>'),
    ('<span class="field-label">Message <span class="field-optional">(optional)</span></span>',
     '<span class="field-label">Mensaje <span class="field-optional">(opcional)</span></span>'),
    ("placeholder=\"Their name, the cemetery, or anything you'd like us to know.\"",
     'placeholder="Su nombre, el cementerio o cualquier cosa que quiera contarnos."'),
    ('<button type="submit" class="button button-primary" aria-live="polite">Send</button>',
     '<button type="submit" class="button button-primary" aria-live="polite">Enviar</button>'),
    ("Your information stays with GVG Memorials and is used only to respond.",
     "Su información se queda con GVG Memorials y solo la usamos para responderle."),

    # --- footer and analytics banner ------------------------------------------------------------------
    ("<span>Headstones and grave markers since 1998</span>", "<span>Lápidas y placas desde 1998</span>"),
    ('<p>Family-owned since 1998</p>',
     '<p>Negocio familiar desde 1998</p>'),
    ('aria-expanded="false">Analytics choices</button>', 'aria-expanded="false">Opciones de análisis</button>'),
    ('aria-label="Analytics privacy choices"', 'aria-label="Opciones de privacidad"'),
    ("<strong>Help us improve this website</strong>", "<strong>Ayúdenos a mejorar este sitio</strong>"),
    ("<p>Privacy-focused analytics show us which pages and contact options help families. No advertising tracking.</p>",
     "<p>Un análisis respetuoso de su privacidad nos muestra qué páginas y formas de contacto ayudan a las familias. Sin rastreo publicitario.</p>"),
    ("data-analytics-accept>Allow analytics</button>", "data-analytics-accept>Permitir</button>"),
    ("data-analytics-decline>Continue without</button>", "data-analytics-decline>Continuar sin análisis</button>"),

    # --- inline slideshow script ----------------------------------------------------------------------
    ('more.textContent = open ? "See more of our work" : "Show fewer";',
     'more.textContent = open ? "Ver más de nuestro trabajo" : "Ver menos";'),
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
    ('            We have your message. A member of GVG Memorials will read it and call or write back personally.',
     '            Ya tenemos su mensaje. Alguien de GVG Memorials lo leerá y le llamará o le escribirá personalmente.'),
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
    ('<a class="button button-outline" href="/">Back to the home page</a>',
     '<a class="button button-outline" href="/es/">Volver a la página de inicio</a>'),
    ('<p>Family-owned since 1998</p>',
     '<p>Negocio familiar desde 1998</p>'),
    ('<span>Headstones and grave markers since 1998</span>',
     '<span>Lápidas y placas desde 1998</span>'),
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
