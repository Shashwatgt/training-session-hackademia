# Attendance Analyzer

# class containing n students, for each student, we are given their attendance percentage
# and we need to determine how many students are eligible for the final exam.

# for loop
# if/ else/ elif
# accumulator/counter
n = int(input("Ener the number of students: "))

eligible= 0
considered= 0
not_eligible= 0

for i in range(1, n+1):
    attendance= float(input(f"Enter attendance for student {i}: "))
    # breakpoint()

    if attendance >=75:
        # eligible = eligible + 1
        eligible+=1
    elif attendance >=65:
        considered+=1
    else:
        not_eligible+=1

print(("\nSummary:")) # \n is for new line
print(f"Eligible students: {eligible}")
print(f"Considered students: {considered}")
print(f"Not eligible students: {not_eligible}")





