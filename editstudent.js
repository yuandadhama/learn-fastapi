// take all form input html element to be filled with exsisted data
const inputName = document.getElementById("name");
const inputAge = document.getElementById("age");
const inputYear = document.getElementById("year");

const form = document.getElementById("input-student");

// const get url id student paramater
const urlParams = new URLSearchParams(window.location.search);
const studentId = urlParams.get("id");

const backLink = document.getElementById("back-link");
backLink.innerHTML = /* html */ `
  <a href="detailstudent.html?id=${studentId}">Back</a>
`;

// url to get student
const urlGET = `http://127.0.0.1:8000/get-student/?id=${studentId}`;
// load the student detail first to make the default value of the form
const loadStudentDetail = async () => {
  try {
    const response = await fetch(urlGET);
    const student = await response.json();

    // set default vaule of the form
    inputName.value = student.name;
    inputAge.value = student.age;
    inputYear.value = student.year;
  } catch (err) {
    console.error(err);
  }
};
loadStudentDetail();

// url to put student / update student
const urlPUT = `http://127.0.0.1:8000/update-student/?id=${studentId}`;
const sendData = async () => {
  const formData = new FormData(form);

  const student = {
    name: formData.get("name"),
    age: parseInt(formData.get("age")),
    year: formData.get("year"),
  };

  try {
    const response = await fetch(urlPUT, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(student),
    });

    const data = await response.json();
    console.log(data);
    alert(data.msg);
  } catch (e) {
    console.log("error");
    console.error(e);
  }
};

form.addEventListener("submit", (e) => {
  e.preventDefault();
  sendData();
  window.location.href = `detailstudent.html?id=${studentId}`;
});
