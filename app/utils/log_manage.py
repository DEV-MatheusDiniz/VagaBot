import logging


class LogManager():
    """
    Classe para montar estrutura de logs
    """
    def __init__(self, nome: str):
        self.nome: str = nome
        self.linhas: list = []
    
    def add_row(self, texto: str):
        """
        Adicionar linha no log
        """
        self.linhas.append(texto)
    
    def print_log(self):
        """
        Printar log
        """
        logging.info("")
        logging.info(f"############### {self.nome}")

        for linha in self.linhas:
            logging.info(f"     {linha}")

        logging.info("")
