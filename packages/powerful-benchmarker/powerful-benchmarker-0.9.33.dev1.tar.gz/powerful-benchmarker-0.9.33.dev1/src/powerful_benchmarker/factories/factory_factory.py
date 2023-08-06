from .base_factory import BaseFactory

class FactoryFactory(BaseFactory):
    def _create_general(self, factory_type):
        return self.getter.get("factory", yaml_dict=factory_type, additional_params={"getter": self.getter})
               