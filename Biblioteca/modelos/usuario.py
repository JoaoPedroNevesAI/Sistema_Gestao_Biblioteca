class Usuario:
    def __init__(self, id_usuario, nome, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email

    def to_csv(self):
        return f"{self.id_usuario},{self.nome},{self.email}\n"

    @staticmethod
    def from_csv(linha):
        partes = linha.strip().split(",")
        if len(partes) != 3:
            return None
        return Usuario(partes[0], partes[1], partes[2])
