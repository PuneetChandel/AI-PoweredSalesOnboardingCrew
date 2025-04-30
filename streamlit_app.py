import streamlit as st
from crew import SalesOnboardingCrew

def main():
    st.title("AI Crew ")
    st.write("Enter the company details to start the onboarding process")

    # Create input fields
    name = st.text_input("Company Name", "Meta Inc.")
    email = st.text_input("Email", "contact@gmail.com")
    address = st.text_input("Address", "New York, NY 10001")
    phone = st.text_input("Phone Number", "")
    website = st.text_input("Website", "")
    industry = st.text_input("Industry", "Technology")

    # Create a button to run the crew
    if st.button("Start Onboarding"):
        inputs = {
            "name": name,
            "email": email,
            "address": address,
            "phone": phone,
            "website": website,
            "industry": industry
        }

        # Show a loading spinner while the crew is running
        with st.spinner("Running the onboarding crew..."):
            crew = SalesOnboardingCrew().crew()
            result = crew.kickoff(inputs=inputs)
            
            # Display the results
            st.success("Onboarding completed!")
            st.write("Results:")
            st.write(result)

if __name__ == "__main__":
    main() 