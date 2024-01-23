from abc import ABCMeta,abstractmethod

class Icomponent(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def notify(msj):
        """The required notify method"""

    @staticmethod
    @abstractmethod
    def receive(msg):
         """The required receive method"""

class Component(Icomponent):
    def __init__(self,mediator,name):
        self.mediator = mediator
        self.name = name
        self.msj = None

    def notify(self,message):
        print(self.name + ": >>> Out >>>: "+ str(message))
        self.mediator.notify(message,self)
    
    def receive(self,message):
        print(self.name + ": <<< int <<<: "+ str(message))
        self.msj = message
   
    def getter_data_msj(self):
        return self.msj

class Mediator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.components = []
        self.message_registry = {}

    def add(self, component):
        self.components.append(component)
        self.message_registry[component] = None

    def notify(self, message, sender):
        for component in self.components:
            if component != sender:
                component.receive(message)
                self.message_registry[component] = message

    def get_message(self, component):
        return self.message_registry.get(component)

Mediaator = Mediator()
Componenen1  = Component(Mediaator,"Component1")
Componenen2  = Component(Mediaator,"Component2")
componenen3  = Component(Mediaator,"Component3")

Mediaator.add(Componenen1)
Mediaator.add(Componenen2)
Mediaator.add(componenen3)

Componenen1.notify("hola")
message2 = Mediaator.get_message(Componenen2)
print(message2)  # Imprime: Hola desde Component2
message_list = [1, 2, 3]
Componenen1.notify(message_list)
message2 = Mediaator.get_message(Componenen2)
print(message2)  # Imprime: Hola desde Component2