from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User



STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

# product category
class ProductCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # tool_tip
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'
        
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(ProductCategory, self).save(*args, **kwargs)
        

  

class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory, related_name='products',
                                 on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=200,
                            db_index=True, null=True, blank=True)
    
    title = models.CharField(max_length=150)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(upload_to='items', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', args=[self.id, self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Product, self).save(*args, **kwargs)
    
  
  # cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField('OrderProduct', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    paid = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        if self.billing_address:
            return f'Order for {self.billing_address.full_name}'
        return f'Order #{self.id}'

    def calculate_total_cost(self):
        total = sum(
            item.quantity * (item.product.discount_price if item.product.discount_price else item.product.price)
            for item in self.products.all()
        )
        self.total_cost = total
        self.save()
        
        



    
    
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    street_address = models.CharField(max_length=255, null=True)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=20, null=True)

   
    def __str__(self):
        return f"Billing Address for {self.full_name}"
    

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
    
    
    

    
  