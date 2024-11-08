import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset containing tourism data
data = pd.read_csv('tourism_data_indian_states.csv')

# Convert Month-Year data to a datetime format for easier plotting and time-based analysis
data['Date'] = pd.to_datetime(data['Month'] + ' ' + data['Year'].astype(str))

# Get a list of unique states
states = sorted(data['State'].unique())


# Display all states for easy selection
def display_states():
    """Prints a numbered list of available states for selection."""
    print("\nAvailable States:")
    for idx, state in enumerate(states, 1):  # Enumerate with starting index 1
        print(f"{idx}. {state}")  # Print the index and state name


# Function to select a state with validation
def select_state():
    """Prompts the user to select a state from the list."""
    display_states()
    while True:
        try:
            choice = int(input("Select a state by number: "))
            if 1 <= choice <= len(states):
                return states[choice - 1]  # Return the selected state
            else:
                print("Invalid number. Please choose a valid state number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to display the main menu
def tourism_visualization_menu():
    """Displays a menu of options to visualize tourism data."""
    while True:
        print("\n--- Tourism Data Visualization Menu ---")
        print("1. Total Tourists by State")
        print("2. Monthly Tourist Trends for a State")
        print("3. Top 5 States by Total Tourists")
        print("4. Growth Percentage by State")
        print("5. Tourist Demographics by State (Domestic vs. Foreign)")
        print("6. State Suitability for Tourism")
        print("7. Foreign vs. Domestic Tourist Trends")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            total_tourists_by_state()  # Show total tourists by state
        elif choice == '2':
            state_name = select_state()  # Let the user select a state
            monthly_tourist_trends(state_name)  # Show monthly trends for the selected state
        elif choice == '3':
            top_5_states_by_tourists()  # Show top 5 states with the highest number of tourists
        elif choice == '4':
            growth_percentage_by_state()  # Show growth percentage by state
        elif choice == '5':
            state_name = select_state()  # Let the user select a state
            tourist_demographics_by_state(state_name)  # Show domestic vs. foreign tourists by state
        elif choice == '6':
            state_suitability_score_map()  # Show suitability of states for tourism
        elif choice == '7':
            state_name = select_state()  # Let the user select a state
            foreign_vs_domestic_trends(state_name)  # Compare foreign and domestic tourist trends
        elif choice == '8':
            print("Exiting the menu. Thank you!")  # Exit the program
            break
        else:
            print("Invalid choice. Please try again.")


# Feature 1: Total Tourists by State
def total_tourists_by_state():
    """Displays a bar chart of the total number of tourists for each state."""
    plt.figure(figsize=(12, 6))
    # Group by state and sum total tourists, then sort the states in ascending order
    state_totals = data.groupby('State')['Total_Tourists'].sum().sort_values()
    state_totals.plot(kind='bar', color='skyblue')  # Plot the data as a bar chart
    plt.title("Total Tourists by State")
    plt.xlabel("Total Tourists")
    plt.ylabel("State")
    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.show()


# Feature 2: Monthly Tourist Trends for a State
def monthly_tourist_trends(state_name):
    """Displays a line chart of monthly tourist trends for the selected state."""
    state_data = data[data['State'] == state_name]  # Filter data for the selected state
    plt.figure(figsize=(10, 5))
    # Plot the total tourists for each month for the selected state
    plt.plot(state_data['Date'], state_data['Total_Tourists'], marker='o', linestyle='-', color='green')
    plt.title(f"Monthly Tourist Trends in {state_name}")
    plt.xlabel("Date")
    plt.ylabel("Total Tourists")
    plt.grid(True)  # Add gridlines for better readability

    # Format the x-axis to show both month and year
    plt.xticks(rotation=45, ha='right')  # Rotate the date labels to avoid overlap
    plt.tight_layout()
    plt.show()


# Feature 3: Top 5 States by Total Tourists
def top_5_states_by_tourists():
    """Displays a bar chart of the top 5 states with the highest total number of tourists."""
    plt.figure(figsize=(8, 5))
    # Get the top 5 states with the highest total tourists
    top_5_states = data.groupby('State')['Total_Tourists'].sum().nlargest(5)
    top_5_states.plot(kind='bar', color='coral')  # Plot the top 5 as a bar chart
    plt.title("Top 5 States by Total Tourists")
    plt.xlabel("State")
    plt.ylabel("Total Tourists")
    plt.xticks(rotation=45)  # Rotate labels to avoid overlap
    plt.tight_layout()
    plt.show()


# Feature 4: Growth Percentage by State
def growth_percentage_by_state():
    """Displays a bar chart of the growth percentage in tourist numbers for each state."""
    plt.figure(figsize=(12, 6))
    # Plot a bar chart of growth percentage for each state
    plt.bar(data['State'], data['Growth_Percentage'])
    plt.title("Growth Percentage by State")
    plt.xlabel("State")
    plt.ylabel("Growth Percentage")
    plt.xticks(rotation=90)  # Rotate labels to avoid overlap
    plt.tight_layout()
    plt.show()


# Feature 5: Tourist Demographics by State (Domestic vs. Foreign)
def tourist_demographics_by_state(state_name):
    """Displays a line chart showing domestic vs. foreign tourists for the selected state."""
    state_data = data[data['State'] == state_name]  # Filter data for the selected state
    plt.figure(figsize=(10, 6))
    # Plot both domestic and foreign tourist trends
    plt.plot(state_data['Date'], state_data['Domestic_Tourists'], label='Domestic Tourists', marker='o')
    plt.plot(state_data['Date'], state_data['Foreign_Tourists'], label='Foreign Tourists', marker='x')
    plt.title(f"Tourist Demographics in {state_name} (Domestic vs. Foreign)")
    plt.xlabel("Date")
    plt.ylabel("Number of Tourists")
    plt.legend()  # Add a legend to differentiate the two lines
    plt.xticks(rotation=45)  # Rotate labels for better readability
    plt.tight_layout()
    plt.show()


# Feature 6: State Suitability for Tourism (Suitable vs. Unsuitable)
def state_suitability_score_map():
    """Displays a stacked bar chart showing suitability for tourism by state."""
    plt.figure(figsize=(12, 8))
    # Count how many states are marked as suitable and unsuitable
    suitable_states = data[data['Suitable_For_Tourism'] == 'Yes']['State'].value_counts()
    unsuitable_states = data[data['Suitable_For_Tourism'] == 'No']['State'].value_counts()

    # Create a list of all states
    labels = list(set(suitable_states.index).union(set(unsuitable_states.index)))
    suitability = [suitable_states.get(state, 0) for state in labels]
    unsuitability = [unsuitable_states.get(state, 0) for state in labels]

    # Plot the data as stacked bars
    plt.bar(labels, suitability, label="Suitable", color='green')
    plt.bar(labels, unsuitability, bottom=suitability, label="Unsuitable", color='red')
    plt.title("State Suitability for Tourism")
    plt.xlabel("State")
    plt.ylabel("Suitability Count")
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


# Feature 7: Foreign vs. Domestic Tourist Trends for a State
def foreign_vs_domestic_trends(state_name):
    """Displays a line chart comparing monthly trends of domestic and foreign tourists in the selected state."""
    state_data = data[data['State'] == state_name]  # Filter data for the selected state
    plt.figure(figsize=(10, 6))
    # Plot trends for both domestic and foreign tourists
    plt.plot(state_data['Date'], state_data['Domestic_Tourists'], label='Domestic Tourists', marker='o', color='blue')
    plt.plot(state_data['Date'], state_data['Foreign_Tourists'], label='Foreign Tourists', marker='x', color='orange')
    plt.title(f"Monthly Tourist Trends in {state_name} (Domestic vs. Foreign)")
    plt.xlabel("Date")
    plt.ylabel("Number of Tourists")
    plt.legend()  # Add a legend to differentiate the two lines

    # Format the x-axis to show both month and year
    plt.xticks(rotation=45, ha='right')  # Rotate the date labels to avoid overlap
    plt.tight_layout()
    plt.show()


# Running the menu
tourism_visualization_menu()