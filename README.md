# TA-Student-Support-CLI-Based-
A lightweight, CLI-based information system designed to help manage students' academic performance and attendance without requiring a heavy database.
Logical design and pseudocode architecture developed independently; Python implementation in collaboration with AI assistance.

A fully functional, error-resistant system consisting of 11 main modules. 

The primary features being:-

1. Display of the interactive "Main Menu" at start up, as well as after exiting each module (except for "Save And Exit").

2. Add/Remove students' data by simply entering their G.R. No. and/or name. Automatically arranges each student in ascending order of G.R. No. by running the helper module designed for efficient bubble sort.

3. Academic Performance Tracker: Allows the user to select the column (E.g: Test 1) for which data is to be entered, asking to input a total mark where necessary, then prompts for the test mark of each student; thus, allowing for batch entry. Also computes percentage of each student for each test and saves the automatically assigned grade to the corresponding grade column (E.g: Grade_Test 1).

4. Attendance Tracker: Allows user to search a student by G.R. No., and input their daily attendance data. Logs the total number of classes each individual has attended (since not everyone joins at the very start of the session), and computes and saves their monthly as well as overall term attendance after daily update.

5. Generate Overall Class Summary: Prompts user to select the assessment for which the report is required, then generates a neatly organized class performance summary which displays the computed average percentage of class, total number of students who appeared in the evaluation, highest mark for the test and the G.R. No. of the top scorer(s).

6. Individual Student's Summary: Displays full profile, average attendance percentage, and all active test marks and grades for a single searched student.

7. Edit Test Data (What appears and is saved in a column): Allows user to add a new column (as long as total number of columns stays less than or equal to the number of active columns allowed by the program) or rename an existing one.

8. Save And Exit: Composes the line for the students' data (1 line per student) by concatenating all the data corresponding to the individual, writes the line to the file, closes the file, and exits the program.

Helper Modules Developed:-

1. AutoSort(): An efficient bubble sort program which sorts students in ascending order based on the numerical portion (char. 4 onwards) of the G.R. Number. Executed after each new addition or removal.

2. LoadDataFromFiles(): Loads the latest updated version of the file (all previously saved data) at initialization of the program; thus, featuring automated file persistence

3. FindStudent(): Run inside almost every module in order to search for a particular student based on a target G.R. No. (input by the user).

Built with input-validation loops across every module to catch incorrect data types or out-of-range values, reprompting the user safely without crashing.
