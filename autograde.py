import os
import sys
import shutil
import subprocess
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import re


def remove_package_declaration(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        content = re.sub(r'^\s*package\s+.*?;\s*', '', content, flags=re.MULTILINE)
    with open(file_path, 'w') as file:
        file.write(content)

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []

    # Extract data from XML
    for testcase in root.findall(".//testcase"):
        testcase_data = [
            testcase.get("classname"),
            testcase.get("name"),
            testcase.get("time"),
            testcase.find("failure").text if testcase.find("failure") is not None else "",
        ]
        data.append(testcase_data)
    return data

def count_failed_testcases(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Count the number of failed test cases
    failed_testcases = sum(1 for testcase in root.findall(".//testcase/failure"))
    # Also add to the count # of errors
    failed_testcases += sum(1 for testcase in root.findall(".//testcase/error"))
    return failed_testcases

def copy_files(src_dir, dest_dir):
    # Ensure the source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory '{src_dir}' does not exist.")
        return

    # Ensure the destination directory exists, create it if not
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate through all files in the source directory recursively
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, file)

            # Copy the file to the destination directory
            shutil.copy2(src_path, dest_path)
            print(f"Copying '{src_path}' to '{dest_path}'")



def delete_files(directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Iterate through all files in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        try:
            # Check if it's a file and not a subdirectory
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
                print(f"Deleting '{file_path}'")
        except Exception as e:
            print(f"Error deleting '{file_path}': {e}")



def main():
    if len(sys.argv) <= 2:
        shutil.rmtree("./reports")
        os.mkdir('./reports')
    else:
        try:
            shutil.rmtree("./reports/" + sys.argv[2])
        except:
            pass
    nocopy = os.listdir('./nocopy')
    template_files = os.listdir('./template')
    problem_students = []
    submission_dir = sys.argv[1] + ('/' if not sys.argv[1][-1] == '/' else '')
    submissions = os.listdir(submission_dir) if len(sys.argv) <= 2 else [sys.argv[2]]
    error_students = []
    successful_students = []

    for submission in submissions:
        try:
            delete_files('./src/main/java/')
            copy_files(submission_dir + submission, './src/main/java/')
            # if os.path.isfile('./src/main/java/LinkedListExercisesTest.java'): # This was hard coded, must change for different assignments
            #     os.remove('./src/main/java/LinkedListExercisesTest.java')
            for file in os.listdir('./src/main/java/'):
                if file in nocopy or file[0] == '.' or '.class' in file or not '.java' in file:
                    os.remove('./src/main/java/' + file)
                    continue
                remove_package_declaration('./src/main/java/' + file)
            for file in template_files:
                if not os.path.isfile('./src/main/java/' + file):
                    shutil.copyfile('./template/' + file, './src/main/java/' + file)

            # p = os.system('mvn clean test')
            p = subprocess.Popen(['mvn', 'clean', 'test'])
            try:
                p.wait(90)
            except subprocess.TimeoutExpired:
                p.kill()
                problem_students.append(submission)
                continue

            report_loc = './target/surefire-reports/'
            # os.rename(report_loc + "TEST-MiniListTest.xml", report_loc + submission + "_report.xml")
            os.mkdir('./reports/' + submission)
            for file in os.listdir(report_loc):
                if not '.xml' in file:
                    continue
                shutil.copy(report_loc + file,'./reports/' + submission)
            # os.system('zip ./reports/' + submission + '_report.zip ' + report_loc + '*.xml') 
            # shutil.move(report_loc + submission + "_report.xml", "./reports/" + submission + "_report.xml")
            failed = 0
            for file in os.listdir(report_loc):
                if not '.xml' in file:
                    continue
                failed += count_failed_testcases(report_loc + file)
            if failed > 0:
                error_students.append((submission, failed))
            else:
                successful_students.append(submission)
                shutil.rmtree("./reports/" + submission)
        except Exception as e:
            problem_students.append(submission)
        # finally:
        #     pass
    print("These students completed with no errors: ")
    for line in successful_students:
        print(line)
    
    print()

    print("These students had errors:")
    for student, errors in error_students:
        print(student + "\t" + str(errors))

    print()
    
    print("These students had problems when grading: ")
    for line in problem_students:
        print(line)


    





if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Usage: \n\tpython autograde.py <DIRECTORY_TO_SUBMISSIONS>\nWhere the submissions directory contains one folder for each submission. All files in each folder will be copied (flatly) to the maven project, then ran with maven. XML files from the tests will be output to ./reports/, and a list of perfect, imperfect, and unrunnable tests in the case of compilation errors will be output to stdout.")
        exit()
    main()

