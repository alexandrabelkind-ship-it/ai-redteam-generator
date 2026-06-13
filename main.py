from src.generator import AttackGenerator


def main():
    print("⚔️  Welcome to the AI Red Team Attack Generator ⚔️")
    print("=" * 50)
    scenario = input("Enter attack scenario (e.g., ransomware, credential_dumping): ").strip()

    if not scenario:
        print("❌ No scenario entered. Exiting.")
        return

    generator = AttackGenerator()
    csv_out, story_out = generator.generate_scenario(scenario)

    print("\n🎉 Attack generated successfully!")
    print(f"   Run the UI with: streamlit run src/app.py")


if __name__ == "__main__":
    main()
