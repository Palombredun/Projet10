import os
import csv

from django.core.management.base import BaseCommand, CommandError
from products.models import Category, Product

class Command(BaseCommand):
    help = "Update the database with the csv contained in the directory products/data"

    def handle(self, *args, **kwargs):
        for csv_file in os.listdir('products/data'):
            if "csv" in csv_file:
                file = "products/data/" + csv_file
                with open(file, "r") as f:
                    reader = csv.DictReader(f, delimiter="\t")
                    for row in reader:
                        if row['product_name_fr'] and \
                        ['categories'] and \
                        row['image_url'] and \
                        row['nutrition_grade_fr']:
                            