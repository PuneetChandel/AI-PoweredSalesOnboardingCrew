from crew import SalesOnboardingCrew

def run():
    inputs = {
            "name": "Meta Inc.",
            "email": "contact@gmail.com",
            "address": "New York, NY 10001",
            "phone": "",
            "website": "",
            "industry": "Technology"}

    crew = SalesOnboardingCrew().crew()
    result = crew.kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()
