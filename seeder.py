import datetime
import random
import time
from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from accounts.models import Nationality
from vendors.models import Category

def seed_categories(num_entries=10, overwrite=False):

    if overwrite:
        print("Overwriting Users")
        Category.objects.all().delete()
    count = 0
    for _ in range(num_entries):
        name = fake.country()
        description = fake.last_name()
        c = Category(
            name = name,
            description = description,
        ).save()
        count += 1
        percent_complete = count / num_entries * 100
        print(
                "Adding {} new Users: {:.2f}%".format(num_entries, percent_complete),
                end='\r',
                flush=True
                )
    print()

def seed_nationalities(num_entries=10, overwrite=False):

    if overwrite:
        print("Overwriting Users")
        Category.objects.all().delete()
    count = 0
    for _ in range(num_entries):
        name = fake.country()
        c = Nationality(
            name = name,
        ).save()
        count += 1
        percent_complete = count / num_entries * 100
        print(
                "Adding {} new Nationalities: {:.2f}%".format(num_entries, percent_complete),
                end='\r',
                flush=True
                )
    print()

