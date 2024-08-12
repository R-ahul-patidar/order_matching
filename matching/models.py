from django.db import models

# Create your models here.


class PendingOrder(models.Model):
    buyer_qty = models.IntegerField()
    buyer_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller_price = models.DecimalField(max_digits=10, decimal_places=2,null=False)
    seller_qty = models.IntegerField()

    def __str__(self):
        return f"Buyer {self.buyer_qty}@{self.buyer_price} / Seller {self.seller_qty}@{self.seller_price}"

class CompletedOrder(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.qty} units @ {self.price}"

