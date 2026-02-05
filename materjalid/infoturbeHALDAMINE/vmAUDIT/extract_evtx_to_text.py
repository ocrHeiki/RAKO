###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒███  ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒             #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  extract_evtx_to_text.py                              |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Skript teisendab Windowsi sündmuselogide             |   #
#   |                (`.evtx`) failid tekstivormingusse, kasutades       |   #
#   |                `evtxexport` tööriista.                              |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import subprocess
import sys
import os

def extract_evtx_to_text(evtx_file_path, output_text_file_path):
    """
    Teisendab .evtx logifaili loetavaks tekstivorminguks, kasutades evtxexport tööriista.
    """
    if not os.path.exists(evtx_file_path):
        print(f"Viga: Sisendfaili ei leitud: {evtx_file_path}")
        sys.exit(1)

    try:
        # Käivitab evtxexport käsu .evtx faili teisendamiseks tekstiks
        # Väljund suunatakse määratud tekstifaili
        with open(output_text_file_path, 'w', encoding='utf-8') as outfile:
            subprocess.run(
                ['evtxexport', evtx_file_path],
                stdout=outfile,
                check=True,
                text=True,
                encoding='utf-8'
            )
        print(f"Fail '{evtx_file_path}' teisendati edukalt: '{output_text_file_path}'")
    except FileNotFoundError:
        print("Viga: 'evtxexport' tööriista ei leitud. Palun veenduge, et see on installitud ja PATH-is.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Viga 'evtxexport' käivitamisel: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Ootamatu viga teisendamisel: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kasutus: python extract_evtx_to_text.py <sisend_evtx_fail> <väljund_teksti_fail>")
        sys.exit(1)

    input_evtx = sys.argv[1]
    output_text = sys.argv[2]
    extract_evtx_to_text(input_evtx, output_text)