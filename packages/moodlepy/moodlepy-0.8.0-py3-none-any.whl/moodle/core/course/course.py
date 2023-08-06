from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional, Union
from moodle import ResponsesFactory


@dataclass
class CourseFormatOption:
    name: str  # course format option name
    value: Union[str, int]  # course format option value


@dataclass
class CourseCustomField:
    name: str  # The name of the custom field
    shortname: str  # The shortname of the custom field
    type: str  # The type of the custom field - text, checkbox...
    value: Optional[str]  # The value of the custom field


@dataclass
class Course:
    id: int  # course id
    shortname: str  # course short name
    categoryid: int  # category id
    categorysortorder: Optional[int]  # sort order into the category
    fullname: str  # full name
    displayname: str  # course display name
    idnumber: Optional[str]  # id number
    summary: str  # summary
    summaryformat: int  # summary format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
    format: str  # course format: weeks, topics, social, site,..
    showgrades: Optional[int]  # 1 if grades are shown, otherwise 0
    newsitems: Optional[
        int]  # number of recent items appearing on the course page
    startdate: int  # timestamp when the course start
    enddate: int  # timestamp when the course end
    numsections: Optional[
        int]  # (deprecated, use courseformatoptions) number of weeks/topics
    maxbytes: Optional[
        int]  # largest size of file that can be uploaded into the course
    showreports: Optional[int]  # are activity report shown (yes = 1, no =0)
    visible: Optional[int]  # 1: available to student, 0:not available
    hiddensections: Optional[
        int]  # (deprecated, use courseformatoptions) How the hidden sections in the course are displayed to students
    groupmode: Optional[int]  # no group, separate, visible
    groupmodeforce: Optional[int]  # 1: yes, 0: no
    defaultgroupingid: Optional[int]  # default grouping id
    timecreated: Optional[int]  # timestamp when the course have been created
    timemodified: Optional[int]  # timestamp when the course have been modified
    enablecompletion: Optional[
        int]  # Enabled, control via completion and activity settings. Disbaled, not shown in activity settings.
    completionnotify: Optional[int]  # 1: yes 0: no
    lang: Optional[str]  # forced course language
    forcetheme: Optional[str]  # name of the force theme
    courseformatoptions: List[
        CourseFormatOption]  # additional options for particular course format]    ):Optional[customfields]  # Custom fields and associated values
    customfields: List[
        CourseCustomField]  # Custom fields and associated values

    @dataclass
    class ToCheck:
        contextlevel: str  # The context level for the file location. Only module supported right now.
        id: int  # Context instance id
        since: datetime  # Check updates since this time stamp


@dataclass
class SearchResult(ResponsesFactory[Course]):
    total: int  # total course count
    courses: List[Course]  # course
    warnings: List[Warning]  # list of warning

    @property
    def items(self) -> List[Course]:
        return self.courses


@dataclass
class CourseBTC:
    id: int  # id
    fullname: str  # fullname
    shortname: str  # shortname
    idnumber: str  # idnumber
    summary: str  # summary
    summaryformat: int  # summary format (1 = HTML, 0 = MOODLE, 2 = PLAIN or 4 = MARKDOWN)
    startdate: int  # startdate
    enddate: int  # enddate
    visible: int  # visible
    fullnamedisplay: str  # fullnamedisplay
    viewurl: str  # viewurl
    courseimage: str  # courseimage
    progress: Optional[int]  # progress
    hasprogress: int  # hasprogress
    isfavourite: int  # isfavourite
    hidden: int  # hidden
    timeaccess: Optional[int]  # timeaccess
    showshortname: int  # showshortname
    coursecategory: str  # coursecategory


@dataclass
class CoursesBTC(ResponsesFactory[CourseBTC]):
    courses: List[CourseBTC]
    nextoffset: int

    @property
    def items(self) -> List[CourseBTC]:
        return self.courses
