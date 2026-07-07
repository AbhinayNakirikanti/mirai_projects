import streamlit as st
import operator

st.set_page_config(page_title="Calculator", page_icon="🧮")

st.title("🧮 Simple Streamlit Calculator")
st.write("Perform basic arithmetic operations.")

num1 = st.number_input("Enter the first number", value=0.0)
num2 = st.number_input("Enter the second number", value=0.0)

operations = {
    "Add (+)": operator.add,
    "Subtract (-)": operator.sub,
    "Multiply (×)": operator.mul,
    "Divide (÷)": operator.truediv,
}

choice = st.selectbox("Select an operation", operations.keys())

if st.button("Calculate"):
    try:
        result = operations[choice](num1, num2)
        st.success(f"✅ Result: {result:.2f}")
    except ZeroDivisionError:
        st.error("❌ Division by zero is not allowed.")