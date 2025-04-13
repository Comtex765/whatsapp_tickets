import core.states.registro as estate
from colorama import Fore, Style
from utils.constantes import estados as est


class RegistroHandler:
    estrategias = {
        est.INICIO_REGISTRO: estate.InicioRegistro,
        est.ESPERANDO_NOMBRE_APELLIDO: estate.EsperandoNombreApellido,
        est.ESPERANDO_FECHA_NACIMIENTO: estate.EsperandoFechaNacimiento,
        est.ESPERANDO_CORREO: estate.EsperandoCorreo,
        est.ESPERANDO_DIRECCION: estate.EsperandoDireccion,
    }

    def handle(self, texto, numero_telefono, sesiones_usuarios):
        try:
            estado = sesiones_usuarios[numero_telefono]["estado"]
            estrategia_class = self.estrategias.get(estado)

            if estrategia_class:
                try:
                    estrategia_class().handle(numero_telefono, texto, sesiones_usuarios)

                    # Verificar si se llegó al final del registro después de ingresar la dirección
                    if estado == est.ESPERANDO_DIRECCION:
                        nuevo_estado = sesiones_usuarios[numero_telefono]["estado"]
                        if nuevo_estado == est.FIN_REGISTRO:
                            try:
                                estate.FinRegistro().handle(
                                    numero_telefono, sesiones_usuarios
                                )
                            except Exception as e:
                                print(
                                    Fore.RED
                                    + "\nERROR EN FinRegistro:\t"
                                    + Fore.WHITE
                                    + f"{e}\n"
                                    + Style.RESET_ALL
                                )

                except Exception as e:
                    print(
                        Fore.RED
                        + "\nERROR EN ESTRATEGIA RegistroHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

            else:
                try:
                    from utils.constantes.mensajes import ERROR_GENERICO
                    from utils.whatsapp import responses as wpp_resp
                    from utils.whatsapp.sender import enviar_mensaje_whatsapp

                    response = wpp_resp.mensaje_texto(numero_telefono, ERROR_GENERICO)
                    enviar_mensaje_whatsapp(response)
                except Exception as e:
                    print(
                        Fore.RED
                        + "\nERROR EN WHATSAPP FALLBACK RegistroHandler:\t"
                        + Fore.WHITE
                        + f"{e}\n"
                        + Style.RESET_ALL
                    )

        except Exception as e:
            print(
                Fore.RED
                + "\nERROR GENERAL RegistroHandler:\t"
                + Fore.WHITE
                + f"{e}\n"
                + Style.RESET_ALL
            )
