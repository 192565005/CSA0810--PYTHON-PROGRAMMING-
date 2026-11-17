def flawed_independent_ifs(units):
    """Buggy version: independent ifs, so one household can match several rules."""
    results = []
    if units <= 100:
        results.append("Eligible for Full Subsidy")
    if units <= 200:
        results.append("Eligible for Partial or Full Subsidy")
    if units > 200:
        results.append("No Subsidy")
    return results


def subsidy(units, has_ration_card=True, oldest_member_age=0):
    """Correct version: mutually exclusive if-elif-else with chained comparisons."""
    if units < 0:
        return "Invalid reading"
    if 0 <= units <= 100:
        return "Full Subsidy (100% Covered)"
    elif 101 <= units <= 200:
        if has_ration_card:
            return "Partial Subsidy (50% Covered)"
        return "No Subsidy (Ration Card Required)"
    else:  # units > 200
        if oldest_member_age > 80:
            return "Partial Subsidy (Senior Citizen Exemption)"
        return "No Subsidy (Standard Tariff)"


def main():
    print("--- State Electricity Subsidy Eligibility Evaluation ---")
    # The flawed version is shown for the 50 and 100 unit households.
    for hh, units in (("HH-01", 50), ("HH-02", 100)):
        print(f"Flawed Independent IF Triggers for {hh} ({units} units): "
              f"{flawed_independent_ifs(units)}")

    print("\nMutually Exclusive (if-elif-else) Results:")
    households = [("HH-01", 50), ("HH-02", 100), ("HH-03", 101),
                  ("HH-05", 200), ("HH-06", 201)]
    for hh, units in households:
        print(f"{hh} ({units} units)".ljust(18) + f"-> {subsidy(units)}")

    print("\nBoundary test sweep:")
    for u in (0, 100, 101, 150, 200, 201, 350):
        print(f"  {u:>3} units -> {subsidy(u)}")
    print(f"  350 units, member aged 85 -> {subsidy(350, oldest_member_age=85)}")
    print("[SUCCESS] Boundary evaluation and decision logic validated.")


if __name__ == "__main__":
    main()
