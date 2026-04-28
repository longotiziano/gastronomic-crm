from app.models.sale import Sale

class SaleRepository():
    def __init__(self, session):
        self.session = session
    
    def get_sales(self):
        pass