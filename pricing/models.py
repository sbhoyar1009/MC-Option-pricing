from django.db import models

class OptionParameters(models.Model):
    ticker = models.CharField(max_length=10)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    risk_free_rate = models.DecimalField(max_digits=5, decimal_places=2)
    volatility = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.ticker


class SimulationResults(models.Model):
    option = models.ForeignKey(OptionParameters, on_delete=models.CASCADE)
    option_price = models.FloatField()

    def __str__(self):
        return f"Price: {self.option_price} for {self.option.ticker}"
