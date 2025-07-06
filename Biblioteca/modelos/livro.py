class Livro:
    def __init__(self, id_livro, titulo, autor, genero, copias):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.copias = int(copias)

    def to_csv(self):
        return f"{self.id_livro},{self.titulo},{self.autor},{self.genero},{self.copias}\n"

    @staticmethod
    def from_csv(linha):
        partes = linha.strip().split(",")
        if len(partes) != 5:
            return None
        return Livro(partes[0], partes[1], partes[2], partes[3], partes[4])
