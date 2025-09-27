const orderedListStudents = document.getElementById("olist-students");

// ambil query param dari url
const urlParams = new URLSearchParams(window.location.search);
const studentId = urlParams.get("id");

// get edit button to make <a> tag that href with parameter
const editButton = document.getElementById("edit-button");
editButton.innerHTML = /*html*/ `
  <a href="editstudent.html?id=${studentId}" style="text-decoration: none; color: black;">Edit</a>
`;

// endpoint backend
const url = `http://127.0.0.1:8000/get-student/?id=${studentId}`;

const loadStudentDetail = async () => {
  try {
    const response = await fetch(url);
    const student = await response.json();

    // Isi ulang list dengan data detail
    orderedListStudents.innerHTML = /*html*/ `
      <li>Name: ${student.name}</li>
      <li>Age: ${student.age}</li>
      <li>Year: ${student.year}</li>
    `;
  } catch (err) {
    console.error(err);
  }
};

loadStudentDetail();

// delete student function area
const deleteButton = document.getElementById("delete-button");

const urlDELETE = `http://127.0.0.1:8000/delete-student/?id=${studentId}`;

deleteButton.addEventListener("click", () => {
  console.log("hea");

  const deleteStudent = async () => {
    const response = await fetch(urlDELETE, {
      method: "DELETE",
    });
    const data = await response.json();

    alert(data.msg);

    if (data.isSuccess) {
      window.location.href = "index.html";
    }
  };

  deleteStudent();
});
