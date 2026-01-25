from pydantic import BaseModel,  Field
from typing import Annotated, List, Optional, Generic, TypeVar


T = TypeVar('T')

class Data(BaseModel, Generic[T]):
    
    value: Annotated[T, Field(description="Extracted ocr text")]
    confidence: Annotated[float, Field(ge=0, le=1, description="Confidence (between 0-1) for extracted text based on ocr quality")]

class SubjectMarks(BaseModel):

    subjectName: Annotated[Data[str], Field(description="Name of the subject")]
    maxMarks: Annotated[Optional[Data[int]], Field(default_factory=lambda: Data[int](value=100, confidence=1.0), description="Maximum marks that can be obtained")]
    obtainedMarks: Annotated[Data[int], Field(description="Marks obetained in the subject")]
    grade: Annotated[Optional[Data[str]], Field(default=None, description="Grade (if present) based on obtained marks")]

class CandidateDetails(BaseModel):
    name: Annotated[Data[str], Field(description="Name of the student")]
    mothersName: Annotated[Optional[Data[str]], Field(default=None, description="Nmae of studen's mother")]
    fathersName: Annotated[Optional[Data[str]], Field(default=None, description="Nmae of student's father")]
    roll_no: Annotated[Data[int], Field(description="Roll number of student")]
    registration_no: Annotated[Optional[Data[str]], Field(default=None, description="student's registration number")]
    dob: Annotated[Data[str], Field(description="date of birht of student")]    # will use date datatype in future
    exam_year: Annotated[Data[int], Field(description="year of exam")]
    board: Annotated[Data[str], Field(description="Name of the examination board")]
    institution: Annotated[Data[str], Field(description="Name of the school")]

class ResultSummary(BaseModel):
    overallResult:  Annotated[Optional[Data[str]], Field(default=None, description="E.g., PASS, FAIL, FIRST DIVISION")]
    totalObtained: Annotated[Optional[Data[int]], Field(default=None, description="Total marks obtained overall")]
    percentage:  Annotated[Optional[Data[float]], Field(default=None, description="Percentage or GPA if present")]

class MetaInfo(BaseModel):
    issueDate: Annotated[Optional[Data[str]], Field(default=None, description="Date of issue of hte marksheet")]
    placeOFIssue: Annotated[Optional[Data[str]], Field(default=None, description="Place of issuing of the marksheet")]

class MarksheetData(BaseModel):
    candidate: CandidateDetails
    subjects: List[SubjectMarks]
    result_summary: ResultSummary
    meta_info: Optional[MetaInfo] = None