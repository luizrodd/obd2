from enum import Enum
import obd

class OBDCommands(Enum):
    VELOCIDADE          = ("Velocidade (km/h)", obd.commands.SPEED)
    RPM                 = ("RPM", obd.commands.RPM)
    ACELERADOR          = ("Acelerador (%)", obd.commands.THROTTLE_POS)
    CARGA_MOTOR         = ("Carga do Motor (%)", obd.commands.ENGINE_LOAD)
    TEMP_AGUA           = ("Temp. de Água (°C)", obd.commands.COOLANT_TEMP)
    TEMP_ADMISSAO       = ("Temp. de Admissão (°C)", obd.commands.INTAKE_TEMP)
    FLUXO_AR            = ("Fluxo de Ar (g/s)", obd.commands.MAF)
    NIVEL_COMBUSTIVEL   = ("Nível de Combustível (%)", obd.commands.FUEL_LEVEL)
    AVANCO_IGNICAO      = ("Avanço de Ignição (°)", obd.commands.TIMING_ADVANCE)
    OIL_TEMP            = ("Temp. do Óleo (°C)", obd.commands.OIL_TEMP)
    PRESSAO_COMBUSTIVEL = ("Pressão do Combustível (kPa)", obd.commands.FUEL_PRESSURE)

    def __init__(self, label, command):
        self.label = label
        self.command = command

    @classmethod
    def get_labels(cls):
        """ Retorna uma lista de nomes formatados para exibição. """
        return [cmd.label for cmd in cls]

    @classmethod
    def get_by_label(cls, label):
        """ Retorna o comando OBD-II associado ao nome exibido. """
        for cmd in cls:
            if cmd.label == label:
                return cmd.command
        return None  # Caso não encontre
