# CS0445 Autograder

## Usage 

### Setup

First ensure the following directories exist alongside `autograde.py`:

- template
- nocopy
- reports

Place all test files in `./src/test/java`. Additionally, add any files (including test files) that should be ignored and not tested into the `./nocopy` directory.


### Running

```
> python autograder.py <SUBMISSION_DIRECTORY> <SUBMISSION:optional>
```

Where submission directory is a directory containing a folder for each student's submission (unzipped). This folder will be copied flatly to the maven project inside of this project and run using `maven clean test`.

To control the starter files that are given to the students, add them to the `template` directory. This will ensure that if a student does not include starter file with their submission, it is uploaded for them.

Files in the `nocopy` directory will not be copied with the rest of the students files. For example, test files that the students did not write themselves should be added to the nocopy directory so that they do not cause errors.

#### Specifying a Submission

When specifying an individual submisison, the autograder will run only that submission. Use the submission directory named when doing this.

After running a submission, it will be left inside of the maven project for you to interact with.

**NOTE:** Since deleting the report directory is necessary for the script to function, ensure you have saved all previous reports before evaluating an individual submission.

## Output

The results of student's who did not pass all test will be within the `reports` directory in XML format. There will be a folder for each student, and a file for each tested class.

Additionally, the names of the students who pass all tests, students who did not pass all tests, and students who's submissions failed to compile will be output to the terminal.

**The original version of this program was written By Jayden Serenari (CS0445 Graduate Teaching Assitant, Spring 2024)**
