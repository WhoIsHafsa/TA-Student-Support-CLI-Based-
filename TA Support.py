# =====================================================================
# CONSTANTS & RECORD STRUCTURE
# =====================================================================
MAX_STUDENTS = 200
MAX_COLS = 15
MAX_MONTHS = 12


class StudentRecord:
    def __init__(self):
        self.GRNo = ""
        self.StudentName = ""
        self.Marks = [0.0] * (MAX_COLS + 1)      # 1-indexed mapping
        self.Grade = [" "] * (MAX_COLS + 1)      # 1-indexed mapping
        self.TotalClasses = 0
        self.TotalAttended = 0
        self.AvgPercentage = 0.0
        self.AvgAttendance = 0.0
        self.AvgMonthlyAttendance = 0.0
        self.MonthlyPresent = [0] * (MAX_MONTHS + 1)
        self.MonthlyTotal = [0] * (MAX_MONTHS + 1)


# Global Master Database Variables (1-indexed padding using dummy index 0)
StudentList = [None] + [StudentRecord() for _ in range(MAX_STUDENTS)]
StudentCount = 0
ActiveCols = 7
ColNames = [""] + ["Test 1", "Test 2", "Test 3", "Mid-term Exam", "Test 5", "Test 6", "Mock Exam"] + [""] * (MAX_COLS - 7)
TestTotals = [0.0] * (MAX_COLS + 1)
FlagLowPerf = [""] * (MAX_STUDENTS + 1)


# =====================================================================
# HELPER FUNCTION: FIND STUDENT BY G.R. NO.
# =====================================================================
def FindStudent(TargetGR):
    global StudentCount, StudentList
    Index = 1
    Found = False

    while Index <= StudentCount and not Found:
        if StudentList[Index].GRNo == TargetGR:
            Found = True
        else:
            Index += 1

    return Found


# =====================================================================
# EFFICIENT BUBBLE SORT
# =====================================================================
def AutoSort():
    global StudentCount, StudentList
    if StudentCount <= 1:
        return

    LastSwap = StudentCount - 1
    Swapped = True

    for i in range(1, StudentCount):
        if not Swapped:
            break
        else:
            Swapped = False
            for j in range(1, LastSwap + 1):
                try:
                    gr1 = StudentList[j].GRNo
                    gr2 = StudentList[j + 1].GRNo
                    Num1 = int(gr1[3:]) if len(gr1) > 3 else 0
                    Num2 = int(gr2[3:]) if len(gr2) > 3 else 0
                except ValueError:
                    Num1, Num2 = 0, 0

                if Num1 > Num2:
                    Temp = StudentList[j]
                    StudentList[j] = StudentList[j + 1]
                    StudentList[j + 1] = Temp
                    Swapped = True
                    LastSwap = j


# =====================================================================
# FILE HANDLING: LOAD & SAVE
# =====================================================================
def LoadDataFromFiles():
    global StudentCount, StudentList, ActiveCols, ColNames
    StudentCount = 0
    try:
        with open("StudentData.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                return

            # FIX 2: Parse Line 1 (Header Row) to restore dynamic ActiveCols and ColNames
            header_line = lines[0].strip()
            if header_line:
                header_parts = header_line.split(",")
                if len(header_parts) > 6:
                    saved_col_count = (len(header_parts) - 6) // 2
                    if 1 <= saved_col_count <= MAX_COLS:
                        ActiveCols = saved_col_count
                        for c in range(1, ActiveCols + 1):
                            raw_header = header_parts[6 + (c - 1) * 2]
                            # Strip "Mark_" prefix to recover original column name
                            if raw_header.startswith("Mark_"):
                                ColNames[c] = raw_header[5:]
                            else:
                                ColNames[c] = raw_header

            # Process student data lines starting from Line 2
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 6:
                        StudentCount += 1
                        idx = StudentCount
                        StudentList[idx].GRNo = parts[0]
                        StudentList[idx].StudentName = parts[1]

                        try:
                            StudentList[idx].TotalClasses = int(parts[2]) if parts[2].strip() else 0
                        except ValueError:
                            StudentList[idx].TotalClasses = 0

                        try:
                            StudentList[idx].TotalAttended = int(parts[3]) if parts[3].strip() else 0
                        except ValueError:
                            StudentList[idx].TotalAttended = 0

                        try:
                            StudentList[idx].AvgPercentage = float(parts[4]) if parts[4].strip() else 0.0
                        except ValueError:
                            StudentList[idx].AvgPercentage = 0.0

                        try:
                            StudentList[idx].AvgAttendance = float(parts[5]) if parts[5].strip() else 0.0
                        except ValueError:
                            StudentList[idx].AvgAttendance = 0.0

                        curr_idx = 6
                        num_cols_saved = (len(parts) - 6) // 2
                        if num_cols_saved > ActiveCols:
                            ActiveCols = num_cols_saved

                        for c in range(1, num_cols_saved + 1):
                            if curr_idx < len(parts):
                                val_str = parts[curr_idx].strip()
                                try:
                                    StudentList[idx].Marks[c] = float(val_str) if val_str else 0.0
                                except ValueError:
                                    StudentList[idx].Marks[c] = 0.0
                            curr_idx += 1

                            if curr_idx < len(parts):
                                val_str = parts[curr_idx].strip()
                                StudentList[idx].Grade[c] = val_str if val_str else " "
                            curr_idx += 1
    except FileNotFoundError:
        pass


def SaveDataToFiles():
    global StudentCount, StudentList, ActiveCols, ColNames
    try:
        with open("StudentData.txt", "w") as file:
            header_parts = ["GRNo", "StudentName", "TotalClasses", "TotalAttended", "AvgPercentage", "AvgAttendance"]
            for c in range(1, ActiveCols + 1):
                header_parts.append(f"Mark_{ColNames[c]}")
                header_parts.append(f"Grade_{ColNames[c]}")

            file.write(",".join(header_parts) + "\n")

            for i in range(1, StudentCount + 1):
                record_parts = [
                    StudentList[i].GRNo,
                    StudentList[i].StudentName,
                    str(StudentList[i].TotalClasses),
                    str(StudentList[i].TotalAttended),
                    str(StudentList[i].AvgPercentage),
                    str(StudentList[i].AvgAttendance)
                ]

                for c in range(1, ActiveCols + 1):
                    record_parts.append(str(StudentList[i].Marks[c]))
                    record_parts.append(str(StudentList[i].Grade[c]))

                file.write(",".join(record_parts) + "\n")
    except IOError:
        print("Error saving data to file.")


# =====================================================================
# MODULE 2: ADD / REMOVE STUDENT DATA
# =====================================================================
def EditClass():
    global StudentCount, StudentList
    Action = 0
    while Action not in [1, 2]:
        try:
            print("\n-- Add / Remove Students Data --")
            print("1. Add New Student")
            print("2. Remove Student")
            Action = int(input("Choose action (1 or 2): "))
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    if Action == 1:
        if StudentCount < MAX_STUDENTS:
            StudentCount += 1
            gr = input("Enter G.R. Num: ").strip()
            name = input("Enter Full Name of Student: ").strip()
            StudentList[StudentCount].GRNo = gr
            StudentList[StudentCount].StudentName = name

            for ColNum in range(1, MAX_COLS + 1):
                StudentList[StudentCount].Marks[ColNum] = 0.0
                StudentList[StudentCount].Grade[ColNum] = " "

            StudentList[StudentCount].TotalClasses = 0
            StudentList[StudentCount].TotalAttended = 0
            StudentList[StudentCount].AvgPercentage = 0.0
            StudentList[StudentCount].AvgAttendance = 0.0

            print("Successfully added!")
            AutoSort()
        else:
            print("Error! Max students enrolled.")
    else:
        TargetGR = input("Enter G.R. No. to remove: ").strip()
        StudentFound = FindStudent(TargetGR)

        if StudentFound:
            Index = 1
            while Index <= StudentCount:
                if StudentList[Index].GRNo == TargetGR:
                    for ShiftIndex in range(Index, StudentCount):
                        StudentList[ShiftIndex] = StudentList[ShiftIndex + 1]
                    StudentCount -= 1
                    print("Student removed successfully.")
                    break
                Index += 1
            AutoSort()
        else:
            print("Error! Student not found.")

    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 3: PERFORMANCE TRACKER
# =====================================================================
def Academics():
    global StudentCount, StudentList, ActiveCols, ColNames, TestTotals, FlagLowPerf

    if StudentCount == 0:
        print("No students enrolled in the system yet.")
        input("\nPress Enter to return to Main Menu...")
        return

    SelCol = 0
    while True:
        try:
            print("\nSelect column to batch-enter data for:")
            for colnum in range(1, ActiveCols + 1):
                print(f"{colnum}. {ColNames[colnum]}")
            SelCol = int(input("Enter column number: "))
            if 1 <= SelCol <= ActiveCols:
                break
        except ValueError:
            pass
        print("Invalid selection. Please choose a valid column number.")

    if TestTotals[SelCol] == 0:
        while True:
            try:
                TestTotals[SelCol] = float(input(f"Enter total mark for {ColNames[SelCol]}: "))
                if TestTotals[SelCol] > 0:
                    break
                print("Total mark must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid numeric value.")

    print(f"\n--- Batch Entry for: {ColNames[SelCol]} (Total: {TestTotals[SelCol]}) ---")

    for Index in range(1, StudentCount + 1):
        print(f"\nStudent: {StudentList[Index].GRNo} - {StudentList[Index].StudentName}")
        while True:
            try:
                RawMark = float(input(f"Enter mark (0 to {TestTotals[SelCol]}): "))
                if 0 <= RawMark <= TestTotals[SelCol]:
                    break
                print(f"Mark must be between 0 and {TestTotals[SelCol]}.")
            except ValueError:
                print("Invalid input. Please enter a valid numeric mark.")

        StudentList[Index].Marks[SelCol] = RawMark
        TestPercentage = (RawMark / TestTotals[SelCol]) * 100

        if TestPercentage >= 90:
            StudentList[Index].Grade[SelCol] = "A*"
        elif TestPercentage >= 80:
            StudentList[Index].Grade[SelCol] = "A"
        elif TestPercentage >= 70:
            StudentList[Index].Grade[SelCol] = "B"
        elif TestPercentage >= 60:
            StudentList[Index].Grade[SelCol] = "C"
        elif TestPercentage >= 50:
            StudentList[Index].Grade[SelCol] = "D"
        else:
            StudentList[Index].Grade[SelCol] = "U"

        if TestPercentage < 30:
            FlagLowPerf[Index] = StudentList[Index].GRNo

    print("\nAll student marks for this test saved successfully!")
    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 4: ATTENDANCE TRACKER
# =====================================================================
def Attendancelog():
    global StudentCount, StudentList
    TargetGR = input("Enter G.R. No: ").strip()
    StudentFound = FindStudent(TargetGR)

    if StudentFound:
        Index = 1
        while Index <= StudentCount and StudentList[Index].GRNo != TargetGR:
            Index += 1

        PresentToday = False
        while True:
            ans = input(f"Was {StudentList[Index].GRNo} present today? (TRUE/FALSE): ").strip().lower()
            if ans in ['true', 't', 'yes', 'y']:
                PresentToday = True
                break
            elif ans in ['false', 'f', 'no', 'n']:
                PresentToday = False
                break
            else:
                print("Invalid input. Please type 'TRUE' or 'FALSE'.")

        StudentList[Index].TotalClasses += 1
        if PresentToday:
            StudentList[Index].TotalAttended += 1

        if StudentList[Index].TotalClasses > 0:
            StudentList[Index].AvgAttendance = (StudentList[Index].TotalAttended / StudentList[Index].TotalClasses) * 100

        print("Attendance logged successfully.")
    else:
        print("Student not found.")

    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 5: OVERALL CLASS SUMMARY (PER TEST) - FIXED
# =====================================================================
def ClassTestSummary():
    global StudentCount, StudentList, ActiveCols, ColNames, TestTotals

    if StudentCount == 0:
        print("No students enrolled in the system yet.")
        input("\nPress Enter to return to Main Menu...")
        return

    print("\nSelect Test to generate summary for overall class (Col Number):")
    for c in range(1, ActiveCols + 1):
        print(f"{c}. {ColNames[c]}")

    SelCol = 0
    while True:
        try:
            SelCol = int(input("Enter column number: "))
            if 1 <= SelCol <= ActiveCols:
                break
        except ValueError:
            pass
        print("Invalid selection. Please choose a valid column number.")

    HighestMark = -999.0
    SumMarks = 0.0
    ActiveStudentsInTest = 0
    TopScorerGR = "None"

    for Index in range(1, StudentCount + 1):
        if StudentList[Index].Grade[SelCol].strip() != "":
            ActiveStudentsInTest += 1
            SumMarks += StudentList[Index].Marks[SelCol]

            if StudentList[Index].Marks[SelCol] > HighestMark:
                HighestMark = StudentList[Index].Marks[SelCol]
                TopScorerGR = StudentList[Index].GRNo

    # Only prompt for total mark and run Grade 'U' check if test data actually exists
    if ActiveStudentsInTest > 0:
        if TestTotals[SelCol] == 0:
            while True:
                try:
                    TestTotals[SelCol] = float(input(f"Enter total mark for {ColNames[SelCol]}: "))
                    if TestTotals[SelCol] > 0:
                        break
                    print("Total mark must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a valid numeric value.")

        Classpercent = ((SumMarks / ActiveStudentsInTest) / TestTotals[SelCol]) * 100
        print(f"\n--- Class Summary for {ColNames[SelCol]} ---")
        print(f"Total Students Graded: {ActiveStudentsInTest}")
        print(f"Average percentage of class: {Classpercent:.2f}%")
        print(f"Highest Mark: {HighestMark} / {TestTotals[SelCol]}")
        print(f"G.R. Num of Top Scorer: {TopScorerGR}")

        print("\n--- Students Requiring Academic Assistance (Grade 'U') ---")
        flagged_count = 0
        for Index in range(1, StudentCount + 1):
            if StudentList[Index].Grade[SelCol].strip() == "U":
                print(f"-> G.R. No: {StudentList[Index].GRNo} | Name: {StudentList[Index].StudentName} | Mark: {StudentList[Index].Marks[SelCol]} / {TestTotals[SelCol]}")
                flagged_count += 1

        if flagged_count == 0:
            print("None! No students scored a 'U' grade in this test.")
        else:
            print(f"Total students requiring intervention: {flagged_count}")
    else:
        print(f"\nNo valid student data recorded for {ColNames[SelCol]} yet.")

    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 6: INDIVIDUAL STUDENT SUMMARY
# =====================================================================
def IndividualSummary():
    global StudentCount, StudentList, ActiveCols, ColNames
    TargetGR = input("Enter G.R. No: ").strip()
    StudentFound = FindStudent(TargetGR)

    if StudentFound:
        Index = 1
        while Index <= StudentCount and StudentList[Index].GRNo != TargetGR:
            Index += 1

        print(f"\n--- Summary for {StudentList[Index].GRNo} ---")
        print(f"G.R. No: {StudentList[Index].GRNo}")
        print(f"Student Name: {StudentList[Index].StudentName}")
        print(f"Avg Attendance: {StudentList[Index].AvgAttendance:.2f}%")

        for c in range(1, ActiveCols + 1):
            print(f"{ColNames[c]} -> Mark: {StudentList[Index].Marks[c]} | Grade: {StudentList[Index].Grade[c]}")
    else:
        print("Student not found.")

    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 7: EDIT TEST DATA (COLUMNS) - FIXED
# =====================================================================
def EditTestData():
    global ActiveCols, ColNames, TestTotals, StudentCount, StudentList
    Choice = 0
    while Choice not in [1, 2]:
        try:
            print("\n--- EDIT TEST DATA ---")
            print("1. Add New Column")
            print("2. Rename Existing Column")
            Choice = int(input("Enter choice (1 or 2): "))
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    if Choice == 1:
        if ActiveCols < MAX_COLS:
            ActiveCols += 1
            NewName = input("Enter name for new column: ").strip()
            ColNames[ActiveCols] = NewName
            TestTotals[ActiveCols] = 0.0

            # Initialize default values for all existing students in the new column
            for idx in range(1, StudentCount + 1):
                StudentList[idx].Marks[ActiveCols] = 0.0
                StudentList[idx].Grade[ActiveCols] = " "

            print(f"Column '{NewName}' added successfully at position {ActiveCols}!")
        else:
            print("Max columns reached.")
    else:
        print("\nCurrent Columns:")
        for c in range(1, ActiveCols + 1):
            print(f"{c}. {ColNames[c]}")

        while True:
            try:
                TargetCol = int(input(f"Enter column number to rename (1 to {ActiveCols}): "))
                if 1 <= TargetCol <= ActiveCols:
                    NewName = input("Enter new name: ").strip()
                    ColNames[TargetCol] = NewName
                    print("Renamed successfully.")
                    break
                else:
                    print("Invalid column number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    input("\nPress Enter to return to Main Menu...")


# =====================================================================
# MODULE 1: MAIN MENU (ITERATIVE CONTROL LOOP)
# =====================================================================
def MainMenu():
    while True:
        Select = 0
        while True:
            try:
                print("\n=========================================")
                print("WELCOME")
                print("Choose:")
                print("1. Main Menu / Refresh")
                print("2. Add/Remove Students' Data")
                print("3. Performance Tracker")
                print("4. Attendance Tracker")
                print("5. Overall Class Summary")
                print("6. Individual Student's Summary")
                print("7. Edit Test Data (columns)")
                print("8. Save And Exit")
                print("=========================================")
                Select = int(input("Enter option (1-8): "))
                if 1 <= Select <= 8:
                    break
            except ValueError:
                pass
            print("Error. Choose from 1 to 8")

        if Select == 1:
            continue
        elif Select == 2:
            EditClass()
        elif Select == 3:
            Academics()
        elif Select == 4:
            Attendancelog()
        elif Select == 5:
            ClassTestSummary()
        elif Select == 6:
            IndividualSummary()
        elif Select == 7:
            EditTestData()
        elif Select == 8:
            SaveDataToFiles()
            print("Data saved. Exiting program. Goodbye!")
            break


# =====================================================================
# INITIALIZATION & PROGRAM ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    StudentCount = 0
    ActiveCols = 7

    for Index in range(1, MAX_COLS + 1):
        TestTotals[Index] = 0.0

    LoadDataFromFiles()
    MainMenu()
