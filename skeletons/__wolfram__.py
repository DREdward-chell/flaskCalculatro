from wolframclient.evaluation import WolframLanguageSession, WolframCloudSession, SecuredAuthenticationKey
from wolframclient.exception import WolframKernelException

# key name is 'FLASK'

KEY = SecuredAuthenticationKey(
    'PaI8q6V4M6V7N1KsLeggf+vIJW4aHsKtUryk8oPdf1c=',
    'DdoLCpHcd9CvpuzIgI8Yq4ZbNLkTUQNa8R6Kw62HBSk='
)

# supporting class for easier evaluation of wolfram language
class WolframEvaluator:
    def __init__(self):
        global KEY

        # start new wolfram language session
        try:
            self.languageSession: WolframLanguageSession = WolframLanguageSession(
                kernel='C:/Program Files/Wolfram Research/Wolfram Engine/13.2/WolframKernel.exe', credentials=KEY
            )
            self.languageSession.start()

        # if kernel exception occurs, start cloud session
        except WolframKernelException:
            self.languageSession: WolframCloudSession = WolframCloudSession(credentials=KEY)
            print("cloud")
            self.languageSession.start()

    # terminating the session
    def end(self) -> None:
        self.languageSession.terminate()
        return None

    # evaluating WL expression
    def evaluate(self, expression: str) -> any:
        return self.languageSession.evaluate(expression)

    # solve an equation
    def solveEquation(self, equation: str, stringFormat: bool = False) -> any:
        expression: str = f'Solve[{equation}]'
        if stringFormat is True: expression = f'ToString[{expression}]'
        return self.evaluate(expression)

    # solve an equation with chosen variables
    def solveWith(self, equation: str, *values, stringFormat: bool = False) -> any:
        variables = '{' + ','.join(values) + '}'
        expression: str = f'SolveValues[{equation}, {variables}]'
        if stringFormat is True: expression = f'ToString[{expression}]'
        return self.evaluate(expression)

    # plot a 2D function
    def plot2d(self,
               func: str,
               xrange: tuple[float, float],
               __format__: str = '.jpg') -> None:
        __start__, __end__ = map(str, xrange)
        self.evaluate(f'Export["./cache/Plotting/plot2d{__format__}", '
                      f'Plot[{func}, {"{x, " + __start__ + ", " + __end__ + "}"}]]')
        return None

    # plot a 3D function
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
