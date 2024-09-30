import numpy as np
import numpy_financial as npf

def calculate_mortgage(property_value, down_payment, interest_rate, mortgage_term):
    loan_amount = property_value - down_payment
    monthly_rate = interest_rate / 12 / 100
    num_payments = mortgage_term * 12
    return npf.pmt(monthly_rate, num_payments, -loan_amount)

def calculate_total_interest(monthly_payment, mortgage_term, property_value, down_payment):
    total_paid = monthly_payment * mortgage_term * 12
    return total_paid - (property_value - down_payment)

def calculate_tax_benefits(deductible_amount, tax_rate):
    return deductible_amount * tax_rate / 100

def calculate_npv(cash_flows, discount_rate):
    return npf.npv(discount_rate / 100, cash_flows)

def calculate_irr(cash_flows):
    return npf.irr(cash_flows)

def buy_vs_lease_analysis():
    # Input variables
    property_value = float(input("Enter property value: "))
    lease_term = int(input("Enter lease term (years): "))
    annual_lease_payment = float(input("Enter annual lease payment: "))
    down_payment = float(input("Enter down payment for buying: "))
    interest_rate = float(input("Enter annual interest rate (%): "))
    mortgage_term = int(input("Enter mortgage term (years): "))
    appreciation_rate = float(input("Enter annual appreciation rate (%): "))
    tax_rate = float(input("Enter tax rate (%): "))
    maintenance_rate = float(input("Enter annual maintenance rate (% of property value): "))
    insurance_rate = float(input("Enter annual insurance rate (% of property value): "))
    discount_rate = float(input("Enter discount rate for NPV calculation (%): "))

    # Buying calculations
    monthly_mortgage = calculate_mortgage(property_value, down_payment, interest_rate, mortgage_term)
    total_interest = calculate_total_interest(monthly_mortgage, mortgage_term, property_value, down_payment)
    future_property_value = property_value * (1 + appreciation_rate/100) ** lease_term
    annual_maintenance = property_value * maintenance_rate / 100
    annual_insurance = property_value * insurance_rate / 100
    
    # Generate cash flow array for buying
    cash_flows_buying = [-down_payment]  # Initial investment
    for year in range(1, lease_term + 1):
        annual_costs = monthly_mortgage * 12 + annual_maintenance + annual_insurance
        tax_benefits = calculate_tax_benefits(total_interest / mortgage_term + annual_maintenance + annual_insurance, tax_rate)
        cash_flows_buying.append(-annual_costs + tax_benefits)
    cash_flows_buying[-1] += future_property_value  # Add property value to last year

    # Leasing calculations
    total_lease_payments = annual_lease_payment * lease_term
    tax_benefits_leasing = calculate_tax_benefits(annual_lease_payment, tax_rate)

    # Generate cash flow array for leasing
    cash_flows_leasing = []
    for year in range(1, lease_term + 1):
        cash_flows_leasing.append(-annual_lease_payment + tax_benefits_leasing)

    # Comparative analysis
    npv_buying = calculate_npv(cash_flows_buying, discount_rate)
    npv_leasing = calculate_npv(cash_flows_leasing, discount_rate)
    irr_buying = calculate_irr(cash_flows_buying)
    
    # Results
    print("\nResults:")
    print(f"NPV of Buying: ${npv_buying:,.2f}")
    print(f"NPV of Leasing: ${npv_leasing:,.2f}")
    print(f"IRR of Buying: {irr_buying*100:.2f}%")
    
    if npv_buying > npv_leasing:
        print("\nRecommendation: Buying appears to be more financially advantageous.")
    elif npv_leasing > npv_buying:
        print("\nRecommendation: Leasing appears to be more financially advantageous.")
    else:
        print("\nRecommendation: Buying and leasing appear to be equally advantageous financially. Consider non-financial factors.")

    print("\nNote: This analysis is based on the provided inputs and assumptions. Please consult with financial and legal professionals before making a decision.")

if __name__ == "__main__":
    buy_vs_lease_analysis()