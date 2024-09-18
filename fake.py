from faker import Faker

fake = Faker()

providers = [method for method in dir(fake) if not method.startswith('_')]

# print the list
for provider in providers:
    print(provider)
