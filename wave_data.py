import json


class WaveData:
    def __init__(self, order: int = None, tau: float = None, radians: float = None,
                 sin: float = None, cos: float = None, tan: float = None, sinh: float = None,
                 cosh: float = None, tanh: float = None):
        self.Order = order
        self.Tau = tau
        self.Radians = radians
        self.Sin = sin
        self.Cos = cos
        self.Tan = tan
        self.Sinh = sinh
        self.Cosh = cosh
        self.Tanh = tanh

    @property
    def Order(self) -> int:
        return self._order

    @Order.setter
    def Order(self, value: int):
        self._order = value

    @property
    def Tau(self) -> float:
        return self._tau

    @Tau.setter
    def Tau(self, value: float):
        self._tau = value

    @property
    def Radians(self) -> float:
        return self._radians

    @Radians.setter
    def Radians(self, value: float):
        self._radians = value

    @property
    def Sin(self) -> float:
        return self._sin

    @Sin.setter
    def Sin(self, value: float):
        self._sin = value

    @property
    def Cos(self) -> float:
        return self._cos

    @Cos.setter
    def Cos(self, value: float):
        self._cos = value

    @property
    def Tan(self) -> float:
        return self._tan

    @Tan.setter
    def Tan(self, value: float):
        self._tan = value

    @property
    def Sinh(self) -> float:
        return self._sinh

    @Sinh.setter
    def Sinh(self, value: float):
        self._sinh = value

    @property
    def Cosh(self) -> float:
        return self._cosh

    @Cosh.setter
    def Cosh(self, value: float):
        self._cosh = value

    @property
    def Tanh(self) -> float:
        return self._tanh

    @Tanh.setter
    def Tanh(self, value: float):
        self._tanh = value

    def toJson(self):
        return json.dumps(self.toDictionary())

    def toDictionary(self):
        result = {'Order': self.Order, 'Tau': self.Tau, 'Radians': self.Radians, 'Sin': self.Sin,
                  'Cos': self.Cos, 'Tan': self.Tan, 'Sinh': self.Sinh, 'Cosh': self.Cosh,
                  'Tanh': self.Tanh}

        return result

    @staticmethod
    def fromJson(content):
        result = WaveData()

        if not content:
            return result

        if 'Order' in content:
            result.Order = content['Order']

        if 'Tau' in content:
            result.Tau = content['Tau']

        if 'Radians' in content:
            result.Radians = content['Radians']

        if 'Sin' in content:
            result.Sin = content['Sin']

        if 'Cos' in content:
            result.Cos = content['Cos']

        if 'Tan' in content:
            result.Tan = content['Tan']

        if 'Sinh' in content:
            result.Sinh = content['Sinh']

        if 'Cosh' in content:
            result.Cosh = content['Cosh']

        if 'Tanh' in content:
            result.Tanh = content['Tanh']

        return result
