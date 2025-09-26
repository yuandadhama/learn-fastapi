const orderedListStudents = document.getElementById('olist-students');

// ambil query param dari url
const urlParams = new URLSearchParams(window.location.search);
const studentId = urlParams.get("id");

// endpoint backend
const url = `http://127.0.0.1:8000/get-student/?id=${studentId}`;

const loadStudentDetail = async () => {
  try {
    const response = await fetch(url);
    const student = await response.json();

    // Isi ulang list dengan data detail
    orderedListStudents.innerHTML = /*html*/`
      <li>Name: ${student.name}</li>
      <li>Age: ${student.age}</li>
      <li>Year: ${student.year}</li>
    `;
  } catch (err) {
    console.error(err);
  }
}

loadStudentDetail();
