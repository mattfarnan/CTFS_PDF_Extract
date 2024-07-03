# Replace the first item in quotes with the name of a vendor that will regularly show in your credit card transactions.
# Within the brackets, the first item in quotes is the sub-category of the transaction. The second quoted item is the category.
# As you process more PDFs, you will determine which vendors you will need to add so categorization becomes more automated.


category_mapping = {
    "GROCERY STORE": ("Grocery", "Living Expenses"),
    "RESTAURANT": ("Restaurant", "Dining"),
    "PARKING": ("Parking and Tolls", "Automotive"),
    "LOCAL GYM": ("Fitness", "Health"),
    "HOME STORE": ("Home Stores", "House"),
}