import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset containing tourism data
data = pd.read_csv('tourism_data_indian_states.csv')

# Convert 'Month' and 'Year' to a proper date format for easier plotting
data['Date'] = pd.to_datetime(data['Month'] + ' ' + data['Year'].astype(str))

# Get a list of unique states
states = sorted(data['State'].unique())

# Display all states for easy selection
def display_states():
    """Prints a numbered list of available states for selection."""
    print("\nAvailable States:")
    for idx, state in enumerate(states, 1):
        print(f"{idx}. {state}")

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
        print("6. Foreign vs. Domestic Tourist Trends")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

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
            state_name = select_state()  # Let the user select a state
            foreign_vs_domestic_trends(state_name)  # Compare foreign and domestic tourist trends
        elif choice == '7':
            print("Exiting the menu. Thank you!")  # Exit the program
            break
        else:
            print("Invalid choice. Please try again.")

# Feature 1: Total Tourists by State
def total_tourists_by_state():
    """Displays a bar chart of the total number of tourists for each state."""
    plt.figure(figsize=(14, 8))
    state_totals = data.groupby('State')['Total_Tourists'].sum().sort_values()
    state_totals.plot(kind='barh', color='royalblue', edgecolor='black', width=0.8)

    for i, v in enumerate(state_totals):
        plt.text(v + 100000, i, f'{v:,}', va='center', fontweight='bold', color='black', fontsize=9)

    plt.title("Total Tourists by State", fontsize=16)
    plt.xlabel("Total Tourists", fontsize=12)
    plt.ylabel("State", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=3.0)
    plt.show()

# Feature 2: Monthly Tourist Trends for a State
def monthly_tourist_trends(state_name):
    """Displays a line chart of monthly tourist trends for the selected state."""
    state_data = data[data['State'] == state_name]
    plt.figure(figsize=(12, 6))
    plt.plot(state_data['Date'], state_data['Total_Tourists'], marker='o', linestyle='-', color='darkgreen',
             linewidth=2, markersize=6)

    for i, v in enumerate(state_data['Total_Tourists']):
        plt.text(state_data['Date'].iloc[i], v + 50000, f'{v:,}', ha='center', va='bottom', fontsize=9, color='black')

    plt.title(f"Monthly Tourist Trends in {state_name}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Tourists", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True)
    plt.tight_layout(pad=3.0)
    plt.show()

# Feature 3: Top 5 States by Total Tourists
def top_5_states_by_tourists():
    """Displays a bar chart of the top 5 states with the highest total number of tourists."""
    plt.figure(figsize=(10, 6))
    top_5_states = data.groupby('State')['Total_Tourists'].sum().nlargest(5)
    top_5_states.plot(kind='bar', color=['tomato', 'seagreen', 'gold', 'steelblue', 'orange'], edgecolor='black')

    for i, v in enumerate(top_5_states):
        plt.text(i, v + 100000, f'{v:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("Top 5 States by Total Tourists", fontsize=16)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Total Tourists", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=3.0)
    plt.show()



# Feature 4: Growth Percentage of Tourists by State (Line Chart with Annotations)
def growth_percentage_by_state():
    """Displays a line chart of the growth percentage in tourist numbers for each state by year."""

    # Grouping the data by State and Year to get the total tourists by year
    state_yearly_data = data.groupby(['State', 'Year'])['Total_Tourists'].sum().reset_index()

    # Calculate the growth percentage for each state year-over-year
    state_yearly_data['Growth_Percentage'] = state_yearly_data.groupby('State')['Total_Tourists'].pct_change() * 100

    # Remove rows where the growth percentage is NaN (which will be present for the first year)
    state_yearly_data = state_yearly_data.dropna(subset=['Growth_Percentage'])

    # Create the plot
    plt.figure(figsize=(14, 8))

    # Plot each state's growth percentage as a line chart
    for state in state_yearly_data['State'].unique():
        state_data = state_yearly_data[state_yearly_data['State'] == state]
        plt.plot(state_data['Year'], state_data['Growth_Percentage'], marker='o', label=state, linewidth=2)

        # Annotate each year with the growth percentage
        for i, row in state_data.iterrows():
            plt.text(row['Year'], row['Growth_Percentage'] + 0.5, f'{row["Growth_Percentage"]:.2f}%',
                     ha='center', fontsize=6, color='black', fontweight='bold')

    # Customize the plot
    plt.title("Growth Percentage of Tourists by State (Year-over-Year)", fontsize=16, fontweight='bold')
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Growth Percentage (%)", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)

    # Add a legend to distinguish the states
    plt.legend(title="States", loc='upper left', fontsize=10)

    # Adjust the layout to avoid clipping
    plt.tight_layout(pad=3.0)

    # Show the plot
    plt.show()

# Feature 5: Tourist Demographics by State (Domestic vs. Foreign)
def tourist_demographics_by_state(state_name):
    """Displays a line chart showing domestic vs. foreign tourists for the selected state."""
    state_data = data[data['State'] == state_name]
    plt.figure(figsize=(12, 6))
    plt.plot(state_data['Date'], state_data['Domestic_Tourists'], label='Domestic Tourists', marker='o', color='blue',
             linewidth=2, markersize=6)
    plt.plot(state_data['Date'], state_data['Foreign_Tourists'], label='Foreign Tourists', marker='x', color='red',
             linewidth=2, markersize=6)
    for i, v in enumerate(state_data['Domestic_Tourists']):
        plt.text(state_data['Date'].iloc[i], v + 50000, f'{v:,}', ha='center', va='bottom', fontsize=9, color='black')
    for i, v in enumerate(state_data['Foreign_Tourists']):
        plt.text(state_data['Date'].iloc[i], v + 50000, f'{v:,}', ha='center', va='bottom', fontsize=9, color='black',
                 rotation=45)
    plt.title(f"Tourist Demographics in {state_name} (Domestic vs. Foreign)", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Number of Tourists", fontsize=12)
    plt.legend()
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=3.0)
    plt.show()

# Feature 6: Foreign vs. Domestic Tourist Trends by State
def foreign_vs_domestic_trends(state_name):
    """Displays a line chart comparing foreign and domestic tourist trends."""
    state_data = data[data['State'] == state_name]
    plt.figure(figsize=(14, 8))
    plt.plot(state_data['Date'], state_data['Domestic_Tourists'], label='Domestic', color='lightgreen', linewidth=2)
    plt.plot(state_data['Date'], state_data['Foreign_Tourists'], label='Foreign', color='coral', linewidth=2)

    # Add text labels for Domestic Tourists
    for i, v in enumerate(state_data['Domestic_Tourists']):
        plt.text(state_data['Date'].iloc[i], v + 50000, f'{v:,}', ha='center', va='bottom', fontsize=9, color='black', rotation=90)

    # Add text labels for Foreign Tourists
    for i, v in enumerate(state_data['Foreign_Tourists']):
        plt.text(state_data['Date'].iloc[i], v + 50000, f'{v:,}', ha='center', va='bottom', fontsize=9, color='black', rotation=45)

    plt.title(f"Foreign vs. Domestic Tourist Trends in {state_name}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Tourist Count", fontsize=12)
    plt.legend()
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True)
    plt.tight_layout(pad=3.0)
    plt.show()

# Call the main menu function to start the program
tourism_visualization_menu()