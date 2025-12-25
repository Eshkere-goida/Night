from services.PizzaBuilder import PizzaBuilder

class MenuDirector:
    @staticmethod
    def make_pepperoni(builder):
        builder.reset()
        return (builder
                .set_thin_dough()
                .add_sauce("томатным соусом")
                .add_cheese()
                .add_pepperoni()
                .add_olives()
                .build())
    @staticmethod
    def make_margherita(builder):
        builder.reset()
        return (builder
                .set_thin_dough()
                .add_sauce("томатным соусом")
                .add_cheese()
                .build())