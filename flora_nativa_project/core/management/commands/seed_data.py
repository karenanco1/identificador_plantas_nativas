from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Region, Planta


REGIONES = [
    (1, "Región de Tarapacá"),
    (2, "Región de Antofagasta"),
    (3, "Región de Atacama"),
    (4, "Región de Coquimbo"),
    (5, "Región de Valparaíso"),
    (6, "Región del Libertador General Bernardo O'Higgins"),
    (7, "Región del Maule"),
    (8, "Región del Biobío"),
    (9, "Región de La Araucanía"),
    (10, "Región de Los Lagos"),
    (11, "Región de Aysén del General Carlos Ibáñez del Campo"),
    (12, "Región de Magallanes y de la Antártica Chilena"),
    (13, "Región Metropolitana de Santiago"),
    (14, "Región de Los Ríos"),
    (15, "Región de Arica y Parinacota"),
    (16, "Región de Ñuble"),
]

PLANTAS = [
    {
        "nombre_comun": "Araucaria",
        "nombre_cientifico": "Araucaria araucana",
        "regiones": [9, 10, 11],
        "ubicacion_especifica": "Laderas de la cordillera de los Andes y la Cordillera de la Costa, entre 600 y 1800 m s.n.m.",
        "descripcion_hoja": "Hojas perennes, aciculares, rígidas y punzantes, dispuestas en espiral, de color verde oscuro.",
        "descripcion_tallo": "Tronco recto y cilíndrico, de corteza gruesa y agrietada de color gris pardusco.",
        "descripcion_flor": "Árbol dioico. Conos masculinos cilíndricos y conos femeninos globosos de gran tamaño.",
        "descripcion_detalle": "Puede alcanzar hasta 50 m de altura. Copa redondeada en ejemplares adultos. Especie emblemática y monumento natural de Chile.",
        "uso_principal": "ORN",
        "detalles_uso": "Uso ornamental y forestal. Semillas comestibles (piñones). Madera de alta calidad.",
    },
    {
        "nombre_comun": "Boldo",
        "nombre_cientifico": "Peumus boldus",
        "regiones": [5, 6, 7, 13],
        "ubicacion_especifica": "Laderas asoleadas y lomajes, desde la Región de Valparaíso hasta el Maule.",
        "descripcion_hoja": "Hojas opuestas, ovaladas, de textura coriácea, borde entero, de color verde amarillento, muy aromáticas.",
        "descripcion_tallo": "Tronco corto con corteza grisácea y agrietada. Ramas abundantes.",
        "descripcion_flor": "Flores pequeñas, blancas o ligeramente rosadas, dispuestas en racimos.",
        "descripcion_detalle": "Árbol de hasta 15 m de altura. Hojas con olor característico a alcanfor. Fruto drupa comestible de color verde amarillento.",
        "uso_principal": "MED",
        "detalles_uso": "Las hojas se usan en infusión para tratar problemas hepáticos y digestivos. Propiedades antioxidantes.",
    },
    {
        "nombre_comun": "Quillay",
        "nombre_cientifico": "Quillaja saponaria",
        "regiones": [4, 5, 6, 7, 13],
        "ubicacion_especifica": "Laderas y cerros desde la Región de Coquimbo hasta el Maule.",
        "descripcion_hoja": "Hojas simples, alternas, oblongas, de borde aserrado, glabras, de color verde brillante.",
        "descripcion_tallo": "Tronco recto de corteza gruesa, gris oscuro, con grietas longitudinales.",
        "descripcion_flor": "Flores pequeñas, blancas o crema, con 5 pétalos, dispuestas en corimbos axilares.",
        "descripcion_detalle": "Árbol siempreverde de hasta 20 m de altura. Corteza rica en saponinas que producen espuma en contacto con el agua.",
        "uso_principal": "IND",
        "detalles_uso": "La corteza se usa como detergente natural (saponina). Industria cosmética y farmacéutica. Uso medicinal como expectorante.",
    },
    {
        "nombre_comun": "Litre",
        "nombre_cientifico": "Lithrea caustica",
        "regiones": [4, 5, 6, 7, 13],
        "ubicacion_especifica": "Laderas asoleadas y formaciones esclerófilas desde Coquimbo hasta el Maule.",
        "descripcion_hoja": "Hojas compuestas, imparipinnadas, de folíolos oblongos, coriáceas, de color verde amarillento.",
        "descripcion_tallo": "Tronco tortuoso con corteza áspera de color gris oscuro.",
        "descripcion_flor": "Flores pequeñas, blancas, dispuestas en panículas terminales.",
        "descripcion_detalle": "Árbol o arbusto de hasta 8 m de altura. Produce una resina que puede causar dermatitis alérgica. Fruto drupa globosa de color pardo.",
        "uso_principal": "VEN",
        "detalles_uso": "Especie venenosa por contacto. La resina puede causar alergias severas. La madera es usada como leña.",
    },
    {
        "nombre_comun": "Copihue",
        "nombre_cientifico": "Lapageria rosea",
        "regiones": [7, 8, 9, 10, 14],
        "ubicacion_especifica": "Bosques templados lluviosos del sur de Chile, crece enredada en árboles y arbustos.",
        "descripcion_hoja": "Hojas alternas, ovaladas, acorazonadas en la base, de textura coriácea, verde oscuro, con nervaduras marcadas.",
        "descripcion_tallo": "Tallo leñoso, delgado y voluble, puede alcanzar varios metros trepando por la vegetación.",
        "descripcion_flor": "Flor grande, tubular, colgante, de 6 pétalos, de color rojo intenso a rosado (existe variedad blanca).",
        "descripcion_detalle": "Flor nacional de Chile. Enredadera leñosa que puede alcanzar hasta 10 m. Fruto baya alargada comestible de pulpa dulce.",
        "uso_principal": "ORN",
        "detalles_uso": "Uso ornamental por su espectacular floración. El fruto es comestible. Especie protegida, su recolección está regulada.",
    },
    {
        "nombre_comun": "Canelo",
        "nombre_cientifico": "Drimys winteri",
        "regiones": [5, 6, 7, 8, 9, 10, 11, 14],
        "ubicacion_especifica": "Bosques húmedos y orillas de cursos de agua desde Valparaíso hasta Magallanes.",
        "descripcion_hoja": "Hojas simples, alternas, oblongo-lanceoladas, de color verde claro en el haz y glaucas en el envés, muy aromáticas.",
        "descripcion_tallo": "Tronco recto de corteza lisa de color gris ceniciento, con lenticelas marcadas.",
        "descripcion_flor": "Flores blancas, pequeñas, dispuestas en umbelas, con 5-7 pétalos, de aroma fragante.",
        "descripcion_detalle": "Árbol siempreverde de hasta 20 m de altura. Corteza con propiedades medicinales. Árbol sagrado para el pueblo mapuche (Foye).",
        "uso_principal": "MED",
        "detalles_uso": "Corteza usada como febrífugo, tónico y digestivo. Hojas aromáticas. Madera utilizada en ebanistería.",
    },
    {
        "nombre_comun": "Arrayán",
        "nombre_cientifico": "Luma apiculata",
        "regiones": [7, 8, 9, 10, 14],
        "ubicacion_especifica": "Orillas de ríos y lagos en el sur de Chile, desde el Maule hasta Aysén.",
        "descripcion_hoja": "Hojas simples, opuestas, ovaladas, de textura coriácea, verde oscuro brillante en el haz, más claras en el envés.",
        "descripcion_tallo": "Tronco de corteza lisa de color canela a naranja, que se desprende en placas delgadas, muy característico.",
        "descripcion_flor": "Flores blancas, pequeñas, con 4-5 pétalos, con numerosos estambres prominentes.",
        "descripcion_detalle": "Árbol o arbusto siempreverde de hasta 15 m. Fruto baya comestible de color negro violáceo. Corteza de color canela muy decorativa.",
        "uso_principal": "COM",
        "detalles_uso": "Frutos comestibles dulces usados para mermeladas. Madera dura y pesada usada en mangos de herramientas y leña. Uso ornamental.",
    },
    {
        "nombre_comun": "Peumo",
        "nombre_cientifico": "Cryptocarya alba",
        "regiones": [4, 5, 6, 7, 13],
        "ubicacion_especifica": "Laderas de cerros y valles desde la Región de Coquimbo hasta el Maule.",
        "descripcion_hoja": "Hojas simples, alternas, ovaladas, de textura coriácea, verde oscuro brillante en el haz y glaucas en el envés.",
        "descripcion_tallo": "Tronco robusto de corteza áspera, gruesa, de color gris pardusco.",
        "descripcion_flor": "Flores pequeñas, de color verde amarillento, dispuestas en panículas axilares.",
        "descripcion_detalle": "Árbol siempreverde de hasta 20 m de altura. Fruto drupa roja comestible (peumo). Madera de alta calidad.",
        "uso_principal": "COM",
        "detalles_uso": "Frutos comestibles. Madera usada en construcción y mueblería. Corteza con propiedades medicinales (astringente).",
    },
    {
        "nombre_comun": "Espino",
        "nombre_cientifico": "Acacia caven",
        "regiones": [4, 5, 6, 7, 13],
        "ubicacion_especifica": "Valles y laderas asoleadas, forma parte del matorral esclerófilo, desde Coquimbo hasta el Maule.",
        "descripcion_hoja": "Hojas compuestas, bipinnadas, con folíolos muy pequeños, de color verde grisáceo.",
        "descripcion_tallo": "Tronco tortuoso de corteza parda oscura y agrietada. Ramas con espinas fuertes y abundantes.",
        "descripcion_flor": "Flores amarillas, fragantes, dispuestas en glomérulos globosos, muy vistosas.",
        "descripcion_detalle": "Árbol espinoso de hasta 8 m de altura. Florece en primavera cubriendo las laderas de amarillo. Fruto legumbre de color oscuro.",
        "uso_principal": "IND",
        "detalles_uso": "Madera usada como combustible y carbón. Corteza con taninos para curtir cueros. Flores melíferas. Uso medicinal (garganta).",
    },
    {
        "nombre_comun": "Palma Chilena",
        "nombre_cientifico": "Jubaea chilensis",
        "regiones": [5, 6, 7, 13],
        "ubicacion_especifica": "Valles y laderas de cerros en areas de clima mediterráneo, principalmente en la Cordillera de la Costa.",
        "descripcion_hoja": "Hojas pinnadas, arqueadas de 3-4 m de largo, con folíolos rígidos de color verde oscuro.",
        "descripcion_tallo": "Estípite único, cilíndrico, de corteza lisa grisácea, puede alcanzar hasta 30 m de altura.",
        "descripcion_flor": "Inflorescencias muy ramificadas, protegidas por una espata leñosa. Flores pequeñas de color púrpura.",
        "descripcion_detalle": "La palma más austral del mundo. Puede vivir más de 1000 años. Fruto (coquito) drupa globosa comestible.",
        "uso_principal": "COM",
        "detalles_uso": "Frutos comestibles (coquitos). Savia usada para producir miel de palma (miel de palma chilena). Especie vulnerable por sobreexplotación.",
    },
]


class Command(BaseCommand):
    help = "Puebla la base de datos con regiones y plantas nativas de ejemplo"

    def handle(self, *args, **options):
        created_regions = []
        for numero, nombre in REGIONES:
            region, created = Region.objects.get_or_create(
                numero=numero, defaults={"nombre": nombre}
            )
            created_regions.append(region)
            if created:
                self.stdout.write(f"  Creada región: {region.nombre}")
            else:
                self.stdout.write(f"  Ya existe: {region.nombre}")

        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )
        if _:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write("  Creado usuario admin (contraseña: admin123)")

        for data in PLANTAS:
            regiones_nombres = data.pop("regiones")
            regiones = Region.objects.filter(numero__in=regiones_nombres)
            planta, created = Planta.objects.get_or_create(
                nombre_cientifico=data["nombre_cientifico"],
                defaults={**data, "creado_por": admin_user},
            )
            if created:
                planta.regiones.add(*regiones)
                self.stdout.write(f"  Creada planta: {planta.nombre_comun}")
            else:
                self.stdout.write(f"  Ya existe: {planta.nombre_comun}")

        self.stdout.write(self.style.SUCCESS("Seed data completada exitosamente."))
