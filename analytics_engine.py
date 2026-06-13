import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Initializing Chennai Real Estate Analytics Engine...")

file_name = "Real Estate Pricing Analytics.xlsx"

if not os.path.exists(file_name):
    print(f" Error: '{file_name}' not found in the current directory!")
    exit()

df = pd.read_excel(file_name, sheet_name='Properties_Data')

df.columns = df.columns.str.strip()

print("\n Generating Descriptive Market Visualizations...")

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]

plt.figure()
locality_price = df.groupby('Locality')['Price per Sq.Ft'].mean().sort_values(ascending=False)
sns.barplot(x=locality_price.values, y=locality_price.index, palette="Blues_r")
plt.title("Chennai Market: Average Price per Sq.Ft by Locality", fontsize=14, pad=15)
plt.xlabel("Price per Sq.Ft (₹)", fontsize=12)
plt.ylabel("Locality", fontsize=12)
plt.tight_layout()
plt.savefig("locality_price_trends.png", dpi=300)
print(" Chart 1 Saved: 'locality_price_trends.png' (Locality Price Performance)")

plt.figure()
sns.boxplot(data=df, x='Property Type', y='Final Price', palette="Set2")
plt.title("Property Type Valuation Distribution", fontsize=14, pad=15)
plt.xlabel("Property Type", fontsize=12)
plt.ylabel("Final Price (in Crores / Lakhs)", fontsize=12)
plt.tight_layout()
plt.savefig("property_valuation_distribution.png", dpi=300)
print("Chart 2 Saved: 'property_valuation_distribution.png' (Market Pricing Spread)")

def property_price_predictor():
    print("\n" + "="*50)
    print("WELCOME TO CHENNAI REAL ESTATE PRICE PREDICTOR ENGINE")
    print("="*50)
    
    available_localities = df['Locality'].unique()
    print(f"\n Available Localities:\n{', '.join(available_localities)}")
    user_locality = input("Enter the Locality from the list above: ").strip()
    
    if user_locality not in available_localities:
        print("Locality not found in baseline data. Standard pricing configs will apply.")
        base_price_sqft = df['Price per Sq.Ft'].mean()
        zone = "Unknown"
        tier = "Tier 3"
    else:
        locality_data = df[df['Locality'] == user_locality].iloc[0]
        base_price_sqft = locality_data['Price per Sq.Ft']
        zone = locality_data['Zone']
        tier = locality_data['Tier']
        
    available_types = df['Property Type'].unique()
    print(f"\n Property Types: {', '.join(available_types)}")
    user_type = input("Enter Property Type: ").strip()
    
    try:
        user_size = float(input("\n Enter the Property Size (in Sq.Ft): "))
    except ValueError:
        print("Invalid size numeric input. Restarting engine pipeline.")
        return

    total_base_price = user_size * base_price_sqft
    
    premium_charge = 0
    if tier == "Tier 1":
        premium_charge = total_base_price * 0.05
        
    final_estimated_price = total_base_price + premium_charge

    print("\n" + "-"*40)
    print(" VALUATION ESTIMATION REPORT")
    print("-"*40)
    print(f" Location      : {user_locality} ({zone} Zone - {tier})")
    print(f" Property Type : {user_type}")
    print(f" Size           : {user_size:,.0f} Sq.Ft")
    print(f" Rate per Sq.Ft: ₹{base_price_sqft:,.0f} / Sq.Ft")
    print(f" Base Valuation : ₹{total_base_price:,.2f}")
    print(f" Premium Charge : ₹{premium_charge:,.2f} (5% Tier-1 Dev Fee)")
    print("-"*40)
    print(f"FINAL ESTIMATED PRICE: ₹{final_estimated_price:,.2f}")
    print("="*50 + "\n")

if __name__ == "__main__":
    property_price_predictor()