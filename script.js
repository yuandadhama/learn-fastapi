const orderedListStudents = document.getElementById('olist-students');
const url = 'http://127.0.0.1:8000/'

async function loadStudents() {
  try {
    const response = await fetch(url);
    const data = await response.json(); // parsing JSON

    // Kosongkan list dulu
    orderedListStudents.innerHTML = ''; 

    // data dari FastAPI berupa object {1: {name:..., age:..., year:...}}
    let liStudent = ''
    Object.keys(data).forEach(id => {
      const student = data[id];
      liStudent += makeStudent(student, id) 
      orderedListStudents.innerHTML = liStudent;
    });
  } catch (err) {
    console.error(err);
  }
}

const makeStudent = (student, id) => {
  return /*html*/`
        <li>
          <a href="detailstudent.html?id=${id}">
            Name: ${student.name}
          </a>
        </li>
      `
}

loadStudents();
