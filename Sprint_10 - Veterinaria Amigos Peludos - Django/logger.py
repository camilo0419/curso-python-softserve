import logging

#Configuracion del logging
logging.basicConfig(
    filename='clinica_veterinaria.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
)


logger = logging.getLogger(__name__)
#logger específico para usar en el resto del programa
