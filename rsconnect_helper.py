import sys
from rsconnect import main

sys.argv = [
    "rsconnect",
    "deploy", "shiny",
    ".",                      # directorio actual
    "--force-generate"        # asegura regenerar el environment en el servidor
]

main.cli()