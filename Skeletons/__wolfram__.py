from wolframclient.evaluation import WolframLanguageSession

class WolframEvaluator:
    def __init__(self):
        self.languageSession: WolframLanguageSession = WolframLanguageSession(
            kernel='C:/Program Files/Wolfram Research/Wolfram Engine/13.2/WolframKernel.exe'
        )
        self.languageSession.start()

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

    def plot2d(self,
               func: str,
               xrange: tuple[float, float],
               __format__: str = '.jpg') -> None:
        __start__, __end__ = map(str, xrange)
        self.evaluate(f'Export["./cache/Plotting/plot2d{__format__}", '
                      f'Plot[{func}, {"{x, " + __start__ + ", " + __end__ + "}"}]]')
        return None

    def plot3d(self,
               func: str,
               xrange: tuple[float, float],
               yrange: tuple[float, float],
               __format__: str = '.jpg') -> None:
        __xstart__, __xend__ = map(str, xrange)
        __ystart__, __yend__ = map(str, yrange)
        self.evaluate(f'Export["./cache/Plotting/plot3d{__format__}", '
                      f'Plot3D[{func}, {"{x, " + __xstart__ + ", " + __xend__ + "}"}, '
                      f'{"{y, " + __ystart__ + ", " + __yend__ + "}"}]]')
