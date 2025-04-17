import math


def A_huntington_hill_allocation():
    # Number of parties
    num_parties = int(input("Enter Number of parties: "))

    # קלט: מספר הקולות לכל מפלגה
    votes = []
    for i in range(num_parties):
        v = int(input(f"Enter the number of votes for party {i + 1}: "))
        votes.append(v)

    # קלט: מספר המושבים שרוצים לחלק
    total_seats = int(input("Enter the number of seats to be distributed: "))

    # אתחול: כל מפלגה מתחילה עם מושב 1
    seats = [1] * num_parties
    total_allocated = num_parties  # התחלנו עם מושב אחד לכל מפלגה

    def f(s):
        return math.sqrt(s * (s + 1))

    # חלוקת שאר המושבים
    while total_allocated < total_seats:
        max_index = 0
        max_value = votes[0] / f(seats[0])

        for i in range(1, num_parties):
            current_value = votes[i] / f(seats[i])
            if current_value > max_value:
                max_value = current_value
                max_index = i

        seats[max_index] += 1
        total_allocated += 1


    print("\nFinal seat distribution:")
    for i, s in enumerate(seats):
        print(f"party {i + 1}: {s} seats")


# לסעיף ב

def allocate_seats(votes, total_seats, y):
    n = len(votes)
    seats = [1] * n  # Start with one seat per party
    allocated = n

    def f(s):
        return s + y

    while allocated < total_seats:
        max_index = 0
        max_value = votes[0] / f(seats[0])
        for i in range(1, n):
            score = votes[i] / f(seats[i])
            if score > max_value:
                max_value = score
                max_index = i
        seats[max_index] += 1
        allocated += 1

    return seats

def print_comparison(parties, current_seats, new_seats, y_val):
    print(f"\nSeat distribution with modifier y = {y_val}:\n")
    print(f" {'Change':<7} | {'New':<7} | {'Current':<7} | {'Party':<6}")

    print("-" * 40)

    changed_count = 0
    for i in range(len(parties)):
        change = new_seats[i] - current_seats[i]
        if change != 0:
            changed_count += 1
        print(f"{parties[i]:<6} | {current_seats[i]:<7} | {new_seats[i]:<7} | {change:+}")

    print("\nSummary:")
    print(f"Number of parties with seat changes: {changed_count}")
    print(f"Number of parties with no change: {len(parties) - changed_count}")

def B():
    # Input data
    votes = [
        1115336,  # מחל
        847435,   # פה
        516470,   # ט
        432482,   # כן
        392964,   # שס
        280194,   # ג
        213687,   # ל
        194047,   # עם
        178735,   # ום
        175992    # אמת
    ]

    parties = ['מחל', 'פה', 'ט', 'כן', 'שס', 'ג', 'ל', 'עם', 'ום', 'אמת']
    current_seats = [32, 24, 14, 12, 11, 7, 6, 5, 5, 4]  # Official Knesset distribution

    # Get y from user
    try:
        y_input = float(input("Enter a value for y: "))
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return

    # Calculate seat distribution with provided y
    new_seats = allocate_seats(votes, 120, y_input)

    # Compare with current Knesset distribution
    print_comparison(parties, current_seats, new_seats, y_input)

if __name__ == "__main__":
    # לסעיף א
    #A_huntington_hill_allocation()
    # לסעיף ב
    #B()
    A_huntington_hill_allocation()
    B()