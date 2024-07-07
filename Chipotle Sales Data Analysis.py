# ### Introduction

# *In this dataset, there are 4622 records of Chipotle orders. Each order shows how many quantities the order contained, what were the items of the order, and the total price. Lets do some Data Exploration and see what we can find*

# ### Data Wrangling

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv('Chipotle Sales.csv')
df


df.info()
#Need to convert Order_ID into string
#Need to convert Item_Price into float


# After Data Cleaning
df.info()


df.describe()
#there are 4622 individual orders here, the average order contains 1.1 quantity(rounded)
#OK there is an order with 15 quantities. Need to check it out, and ask if it is real

#order price averages around $7.50


df[df['Quantity'] >= 5]
#Someone ordered 15 only chips and Salsa
#And another person ordered 10 bottles of water
# will decide in exploratory analysis if these two should be removed

df.isna().sum()
#29% of the data has empty Choice_Description


len(df[df.duplicated()])
#there are 59 duplicate rows

#df[df.duplicated()]

df.query('Order_ID == "103" ')

#Yes there is duplicate Order_IDs, but these look like different orders to me 


# ### Data Cleaning


df['Order_ID'] = df['Order_ID'].astype(str)
df['Item_Price'] = df['Item_Price'].replace('[\$,]', '', regex=True).astype(float)


df


#Create Order_Type column, i.e. is it Bowl, Burrito or Tacos
df['Order_Type'] = np.where(df['Item_Name'].str.contains('Burrito'), 'Burrito', 
                   np.where(df['Item_Name'].str.contains('Salad'), 'Salad',            
                   np.where(df['Item_Name'].str.contains('Bowl'), 'Bowl', 
                   np.where(df['Item_Name'].str.contains('Tacos'), 'Tacos',
                   np.where(df['Item_Name'].str.contains('Izze|Nantucket Nectar|Canned Soda|Bottled Water|Canned Soft Drink|6 Pack Soft Drink', case=False), 'Drink',
                   np.where(df['Item_Name'].str.contains('Salsa'), 'Salsa', 
                   np.where(df['Item_Name'].str.contains('Chips and Guacamole'), 'Chips and Guacamole', 
                   np.where(df['Item_Name'].str.contains('Chips'), 'Chips',       'n/a')
                            
                )))))))

#df


#Create Order_Type column, i.e. is it Bowl, Burrito or Tacos
df['Meat_Type'] = np.where(df['Item_Name'].str.contains('Steak'), 'Steak', 
                   np.where(df['Item_Name'].str.contains('Chicken'), 'Chicken',            
                   np.where(df['Item_Name'].str.contains('Barbacoa'), 'Barbacoa', 
                   np.where(df['Item_Name'].str.contains('Carnitas'), 'Carnitas',
                   np.where(df['Item_Name'].str.contains('Veggie'), 'Veggie',  'other')
                            
                ))))

#df


meat = ['Chicken', 'Steak']
chicken_steak_df = df.query('Meat_Type == "Chicken" or Meat_Type == "Steak" ')
#Exclude outliers to show the true price distribution >> Back to Data Cleaning exclude those above $15 dollars

chicken_steak_df = chicken_steak_df.query('Item_Price <= 15.0')


# ### Exploratory Data Analysis

# What is Number 1 Item_Name mostly sold?
item_counts = df['Item_Name'].value_counts().sort_values(ascending=True)

plt.figure(figsize=(10, 10))
item_counts.plot(kind='barh', color='skyblue')

plt.title('Item_Name Counts')
plt.xlabel('Count')
#plt.ylabel('Item_Name')

plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)

plt.tight_layout()
plt.show()

#Chicken Bowl and Chicken Borrito are the top orders, then the Steak Borrito and Bowls
#Now I want to know if customers buy bowl, burrito, or tacos mostly? Back to Data Cleaning

#Second question I have is, which meat has most orders: Chicken or Steak or Barbacoa or Carnitas or Veggie. Back to Data Cleaning
# and also, is one pricer then the other?

#to answer above questions, lets do pie graph
order_type_counts = df['Order_Type'].value_counts()

plt.figure(figsize=(6, 5))
plt.pie(order_type_counts, labels=order_type_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Order types')

plt.legend(title='Categories', loc='center left', bbox_to_anchor=(1, 0.5))

plt.axis('equal') 
plt.show()

#OK there is equal spread of customers that order bowl and burrito

meat_counts = df[df['Meat_Type'] != 'other']['Meat_Type'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(4, 4))
meat_counts.plot(kind='bar', color='purple')

plt.title('Meat_Type Counts')
plt.xlabel('Meat_Type')
plt.ylabel('Number of Orders')

plt.tight_layout()
plt.show()

print(meat_counts)

#Well, more than half of the orders chicken is ordered, I was expecting steak and chicken to be close but not this much difference between then
#Now lets see what is the price difference



def calculate_quartiles(group):
    return group.quantile([0, 0.25, 0.5, 0.75, 1])

summary = chicken_steak_df.groupby('Meat_Type')['Item_Price'].apply(calculate_quartiles).unstack()
summary.columns = ['min', 'Q1', 'median', 'Q3', 'max']
summary.loc['difference'] = summary.loc['Chicken'] - summary.loc['Steak']
print(summary)

plt.figure(figsize=(8, 6))
sns.boxplot(x='Meat_Type', y='Item_Price', data=chicken_steak_df)
plt.title('Price Distribution')
plt.xlabel('Meat Type')
plt.ylabel('Item_Price')
plt.show()

#Steak definitely runs higher price, on average by 50 cents


#Lastly I want to know what is the number one Item in Choice_Description. One that is most often in all orders

from wordcloud import WordCloud

all_choices = ' '.join(df['Choice_Description'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_choices)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#Tomatoe Salsa, Sour Creak, Black Beans, Fresh Tomatoe amongst the most choices used in the orders

# the order with most item_price
top_expensive_orders = df.sort_values(by='Item_Price', ascending=False).head(5)
top_expensive_orders


# ### Conclusion

# The following was discovered:
# - Chicken Bowl and Chicken Borrito are the top orders, then the Steak Borrito and Bowls
# - 25.1% of the orders are Bowl and 25.4% are Burrito
# - more than half of the orders are Chicken meat (1560 orders are for Chicken and 702 are for Steak)
# - though the price for Steak runs on average higher by $0.50
# - Given the available choices: Tomato Salsa, Sour Creak, Black Beans and Fresh Tomato are the top 4 choices
# - Order_ID 1443 is for 15 items of Chips and Fresh Tomatoe Salsa



