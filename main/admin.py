from django.contrib import admin
from .models import * 

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Card)
admin.site.register(Order)
admin.site.register(Product,ProductsAdmin)
admin.site.register(Reserved)
admin.site.register(Wishlist)
admin.site.register(Company)
admin.site.register(Message)
admin.site.register(ProductCard)
admin.site.register(ProductReview)
admin.site.register(Comment)
admin.site.register(UserModel)
admin.site.register(Likee)