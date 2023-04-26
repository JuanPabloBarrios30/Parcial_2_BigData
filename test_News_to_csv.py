import csv
import requests
from datetime import date
from bs4 import BeautifulSoup
from News_to_csv import get_link_ee, get_link_et

html = '''
<article class="simple" data-autor="Alejandra lopez plazas" data-bloqueo="Abierto" data-board="Hs : Salud" data-category="salud" data-clasecontenido="Estandar" data-editorial="Editorial" data-id="762667" data-name="Invima admite tener más de 3.900 solicitudes de registros sanitarios represadas" data-publicacion="2023-04-25" data-seccion="Salud" data-subseccion="" data-tipocontenido="Articulo" dtm-name="Contenido7" id="m2625-9-2626" itemscope="" itemtype="https://schema.org/NewsArticle"><div class="category-published">
<a class="category page-link salud" href="/salud" id="m2630-2629-2631">Salud</a><span class="published-at" id="m2636-1-2637">6:00 pm</span></div>
<h2 class="title-container" itemprop="headline">
<a class="multimediatag page-link" href="/salud/invima-admite-tener-3-906-solicitudes-de-registros-sanitarios-represadas-762667">
<span id="m2642-2-2643">Video</span></a>
<a class="title page-link" href="/salud/invima-admite-tener-3-906-solicitudes-de-registros-sanitarios-represadas-762667" id="m2648-3-2649">Invima admite tener más de 3.900 solicitudes de registros sanitarios represadas</a></h2>
<meta content="2023-04-25" itemprop="datePublished"/><meta content="2023-04-25" itemprop="dateModified"/><meta itemid="https://www.eltiempo.com/salud/invima-admite-tener-3-906-solicitudes-de-registros-sanitarios-represadas-762667" itemprop="mainEntityOfPage" itemscope="" itemtype="https://schema.org/WebPage"/><span class="oculto" itemprop="author" itemscope="" itemtype="https://schema.org/Person">
<span itemprop="name">Alejandra López Plazas</span>
</span>
<div class="oculto" itemprop="publisher" itemscope="" itemtype="https://schema.org/Organization">
<div itemprop="logo" itemscope="" itemtype="https://schema.org/ImageObject">
<meta content="https://www.eltiempo.com/bundles/eltiempocms/images/el-tiempo/logo-el-tiempo-azul.jpg" itemprop="url"/><meta content="600" itemprop="width"/><meta content="60" itemprop="height"/></div>
<meta content="EL TIEMPO" itemprop="name"/><meta content="https://www.eltiempo.com" itemprop="url"/></div>
<div class="oculto" itemprop="image" itemscope="" itemtype="https://schema.org/ImageObject"><meta content="570" itemprop="width"/><meta content="380" itemprop="height"/><meta content="https://www.eltiempo.com/bundles/eltiempocms/images/default.jpg" itemprop="url"/></div></article>
'''

html_espectador = '''
<h2 class="Card-Title Title Title_main"><a class="Bloque_Apertura_Home_0" href="/salud/los-detalles-de-la-ponencia-de-la-reforma-a-la-salud-aprobada/" rel="noreferrer" target="_self">Los detalles de la ponencia de la reforma a la salud aprobada</a></h2>,
<h2 class="Card-Title Title Title"><a class="Basico_12_0" href="/mundo/america/migrantes-protestan-contra-autoridades-mexicanas-suturandose-los-labios/" rel="noreferrer" target="_self">Migrantes protestan contra autoridades mexicanas suturándose los labios</a></h2>,
<h2 class="Card-Title Title Title"><a class="Basico_12_1" href="/mundo/america/cumbre-de-venezuela-que-organizo-petro-buenas-intenciones-pocas-novedades/" rel="noreferrer" target="_self">Cumbre de Venezuela que organizó Petro: ¿buenas intenciones, pocas novedades?</a></h2>,
<h2 class="Card-Title Title Title"><a class="Basico_12_2" href="/bogota/en-vivo-primer-debate-de-precandidatos-a-la-alcaldia-de-bogota/" rel="noreferrer" target="_self">Corferias suspende debate de precandidatos a la Alcaldía por razones de seguridad</a></h2>,
<h2 class="Card-Title Title Title"><a href="/salud/67-millones-de-ninos-en-el-mundo-no-han-sido-vacunados-como-influyo-la-pandemia-noticias-hoy/" rel="noreferrer" target="_self">67 millones de niños en el mundo no han sido vacunados, ¿cómo influyó la pandemia?</a></h2>,
<h2 class="Card-Title Title Title"><a href="/judicial/los-testigos-contra-el-exparamiltar-pajaro-por-la-masacre-de-la-autopista-norte/" rel="noreferrer" target="_self">Los testigos contra el exparamiltar “Pájaro” por la masacre en la Autopista Norte</a></h2>,
<h2 class="Card-Title Title Title"><a href="/deportes/futbol-colombiano/dimayor-confirmo-sancion-a-once-caldas-por-disturbios-en-el-estadio-palogrande/" rel="noreferrer" target="_self">Dimayor confirmó sanción a Once Caldas por disturbios en el estadio Palogrande</a></h2>,
<h2 class="Card-Title Title Title"><a href="/mundo/america/abogados-de-trump-arremeten-contra-la-mujer-que-lo-denuncia-por-violacion/" rel="noreferrer" target="_self">Abogados de Trump arremeten contra la mujer que lo denuncia por violación</a></h2>,
<h2 class="Card-Title Title Title"><a href="/ambiente/preocupacion-porque-podrian-talarse-los-arboles-mas-grandes-de-un-bosque-de-eeuu/" rel="noreferrer" target="_self">Preocupación porque podrían talarse los árboles más grandes de un bosque de EE.UU.</a></h2>,
<h2 class="Card-Title Title Title"><a href="/contenido-patrocinado/guardianes-de-la-selva-asi-funciona-la-tecnologia-que-salva-ecosistemas/" rel="noreferrer" target="_self">Guardianes de la selva: así funciona la tecnología que salva ecosistemas</a></h2>,
<h2 class="Title_section Title_sectionBottomUnbordered"></h2>,
<h2 class="Card-Title Title Title"><a href="/opinion/columnistas/aldo-civico/resiliencia-2/" rel="noreferrer" target="_self">Resiliencia</a></h2>,
<h2 class="Card-Title Title Title"><a href="/opinion/columnistas/oscar-alarcon/estados-unidos-y-colombia/" rel="noreferrer" target="_self">Estados Unidos y Colombia</a></h2>,
<h2 class="Card-Title Title Title"><a href="/opinion/columnistas/aura-lucia-mera/berlin/" rel="noreferrer" target="_self">Berlín</a></h2>,
<h2 class="Card-Title Title Title"><a href="/opinion/columnistas/yesid-reyes-alvarado/de-micos-y-leguleyadas/" rel="noreferrer" target="_self">De micos y leguleyadas</a></h2>,
<h2 class="Card-Title Title Title_main"><a href="/opinion/editorial/los-conflictos-de-intereses-del-ministro-de-transporte/" rel="noreferrer" target="_self">Los conflictos de intereses del ministro de Transporte</a></h2>,
<h2 class="Card-Title Title Title"><a href="/contenido-patrocinado/el-programa-cajita-feliz-libros-de-mcdonalds-esta-presente-en-la-filbo-2023/" rel="noreferrer" target="_self">El Programa Cajita Feliz Libros de McDonald’s está presente en la Filbo 2023</a></h2>
'''

text_response = '"Invima admite tener más de 3.900 solicitudes de registros sanitarios represadas","salud","/salud/invima-admite-tener-3-906-solicitudes-de-registros-sanitarios-represadas-762667"\n'

text_response_2 = 'los detalles de la ponencia de la reforma a la  aprobada,salud,/salud/los-detalles-de-la-ponencia-de-la-reforma-a-la-salud-aprobada/\n'


def test_get_link_et():

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a')[2]

    assert get_link_et(links) == text_response

def test_get_link_ee():

    soup = BeautifulSoup(html_espectador, "html.parser")
    links = soup.find_all('a')[0]
    
    assert get_link_ee(links) == text_response_2

    