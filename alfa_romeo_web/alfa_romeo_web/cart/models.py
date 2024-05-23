from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from alfa_romeo_web.checkout.models import ShippingAddress
from alfa_romeo_web.products.models import Products

UserModel = get_user_model()


class OrderItem(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    item = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        default=1,
    )

    ordered = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    # def get_image(self):
    #     return self.item.images.image.url

    def get_total_item_price(self):
        if self.item.discount_price == 0:
            return self.quantity * self.item.price
        else:
            return self.quantity * self.item.discount_price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class ShoppingCart(models.Model):
    PENDING = 'pending'
    SENT = 'sent'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
        (COMPLETED, 'Completed'),
    ]

    MAX_CHOICES_LENGTH = max(len(choice[0]) for choice in STATUS_CHOICES) + 1

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    ordered = models.BooleanField(
        default=False,
    )

    items = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(
        auto_now_add=True,
    )

    ordered_date = models.DateTimeField(
        default=timezone.now,
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=MAX_CHOICES_LENGTH,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
