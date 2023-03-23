from wolframclient.evaluation import WolframLanguageSession

class WolframEvaluator:
    def __init__(self):
        self.languageSession: WolframLanguageSession = WolframLanguageSession(
            kernel='C:/Program Files/Wolfram Research/Wolfram Engine/13.2/WolframKernel.exe'
        )
        self.languageSession.start()

    def start(self) -> None:
        self.languageSession.start()
        return None

    def end(self) -> None:
        self.languageSession.terminate()
        return None

    def evaluate(self, expression: str) -> any:
        return self.languageSession.evaluate(expression)

    def solveEquation(self, equation: str, stringFormat: bool = False) -> any:
        expression: str = f'Solve[{equation}]'
        if stringFormat is True: expression = f'ToString[{expression}]'
        return self.evaluate(expression)

    def solveWith(self, equation: str, *values, stringFormat: bool = False) -> any:
        variables = '{' + ','.join(values) + '}'
        expression: str = f'SolveValues[{equation}, {variables}]'
        if stringFormat is True: expression = f'ToString[{expression}]'
        return self.evaluate(expression)
