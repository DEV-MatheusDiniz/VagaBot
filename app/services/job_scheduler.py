import schedule
import time
from typing import Callable, List


class JobSchedule:
    @staticmethod
    def run(horarios: List[str], funcao: Callable, **kwargs):
        """
        Inicia a execução de uma função nos horários especificados.

        :param horarios: Lista de horários no formato "HH:MM".
        :param funcao: Função a ser executada.
        :param kwargs: Argumentos nomeados para a função.
        """
        # Configurar horários de execução
        for horario in horarios:
            schedule.every().day.at(horario).do(funcao, **kwargs)

        # Loop principal de execução
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Execução interrompida pelo usuário.")
