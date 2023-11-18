import subprocess

from module import Module


class BoomerModule(Module):

    def __init__(self):
        info = {
            "Name": "Unquoted Service Path",
            "Author": "Josue Encinar",
            "Description": """Look for services with BINARY_PATH_NAME without quoted and with spaces
        [ Only English and Spanish OS ]"""
        }
        options = {
        }
        super(BoomerModule, self).__init__(options, info)

    def run(self):
        self.print_info("Searching services...")
        found = False
        blank = " "
        try:
            services = subprocess.check_output(["sc", "query", "type=", "service"], universal_newlines=True)
            for service in services.split("\n"):
                if "SERVICE_NAME" in service or "NOMBRE_SERVICIO" in service:
                    data = service.split(":")[1].strip()
                    try:
                        info = subprocess.check_output(["sc", "qc", data], universal_newlines=True)
                        s_name = None
                        s_path = None
                        s_start = None
                        for entry in info.split("\n"):
                            if ("BINARY_PATH_NAME" in entry or "NOMBRE_RUTA_BINARIO" in entry) \
                                    and ('\"' not in entry):
                                aux = entry.split(": ")[1].strip()
                                if (blank in aux.split(" -k ")[0]) and (blank in aux.split(" /")[0]):
                                    s_name = data
                                    s_path = aux
                            elif "SERVICE_START_NAME" in entry or "NOMBRE_INICIO_SERVICIO" in entry:
                                s_start = entry.split(": ")[1]
                        if s_name:
                            found = True
                            print(f"[*] Service: {s_name}")
                            print(f"    - Path: {s_path}")
                            print(f"    - Service Start: {s_start}")

                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        if not found:
            print("No service with these characteristics has been found")
