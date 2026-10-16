from fastapi.middleware.cors import CORSMiddleware
from models import Course, Enrollment, EnrollmentIn

from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query

from data import find_course, get_all_courses


app = FastAPI(title="Course Catalog API")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Content-Type"],
)
ENROLLMENTS: list[Enrollment] = []



def pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> dict[str, int]:
    return {"offset": (page - 1) * page_size, "limit": page_size}


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


@app.get("/courses", response_model=list[Course])
def list_courses(
    is_elective: bool | None = None,
    sort: Literal["popular", "title"] = "popular",
    p: dict[str, int] = Depends(pagination),
):
    courses = get_all_courses()

    if is_elective is not None:
        courses = [course for course in courses if course.is_elective == is_elective]

    if sort == "title":
        courses = sorted(courses, key=lambda course: course.title)
    else:
        courses = sorted(courses, key=lambda course: course.likes, reverse=True)

    offset = p["offset"]
    limit = p["limit"]
    return courses[offset : offset + limit]


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course



@app.post("/courses/{course_id}/like", response_model=Course)
def like_course(course_id: str):
    course = find_course(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course.likes += 1
    return course

@app.post("/enrollments", response_model=Enrollment, status_code=201)
def create_enrollment(data: EnrollmentIn):
    if find_course(data.course_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    new_enrollment = Enrollment(
        id=len(ENROLLMENTS) + 1,
        course_id=data.course_id,
        student_name=data.student_name
    )
    ENROLLMENTS.append(new_enrollment)
    return new_enrollment

@app.get("/enrollments", response_model=list[Enrollment])
def list_enrollments():
    return ENROLLMENTS