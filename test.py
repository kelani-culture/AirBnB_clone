class Car:
    None


porsche = Car()
setattr(porsche, 'car', 100)

tesla = Car()
setattr(tesla, 'brand', 'tesla')
print(tesla.brand)
