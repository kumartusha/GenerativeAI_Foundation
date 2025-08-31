from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Student(BaseModel):

    name: str
    name: str = 'nitish'               # Default values
    age: Optional[int] = None          # Set the None value if the value is not passing.
    # email: EmailStr                    # Through error if the syntax is wrong.
    cgpa: float = Field(gt = 0, lt= 10, default = 5, description='A decimal Value representing the cgpa of the student.')

new_student = {"name": "nitish"}       # Working Fine as the datatype is     explicetely mention as string.
# new_student = {"name": 32}             # give error bcoz in pydantic uses for the validation.
# new_student = {"age": '32'}            # it is smart it will automatically convert this string into the integer.( Smart Enough )
# new_student = {"name": "nitish", 'email': 'tushar.kumar@gmail.com', 'cgpa': 12}
new_student = {"name": "nitish", 'cgpa': 3, 'age': 20}

student = Student(**new_student)

print(student)
print(type(student))

student_dict = dict(student)

student_json = student.model_dump_json()

print(student_dict['age'])