from wolframclient.evaluation import WolframLanguageSession, WolframCloudSession, SecuredAuthenticationKey
from wolframclient.exception import WolframKernelException
import typing

Path = typing.TypeVar('Path', bound=typing.Callable[..., typing.Any])

# key name is 'FLASK'

KEY: SecuredAuthenticationKey = SecuredAuthenticationKey(
    'PaI8q6V4M6V7N1KsLeggf+vIJW4aHsKtUryk8oPdf1c=',
    'DdoLCpHcd9CvpuzIgI8Yq4ZbNLkTUQNa8R6Kw62HBSk='
)

# supporting class for easier evaluation of wolfram language
class WolframEvaluator:
    def __init__(self) -> None:
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
        return

    # terminating the session
    def end(self) -> None:
        self.languageSession.terminate()
        return

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
    def plot2d(self, func: str, xrange: tuple[str, str], path: Path) -> None:
        __start__, __end__ = xrange
        self.evaluate(f'Export["{path}", '
                      f'Plot[{func}, {"{x, " + __start__ + ", " + __end__ + "}"}]]')
        return

    # plot a 3D function
    def plot3d(self, func: str, xrange: tuple[str, str], yrange: tuple[str, str]) -> None:
        __xstart__, __xend__ = xrange
        __ystart__, __yend__ = yrange
        self.evaluate(f'Export["./cache/Plotting/3DPLOT.obj", '
                      f'Plot3D[{func}, {"{x, " + __xstart__ + ", " + __xend__ + "}"}, '
                      f'{"{y, " + __ystart__ + ", " + __yend__ + "}"}]]')
        return

    # special plot function
    def parametricPlot(self, func1: str, func2: str, urange: tuple[str, str], path: Path) -> None:
        __start__, __end__ = urange
        self.evaluate(f'Export["{path}", '
                      f'ParametricPlot[{"{"}{func1}, {func2}{"}"}, {"{u, " + __start__ + ", " + __end__ + "}"}]]')
        return

    # plot a molecule
    def moleculePlot(self, molecule: str, path: Path) -> None:
        self.evaluate(f'Export["{path}", MoleculePlot["{molecule}"]]')

    # balance chemical reaction
    def reactionBalance(self, reaction: str) -> str:
        return self.evaluate(f'ToString[ReactionBalance["{reaction}"]["EquationString"]]')

    # count molecular mass
    def molecularMass(self, molecule: str) -> str:
        return self.evaluate(f'ToSrting[ChemicalFormula["{molecule}"]["MolecularMass"]]')

    # get data about chemical element
    def elementData(self, element: str, data: str) -> str:
        return self.evaluate(f'ToString[ElementData["{element}", "{data}"]]')

    # unit convertion
    def unitConvert(self, value: int | float, from_unit: str, to_unit: str) -> str:
        return self.evaluate(f'ToString[UnitConvert[Quantity[{value}, "{from_unit}"], "{to_unit}"]]')

    # find sequence function
    def findSequence(self, sequence: list) -> str:
        return self.evaluate(f'ToString[FindSequenceFunction[{str(sequence).replace("[", "{").replace("]", "}")}, n]]')

    def find_textural_answer(self, text: str, question: str) -> str:
        return self.evaluate(f'ToString[FindTextualAnswer["{text}", "{question}"]]')
