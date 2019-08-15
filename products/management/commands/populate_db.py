import json
import csv

from django.core.management.base import BaseCommand, CommandError
from products.models import Category, Product

class Command(BaseCommand):
    help = "Populate the database with the products previously downloaded."

    def handle(self, *args, **options):
        products = []
        categories = []
        
        with open('products/management/commands/openfoodfacts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                if row['product_name'] and \
                row['categories'] and \
                row['image_url'] and \
                row['nutrition_grade_fr']:
    
                    current_categories = row['categories'].split(', ')[:3]
                    if current_categories not in categories and \
                    len(current_categories) == 3:

                        categories.append(current_categories)

                        products.append([
                            row['product_name'],
                            row['nutrition_grade_fr'],
                            row['image_url'],
                            row['url'],
                            row['purchase_places'],
                            row['energy_100g'],
                            row['fat_100g'],
                            row['saturated-fat_100g'],
                            row['carbohydrates_100g'],
                            row['sugars_100g'],
                            row['fiber_100g'],
                            row['proteins_100g'],
                            ]
                            )

            for category in categories:
                if category[0] not in Category.objects.get(name=category[0]):
                    cat = Category.objects.create(name=category[0], parent=null)
                elif category[1] not in Category.objects.get(name=category[1]):
                    id_parent = Category.objects.get(name=category[0]).id
                    sub_cat = Category.objects.create(name=category[1], parent=id_parent)
                elif category[2] not in Category.objects.get(name=category[2]):
                    id_parent = Category.objects.get(name=category[1]).id
                    sub_sub_cat = Category.objects.create(name=category[2], parent=id_parent)
                else:
                    sub_sub_cat = Category.objects.get(name=category[2])
    
                for product in products:
                    if product['category_name'] == category:
                        new_product = Productobjects.create(
                            product_name=product['product_name'],
                            nutriscore=product['nutriscore'],
                            image_url=product['image_url'],
                            product_url = product['product_url'],
                            category=sub_sub_cat,
                            purchase_places=product['purchase_place'],
                            energy_100g=product['energy_100g'],
                            fat_100g=product['fat_100g'],
                            saturated_fats_100g=product['saturated_fat_100g'],
                            carbohydrates_100g=product['carbohydrates_100g'],
                            sugars_100g=product['sugars_100g'],
                            fibers_100g=product['fiber_100g'],
                            proteins_100g=product['proteins_100g'],
                            salt_100g=product['salt_100g'],
                            )
                        #new_product.save() 