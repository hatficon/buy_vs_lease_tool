import streamlit as st
import numpy as np
from scipy import optimize

def calculate_mortgage(property_value, down_payment, interest_rate, mortgage_term):
    loan_amount = property_value - down_payment
    monthly_rate = interest_rate / 12 / 100
    num_payments = mortgage_term * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

def calculate_total_interest(monthly_payment, mortgage_term, property_value, down_payment):
    total_paid = monthly_payment * mortgage_term * 12
    return total_paid - (property_value - down_payment)

def calculate_tax_benefits(deductible_amount, tax_rate):
    return deductible_amount * tax_rate / 100

def calculate_npv(cash_flows, discount_rate):
    return np.sum(np.array(cash_flows) / (1 + discount_rate / 100) ** np.arange(len(cash_flows)))

def npv_func(rate, cash_flows):
    return np.sum(np.array(cash_flows) / (1 + rate) ** np.arange(len(cash_flows)))

def calculate_irr(cash_flows):
    try:
        result = optimize.root_scalar(npv_func, args=(cash_flows,), bracket=[-0.99, 100], method='brentq')
        return result.root if result.converged else None
    except ValueError:
        return None  # Return None if IRR calculation fails

def buy_vs_lease_analysis(property_value, lease_term, annual_lease_payment, down_payment, 
                          interest_rate, mortgage_term, appreciation_rate, tax_rate, 
                          maintenance_rate, insurance_rate, discount_rate):
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
    
    return npv_buying, npv_leasing, irr_buying

st.title('Buy vs. Lease Analysis Tool')

st.sidebar.header('Input Parameters')
property_value = st.sidebar.number_input('Property Value', min_value=0.0, value=1000000.0)
lease_term = st.sidebar.number_input('Lease Term (years)', min_value=1, value=10)
annual_lease_payment = st.sidebar.number_input('Annual Lease Payment', min_value=0.0, value=50000.0)
down_payment = st.sidebar.number_input('Down Payment for Buying', min_value=0.0, value=200000.0)
interest_rate = st.sidebar.number_input('Annual Interest Rate (%)', min_value=0.0, max_value=100.0, value=4.0)
mortgage_term = st.sidebar.number_input('Mortgage Term (years)', min_value=1, value=30)
appreciation_rate = st.sidebar.number_input('Annual Appreciation Rate (%)', min_value=-100.0, max_value=100.0, value=3.0)
tax_rate = st.sidebar.number_input('Tax Rate (%)', min_value=0.0, max_value=100.0, value=25.0)
maintenance_rate = st.sidebar.number_input('Annual Maintenance Rate (% of property value)', min_value=0.0, max_value=100.0, value=1.0)
insurance_rate = st.sidebar.number_input('Annual Insurance Rate (% of property value)', min_value=0.0, max_value=100.0, value=0.5)
discount_rate = st.sidebar.number_input('Discount Rate for NPV Calculation (%)', min_value=0.0, max_value=100.0, value=5.0)

if st.button('Calculate'):
    npv_buying, npv_leasing, irr_buying = buy_vs_lease_analysis(
        property_value, lease_term, annual_lease_payment, down_payment, 
        interest_rate, mortgage_term, appreciation_rate, tax_rate, 
        maintenance_rate, insurance_rate, discount_rate
    )

    st.header('Results')
    st.write(f"NPV of Buying: ${npv_buying:,.2f}")
    st.write(f"NPV of Leasing: ${npv_leasing:,.2f}")
    if irr_buying is not None:
        st.write(f"IRR of Buying: {irr_buying*100:.2f}%")
    else:
        st.write("IRR of Buying: Could not be calculated")

    if npv_buying > npv_leasing:
        st.success("Recommendation: Buying appears to be more financially advantageous.")
    elif npv_leasing > npv_buying:
        st.success("Recommendation: Leasing appears to be more financially advantageous.")
    else:
        st.success("Recommendation: Buying and leasing appear to be equally advantageous financially. Consider non-financial factors.")

    st.warning("Note: This analysis is based on the provided inputs and assumptions. Please consult with financial and legal professionals before making a decision.")