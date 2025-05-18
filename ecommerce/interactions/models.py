from django.db import models
from accounts.models import User,Time
from catalog.models import Product



class Rate(Time):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ("user", "product")  # هر کاربر یک بار به هر محصول امتیاز می‌ده

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.score}"


class Comment(Time):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        return f"{self.user.username} on {self.product.name}"
