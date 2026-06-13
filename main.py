from src.generator import AttackGenerator

def main():
    print("🤖 Welcome to the AI Red Team Attack Generator 🤖")
    scenario = input("Enter attack scenario (e.g., ransomware, credential_dumping): ")
    
    generator = AttackGenerator()
    csv_out, story_out = generator.generate_scenario(scenario)
    
    print("\n--- Process Finished ---")

if __name__ == "__main__":
    main()