import datetime

# Generate all Mondays in 2024
monday_dates = []
start_date = datetime.date(2024, 1, 1)
while start_date.weekday() != 0:  # 0 means Monday
    start_date += datetime.timedelta(days=1)
end_date = datetime.date(2024, 12, 31)

current_date = start_date
while current_date <= end_date:
    monday_dates.append(current_date)
    current_date += datetime.timedelta(weeks=1)

# List of 20 example GitHub repository URLs
github_urls = [
    "https://github.com/repo1", "https://github.com/repo2",
    "https://github.com/repo3", "https://github.com/repo4",
    "https://github.com/repo5", "https://github.com/repo6",
    "https://github.com/repo7", "https://github.com/repo8",
    "https://github.com/repo9", "https://github.com/repo10",
    "https://github.com/repo11", "https://github.com/repo12",
    "https://github.com/repo13", "https://github.com/repo14",
    "https://github.com/repo15", "https://github.com/repo16",
    "https://github.com/repo17", "https://github.com/repo18",
    "https://github.com/repo19", "https://github.com/repo20"
]

# Generate 1000 INSERT statements
insert_statements = []
for i in range(1000):
    example_date = monday_dates[i % len(monday_dates)]
    url = github_urls[i % len(github_urls)]
    example_integer = i + 1
    statement = f"INSERT INTO examples (url, example_date, example_integer) VALUES ('{url}', '{example_date}', {example_integer});"
    insert_statements.append(statement)
breakpoint()
# Output the INSERT statements
with open('insert_statements.sql', 'w') as f:
    for statement in insert_statements:
        f.write(statement + '\n')

print("1000 INSERT statements generated and written to insert_statements.sql")
