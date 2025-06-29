import pandas as pd

# Define the data based on the user query
questions_data = [
    {
        "S No.": 1,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "Which of the following statements about contextual tabs in Excel pivot tables is correct?",
        "OPTION1": "They are always visible, regardless of the selection.",
        "OPTION2": "They only appear when a pivot table is selected.",
        "OPTION3": "They provide options for data visualization only.",
        "OPTION4": "They can be customized by the user without any limitations.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "Contextual tabs in Excel, such as the 'PivotTable Analyze' and 'Design' tabs, appear on the ribbon only when a pivot table is selected. These tabs provide specific tools for analyzing and formatting the selected pivot table[2].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 2,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "What happens when you encounter an empty cell within a pivot table?",
        "OPTION1": "The pivot table displays a value of zero.",
        "OPTION2": "It shows a user-defined text in place of the blank.",
        "OPTION3": "The empty cell will cause an error message to appear.",
        "OPTION4": "The pivot table automatically deletes the row with the empty cell.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "Excel allows users to define what is displayed in empty cells within a pivot table. Instead of showing a blank, you can set it to display a zero or a user-defined text to improve readability[5].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 3,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "MULTICORRECT",
        "QUESTION TEXT": "Which of the following options allows you to visually filter data in a pivot table? (Select all that apply)",
        "OPTION1": "Insert Timeline",
        "OPTION2": "Field Settings",
        "OPTION3": "Insert Slicer",
        "OPTION4": "Refresh Button",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "1,3",
        "EXPLANATION": "Slicers and Timelines are both visual filtering tools for pivot tables. Slicers provide buttons to filter data, while Timelines are used specifically for date fields[6]. Field Settings are used to configure how fields are displayed and summarized, and the Refresh Button updates the data in the pivot table.",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 4,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "When utilizing the ‘Refresh All’ button in a pivot table, what is the expected outcome?",
        "OPTION1": "It refreshes only the selected pivot table.",
        "OPTION2": "It updates all data sources linked to the workbook.",
        "OPTION3": "It clears all filters applied to the pivot tables.",
        "OPTION4": "It refreshes all pivot tables in the current workbook.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "4",
        "EXPLANATION": "The ‘Refresh All’ button, found under the Data tab or the Analyze tab (as a dropdown option under Refresh), updates all pivot tables in the current workbook to reflect the latest changes in their respective data sources[7].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 5,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "What is the primary purpose of a calculated field within a pivot table?",
        "OPTION1": "To format the appearance of values in the pivot.",
        "OPTION2": "To create a new data column based on existing data.",
        "OPTION3": "To filter out irrelevant data.",
        "OPTION4": "To group data automatically by date.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "A calculated field is used to create a new column in the pivot table based on a formula that uses existing columns from the data source. This allows for performing calculations and deriving new insights from the data[8].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 6,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "If a student wants to present a pivot table in a clean format without subtotals, what should they do?",
        "OPTION1": "Enable the grand totals feature.",
        "OPTION2": "Select the option to remove subtotals.",
        "OPTION3": "Change the report layout to outline form.",
        "OPTION4": "Use the repeat item labels feature.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "To remove subtotals from a pivot table, you should select the option to remove subtotals in the Field Settings dialog box[9]. This ensures a cleaner presentation of the data.",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 7,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "What is implied when a user selects the ‘Calculated Item’ feature in a pivot table?",
        "OPTION1": "It applies calculations directly to the values in the table.",
        "OPTION2": "It is only available for measures, not dimensions.",
        "OPTION3": "It allows users to input a specific reference for comparison.",
        "OPTION4": "It is used to display totals at a grouped level.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "3",
        "EXPLANATION": "The ‘Calculated Item’ feature allows users to create a new item within a pivot table field by combining other items and categories into formulas or custom calculations. This is used to input a specific reference for comparison[10].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 8,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "In the context of pivot tables, why might one choose to enable ‘Repeat All Item Labels’?",
        "OPTION1": "To consolidate the data into fewer rows.",
        "OPTION2": "To improve visual clarity by repeating label names.",
        "OPTION3": "To prevent data from being grouped automatically.",
        "OPTION4": "To calculate averages across multiple dimensions.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "Enabling ‘Repeat All Item Labels’ improves visual clarity by repeating the label names for each item in the pivot table, making the data easier to scan and understand[11].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 9,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "To change the data source of the pivot table, which step should be taken?",
        "OPTION1": "Use the ‘Insert Slicer’ option.",
        "OPTION2": "Go to the Analyze tab and select ‘Change Data Source’.",
        "OPTION3": "Refresh the pivot table.",
        "OPTION4": "Clear all filters before making changes.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "2",
        "EXPLANATION": "To change the data source of a pivot table, navigate to the Analyze tab (or PivotTable Analyze tab) and select ‘Change Data Source’. This allows you to specify a new range or table for the pivot table[12].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    },
    {
        "S No.": 10,
        "SUBJECT": "Data Analysis",
        "TOPIC": "Pivot Tables",
        "TAGS": "",
        "QUESTION TYPE": "SINGLECORRECT",
        "QUESTION TEXT": "What does the ‘Print Options’ feature in a pivot table allow you to customize?",
        "OPTION1": "The process of filtering data before printing.",
        "OPTION2": "The visibility of subtotals in the printed output.",
        "OPTION3": "The display of row labels and how they repeat across pages.",
        "OPTION4": "The colors and themes applied to the pivot table.",
        "OPTION5": None,
        "OPTION6": None,
        "OPTION7": None,
        "OPTION8": None,
        "OPTION9": None,
        "OPTION10": None,
        "RIGHT ANSWER": "3",
        "EXPLANATION": "The ‘Print Options’ feature in a pivot table allows you to customize the display of row labels and how they repeat across pages, including the ability to repeat row labels on each printed page for better readability[13].",
        "CORRECT MARKS": 1,
        "NEGATIVE MARKS": 0,
        "DIFFICULTY": "Medium"
    }
]

# Convert the data into a DataFrame
questions_df = pd.DataFrame(questions_data)

# Save the formatted DataFrame to an Excel file
output_file = "Formatted_Questions_Pivot_Tables_Advanced.xlsx"
questions_df.to_excel(output_file, index=False)
output_file
